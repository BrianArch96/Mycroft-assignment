import smtplib

def send_email(subject, content, recipient):

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    
    mail.ehlo()

    mail.starttls()

    mail.login('Mycroft.studentAssistant@gmail.com','Hannah10@')

    mail.sendmail("Mycroft.studentAssistant@gmail.com", recipient, content)

    mail.quit()


Subject = "Mycroft Assignment Update"
message = "Hello,\n\nSomething has been updated within the assignment skill.\n\n Best regards,\n\n Student Assistant Team."
recipient = "brianarch1996@gmail.com"
send_email(Subject, message, recipient)
