**MailGuardian** is a robust and secure email management system designed to enhance email interactions through controlled access and monitoring. Utilizing FastAPI for backend operations, MailGuardian leverages SendGrid as a proxy SMTP server to manage the sending and receiving of emails. With built-in user authentication and permissions management, MailGuardian ensures that access to email data and operations is both secure and efficient.

### Features

- **User Authentication:** Secure login system with JWT (JSON Web Token) for accessing API endpoints.
- **Role-Based Access Control:** Define roles such as viewer, member, or admin to grant varying levels of access to email data.
- **Email Management:** Send and receive emails securely via SendGrid, with support for managing permissions for different collections and email addresses.
- **Secure Setup:** Uses bcrypt for hashing passwords to ensure data security.

### Installation

MailGuardian requires Python 3.7+ and MongoDB. Before installation, ensure that you have Python and MongoDB installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LoganRickert/MailGuardian.git
   cd MailGuardian
   ```

2. **Setup Virtual Environment (optional but recommended):**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   python setup.py install
   ```

### Configuration

Before running the application, configure the necessary environment variables:

- **Database URL:** Set the MongoDB connection string in your environment variables.
- **SendGrid API Key:** Ensure your SendGrid API Key is set to allow MailGuardian to send and receive emails.
- **JWT Secret Key:** Used for signing the JWT tokens. This should be a long, random, and secure string.

These variables can be set in a `.env` file or directly in your shell.

### Running the Server

To start the MailGuardian server, simply run:

```bash
./run.sh
```

This script initializes the FastAPI server and makes the application available on `http://localhost:5000` by default.

### Usage

After starting the server, you can access MailGuardian via the following endpoints:

- **POST /login:** Authenticate users and retrieve a token.
- **POST /users/:** Create, update, and delete user information.
- **GET /list-collections:** Retrieve a list of all collections a user has access to, based on their permissions.

Detailed API documentation is available at `http://localhost:5000/docs` thanks to FastAPI's automatic Swagger UI.

### Support

For support, please open an issue on the GitHub repository.

---

**MailGuardian** is dedicated to providing a secure and efficient email management solution. For more information, updates, and contributions, please visit the GitHub repository.

## Client

curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt-get install -y nodejs
npm install -g @angular/cli

cp environments/environment.ts environments/environment.dev.ts
