from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import speech_recognition as sr

class Inflow():
    def __init__(self):
        # Specify the path to chromedriver using Service class
        service = Service(executable_path=r'C:\drivers\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)

    def get_info(self, query):
        self.query = query
        self.driver.get("https://www.wikipedia.org")
        # Wait for the search input box to be present before proceeding
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
        except Exception as e:
            print("Page failed to load or search input not found:", e)
            return
        
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        enter = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button')
        enter.click()

        # Listen for exit command
    def listen_for_exit_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say 'exit' to close the program.")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                if text.lower() == 'exit':
                    self.driver.quit()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))


