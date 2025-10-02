from flask import jsonify
from .service import (
    verify_waec_result,
    verify_waec_dummy,
    verify_neco_result,
    verify_neco_dummy
)
from typing import Dict, Any

from .nysc_service import verify_nysc  
import re

def _validate_waec_neco_request(data: Dict[str, Any]) -> (bool, str):
    required = ['PIN', 'ExamType', 'ExamYear', 'CandidateNo', 'ExamName', 'Name', 'subjects', 'CentreName']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    # PIN numeric-ish check
    if not str(data.get('PIN')).isdigit():
        return False, "PIN must be numeric."
    if not re.match(r'^\d{4}$', str(data.get('ExamYear'))):
        return False, "ExamYear must be a 4-digit year."
    return True, None

def _validate_nysc_request(data: Dict[str, Any]) -> (bool, str):
    # accept callup_no OR certificate_no and dob
    if not (data.get('callup_no') or data.get('certificate_no')):
        return False, "Provide callup_no or certificate_no"
    if not data.get('dob'):
        return False, "Provide date of birth (dob) for NYSC verification"
    return True, None


def generate_mismatch_response(user_data, parsed_data, validated_data, exam_type="WAEC"):
    """Handle mismatches and format response for frontend"""
    transformed_user_subjects = [
        {"subject": sub['subject'], "grade": sub['grade']}
        for sub in user_data.get('subjects', [])
    ]

    parsed_subject_names = {sub['subject'] for sub in parsed_data.get('subject_grades', [])}
    for subject in transformed_user_subjects:
        if subject['subject'] not in parsed_subject_names:
            subject['grade'] = "N/A"

    content = {
        "candidate_info": parsed_data.get('candidate_info', {}),
        "subject_grades": transformed_user_subjects,
    }
    if exam_type == 'WAEC':
        content["card_info"] = parsed_data.get('card_info', {})

    return jsonify({
        "success": True,
        "mismatch": True,
        "content": content,
        "mismatches": {
            "Info Mismatches": validated_data.get('Info Mismatches', {}),
            "Subj Mismatches": validated_data.get('Subj Mismatches', {}),
        }
    }), 422
# ---------- Comparison utilities ----------
def _normalize_text(s):
    return (s or "").strip().lower()

def compare_fields(user: Dict[str, Any], parsed: Dict[str, Any], exam_type: str = "WAEC") -> Dict[str, Any]:
    """
    Compare user input to parsed data and return a structured result indicating matches/mismatches.
    Result contains:
      - Info Match: bool
      - Subj Match: bool
      - Info Mismatches: { field: {expected, received} }
      - Subj Mismatches: { subject: {expected, received} }
    """
    info_mismatches = {}
    subj_mismatches = {}

    parsed_info = parsed.get('candidate_info', {})
    # Standard keys to compare (map user keys -> parsed keys)
    mappings = {
        'Name': ['Name', 'Full Name', 'Surname', 'Candidate Name'],
        'CandidateNo': ['Exam Number', 'Candidate Number', 'Exam No', 'Reg No'],
        'ExamYear': ['Exam Year', 'Year'],
        'CentreName': ['Centre Name', 'Centre']
    }

    # Compare simple identity fields
    for user_key, parsed_key_choices in mappings.items():
        user_val = None
        if user_key in user:
            user_val = user[user_key]
        else:
            # sometimes client uses 'CandidateNo' vs parsed 'Exam Number'
            user_val = user.get('CandidateNo') if user_key == 'CandidateNo' else user.get(user_key)

        # find matching parsed key
        parsed_val = None
        parsed_key_used = None
        for pk in parsed_key_choices:
            if pk in parsed_info:
                parsed_val = parsed_info[pk]
                parsed_key_used = pk
                break

        if parsed_val is None:
            continue

        if _normalize_text(str(user_val)) != _normalize_text(str(parsed_val)):
            info_mismatches[parsed_key_used or user_key] = {
                "expected": str(parsed_val),
                "received": str(user_val or "")
            }

    # Compare subjects if available
    user_subjects = { (s['subject'].strip().upper()): s.get('grade','').strip().upper() for s in user.get('subjects', []) }
    parsed_subjects = { (s['subject'].strip().upper()): s.get('grade','').strip().upper() for s in parsed.get('subject_grades', []) }

    # ensure we check all parsed subjects
    for subj_name, expected_grade in parsed_subjects.items():
        received_grade = user_subjects.get(subj_name)
        if received_grade is None:
            subj_mismatches[subj_name] = {"expected": expected_grade, "received": "N/A"}
        elif received_grade != expected_grade:
            subj_mismatches[subj_name] = {"expected": expected_grade, "received": received_grade}

    # Also detect any user-subjects that are not in parsed (treat as mismatch)
    for subj_name, received_grade in user_subjects.items():
        if subj_name not in parsed_subjects:
            subj_mismatches[subj_name] = {"expected": "N/A", "received": received_grade}

    return {
        "Info Match": len(info_mismatches) == 0,
        "Subj Match": len(subj_mismatches) == 0,
        "Info Mismatches": info_mismatches,
        "Subj Mismatches": subj_mismatches
    }


# ---------- Response shaping ----------
def _mismatch_response(user_data: Dict[str, Any], parsed_data: Dict[str, Any], validated_data: Dict[str, Any], exam_type: str = "WAEC"):
    """
    Returns a response compatible with the frontend:
    - success: True (the call succeeded)
    - mismatch: True
    - content: candidate_info + transformed subject list
    - mismatches: detailed mismatches
    """
    # transform user subjects into backend-expected format
    transformed_user_subjects = [{"subject": s.get("subject",""), "grade": s.get("grade","")} for s in user_data.get("subjects", [])]

    content = {
        "candidate_info": parsed_data.get("candidate_info", {}),
        "subject_grades": transformed_user_subjects
    }
    if exam_type.upper() == "WAEC":
        content["card_info"] = parsed_data.get("card_info", {})

    return jsonify({
        "success": True,
        "mismatch": True,
        "content": content,
        "mismatches": {
            "Info Mismatches": validated_data["Info Mismatches"],
            "Subj Mismatches": validated_data["Subj Mismatches"]
        }
    }), 422


# ---------- Request handlers ----------
def waec_request_handler(request):
    try:
        data = request.get_json()
        ok, err = _validate_waec_neco_request(data)
        if not ok:
            return jsonify({"error": err}), 400

        # extract fields
        pin = data["PIN"]
        serial = data.get("serial", "")
        exam_year = data["ExamYear"]
        exam_number = data["CandidateNo"]
        exam_name = data["ExamName"]

        parsed, status = verify_waec_dummy(exam_number, exam_year, pin, serial)
        if status != 200:
            return jsonify({"success": False, "error": "Verification service error"}), 500

        validated = compare_fields(data, parsed, "WAEC")
        if validated["Info Match"] and validated["Subj Match"]:
            return jsonify({"success": True, "content": parsed}), 200
        else:
            return _mismatch_response(data, parsed, validated, "WAEC")

    except Exception as e:
        print(f"Error in waec_request_handler: {e}")
        return jsonify({"error": "Internal server error"}), 500

def neco_request_handler(request):
    try:
        data = request.get_json()
        ok, err = _validate_waec_neco_request(data)
        if not ok:
            return jsonify({"error": err}), 400

        pin = data["PIN"]
        exam_year = data["ExamYear"]
        exam_number = data["CandidateNo"]
        exam_name = data["ExamName"]

        parsed, status = verify_neco_dummy(exam_number, exam_year, pin, exam_name)
        if status != 200:
            return jsonify({"success": False, "error": "Verification service error"}), 500

        validated = compare_fields(data, parsed, "NECO")
        if validated["Info Match"] and validated["Subj Match"]:
            return jsonify({"success": True, "content": parsed}), 200
        else:
            return _mismatch_response(data, parsed, validated, "NECO")

    except Exception as e:
        print(f"Error in neco_request_handler: {e}")
        return jsonify({"error": "Internal server error"}), 500

def nysc_request_handler(request):
    try:
        data = request.get_json()
        ok, err = _validate_nysc_request(data)
        if not ok:
            return jsonify({"error": err}), 400

        callup_no = data.get("callup_no")
        certificate_no = data.get("certificate_no")
        dob = data.get("dob")

        result = verify_nysc(callup_no, certificate_no, dob)

        if not result.get("success"):
            return jsonify({"success": False, "error": result.get("error", "NYSC verification failed")}), 500

        parsed = result.get("data", {})
        # Build a user-like structure for comparison
        # We'll compare Name and Date of Birth primarily
        user_equivalent = {
            "Name": data.get("name", ""),  # optional, frontend may not provide name
            "CandidateNo": certificate_no or "",
            "ExamYear": "",  # not applicable
            "subjects": []  # not applicable for NYSC
        }

        # For NYSC we create a relaxed validation: check name & dob & callup/cert no
        info_mismatches = {}
        parsed_info = parsed.get("candidate_info", {})
        # Name
        if data.get("name"):
            if data.get("name", "").strip().lower() != parsed_info.get("Name", "").strip().lower():
                info_mismatches["Name"] = {"expected": parsed_info.get("Name", ""), "received": data.get("name", "")}
        # DOB
        if dob and dob.strip() != parsed_info.get("Date of Birth", parsed_info.get("Date of Birth", "")):
            info_mismatches["Date of Birth"] = {"expected": parsed_info.get("Date of Birth", ""), "received": dob}

        # Callup or Certificate
        if callup_no and callup_no.strip() != parsed_info.get("Call-up Number", parsed_info.get("CallUpNumber", "")):
            info_mismatches["Call-up Number"] = {"expected": parsed_info.get("Call-up Number", ""), "received": callup_no}
        if certificate_no and certificate_no.strip() != parsed_info.get("Certificate Number", parsed_info.get("CertificateNumber", "")):
            info_mismatches["Certificate Number"] = {"expected": parsed_info.get("Certificate Number", ""), "received": certificate_no}

        if len(info_mismatches) == 0:
            return jsonify({"success": True, "content": parsed}), 200
        else:
            return jsonify({
                "success": True,
                "mismatch": True,
                "content": parsed,
                "mismatches": {"Info Mismatches": info_mismatches}
            }), 422

    except Exception as e:
        print(f"Error in nysc_request_handler: {e}")
        return jsonify({"error": "Internal server error"}), 500