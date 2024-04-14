import requests
import uuid

# URL of the endpoint
url = 'http://localhost:5000/users/'  # Adjust the port if necessary

# Data to send in the POST request
user_data = {
    "username": "679b8acc-b61c-49ad-8fc6-17c261b3130c",
    "password": "56a9ba4d-7fbe-44c5-be8b-8a1f167291be",
    "role": "member",
    "permissions": [
        {
            "collection_name": "example_collection",
            "emails": ["example@example.com"],
            "can_read": True,
            "can_send": False
        }
    ]
}

def create_user():
    print(user_data)
    # Send the POST request
    response = requests.post(url, json=user_data)

    # Print the status code and response data
    print(f'Status Code: {response.status_code}')
    print('Response:', response.json())

if __name__ == "__main__":
    create_user()
