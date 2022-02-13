import yaml
import smtplib
from email.mime.text import MIMEText

if __name__ == '__main__':
    # open file
    with open("emails.yaml") as f:
        try:
            data = yaml.load(f, Loader=yaml.Loader)
        except Exception as e:
            print(f"Email file not found\nError: {e}")
        else:
            # go over every account
            # first ask for a bot receiver
            receiver = input("Add receiver: ")
            subject = input('Add a subject: ')
            message = input("Message: ")

            if len(receiver) < 1:
                print("No receiver added")
                exit(1)

            if len(subject) < 1:
                print("No subject added")
                exit(1)

            if len(message) < 1:
                print("No Message")
                exit(1)

            for account in data:
                name = account['name']
                email = account['email']
                password = account['password']
                smtp = account['smtp']
                smtp_port = account['smtp_port']
                imap = account['imap']

                # check if smtp is defined
                if smtp is None or smtp_port is None:
                    print(F"smtp must be defined for: {email}")
                    continue

                # create smtp request
                sender = email
                port = 1025
                msg = MIMEText(message)

                # put message together

                msg['Subject'] = subject
                msg['From'] = email
                msg['To'] = receiver

                # send message
                try:

                    with smtplib.SMTP(smtp, smtp_port) as server:
                        # config
                        server.ehlo()
                        server.starttls()
                        server.ehlo()
                        # login
                        server.login(email, password)
                        # send
                        server.sendmail(sender, receiver, msg.as_string())
                except Exception as e:
                    print(f"Error: Email couldn't be send\nError: {e}")
                else:
                    print("Email was send")
