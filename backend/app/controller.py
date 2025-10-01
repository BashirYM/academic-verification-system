from flask import jsonify
from .service import (
    verify_waec_result,
    verify_neco_result,
    verify_document_dummy,
    verify_neco_dummy
)
from .nysc_service import verify_nysc  # 👈 real scraper
from .validate_info import validate
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


def validate_nysc_request(data):
    """Validation tailored for NYSC inputs"""
    required_fields = ['callup_no', 'certificate_no', 'dob']

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"

    # Basic format checks
    if len(data['callup_no']) < 5:
        return False, "Invalid Call-up Number."
    if len(data['certificate_no']) < 5:
        return False, "Invalid Certificate Number."
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data['dob']):
        return False, "DOB must be in YYYY-MM-DD format."

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


def waec_request_handler(request):
    """Handle WAEC requests"""
    try:
        data = request.json
        is_valid, validation_error = validate_request(data)
        if not is_valid:
            return jsonify({"error": validation_error}), 400

        result, status_code = verify_document_dummy()
        if status_code == 200:
            parsed_data = result.get_json()['content']['message']
            validated_data = validate(data, parsed_data)

            if validated_data['Info Match'] and validated_data['Subj Match']:
                return jsonify({"success": True, "content": parsed_data}), status_code
            else:
                return generate_mismatch_response(data, parsed_data, validated_data)
        else:
            error = result.get_json()['content']['error_message']
            return jsonify({"success": False, "content": error}), status_code

    except Exception as e:
        print(f"Error in waec_request_handler: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


def neco_request_handler(request):
    """Handle NECO requests"""
    try:
        data = request.json
        is_valid, validation_error = validate_request(data)
        if not is_valid:
            return jsonify({"error": validation_error}), 400

        result, status_code = verify_neco_dummy()
        if status_code == 200:
            parsed_data = result.get_json()['content']['message']
            validated_data = validate(data, parsed_data)

            if validated_data['Info Match'] and validated_data['Subj Match']:
                return jsonify({"success": True, "content": parsed_data}), status_code
            else:
                return generate_mismatch_response(data, parsed_data, validated_data, "NECO")
        else:
            error = result.get_json()['content']['error_message']['info']
            message = result.get_json()['content']['error_message']['message']
            return jsonify({"success": False, "message": message, "content": error}), status_code

    except Exception as e:
        print(f"Error in neco_request_handler: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# ================= NYSC ====================
def verify_nysc_dummy(callup_no, certificate_no, dob):
    """Dummy NYSC verifier for testing without portal access"""
    return jsonify({
        "content": {
            "message": {
                "Name": "John Doe",
                "Call-up Number": callup_no,
                "Certificate Number": certificate_no,
                "Date of Birth": dob,
                "Status": "Valid"
            }
        }
    }), 200


def nysc_request_handler(request):
    """Handle NYSC requests (dummy + scraper ready)"""
    try:
        data = request.json
        is_valid, validation_error = validate_nysc_request(data)
        if not is_valid:
            return jsonify({"error": validation_error}), 400

        callup_no = data.get("callup_no")
        certificate_no = data.get("certificate_no")
        dob = data.get("dob")

        # Swap to verify_nysc() when portal scraping is active
        result, status_code = verify_nysc_dummy(callup_no, certificate_no, dob)

        if status_code == 200:
            parsed_data = result.get_json()['content']['message']
            validated_data = validate(data, parsed_data)

            if validated_data['Info Match']:
                return jsonify({"success": True, "content": parsed_data}), status_code
            else:
                return generate_mismatch_response(data, parsed_data, validated_data, "NYSC")
        else:
            error = result.get_json()['content']['error_message']
            return jsonify({"success": False, "content": error}), status_code

    except Exception as e:
        print(f"Error in nysc_request_handler: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# def nysc_request_handler(request):
#     try:
#         data = request.get_json()

#         callup_no = data.get("callup_no")
#         certificate_no = data.get("certificate_no")
#         dob = data.get("dob")

#         if not callup_no or not certificate_no or not dob:
#             return jsonify({"success": False, "error": "Missing required fields"}), 400

#         result = verify_nysc(
#             callup_no=callup_no,
#             certificate_no=certificate_no,
#             dob=dob
#         )

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

