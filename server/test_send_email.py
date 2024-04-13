import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
webhook_uuid = os.getenv('WEBHOOK_UUID', 'default-uuid')

# Endpoint URL
url = f'http://localhost:5000/webhook/{webhook_uuid}'

# Prepare the multipart/form-data
form_data = {
    'headers': 'Example header content',
    'dkim': 'pass',
    'html': '<div>Sample HTML content</div>',
    'text': 'Sample plain text',
    'from': 'sender@example.com',
    'to': 'receiver@example.com',
    'sender_ip': '192.168.1.1',
    'spam_report': 'No spam detected',
    'envelope': '{"to":["receiver@example.com"],"from":"sender@example.com"}',
    'attachments_count': '1',
    'subject': 'Test Email',
    'spam_score': '0.1',
    'charsets': '{"html":"UTF-8"}',
    # 'SPF': 'pass'
}

# Files to upload
files = {
    'files': ('README.md', open('README.md', 'rb'), 'text/plain')
}

# Send the POST request
response = requests.post(url, data=form_data, files=files)

# Close the file handle
files['files'][1].close()

# Print the response from the server
print(f'Status Code: {response.status_code}')
print('Response:', response.text)
