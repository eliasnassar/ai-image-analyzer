# AI Image Analyzer

AI-powered Streamlit web application for batch image analysis using OpenAI Vision models.

The app allows users to upload multiple images, generate structured AI metadata, search results, and export per-image JSON files.

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

## Installation

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

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Docker

Build image:

```bash
docker build -t ai-image-analyzer .
```

Run container:

```bash
docker run -p 8501:8501 ai-image-analyzer
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
