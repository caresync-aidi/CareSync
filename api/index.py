from fastapi import FastAPI
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app instance from backend
from app import app

# Vercel requires the app instance to be accessible. 
# This file acts as the entry point for the @vercel/python runtime.
