import yaml
import smtplib, ssl

class Mail:

    def __init__(self, smtp_domain, smtp_port, smtp_sender, sender_password):
        self.port = smtp_port
        self.smtp_domain = smtp_domain
        self.smtp_sender = smtp_sender
        self.sender_password = sender_password

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_domain, self.port, context=ssl_context)
        service.login(self.smtp_sender, self.sender_password)
        
        for email in emails:
            result = service.sendmail(self.smtp_sender, email, f"Subject: {subject}\n{content}")

        service.quit()
        return result