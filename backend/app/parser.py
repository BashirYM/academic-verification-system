from bs4 import BeautifulSoup
"""
This module provides functions to parse various sections of an WAEC response and
NECO response data.
Functions:
    parse_candidate_info(soup)
    parse_subject_grades(soup)
    parse_card_info(soup)
    parse_html_response(html_content)
    parse_neco_response(data)"""


def parse_candidate_info(soup):
    """
    Parses candidate information from an HTML table with the id 'tbCandidInfo'.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the HTML content.

    Returns:
        dict: A dictionary where the keys are the table's first column values and the
              values are the table's second column values.
    """
    candidate_info = {}
    candidate_table = soup.find('table', {'id': 'tbCandidInfo'})
    for row in candidate_table.find_all('tr'):
        cells = row.find_all('td')
        key = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)
        candidate_info[key] = value
    return candidate_info


def parse_subject_grades(soup):
    """
    Parses the subject grades from an HTML table with the id 'tbSubjectGrades'.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the HTML content.

    Returns:
        list: A list of dictionaries, each containing 'subject' and 'grade' keys.
    """
    subject_grades = []
    subject_table = soup.find('table', {'id': 'tbSubjectGrades'})
    for row in subject_table.find_all('tr'):
        cells = row.find_all('td')
        subject = cells[0].get_text(strip=True)
        grade = cells[1].get_text(strip=True)
        subject_grades.append({'subject': subject, 'grade': grade})
    subject_grades.sort(key=lambda x: x['subject'])
    return subject_grades


def parse_card_info(soup):
    """
    Parses card information from an HTML table with the id 'tbCardInfo'.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the HTML content.

    Returns:
        dict: A dictionary containing the card information where the keys are the 
              table's first column values and the values are the table's
              second column values.
    """
    card_info = {}
    card_table = soup.find('table', {'id': 'tbCardInfo'})
    for row in card_table.find_all('tr'):
        cells = row.find_all('td')
        key = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)
        card_info[key] = value
    return card_info


def parse_html_response(html_content):
    """
    Parses the given HTML content and extracts candidate information, subject grades,
    and card information.
    Args:
        html_content (str): The HTML content to be parsed.
    Returns:
        dict: A dictionary containing the parsed data with the following keys:
            - 'candidate_info': Information about the candidate.
            - 'subject_grades': Grades for various subjects.
            - 'card_info': Information about the card.
    """
    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(html_content, 'lxml')

    # Parse different sections of the HTML
    candidate_info = parse_candidate_info(soup)
    subject_grades = parse_subject_grades(soup)
    card_info = parse_card_info(soup)

    # Combine and return parsed data
    return {
        'candidate_info': candidate_info,
        'subject_grades': subject_grades,
        'card_info': card_info
    }


def parse_neco_response(data):
    """
    Parses the NECO response data and extracts student information and their
    subjects with grades.
    
    Args:
        data (dict): A dictionary containing the NECO response data.
        Expected keys include:
            - "full_name" (str): The full name of the student.
            - "reg_number" (str): The registration number of the student.
            - "exam_year" (str): The year of the examination.
            - "dob" (str): The date of birth of the student.
            - "centre_code" (str): The examination centre code.
            - "num_of_sub" (int): The number of subjects taken by the student.
            - "sub{i}_name" (str): The name of the i-th subject.
            - "sub{i}_grade" (str): The grade of the i-th subject.
    
    Returns:
        dict: A dictionary containing the parsed student information with the
        following structure:
            {
                "candidate_info": {
                    "Candidate's Name": str,
                    "Examination Number": str,
                    "Exam Year": str,
                    "Centre": str,
                },
                "subject_grades": [
                    {
                        "subject": str,
                        "grade": str
                    },
                    ...
                ]
            }
    """
    # Extract candidate information
    candidate_info = {
        "Candidate's Name": data.get("full_name"),
        "Examination Number": data.get("reg_number"),
        "Exam Year": data.get("exam_year"),
        "Centre": data.get("centre_name")
    }

    # Extract subject names and grades
    subjects = []
    for i in range(1, data.get("num_of_sub") + 1):
        subject_name = data.get(f"sub{i}_name")
        subject_grade = data.get(f"sub{i}_grade")

        if subject_name and subject_grade:
            if subject_name == 'General Mathematics':
                subject_name = 'Mathematics'
            if subject_name == 'Literature in English':
                subject_name = 'Literature'
            subjects.append({
                "subject": subject_name.upper(),
                "grade": subject_grade.upper(),
            })
    subjects.sort(key=lambda x: x['subject'])

    return {
        "candidate_info": candidate_info,
        "subject_grades": subjects
    }
