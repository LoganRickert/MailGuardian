import requests

# URL of the login endpoint
url = 'http://localhost:5000/api/v1/login'  # Adjust the port and endpoint if necessary

# Data to send in the POST request
login_data = {
    "username": "679b8acc-b61c-49ad-8fc6-17c261b3130c",
    "password": "56a9ba4d-7fbe-44c5-be8b-8a1f167291be"
}

def login_user():
    # Send the POST request
    response = requests.post(url, data=login_data)

    # Print the status code and response data
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print('Login Successful! Token:', response.json())
    else:
        print('Login Failed. Response:', response.json())

if __name__ == "__main__":
    login_user()
