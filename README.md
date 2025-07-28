
# 📘 Vehicle Inspection Backend API (Flask + MySQL)

A secure and modular REST API built using **Flask** and **MySQL** to manage vehicle damage inspections. It supports:

- ✅ User registration & login with JWT authentication (access + refresh tokens)
- ✅ Inspection creation and updates
- ✅ Full input validation using **Pydantic**
- ✅ Centralized error handling & logging
- ✅ Docker-ready setup and CI/CD friendly structure

---

## ⚙️ How to Run Locally

### 🔧 Prerequisites

- Python 3.8+
- MySQL Server (running & accessible)
- (Optional but recommended) Python virtual environment

---

### 🔌 Setup Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Yeshu008/inspektlabs-backend.git
cd inspektlabs-backend
```

#### 2️⃣ Create a `.env` File

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@localhost/inspection_db
```

> Replace `<username>` and `<password>` with your MySQL credentials.

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Initialize the Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 5️⃣ Run the Application

```bash
python run.py
```

> 🚀 The server will start at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🔐 API Authentication

- 🔑 **Access Token** (valid for 4 hours)
- ♻️ **Refresh Token** (used to get new access token)

Add this header to access protected routes:

```
Authorization: Bearer <access_token>
```

---

## 🔑 Authentication Endpoints

| Method | Endpoint   | Description          |
|--------|------------|----------------------|
| POST   | `/signup`  | Register a new user  |
| POST   | `/login`   | Log in and get tokens|
| POST   | `/refresh` | Get a new access token|

### ✅ Validation

#### `/signup`
- `username`: required, non-empty
- `password`: required, minimum 6 characters

#### `/login`
- `username`: required
- `password`: required

---

## 🧾 Inspection Endpoints

| Method | Endpoint             | Description                       |
|--------|----------------------|-----------------------------------|
| POST   | `/inspection`        | Create a new inspection           |
| GET    | `/inspection`        | List all inspections              |
| GET    | `/inspection/<id>`   | Get details of a specific record  |
| PATCH  | `/inspection/<id>`   | Update inspection status          |

### ✅ Validation

#### `/inspection` (POST)

- `vehicle_number`: required, max length 15
- `damage_report`: required
- `image_url`: required, must end with `.jpg`, `.jpeg`, or `.png`

#### `/inspection/<id>` (PATCH)

- `status`: must be either `"reviewed"` or `"completed"`

---

## 🧱 Database Setup

- **MySQL** is the database engine
- **SQLAlchemy** is used for ORM
- **Flask-Migrate** handles schema migrations

### Migration Commands

```bash
flask db init      # First-time setup
flask db migrate   # Detects model changes
flask db upgrade   # Applies migrations
```

### Tables

- `users`: Stores username & hashed password
- `inspections`: Stores inspection data, user linkage, and status

---

## 🚨 Centralized Error Handling

All errors return consistent JSON responses:

| Status Code | Description                    |
|-------------|--------------------------------|
| 400         | Validation error               |
| 401         | Unauthorized / Invalid Token   |
| 403         | Forbidden (e.g., wrong user)   |
| 404         | Resource not found             |
| 500         | Internal server error          |

---

## 🧰 Tools Used

| Tool                  | Purpose                      |
|-----------------------|------------------------------|
| **Flask**             | Web framework                |
| **Flask-JWT-Extended**| JWT Authentication           |
| **Flask-Bcrypt**      | Password hashing             |
| **Pydantic**          | Input validation             |
| **Flask-SQLAlchemy**  | Database ORM                 |
| **Flask-Migrate**     | DB migrations                |
| **MySQL**             | Relational database          |
| **Python-Dotenv**     | Load environment variables   |
| **Docker**            | Optional: Containerization   |

---

## 🧪 Postman Collection (for Testing)

A full Postman collection is provided:

### ✅ Includes

- Signup & Login
- Token Refresh
- Authenticated Inspection POST / GET / PATCH
- Validation error examples

### 📥 How to Use

1. Open Postman
2. Click **Import**
3. Upload: `VehicleInspection.postman_collection.json`
4. Add your token to:
   ```
   Authorization → Bearer <access_token>
   ```

---

## ✅ Goals Covered

| Requirement                                         | Status  |
|----------------------------------------------------|---------|
| Flask app with login/register                      | ✅       |
| JWT Auth + Refresh                                 | ✅       |
| CRUD operations with MySQL                         | ✅       |
| Request validation using Pydantic                  | ✅       |
| Centralized error handling                         | ✅       |
| Logging with Python’s logging module               | ✅       |
| Modular project structure                          | ✅       |


🚀 Live API Deployment
The Vehicle Inspection API is live and accessible at:
https://inspection-backend-y7gx.onrender.com

