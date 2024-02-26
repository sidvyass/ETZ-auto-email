import win32com.client
import os

outlook = win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")

# number 6 represents the inbox folder.
inbox = outlook.GetDefaultFolder(6)

messages = inbox.Items
print(messages.GetLast())
