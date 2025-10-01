from app.parser import parse_html_response, parse_neco_response


# Example of using the parser in the app
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

neco_result = {
    "success": True
}


parsed_data = parse_neco_response(neco_result["content"])

# Access the parsed information
candidate_info = parsed_data['candidate_info']
subject_grades = parsed_data['subject_grades']

print(parsed_data)

# Display extracted data
print("Candidate Information:")
for key, value in candidate_info.items():
    print(f"{key}: {value}")

print("\nSubject Grades:")
for item in subject_grades:
    print(f"{item['subject']}: {item['grade']}")
