# Healthy-eye

A modern API for detecting fruits & vegetables in meal images. This project aims to help users identify and analyze the nutritional content of their meals through image recognition.

## Features

- Image-based fruit and vegetable detection using GroundingDINO
- Zero-shot detection capabilities
- Detailed confidence scores for detected items
- RESTful API endpoints for easy integration
- Real-time processing capabilities
- Comprehensive API documentation

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

3. Install GroundingDINO:
```bash
cd GroundingDINO && pip install -e . && cd ..
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

### GET /
- Description: Welcome endpoint
- Response: Welcome message

### POST /detect
- Description: Upload an image and detect fruits and vegetables in it
- Content-Type: multipart/form-data
- Parameters:
  - file: Image file (jpg, png, etc.)
- Response:
  ```json
  {
    "message": "Image processed successfully",
    "detected_items": ["apple", "banana", "carrot"],
    "confidence_scores": [0.95, 0.88, 0.92]
  }
  ```

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc`

## Project Structure

```
healthy-eye/
├── app/
│   ├── models/          # Data models
│   ├── routes/          # API routes
│   └── services/        # Business logic
├── GroundingDINO/       # GroundingDINO model
├── main.py             # Main FastAPI application
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 