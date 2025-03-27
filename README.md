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

1. Clone the repository:
```bash
git clone https://github.com/kaiodadalt/healthy-eye.git
cd healthy-eye
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the model weights:
   - Download the GroundingDINO model weights from [Google Drive](https://drive.google.com/file/d/1X-XS4k4RQ2CN6oJSitg0AozbcCbZO1wl/view?usp=sharing)
   - Create a `weights` directory in the project root:
     ```bash
     mkdir weights
     ```
   - Place the downloaded `groundingdino_swint_ogc.pth` file in the `weights` directory

5. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

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
├── weights/
│   └── groundingdino_swint_ogc.pth
├── test_images/
├── main.py             # Main FastAPI application
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 