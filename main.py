#Source: Arnab Mondal (Analytics Vidhya)
#Modified: Shivansh Shukla (SJSU, Graduated Fall '23)


# Import necessary libraries for speech-to-text, text-to-speech, language model, and other functionalities
import speech_recognition as sr
from gtts import gTTS
import transformers
import os
import time
import datetime
import numpy as np

# Define a class for the ChatBot
class ChatBot():
    def __init__(self, name):
        # Display a message indicating the ChatBot is starting up
        print("----- Starting up", name, "-----")
        self.name = name
    
    # Method for converting speech to text using Google's speech recognition
    def speech_to_text(self):
        # Create a speech recognizer instance
        recognizer = sr.Recognizer()
        # Use the microphone to capture audio
        with sr.Microphone() as mic:
            # Display a message indicating that the ChatBot is listening
            print("Listening...")
            # Listen to the microphone input
            audio = recognizer.listen(mic)
            # Set a default value for the text (in case of an error)
            self.text="ERROR"
        try:
            # Attempt to recognize speech using Google's speech recognition
            self.text = recognizer.recognize_google(audio)
            # Display the recognized text
            print("Me  --> ", self.text)
        except:
            # Display an error message if speech recognition fails
            print("Me  -->  ERROR")
    
    # Static method for converting text to speech using gTTS library
    @staticmethod
    def text_to_speech(text):
        # Display a message indicating that the AI is responding
        print("AI --> ", text)
        # Create a gTTS instance with the specified text and language
        speaker = gTTS(text=text, lang="en", slow=False)
        # Save the speech as an MP3 file
        speaker.save("res.mp3")
        # Get information about the MP3 file
        statbuf = os.stat("res.mp3")
        # Calculate the duration of the speech based on file size
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        # Play the MP3 file using the appropriate system command (Mac or Windows)
        os.system('afplay res.mp3')  # If you are using Mac -> afplay, for Windows -> start
        # Pause for a specific duration to allow speech playback
        time.sleep(int(50*duration))
        # Remove the temporary MP3 file
        os.remove("res.mp3")
    
    # Method to check if the wake-up phrase is detected in the input text
    # def wake_up(self, text):
    #     # Return True if the wake-up phrase is found in the lowercase version of the text
    #     return True if self.name in text.lower() else False
    
    # Static method to get the current time
    @staticmethod
    def action_time():
        # Return the current time in the format HH:MM
        return datetime.datetime.now().time().strftime('%H:%M')

# Main part of the code where the AI is instantiated and runs
if __name__ == "__main__":
    # Create an instance of the ChatBot class with the name "Jarvis"
    ai = ChatBot(name="Jarvis")
    
    # Load a conversational language model using Hugging Face's Transformers library
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    
    # Set an environment variable for parallel tokenization
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    
    # Variable to control the loop
    ex=True
    
    # Main loop for the conversation with the AI
    while ex:
        # Get input from the user through speech
        ai.speech_to_text()
        
        # Check for wake-up phrase
        if any(i in ai.text for i in ["Jarvis","Jarvis"]): #ai.wake_up(ai.text) is True:
            # Generate a response if the wake-up phrase is detected
            res = "Hello I am Jarvis, what can I do for you?"
        # Check for the request for the current time
        elif "time" in ai.text:
            # Get the current time and set it as the response
            res = ai.action_time()
        # Respond politely to "thank you"
        elif any(i in ai.text for i in ["thank","thanks"]):
            # Choose a random polite response from a list
            res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","mention not"])
        # Exit the conversation if the user says "exit" or "close"
        elif any(i in ai.text for i in ["exit","close"]):
            # Choose a random farewell message and set it as the response
            res = np.random.choice(["Tata","Have a good day","Bye","Goodbye","Hope to meet soon","peace out!"])
            # Set the loop control variable to False to exit the loop
            ex=False
        # Continue the conversation using the language model
        else:   
            # Handle the case when there is an error in speech recognition
            if ai.text=="ERROR":
                # Set an error message as the response
                res="Sorry, come again?"
            else:
                # Use the language model to generate a response
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                # Extract the bot's response from the model's output
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()
        
        # Convert the response to speech and play it
        ai.text_to_speech(res)
    
    # Display a closing message when the conversation ends
    print(f"----- Closing down {ai.name} -----")



