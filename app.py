"""
AI Image Analyzer

A Streamlit web app that allows users to upload images and analyze them using
OpenAI's vision models. The app extracts structured metadata such as:
- Description
- Objects
- Mood
- Caption

Users can search results and download metadata as JSON.
"""

from dotenv import load_dotenv
import os
import base64
import json
from typing import List, Dict, Any

from PIL import Image
import streamlit as st
from openai import OpenAI


MODEL_NAME = "gpt-4.1-mini"


# ------------------------
# Setup
# ------------------------
def init_client() -> OpenAI:
    """
    Initialize OpenAI client using API key from environment variables.

    Returns:
        OpenAI: Configured OpenAI client instance.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    return OpenAI(api_key=api_key)


def init_session() -> None:
    """
    Initialize Streamlit session state.

    Ensures 'results' key exists in session state.
    """
    if "results" not in st.session_state:
        st.session_state.results = []


# ------------------------
# UI Components
# ------------------------
def render_header():
    """
    Render the main header and file uploader.

    Returns:
        tuple: Uploaded files and center column container.
    """
    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.title("AI Image Analyzer")
        uploaded_files = st.file_uploader(
            "Upload images",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )

    return uploaded_files, center


def render_upload_preview(uploaded_files, center) -> List[Dict[str, Any]]:
    """
    Display uploaded images in a grid preview.

    Args:
        uploaded_files: List of uploaded file objects.
        center: Streamlit column container.

    Returns:
        List[Dict]: Processed image data including name, PIL image, and bytes.
    """
    images_data = []

    with center:
        st.subheader("Uploaded Images")
        cols = st.columns(5, gap="small")

        for i, file in enumerate(uploaded_files):
            image = Image.open(file)

            preview = image.copy()
            preview.thumbnail((300, 300))

            with cols[i % 5]:
                st.image(preview)
                st.caption(file.name)

            images_data.append({
                "name": file.name,
                "image": image,
                "bytes": file.getvalue()
            })

    return images_data


# ------------------------
# Processing
# ------------------------
def analyze_image(client: OpenAI, item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a single image using OpenAI API.

    Args:
        client (OpenAI): OpenAI client instance.
        item (dict): Image data including raw bytes.

    Returns:
        dict: Parsed JSON response or error message.
    """
    image_base64 = base64.b64encode(item["bytes"]).decode("utf-8")

    prompt = """
    Return ONLY valid JSON:

    {
      "description": "...",
      "objects": ["..."],
      "mood": "...",
      "caption": "..."
    }
    """

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }]
        )

        text = response.output_text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except (json.JSONDecodeError, KeyError, AttributeError) as exc:
        return {"error": f"Invalid response format: {str(exc)}"}

    except Exception as exc:
        return {"error": f"Unexpected error: {str(exc)}"}


def process_images(client: OpenAI, images_data: List[Dict[str, Any]]) -> None:
    """
    Process multiple images and store results in session state.

    Args:
        client (OpenAI): OpenAI client instance.
        images_data (list): List of image data dictionaries.
    """
    st.session_state.results = []
    progress_bar = st.progress(0)

    total = len(images_data)

    for idx, item in enumerate(images_data):
        result = analyze_image(client, item)

        st.session_state.results.append({
            "name": item["name"],
            "image": item["image"],
            "result": result
        })

        progress_bar.progress((idx + 1) / total)


# ------------------------
# Results UI
# ------------------------
def filter_results(results: List[Dict], query: str) -> List[Dict]:
    """
    Filter results based on keyword search.

    Args:
        results (list): List of analyzed image results.
        query (str): Search query.

    Returns:
        list: Filtered results.
    """
    if not query:
        return results

    query = query.lower()

    keywords = [
        query,
        f"{query}s",
        f"{query}ing",
        f"{query.rstrip('e')}ing"
    ]

    filtered = []

    for item in results:
        result = item["result"]

        if "error" in result:
            continue

        text_blob = (
            f"{result['description']} "
            f"{result['mood']} "
            f"{' '.join(result['objects'])}"
        ).lower()

        if any(keyword in text_blob for keyword in keywords):
            filtered.append(item)

    return filtered


def render_results() -> None:
    """
    Render analyzed results and search functionality.
    """
    if not st.session_state.results:
        return

    st.subheader("Results")

    query = st.text_input("🔍 Search (e.g. dog, calm, selfie)")
    filtered_results = filter_results(st.session_state.results, query)

    if not filtered_results:
        st.info("No matching results found")
        return

    cols = st.columns(3)

    for idx, item in enumerate(filtered_results):
        col = cols[idx % 3]

        with col:
            preview = item["image"].copy()
            preview.thumbnail((250, 250))
            st.image(preview)

            result = item["result"]

            if "error" not in result:
                st.markdown(f"**{item['name']}**")
                st.write("🧠 Description:", result["description"])
                st.write("📦 Objects:", ", ".join(result["objects"]))
                st.write("🎭 Mood:", result["mood"])
                st.write("✏️ Caption:", result["caption"])

                filename = os.path.splitext(item["name"])[0]

                st.download_button(
                    label="⬇️ Download JSON",
                    data=json.dumps(result, indent=2),
                    file_name=f"{filename}.json",
                    mime="application/json",
                    key=f"download_{idx}"
                )
            else:
                st.write("❌ Error processing image")

            st.markdown("---")


# ------------------------
# Main App
# ------------------------
def main() -> None:
    """
    Entry point for the Streamlit application.
    """
    st.set_page_config(layout="wide")

    client = init_client()
    init_session()

    uploaded_files, center = render_header()

    if uploaded_files:
        images_data = render_upload_preview(uploaded_files, center)

        with center:
            start = st.button("Start Captioning")

        if start:
            process_images(client, images_data)

    render_results()


if __name__ == "__main__":
    main()