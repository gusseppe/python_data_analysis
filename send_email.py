import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
fromaddr = "email@gmail.com"
toaddr = "email@gmail.com"
 
msg = MIMEMultipart()
         
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Bolsa de valores"

body = "Datos"

msg.attach(MIMEText(body, 'plain'))

filename = "data.h5"
attachment = open("./data.h5", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
