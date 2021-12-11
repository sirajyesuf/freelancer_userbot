from twilio.rest import Client
import config
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def send_sms(me, job_description, url):
    to_phone_number = f"+{me.phone}"
    client.messages.create(to=to_phone_number, from_=config.TWILIO_FROM_PHONE_NUMBER,
                           body=f"{job_description}\n\n{url}")
