from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACf97f59a4fd24c6f630c588cea3f7a68c"
# Your Auth Token from twilio.com/console
auth_token  = "3a0280a6c90780d2def86447303a83fd"

client = Client(account_sid, auth_token)

# message = client.messages.create(
#     to="+12015510233",
#     from_="+18447443520",
#     body="Hello from Python Script!")

# try:
#   # This could potentially throw an exception!
#   message = client.messages.create(
#     to="+15558675309",
#     from_="+15017250604",
#     body="Hello there!")
# except TwilioRestException as err:
#   # Implement your fallback code here
#   print(err)

# Silas: 14242074406
# Amy: 18326127916
# Wonjun: 12015510233

# print(message.sid)

for sms in client.messages.list():
  print(sms.to)