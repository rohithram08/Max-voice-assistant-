import os
import requests
from bs4 import BeautifulSoup
import pyttsx3
from urllib.parse import urljoin

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def download_file(url, filename):
    """Download a file from a given URL and save it as filename"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for request errors
        
        # Check Content-Type to ensure it's an image
        content_type = response.headers.get('Content-Type')
        if not content_type or not content_type.startswith('image'):
            print(f"Invalid content type: {content_type}")
            return None

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def find_image_url(query):
    """Find an image URL based on a search query"""
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    if img_tags:
        img_url = img_tags[1]['src']
        img_url = urljoin(search_url, img_url)  # Ensure the URL is complete
        print(f"Found image URL: {img_url}")  # Debugging: Print the URL
        return img_url
    return None

def handle_download_request(text):
    """Handle download request based on user voice command"""
    if "download" in text:
        search_query = text.split("download")[-1].strip()
        speak(f"Okay sir, your download for {search_query} is in progress.")
        
        # Find image URL
        image_url = find_image_url(search_query)
        if image_url:
            # Download the image
            filename = f"{search_query}.jpg"
            result = download_file(image_url, filename)
            if result:
                speak(f"Here is the image you asked for: {filename}")
                print(f"Image downloaded and saved as {filename}")
            else:
                speak("Sorry, I couldn't download the image.")
        else:
            speak("Sorry, I couldn't find an image for that search query.")
