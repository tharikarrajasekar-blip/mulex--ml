"""
Configuration settings for MuleX AI Backend
Loads environment variables from .env file
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mulex")

# Server
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")

# Validation checks
if "postgresql" not in DATABASE_URL:
    print("⚠️ Warning: DATABASE_URL should use PostgreSQL connection string")
