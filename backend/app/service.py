import requests
from urllib.parse import urlencode, urlparse, parse_qs
from flask import jsonify
from .parser import parse_html_response, parse_neco_response
from config import WAEC_DIRECT, NECO
from typing import List, Tuple, Dict, Any

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
html_content = '''
<html xmlns="http://www.w3.org/1999/xhtml"><head><script language="javascript">
var message="Right-mouse click has been disabled.";
function click(e)
{
  if (document.all)
  {
    if (event.button==2||event.button==3)
    {
      alert(message);
      return false;
    }
  }
  else
  {
    if (e.button==2||e.button==3)
    {
      e.preventDefault();
      e.stopPropagation();
      alert(message);
      return false;
    }
  }
  if (e.which)
  {
    
  }
}

if (document.all) // for IE
{
  document.onmousedown=click;
}
else // for FF & Chrome
{
  document.onclick=click;  
  document.oncontextmenu=click;
}

</script>

<script type="text/javascript" language="javascript">
 
   function hideprint()
            {
               
                 document.getElementById("dvmodule").style.display = 'none';
                
            }
</script>

<script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.2.1.min.js"></script>

<script language="JavaScript" type="text/JavaScript">
<!--
    //clearing the pin from the calling window...
  
	$(document).keydown(function(event){
    if(event.keyCode==123){
    return false;
   }
else if(event.ctrlKey && event.shiftKey && event.keyCode==73){        
      return false;  //Prevent from ctrl+shift+i
   }
});

$(document).on("contextmenu",function(e){        
   e.preventDefault();
});
//-->
</script>



<title>
	WAECDIRECT ONLINE - RESULTS
</title><link rel="STYLESHEET" type="text/css" href="include/waecdirect.css"></head>
<body>
    <form method="post" action="./DisplayResult.aspx?ExamNumber=4220416015&amp;ExamYear=2018&amp;serial=WRN191970170&amp;pin=486008951204&amp;ExamType=MAY%2fJUN" id="form1">
<div class="aspNetHidden">
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwULLTEwNzIzNTc3NzkPZBYCAgMPZBYCAgEPD2QPEBYHZgIBAgICAwIEAgUCBhYHFgIeDlBhcmFtZXRlclZhbHVlZBYCHwBkFgIfAGQWAh8AZBYCHwBkFgIfAGQWAh8AZBYHAgMCAwIDAgMCAwIDAgNkZGRyiMBp3Q9TfXzwKuK9NefhwmNeiXg+sxcJk+55ZYLhJw==">
</div>

<div class="aspNetHidden">

	<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="8EC363C2">
</div>
        <table width="500" height="580" border="0" cellspacing="1" cellpadding="0" align="left">
      <tbody><tr>
                <td width="100%" align="left" valign="middle">
                    <img src="images/top_small.jpg" alt="WAEC logo" width="480" height="66" hspace="0" vspace="0" border="0" align="left">                </td>
          </tr>
            <tr>
                <td width="100%" class="darkblue">
                    <a href="http://www.waecnigeria.org/" target="_blank">Click here to visit our corporate
                        website</a></td>
            </tr>
            <tr>
              <td height="60"> 
                <div id="dvmodule" style="display:block"> 
                 <table style="width: 100%" id="Table1">
                    <tbody><tr>
                       <td align="center" valign="top"><span class="style20"></span>
                           
                         </td>
                      </tr>                 
                      
                    </tbody></table>
               </div>
              </td>
            </tr>
            <tr>
                <td width="100%" class="nightblue">
                    
                    Results</td>
            </tr>
            <tr>
                <td width="100%" height="90%" colspan="2" valign="top" class="purple">
                    <br>
                    <table width="94%" height="10%" border="0" cellspacing="1" cellpadding="4" align="center" class="nightblue">
                        <tbody><tr>
                            <th colspan="2" class="result" style="width: 450px">
                                Candidate's Information</th>
                        </tr>
                        <tr>
                            <td>
                                <table id="tbCandidInfo" class="result" style="width: 100%">
	<tbody><tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">Examination Number</td>
		<td align="left" width="60%">4220416015</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">Candidate's Name</td>
		<td align="left" width="60%">MUHAMMAD ATTAHIRU KAMBA                 </td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">Examination</td>
		<td align="left" width="60%">WASSCE FOR SCHOOL CANDIDATES 2018</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">Centre</td>
		<td align="left" width="60%">JODA INTERNATIONAL SCHOOL, B/KEBBI</td>
	</tr>
</tbody></table>
                            </td>
                        </tr>
                    </tbody></table>
                    <table width="94%" height="10%" border="0" cellspacing="1" cellpadding="4" align="center" class="nightblue">
                        <tbody><tr>
                            <th colspan="2" class="result" style="width: 450px">
                                Subject/Grade</th>
                        </tr>
                        <tr>
                            <td>
                                <table id="tbSubjectGrades" class="result" style="width: 100%">
	<tbody><tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">MARKETING                     </td>
		<td align="left" width="60%">B2</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">CIVIC EDUCATION               </td>
		<td align="left" width="60%">B2</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">ENGLISH LANGUAGE              </td>
		<td align="left" width="60%">B3</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">MATHEMATICS                   </td>
		<td align="left" width="60%">B2</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">AGRICULTURAL SCIENCE          </td>
		<td align="left" width="60%">A1</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">BIOLOGY                       </td>
		<td align="left" width="60%">B3</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">CHEMISTRY                     </td>
		<td align="left" width="60%">B2</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">PHYSICS                       </td>
		<td align="left" width="60%">B3</td>
	</tr>
	<tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">COMPUTER STUDIES              </td>
		<td align="left" width="60%">A1</td>
	</tr>
</tbody></table>
                            </td>
                        </tr>
                    </tbody></table>
                    <table width="94%" height="10%" border="0" cellspacing="1" cellpadding="4" align="center" class="nightblue">
                        <tbody><tr>
                            <th colspan="2" class="result" style="width: 450px">
                                Card Information</th>
                        </tr>
                        <tr>
                            <td>
                                <table id="tbCardInfo" class="result" style="width: 100%">
	<tbody><tr style="background-color:#E9D772;color:#000000;font-family:Arial, Verdana, Sans-serrif;font-size:9pt;font-weight:bold;vertical-align:top;">
		<td align="left" width="40%">Card Use</td>
		<td align="left" width="60%">4 of 5</td>
	</tr>
</tbody></table>
                            </td>
                        </tr>
						 <tr>
                            <td>
                                <table id="tbWithHeld" class="result" style="width: 100%">
</table>
                            </td>
                        </tr>
                    </tbody></table>                </td>
            </tr>
            <tr>
                <td colspan="2" style="text-align: center" class="result">
                    
             <p><font size="2" face="Geneva, Arial, Helvetica, sans-serif" style="background-color:black;"><a href="javascript:window.print();" onclick="javascript:hideprint();">Click Here to Print</a></font></p>      
                </td>
</tr>
             <tr>
                
            </tr>
            <tr>
                <td colspan="2" style="text-align: right" class="result">
                    <input type="submit" value="Close Window" class="button" onclick="window.close()"><object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0" width="1" height="1"><param name="movie" value="cardauditor.swf"><param name="quality" value="high">
                        <embed src="images/cardauditor.swf" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="639" height="82"></object></td>
            </tr>
        </tbody></table>
</form>


</body></html>

'''
def _sample_subjects_for_bashir() -> List[Dict[str, str]]:
    # exactly nine subjects for the UI's 9-slot input requirement
    return [
        {"subject": "MATHEMATICS", "grade": "A1"},
        {"subject": "ENGLISH LANGUAGE", "grade": "B2"},
        {"subject": "COMPUTER STUDIES", "grade": "B3"},
        {"subject": "CHEMISTRY", "grade": "B3"},
        {"subject": "PHYSICS", "grade": "C4"},
        {"subject": "GEOGRAPHY", "grade": "C5"},
        {"subject": "ECONOMICS", "grade": "C5"},
        {"subject": "CIVIC EDUCATION", "grade": "C6"},
        {"subject": "AGRICULTURAL SCIENCE", "grade": "C6"},
    ]
# Helper function to build the request URL
def make_request_url(base_url, params):
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"


def verify_waec_result(CandidateNo, ExamYear, pin, ExamName, serial):
    try:
        # Construct the request URL
        params = {
            'ExamNumber': CandidateNo,
            'ExamYear': ExamYear,
            'pin': pin,
            'ExamType': ExamName,
            'serial': serial
        }
        url = make_request_url(WAEC_DIRECT, params)
        print(url)

        headers = {
            "Accept": "*/*",
            "Access-Control-Allow-Origin": "*",
        }

        # Make the GET request with allow_redirects=False to capture redirects
        response = requests.get(url, allow_redirects=False)

        # Handle the response or follow redirects
        if response.is_redirect:
            redirect_url = response.headers.get('Location')
            redirect_url = f'https://www.waecdirect.org/{redirect_url}'
            print(redirect_url)
            redirect_response = requests.get(redirect_url, headers=headers)
            return handle_response(redirect_response, redirect_url)
        else:
            return handle_response(response)

    except Exception as e:
        return jsonify({
            "http_code": 500,
            "success": False,
            "content": {
                "error_title": "Request Exception",
                "error_message": str(e)
            }
        }), 500


def handle_response(response, redirect_url=None):
    if redirect_url:
        error_content = parse_failed_request(redirect_url)
        return jsonify({
            "http_code": 400,
            "success": False,
            "content": {
                "error_title": error_content['error_title'],
                "error_message": error_content['error_message']
            }
        }), 400

    if response.status_code == 200:
        return jsonify({
            "http_code": response.status_code,
            "success": True,
            "content": {
                "title": "WAECDIRECT ONLINE - RESULTS",
                "message": parse_html_response(response.text),
                "verified": True,
            }
        }), 200
    

def verify_waec_dummy(exam_number: str, exam_year: str, pin: str, serial: str) -> Tuple[Dict[str, Any], int]:
    """
    Dummy WAEC verifier.
    Candidate verification works ONLY if PIN + Serial match the sample.
    Secondary fields are checked for mismatches.
    """
    sample = {
        "Name": "Bashir Mustapha",
        "Exam Number": "1234567890",
        "Exam Year": "2024",
        "Centre Name": "Air Force School",
        "PIN": "111122223333",
        "Serial": "SERIAL1234"
    }

    # Primary validation (PIN + Serial must match)
    if str(pin).strip() != sample["PIN"] or str(serial).strip() != sample["Serial"]:
        return ({
            "error": "Invalid PIN or Serial Number",
            "expected": {"PIN": sample["PIN"], "Serial": sample["Serial"]},
            "provided": {"PIN": pin, "Serial": serial}
        }, 400)

    # Secondary mismatches
    mismatches = []
    if str(exam_number).strip() != sample["Exam Number"]:
        mismatches.append(f"Exam Number mismatch (expected '{sample['Exam Number']}', got '{exam_number}')")
    if str(exam_year).strip() != sample["Exam Year"]:
        mismatches.append(f"Exam Year mismatch (expected '{sample['Exam Year']}', got '{exam_year}')")

    parsed = {
        "candidate_info": {
            "Name": sample["Name"],
            "Exam Number": sample["Exam Number"],
            "Exam Year": sample["Exam Year"],
            "Centre Name": sample["Centre Name"]
        },
        "subject_grades": _sample_subjects_for_bashir(),
        "card_info": {"PIN": sample["PIN"], "Serial": sample["Serial"]}
    }

    if mismatches:
        parsed["mismatches"] = mismatches

    return (parsed, 200)

def verify_neco_dummy(exam_number: str, exam_year: str, pin: str, exam_name: str) -> Tuple[Dict[str, Any], int]:
    """
    Dummy NECO verifier.
    Candidate verification works ONLY if PIN matches the sample.
    """
    sample = {
        "Name": "Bashir Mustapha",
        "Exam Number": "1234567890",
        "Exam Year": "2025",
        "Centre Name": "Air Force School",
        "PIN": "1111222233"
    }

    # Primary validation (PIN must match)
    if str(pin).strip() != sample["PIN"]:
        return ({
            "error": "Invalid NECO Token",
            "expected": {"PIN": sample["PIN"]},
            "provided": {"PIN": pin}
        }, 400)

    # Secondary mismatches
    mismatches = []
    if str(exam_number).strip() != sample["Exam Number"]:
        mismatches.append(f"Exam Number mismatch (expected '{sample['Exam Number']}', got '{exam_number}')")
    if str(exam_year).strip() != sample["Exam Year"]:
        mismatches.append(f"Exam Year mismatch (expected '{sample['Exam Year']}', got '{exam_year}')")

    parsed = {
        "candidate_info": {
            "Name": sample["Name"],
            "Exam Number": sample["Exam Number"],
            "Exam Year": sample["Exam Year"],
            "Centre Name": sample["Centre Name"]
        },
        "subject_grades": _sample_subjects_for_bashir()
    }

    if mismatches:
        parsed["mismatches"] = mismatches

    return (parsed, 200)

def verify_neco_result(CandidateNo, ExamYear, pin, ExamName):
    try:
        # Construct the request URL
        #  exam_year=2024&exam_type=ssce_int&reg_no=2410018877GI&token=528492244243
        params = {
            'reg_no': CandidateNo,
            'exam_year': ExamYear,
            'token': pin,
            'exam_type': ExamName,
        }
        url = make_request_url(NECO, params)
        print(url)

        headers = {
            "Accept": "*/*",
            "Access-Control-Allow-Origin": "*",
        }

        # Make the GET request with allow_redirects=False to capture redirects
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            return jsonify({
                "http_code": response.status_code,
                "success": False,
                "content": {
                    "error_title": "Request Failed",
                    "error_message": response.json()
                }
            }), response.status_code     
        
        return jsonify({
            "http_code": response.status_code,
            "success": True,
            "content": {
                "title": "NECO RESULTS",
                "message": parse_neco_response(response.json()['content'])
            }
        }), 200
    except Exception as e:
        return jsonify({
            "http_code": 500,
            "success": False,
            "content": {
                "error_title": "Request Exception",
                "error_message": str(e)
            }
        }), 500

def parse_failed_request(redirect_url):
    # Parse the redirect URL to extract error details
    parts = urlparse(redirect_url)
    query_params = parse_qs(parts.query)

    error_message = query_params.get('errMsg', [None])[0]
    error_title = query_params.get('errTitle', [None])[0]

    # You can also extract the title from the HTML if needed (assuming the response contains HTML)
    # For now, we're focusing on the error message and title from the URL

    return {
        "error_title": error_title or "Unknown Error",
        "error_message": error_message or "An unknown error occurred."
    }

