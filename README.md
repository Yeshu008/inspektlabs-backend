📘 Vehicle Inspection Backend API (Flask + MySQL)
🔍 What It Does
This is a backend REST API built using Flask (Python) and MySQL, designed for securely managing vehicle damage inspections. It allows users to register, log in, create inspections for vehicles, update their status (like "reviewed" or "completed"), and retrieve inspection data securely using JWT-based authentication.

* The project is modular, production-ready, and includes:
* Full input validation using Pydantic
* Centralized error handling
* Logging
* JWT token authentication with refresh token support
* MySQL database integration using SQLAlchemy
* Docker and optional CI/CD readiness

*********************************************************************************

⚙️ How to Run the App Locally
🔧 Prerequisites
Python 3.8+
MySQL Server (running and accessible)
(Optional but recommended) Virtual environment setup

🔌 Setup Steps
1.Clone the repository
    git clone https://github.com/yourname/vehicle-inspection-api.git
    cd vehicle-inspection-api

2.Create a .env file in the root directory with the following content:
    FLASK_ENV=development
    SECRET_KEY=your-secret-key
    JWT_SECRET_KEY=your-jwt-secret
    SQLALCHEMY_DATABASE_URI=mysql+pymysql://<user>:<password>@localhost/inspection_db

3.Install dependencies
    pip install -r requirements.txt

4.Initialize the MySQL database
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

5.Run the application
    python run.py

****Server will start on: http://127.0.0.1:5000/*****

******************************************************************************************
🔐 API Authentication Flow
    JWT Access Token (valid for 4 hours)
    JWT Refresh Token (used to get a new access token)
    Tokens are returned on login.

    Protected routes require:
    Authorization: Bearer <access_token>

    🔑 Authentication Routes
    
    | Method | Endpoint   | Description          |
    | ------ | ---------- | -------------------- |
    | POST   | `/signup`  | Register a new user  |
    | POST   | `/login`   | Login and get tokens |
    | POST   | `/refresh` | Refresh access token |

    🔒 Validation (via Pydantic)
        /signup
            * username: required, non-empty
            * password: required, strong string (validated)

        /login
            * username: required
            * password: required

    🧾 Inspection Routes

        | Method | Endpoint           | Description                       |
        | ------ | ------------------ | --------------------------------- |
        | POST   | `/inspection`      | Create a new inspection           |
        | GET    | `/inspection`      | List all inspections (filterable) |
        | GET    | `/inspection/<id>` | Get inspection details            |
        | PATCH  | `/inspection/<id>` | Update inspection status          |

        ✅ Validation for /inspection (POST)
            * vehicle_number: required, max length 15
            * damage_report: required
            * image_url: required, must end with .jpg, .jpeg, or .png

        ✅ Validation for /inspection/<id> (PATCH)
            * status: must be either "reviewed" or "completed" (validated using Literal in Pydantic)

***********************************************************************************************************

🧱 Database Setup
    * MySQL is used as the relational database.

    * SQLAlchemy is the ORM (Object Relational Mapper).

    * Flask-Migrate (based on Alembic) is used to manage schema migrations:

        * flask db init: initializes migration folder
        * flask db migrate: detects model changes and creates migration scripts
        * flask db upgrade: applies migration scripts to the database

    Tables:
        * users: Stores id, username, and hashed password
        * inspections: Stores id, vehicle_number, damage_report, image_url, status, user_id, timestamps


*****************************************************************************************************************

🚨 Centralized Error Handling
All errors are caught and returned in a consistent JSON format:
    Handled Error Codes:

        * 400: Validation errors or missing fields
        * 401: Invalid credentials or token
        * 403: Accessing another user’s inspection
        * 404: Resource not found
        * 500: Internal server error (logged)

**************************************************************************************************************

🧰 Tools Used
    | Tool                   | Purpose                    |
    | ---------------------- | -------------------------- |
    | **Flask**              | Web framework              |
    | **Flask-JWT-Extended** | Authentication using JWTs  |
    | **Flask-Bcrypt**       | Password hashing           |
    | **Pydantic**           | Payload validation         |
    | **Flask-SQLAlchemy**   | ORM for database           |
    | **Flask-Migrate**      | DB schema versioning       |
    | **MySQL**              | Relational DB              |
    | **Python Dotenv**      | Config loading from `.env` |
    | **Docker (optional)**  | Containerization           |


**********************************************************************************************************

🧪 Postman Collection for Testing
To test the API easily, a Postman collection is provided.

📥 How to Use:
    Open Postman.
    Click "Import" (top-left).
    Choose "Upload Files".
    Select the file: VehicleInspection.postman_collection.json
    It includes all routes with example requests and headers.

✅ Includes:

    Signup & Login with token response
    Token refresh
    Authenticated POST, GET, PATCH on /inspection
    Invalid test cases for validation errors

🔐 Don’t forget to replace the {{access_token}} variable with your JWT token in Authorization → Bearer Token before testing protected routes.

***************************************************************************************************************************************************
✅ Assessment Goals Covered

| Requirement                                         | Status  |
| --------------------------------------------------- | ------  |
| Flask app with login, register                      | ✅      |
| JWT Auth + Refresh                                  | ✅      |
| CRUD with MySQL + SQLAlchemy                        | ✅      |
| Pydantic validation for requests                    | ✅      |
| Centralized error handling with `@app_errorhandler` | ✅      |
| Logging using Python logger                         | ✅      |
| Organized modular codebase                          | ✅      |
| Docker/CI-ready codebase (optional)                 | ✅      |




