import smtplib
from smtplib import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
def send_email(email_id,fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode):
	me = "ekyc59@gmail.com"
	you = email_id

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "E-KYC Application Success"
	msg['From'] = me
	msg['To'] = you

	html = """\
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	</head>
	<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; background-color: #F8FAFC; color: #74787E; height: 100%; hyphens: auto; line-height: 1.4; margin: 0; -moz-hyphens: auto; -ms-word-break: break-all; width: 100% !important; -webkit-hyphens: auto; -webkit-text-size-adjust: none; word-break: break-word;">
	    <style>
	        @media  only screen and (max-width: 600px) {
	            .inner-body {
	                width: 100% !important;
	            }

	            .footer {
	                width: 100% !important;
	            }
	        }

	        @media  only screen and (max-width: 500px) {
	            .button {
	                width: 100% !important;
	            }
	        }
	    </style>

	    <table class="wrapper" width="100%" cellpadding="0" cellspacing="0" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; background-color: #F8FAFC; margin: 0; padding: 0; width: 100%; -premailer-cellpadding: 0; -premailer-cellspacing: 0; -premailer-width: 100%;">
	        <tr>
	            <td align="center" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box;">
	                <table class="content" width="100%" cellpadding="0" cellspacing="0" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; margin: 0; padding: 0; width: 100%; -premailer-cellpadding: 0; -premailer-cellspacing: 0; -premailer-width: 100%;">
	                    <tr>
	    <td class="header" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; padding: 25px 0; text-align: center;">
	        <a href="http://localhost:8000" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; color: #bbbfc3; font-size: 19px; font-weight: bold; text-decoration: none; text-shadow: 0 1px 0 white;">
	            E-KYC Automation System
	        </a>
	    </td>
	</tr>

	                    <!-- Email Body -->
	                    <tr>
	                        <td class="body" width="100%" cellpadding="0" cellspacing="0" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; background-color: #FFFFFF; border-bottom: 1px solid #EDEFF2; border-top: 1px solid #EDEFF2; margin: 0; padding: 0; width: 100%; -premailer-cellpadding: 0; -premailer-cellspacing: 0; -premailer-width: 100%;">
	                            <table class="inner-body" align="center" width="570" cellpadding="0" cellspacing="0" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; background-color: #FFFFFF; margin: 0 auto; padding: 0; width: 570px; -premailer-cellpadding: 0; -premailer-cellspacing: 0; -premailer-width: 570px;">
	                                <!-- Body content -->
	                                <tr>
	                                    <td class="content-cell" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; padding: 35px;">
	                                        <h1 style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; color: #3D4852; font-size: 19px; font-weight: bold; margin-top: 0; text-align: left;">Hello!</h1>
	<p style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; color: #3D4852; font-size: 16px; line-height: 1.5em; margin-top: 0; text-align: left;">E-KYC Application Notification</p>
	<p style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; color: #3D4852; font-size: 16px; line-height: 1.5em; margin-top: 0; text-align: left;">Following details have been successfully saved in our database:<br>"""
	details = [['First Name',fname],['Last Name',lname],["Father's Name",father_name],
				['Gender',gender],['Date of Birth',dob],['Aadhar No.',aadhar_no],
				['PAN No.',pan_no],['City/Post Office',city],['State',state],['Pincode',pincode]]
	for i in details:
		html += '<br>'+i[0]+' : '+i[1]
	html += """</p><p style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box; color: #3D4852; font-size: 16px; line-height: 1.5em; margin-top: 0; text-align: left;">Regards,<br>E-KYC Team</p>

	                                        
	                                    </td>
	                                </tr>
	                            </table>
	                        </td>
	                    </tr>

	                    <tr>
	    <td style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; box-sizing: border-box;">
	        
	    </td>
	</tr>
	                </table>
	            </td>
	        </tr>
	    </table>
	</body>
	</html>
	"""
	part = MIMEText(html, 'html')
	msg.attach(part)
	try:
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login('ekyc59@gmail.com', 'kunal123*')
		mail.sendmail(me, you, msg.as_string())
		mail.quit()
		print('Email Sent Successfully')
		return [1,'success','success']
	except SMTPResponseException as e:
		error_code = e.smtp_code
		error_message = e.smtp_error
		print('Email Sending Failed')
		print(error_code+': '+error_message)
		return [0,error_code,error_message]
	

if __name__ == '__main__':
	send_email('pawarkunal5028@gmail.com','Abc','Def','Ghi','Male','12/12/1988','1233 6544 9877','ABHGY6759F','Jkl','Mno','908544')