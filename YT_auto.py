import pywhatkit as kit
import pyttsx3 as tts
import speech_recognition as sr

# Initialize text-to-speech engine
engine = tts.init()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            engine.say(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            engine.say("Sorry, I did not understand that.")
            engine.runAndWait()
            return None
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            engine.say("Sorry, there was an issue with the speech recognition service.")
            engine.runAndWait()
            return None

def youtube():
    command = listen_for_command()
    if command:
        # Remove the word "play" and "on youtube" from the command
        cleaned_command = command.lower().replace("play", "").replace("on youtube", "").strip()
        
        # Print and speak the notification
        print(f"Playing '{cleaned_command}' on YouTube")
        engine.say(f"Playing '{cleaned_command}' on YouTube")
        
        # Play the video on YouTube
        kit.playonyt(cleaned_command)
        engine.runAndWait()

if __name__ == "__main__":
    youtube()
