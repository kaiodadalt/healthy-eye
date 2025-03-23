# FastAPI Starter Project

A simple FastAPI starter project with a hello world endpoint.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

You can run the application in two ways:

1. Using Python directly:
```bash
python main.py
```

2. Using Uvicorn:
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Returns a hello world message
- `GET /hello/{name}`: Returns a personalized hello message

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc` 