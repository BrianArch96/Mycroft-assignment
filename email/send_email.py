import smtplib

def send_email(subject, content, recipient):

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    
    mail.ehlo()

    mail.starttls()

    mail.login('Mycroft.studentAssistant@gmail.com','Hannah10@')

    mail.sendmail("Mycroft.studentAssistant@gmail.com", recipient, content)

    mail.quit()
