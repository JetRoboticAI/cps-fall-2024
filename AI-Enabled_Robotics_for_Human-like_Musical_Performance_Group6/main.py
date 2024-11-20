from openai import OpenAI
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
import time
from tkinter import messagebox  # Import messagebox for confirmation dialogs

client = OpenAI(
    api_key='Your api_key')


# Replace with your OpenAI API key

def ask_gpt(question):
    try:
        response = client.chat.completions.create(model="gpt-4",
                                                  messages=[
                                                      {"role": "user", "content": question}
                                                  ],
                                                  max_tokens=1000,
                                                  temperature=0.7,
                                                  top_p=1,
                                                  frequency_penalty=0,
                                                  presence_penalty=0)
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"


def use_microphone():
    recognizer1 = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            output_text.insert(tk.END, "Waiting for the microphone to be ready...\n")
            output_text.update()
            recognizer1.adjust_for_ambient_noise(source, duration=3)

            time.sleep(1)
            output_text.insert(tk.END, "The microphone is ready, I am listening...\n")
            output_text.update()

            audio = recognizer1.listen(source, timeout=20, phrase_time_limit=30)



            question = recognizer1.recognize_google(audio, language='en-US')
            output_text.insert(tk.END, f"Is this what you said: {question}\n")

            # Proceed to confirmation step after recognizer1 finishes
            confirm_by_voice(question)  # Call a separate function for recognizer2

    except sr.UnknownValueError:
        output_text.insert(tk.END, "Oops, looks like I didn't get that right. Do you want to try again?\n")
        output_text.insert(tk.END, "Please click the microphone button...\n")
        output_text.update()
    except sr.RequestError as e:
        output_text.insert(tk.END, f"Could not request results from Google Speech Recognition service; {str(e)}\n")
        output_text.insert(tk.END, "Please click the microphone button...\n")
        output_text.update()

    # New function for the confirmation step


def confirm_by_voice(question):
    recognizer2 = sr.Recognizer()
    try:
        with sr.Microphone() as confirm_source:
            output_text.insert(tk.END, "Listening for your confirmation...Please say 'Yes' or 'No'\n")
            output_text.update()
            recognizer2.adjust_for_ambient_noise(confirm_source, duration=3)

            time.sleep(1)
            output_text.insert(tk.END, "The microphone is ready, I am listening...\n")
            output_text.update()

            confirm_audio = recognizer2.listen(confirm_source, timeout=20, phrase_time_limit=30)  # Shorter time limit
            confirmation = recognizer2.recognize_google(confirm_audio, language='en-US').lower()

            # Check if the response was 'yes' or 'no'
        if 'yes' in confirmation:
            process_question(question)  # Proceed if user says "yes"
        elif 'no' in confirmation:
            output_text.insert(tk.END, "Oops, looks like I didn't get that right. Do you want to try again?\n")
            output_text.insert(tk.END, "Please click the microphone button...\n")
            output_text.update()
        else:
            output_text.insert(tk.END, "Unrecognized response. Please only say 'yes or 'no'.\n")
            output_text.insert(tk.END, "Please click the microphone button...\n")
            output_text.update()

    except sr.UnknownValueError:
        output_text.insert(tk.END, "Sorry, I didn't catch that. Please say 'yes' or 'no'.\n")
        output_text.insert(tk.END, "Please click the microphone button...\n")
        output_text.update()

    except sr.RequestError as e:
        output_text.insert(tk.END, f"Could not request results from Google Speech Recognition service; {str(e)}\n")
        output_text.insert(tk.END, "Please click the microphone button...\n")
        output_text.update()


def process_question(question):
    extra_text = " create a song which generate a 1 x N matrix with a single octave, with N not less than 100, starting with middle C as 1. The octave will be a new song made by you and never heard in human history. You must use only white keys on a piano, do not return black keys. You must return your output in the format: octave = [1, 2, 3, 4, 5, 6, 7]. Please do not return any words except the octave. The rhythm must not repeat, and it must sound good. Please check the format again before you give me the answer, I just need the answer like octave = [1, 2, 3, 4, 5, 6, 7], I don't need any other words. "
    question += extra_text
    answer = ask_gpt(question)
    output_text.insert(tk.END, f"GPT's answer: {answer}\n")
    try:
        Octave = eval(answer[answer.index('['):answer.index(']') + 1])
        # Export Octave to a file
        with open("/Users/jacson/Desktop/SEP769/octave.txt", "w") as f:
            f.write(str(Octave))
        output_text.insert(tk.END, "Octave saved to /Users/jacson/Desktop/SEP769/octave.txt\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error extracting list: {str(e)}\n")
        output_text.insert(tk.END, "Please click the microphone button...\n")
        output_text.update()
        # Create the main window


root = tk.Tk()
root.title("Voice Assistant with GPT-4")
root.geometry("600x400")

# Question
# question_label = tk.Label(root, text="Click on the button and ask your question")
# question_label.pack()

# Microphone button
mic_button = tk.Button(root, text="Use Microphone", command=use_microphone)
mic_button.pack()

# Output text area
output_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
output_text.pack()
output_text.insert(tk.END, "Please click the microphone button...\n")

# Run the main loop
root.mainloop()
