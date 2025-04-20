import speech_recognition as sr
import pyttsx3
import json

# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Adjust microphone sensitivity (optional)
def adjust_microphone_sensitivity(source):
    r.adjust_for_ambient_noise(source)

def recognize_speech():
    with sr.Microphone() as source:
        adjust_microphone_sensitivity(source)
        try:
            audio = r.listen(source, timeout=10) 
            text = r.recognize_google(audio)
            print(f"{text}")
            return text
        except sr.UnknownValueError:
            print("Speech not understood.")
            return None
        except sr.RequestError:
            print("Error with the speech recognition service.")
            return "Error with the speech recognition service."
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None

# Define a function to handle text-to-speech
def speak_text(text):
    print(f"{text}")
    engine.say(text)
    engine.runAndWait()

# Define a function to get input from the user with error handling
def get_input(prompt):
    speak_text(prompt)
    response = recognize_speech()
    while response is None or response == "I didn't understand that.":
        speak_text("Sorry, I didn't catch that. Please repeat.")
        print("Sorry, I didn't catch that. Please repeat.")
        response = recognize_speech()
    return response

# Define a function to build a resume
def build_resume():
    resume = {}
    
    # Collect personal information
    resume["name"] = get_input("What is your full name?")
    resume["email"] = get_input("What is your email address?")
    resume["phone"] = get_input("What is your phone number?")
    resume["linkedin"] = get_input("What is your LinkedIn profile URL?")
    resume["github"] = get_input("What is your GitHub profile URL?")
    
    # Collect professional information
    resume["summary"] = get_input("Please provide a professional summary.")
    resume["skills"] = get_input("What are your key skills? Please mention them separated by commas.")
    resume["experience"] = get_input("Please describe your professional experience, including your job titles, companies, and dates.")
    resume["education"] = get_input("Please describe your education background, including your degrees and institutions.")
    
    # Collect additional sections
    resume["certifications"] = get_input("Do you have any certifications or awards? Please describe them.")
    resume["projects"] = get_input("Do you have any notable projects? Please provide details.")
    resume["affiliations"] = get_input("Are there any professional affiliations or memberships you would like to include?")
    resume["languages"] = get_input("What languages do you speak? Please mention them separated by commas.")
    resume["hobbies"] = get_input("What are your hobbies or interests? Please describe them.")
    
    # Save the resume to a JSON file
    try:
        with open("resume.json", "w") as f:
            json.dump(resume, f, indent=4)
        speak_text("Resume saved successfully!")
    except IOError:
        speak_text("An error occurred while saving the resume.")
        print("An error occurred while saving the resume.")
