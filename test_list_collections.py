import requests

# Function to log in and get a JWT
def get_jwt():
    login_url = 'http://localhost:5000/login'  # Adjust this if your login endpoint differs
    login_data = {
        "username": "679b8acc-b61c-49ad-8fc6-17c261b3130c",
        "password": "56a9ba4d-7fbe-44c5-be8b-8a1f167291be"
    }
    response = requests.post(login_url, data=login_data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to retrieve JWT token: ' + response.text)

# Function to access the list-collections endpoint with JWT authentication
def list_collections(jwt):
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    response = requests.get(url, headers=headers)
    
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print('Response:', response.json())
    else:
        print('Failed to list collections:', response.text)

if __name__ == "__main__":
    # Endpoint URL for listing collections
    url = 'http://localhost:5000/list-collections'

    # Get JWT
    token = get_jwt()

    # Use JWT to authenticate and access the list-collections endpoint
    list_collections(token)
