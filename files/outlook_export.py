import win32com.client
import pandas as pd
from collections import Counter

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox

messages = inbox.Items
messages.Sort("[ReceivedTime]", True)  # Sort by most recent

# Extract senders
senders = []

print("Scanning emails...")

for message in messages:
    try:
        sender = message.SenderEmailAddress
        if sender:
            senders.append(sender.lower())
    except AttributeError:
        continue  # Skip calendar items or invalid messages

# Count frequency
sender_counts = Counter(senders)

# Convert to DataFrame
df = pd.DataFrame(sender_counts.items(), columns=['Sender', 'Count'])
df = df.sort_values(by='Count', ascending=False)

# Export to Excel
output_file = "outlook_sender_frequency.xlsx"
df.to_excel(output_file, index=False)

print(f"Export complete! File saved as {output_file}")