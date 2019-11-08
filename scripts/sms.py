# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC6ce5df1704f5ddd99953cec6f949e62a'
auth_token = 'd16e9ffe6d833cdfe9c743cee1c467e1'
client = Client(account_sid, auth_token)

def send_message(text, number):
    message = client.messages \
                    .create(
                        # body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        body = text,
                        from_='+12563635806',
                        # to='+6597700901'
                        to = number
                    )
    print(message.sid)