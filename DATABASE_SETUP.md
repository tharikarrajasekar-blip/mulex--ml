# MuleX AI Backend - Database Connection Guide

## Prerequisites

Before running the backend, ensure you have:

1. **PostgreSQL** installed and running
2. **Python 3.8+** installed
3. **pip** package manager

## Step 1: Install Dependencies

```powershell
cd c:\Users\thari\Downloads\MULEX.ML\backend
pip install -r requirements.txt
```

## Step 2: Configure Database Connection

Edit `.env` file with your PostgreSQL credentials:

```
DATABASE_URL=postgresql://username:password@hostname:port/database_name
PORT=8000
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Example Configurations:

**Local PostgreSQL (default):**
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/mulex
```

**Remote PostgreSQL:**
```
DATABASE_URL=postgresql://user:password@db.example.com:5432/mulex
```

**Using PostgreSQL on Windows:**
```
DATABASE_URL=postgresql://postgres:YourPassword@127.0.0.1:5432/mulex
```

## Step 3: Initialize Database

Run the initialization script to create all tables:

```powershell
python init_db.py
```

Expected output:
```
==================================================
MuleX AI Backend - Database Setup
==================================================
✅ Database connection successful!
🔄 Creating database tables...
✅ Database tables created successfully!

✅ Database setup complete! Ready to start the server.
   Run: uvicorn app.main:app --reload
```

## Step 4: Start the Server

```powershell
python -m uvicorn app.main:app --reload
```

Server will be running at: `http://localhost:8000`

API Documentation available at: `http://localhost:8000/docs`

## Database Tables Created

- `users` - User accounts and authentication
- `alerts` - Risk alerts and notifications
- `transactions` - Transaction records

## Available API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/token` | POST | Login / Get access token |
| `/users/me` | GET | Get current user info |
| `/dashboard/metrics` | GET | Get dashboard KPI metrics |
| `/dashboard/alerts` | GET | Get alerts list |
| `/alerts` | POST | Create new alert |
| `/transactions` | POST | Create transaction record |
| `/ws/feed` | WebSocket | Live transaction feed stream |

## Troubleshooting

### ❌ "Connection refused" error
- Ensure PostgreSQL is running
- Check DATABASE_URL format is correct
- Verify hostname, port, and credentials

### ❌ "Database does not exist" error
- Create the database first: `CREATE DATABASE mulex;`
- Or update DATABASE_URL with correct database name

### ❌ "FATAL: Ident authentication failed"
- Use password authentication in connection string
- Format: `postgresql://username:password@localhost/dbname`

### ❌ "psycopg2" import error
- Run: `pip install psycopg2-binary`

## Next Steps

1. ✅ Configure `.env` file
2. ✅ Run `python init_db.py`
3. ✅ Start server with `uvicorn app.main:app --reload`
4. ✅ Connect frontend to `http://localhost:8000`
5. ✅ Add more models/routes as needed

---
For more help, check the FastAPI docs: https://fastapi.tiangolo.com/
