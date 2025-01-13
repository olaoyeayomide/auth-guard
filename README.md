# Auth Guard

### Authentication App

This is an authentication application built using FastAPI, SQLAlchemy, and JWT. The app provides a secure system for user registration, login, and password recovery. It supports email-based authentication and token-based security using JWT.

## Features

- User Registration
- User Login
- Token-based Authentication (JWT)
- Password Recovery (Forgotten Password)
- Database Integration with PostgreSQL
- Secure Password Hashing using Bcrypt

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Email Service**: `fastapi_mail` for sending recovery emails
- **Password Hashing**: Bcrypt

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/olaoyeayomide/PRODIGY_FS_01.git
    cd PRODIGY_FS_01
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    .\venv\Scripts\activate  # For Windows
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables in a `.env` file:

    ```
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=postgresql://username:password@localhost:5432/dbname
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    MAIL_FROM=your_email@example.com
    MAIL_PORT=587
    MAIL_SERVER=smtp.example.com
    ```

5. Set up the PostgreSQL database:

    - Make sure PostgreSQL is installed and running.
    - Create a new database in PostgreSQL and update the `DATABASE_URL` in your `.env` file.

6. Apply database migrations:

    ```bash
    alembic upgrade head
    ```

7. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

    The app will be available at `http://127.0.0.1:8000`.

## Endpoints

- **POST** `/register`: Register a new user.
- **POST** `/login`: Log in a user and receive a JWT token.
- **POST** `/forgot-password`: Request a password reset link via email.
- **POST** `/reset-password`: Reset the password using the token from the email.
- **GET** `/users/me`: Get information about the currently authenticated user.

## Project Structure


## Usage

1. **Register a User**:
   - Send a POST request to `/register` with a JSON payload:
     ```json
     {
       "email": "user@example.com",
       "password": "your_password"
     }
     ```

2. **Login**:
   - Send a POST request to `/login` with your email and password. It will return a JWT token.
     ```json
     {
       "email": "user@example.com",
       "password": "your_password"
     }
     ```

3. **Forgot Password**:
   - Send a POST request to `/forgot-password` with your email to receive a password reset link.

4. **Reset Password**:
   - Use the token received from the email and send a POST request to `/reset-password` with the new password.

## Contributing

Feel free to fork this repository, create a branch, and submit a pull request for any improvements.

## License

This project is licensed under the MIT License.


