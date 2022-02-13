import yaml

if __name__ == '__main__':
    # open file
    with open("emails.yaml") as f:
        try:
            data = yaml.load(f, Loader=yaml.Loader)
        except:
            print("Email file not found")
        else:
            # go over every account

            for account in data:
                name = account['name']
                email = account['email']
                password = account['password']
                smtp = account['smtp']
                imap = account['imap']

                # check if smtp is defined
                if smtp is None:
                    print(F"smtp must be defined for: {email}")
                    continue

                # create smtp request

