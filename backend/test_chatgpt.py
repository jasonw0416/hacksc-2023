import chat_gpt as master

response = master.ask_chat_gpt("USC", "UCLA", "bus", 300)
print(response.strip())


