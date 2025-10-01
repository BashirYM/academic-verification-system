def compare_candidate_info(user_data, parsed_data):
    user_info = {
        "Examination Number": user_data.get('CandidateNo'),
        "Candidate's Name": user_data.get('Name').upper(),
    }

    # Return detailed comparison, showing which fields matched or mismatched
    mismatches = {
        key: {
            "received": user_info[key],
            "expected": parsed_data.get(key, "N/A")
        }
        for key in user_info if user_info[key] != parsed_data.get(key)
    }

    return len(mismatches) == 0, mismatches


def compare_subject_grades(user_data, parsed_data):
    """
    Compares the grades of subjects between user data and parsed data.
    Args:
        user_data (dict): A dictionary containing user information, including
                          a list of subjects and their grades.
        parsed_data (list): A list of dictionaries, each containing a subject
                            and its corresponding grade.
    Returns:
        tuple: A tuple containing:
            - bool: True if all subjects and grades match, False otherwise.
            - dict: A dictionary of mismatched subjects with their received and
                    expected grades.
    """
    # Convert subjects to uppercase to make the comparison case-insensitive
    user_subjects = {sub['subject'].upper(): sub['grade']
                     for sub in user_data.get('subjects', [])}
    parsed_subjects = {sub['subject']: sub['grade']
                       for sub in parsed_data[:]}

    # Return detailed comparison, showing mismatched subjects and grades
    mismatches = {
        subject: {
            "received": user_subjects[subject],
            "expected": parsed_subjects.get(subject, "N/A")
        }
        for subject in user_subjects
        if user_subjects[subject] != parsed_subjects.get(subject)
    }

    return len(mismatches) == 0, mismatches



def validate(user_data, parsed_data):
    """
    Validates the user-supplied data against the parsed result data.
    
    Args:
        user_data (dict): The data supplied by the user.
        parsed_data (dict): The data parsed from the NECO or WAEC response.
    
    Returns:
        dict: Validation result with mismatches.
    """
    # Compare candidate information
    cand_info = parsed_data['candidate_info']
    info_match, info_mismatches = compare_candidate_info(
        user_data, cand_info)

    # Compare subject grades
    subj_info = parsed_data['subject_grades']
    subjects_match, subjects_mismatches = compare_subject_grades(
        user_data, subj_info)

    return {
        "Info Match": info_match,
        "Subj Match": subjects_match,
        "Info Mismatches": info_mismatches,
        "Subj Mismatches": subjects_mismatches
    }
