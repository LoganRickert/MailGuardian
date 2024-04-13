import requests

# Base URL for the email operations
base_url = 'http://localhost:5000/emails/'

# JSON data for requests
data_no_filter = {
    "collection_name": "example.com",
    "limit": 10
}
data_with_filter = {
    "collection_name": "example.com",
    "email_filter": "receiver@example.com",
    "limit": 10
}

# Function to log in and retrieve JWT
def get_jwt():
    login_url = 'http://localhost:5000/login'  # Change this if your login URL is different
    login_data = {
        "username": "679b8acc-b61c-49ad-8fc6-17c261b3130c",
        "password": "56a9ba4d-7fbe-44c5-be8b-8a1f167291be"
    }
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Authentication failed: ' + response.text)

# Function to make POST requests with JWT authentication
def make_request(data):
    jwt_token = get_jwt()  # Get JWT from the login function
    headers = {'Authorization': f'Bearer {jwt_token}'}  # Set the Authorization header
    response = requests.post(base_url, json=data, headers=headers)
    print(f'Requesting with data: {data}')
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print('Response:', response.json())
    else:
        print('Response:', response.text)

# Test without 'from' email filter
make_request(data_no_filter)

# Test with 'from' email filter
make_request(data_with_filter)
