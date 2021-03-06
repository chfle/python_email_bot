import yaml
import smtplib
from email.mime.text import MIMEText
import threading


def send_mail(smtp_, smtp_port_, email_, password_, sender_, receiver_, msg_):
    try:

        with smtplib.SMTP(smtp_, smtp_port_) as server:
            # config
            server.ehlo()
            server.starttls()
            server.ehlo()
            # login
            server.login(email_, password_)
            # send
            server.sendmail(sender_, receiver_, msg_.as_string())
    except Exception as e:
        print(f"Error: Email couldn't be send\nError: {e}")
    else:
        print(f"{email_}- Email was send")


if __name__ == '__main__':
    # open file
    with open("emails.yaml") as f:
        print("""\033[92m              _____ __  __    _    ___ _         ____   ___ _____ 
             | ____|  \/  |  / \  |_ _| |       | __ ) / _ \_   _|
             |  _| | |\/| | / _ \  | || |       |  _ \| | | || |  
             | |___| |  | |/ ___ \ | || |___    | |_) | |_| || |  
             |_____|_|  |_/_/   \_\___|_____|___|____/ \___/ |_|  
                                |Christian Lehnert|
        \033[0m""")
        print("\033[91m OWNER: Christian Lehnert <https://github.com/chfle> \033[0m")
        print("\033[92m REPO: https://github.com/chfle/python_email_bot \033[0m")
        print("\033[95m Version: 1.1.0 \033[0m")
        print("\n\n")
        try:
            data = yaml.load(f, Loader=yaml.Loader)
        except Exception as e:
            print(f"Email file not found\nError: {e}".center(80))

        else:
            # go over every account
            # first ask for a bot receiver
            receiver = input("\033[93m \033[4mReceiver:\033[0m ")

            subject = input("\033[93m \033[4mSubject:\033[0m ")
            message = input("\033[93m \033[4mMessage:\033[0m ")

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

                # send message with threads
                try:
                    threading.Thread(target=send_mail,
                                     args=(smtp, smtp_port, email, password, sender, receiver, msg)).start()
                except Exception as e:
                    print(f"Thread failed\nError: {e}")
