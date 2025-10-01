from flask import jsonify
from .service import (
    verify_waec_result,
    verify_neco_result,
    verify_document_dummy,
    verify_neco_dummy
)
from .nysc_service import verify_nysc_dummy  # 👈 real scraper
from .validate_info import validate
from .service import compare_fields
import re


def validate_request(data):
    """Function to validate the incoming WAEC/NECO data"""
    required_fields = ['PIN', 'ExamType', 'ExamYear', 'CandidateNo',
                       'ExamName', 'Name', 'subjects']

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"

    if len(data['PIN']) not in range(10, 21) or not data['PIN'].isdigit():
        return False, "PIN must be a number between 10 and 20 digits."

    if len(data['CandidateNo']) not in range(10, 21):
        return False, "Candidate number must be between 10 and 15 digits."

    str_exam_year = str(data['ExamYear'])
    if not re.match(r'^\d{4}$', str_exam_year):
        return False, "Exam year must be a 4-digit number."

    return True, None


# def validate_nysc_request(data):
#     """Validation tailored for NYSC inputs"""
#     required_fields = ['callup_no', 'certificate_no', 'dob']

#     missing_fields = [field for field in required_fields if not data.get(field)]
#     if missing_fields:
#         return False, f"Missing fields: {', '.join(missing_fields)}"

#     # Basic format checks
#     if len(data['callup_no']) < 5:
#         return False, "Invalid Call-up Number."
#     if len(data['certificate_no']) < 5:
#         return False, "Invalid Certificate Number."
#     if not re.match(r'^\d{4}-\d{2}-\d{2}$', data['dob']):
#         return False, "DOB must be in YYYY-MM-DD format."

#     return True, None


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


def waec_request_handler(request):
    try:
        data = request.json
        result, status_code = verify_document_dummy()

        if status_code == 200:
            parsed_data = result.get_json()["content"]["message"]
            mismatches = compare_fields(data, parsed_data, "WAEC")

            if mismatches:
                return jsonify({
                    "success": False,
                    "error": "Verification failed",
                    "mismatches": mismatches
                }), 422

            return jsonify({
                "success": True,
                "content": parsed_data
            }), 200

        else:
            return jsonify({"success": False, "error": "Backend error"}), status_code

    except Exception as e:
        print(f"Error in WAEC handler: {e}")
        return jsonify({"error": "Unexpected error"}), 500

def neco_request_handler(request):
    try:
        data = request.json
        result, status_code = verify_neco_dummy()

        if status_code == 200:
            parsed_data = result.get_json()["content"]["message"]
            mismatches = compare_fields(data, parsed_data, "NECO")

            if mismatches:
                return jsonify({
                    "success": False,
                    "error": "Verification failed",
                    "mismatches": mismatches
                }), 422

            return jsonify({
                "success": True,
                "content": parsed_data
            }), 200

        else:
            return jsonify({"success": False, "error": "Backend error"}), status_code

    except Exception as e:
        print(f"Error in NECO handler: {e}")
        return jsonify({"error": "Unexpected error"}), 500

def nysc_request_handler(request):
    try:
        data = request.get_json() or {}
        callup_no = data.get("callup_no")
        certificate_no = data.get("certificate_no")
        dob = data.get("dob")

        if not (callup_no or certificate_no):
            return jsonify({"success": False, "error": "Provide callup_no or certificate_no"}), 400

        # Call scraper (may return { success: True/False, data: {...} or error: ... })
        result = verify_nysc(callup_no=callup_no, certificate_no=certificate_no, dob=dob)

        if not result.get("success"):
            # propagate helpful message and raw for debugging if present
            return jsonify({
                "success": False,
                "error": result.get("error", "NYSC verification failed"),
                "raw": result.get("raw")
            }), 400

        # result["data"] is the parsed dict from the scraper. Normalize into expected shape:
        parsed = result.get("data", {})

        # Build a consistent parsed_data structure matching other endpoints
        parsed_data = {
            "candidate_info": {
                # keys chosen to match what compare_fields expects; adapt if needed
                "Name": parsed.get("Name") or parsed.get("FullName") or parsed.get("name"),
                "Call-up Number": parsed.get("Call-up Number") or parsed.get("CallupNumber") or callup_no,
                "Certificate Number": parsed.get("Certificate Number") or parsed.get("CertificateNumber") or certificate_no,
                "Date of Birth": parsed.get("Date of Birth") or parsed.get("DOB") or dob,
                "Status": parsed.get("Status") or parsed.get("VerificationStatus") or "Unknown",
            },
            # NYSC has no 'subject_grades' or 'card_info' — leave empty array / None for compatibility
            "subject_grades": [],
            "card_info": None,
        }

        mismatches = compare_fields(
            # adapt the fields coming from frontend into expected keys for compare_fields
            {
                "callup_no": callup_no,
                "certificate_no": certificate_no,
                "dob": dob,
            },
            parsed_data,
            "NYSC"
        )

        if mismatches:
            return jsonify({
                "success": False,
                "error": "Verification failed",
                "mismatches": mismatches,
                "content": parsed_data
            }), 422

        return jsonify({
            "success": True,
            "content": parsed_data
        }), 200

    except Exception as e:
        print(f"Error in nysc_request_handler: {e}")
        return jsonify({"error": "Unexpected error"}), 500
