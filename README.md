# AI Image Analyzer

AI-powered Streamlit web application for batch image analysis using OpenAI Vision models.

The app allows users to upload multiple images, generate structured AI metadata, search results, and export per-image JSON files.

---

## Screenshots

### Upload Screen

![Upload Screen](screenshots/upload-screen.png)

---

### Analysis Results

![Analysis Results](screenshots/results-screen.png)

---

## Features

- Upload multiple images
- AI-generated image descriptions
- Object detection
- Mood analysis
- Caption generation
- Keyword search across analyzed images
- Download metadata as JSON
- Responsive Streamlit UI
- Docker support

---

## Tech Stack

- Python
- Streamlit
- OpenAI API
- Pillow (PIL)
- Docker

---

# Running the Application

You can run the project either:

1. Locally with Python
2. Using Docker

---

## Option 1 — Run Locally

### Clone repository

```bash
git clone https://github.com/eliasnassar/ai-image-analyzer.git
cd ai-image-analyzer
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create `.env` file

```env
OPENAI_API_KEY=your_api_key_here
```

### Run application

```bash
streamlit run app.py
```

Open in browser:

```text
http://localhost:8501
```

---

## Option 2 — Run with Docker

### Clone repository

```bash
git clone https://github.com/eliasnassar/ai-image-analyzer.git
cd ai-image-analyzer
```

### Build Docker image

```bash
docker build -t ai-image-analyzer .
```

### Run Docker container

```bash
docker run -p 8501:8501 \
-e OPENAI_API_KEY=your_api_key_here \
ai-image-analyzer
```

Open in browser:

```text
http://localhost:8501
```

---

## Option 3 — Run Prebuilt Docker Hub Image

Pull image from Docker Hub:

```bash
docker pull eliasnassar/image-analyzer:v1
```

Run container:

```bash
docker run -p 8501:8501 \
-e OPENAI_API_KEY=your_api_key_here \
eliasnassar/image-analyzer:v1
```

Open in browser:

```text
http://localhost:8501
```

---

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .dockerignore
└── README.md
```

---

## Future Improvements

- Drag & drop uploads
- Better semantic search
- Image tagging system
- Database storage
- Authentication
- Gallery view
- Async processing

---

## License

MIT License
