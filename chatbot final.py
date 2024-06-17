import tkinter as tk
from tkinter import scrolledtext
import random
import json

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        
        # Load personalized responses from JSON file
        self.personalized_responses = self.load_personalized_responses()
        
        # Default responses and rules
        self.responses = {
            "hi": ["Hello!", "Hi there!", "Hey!"],
            "how are you": ["I'm doing well, how can I help you?", "I'm good, thanks for asking."],
            "bye": ["Okay, come again!", "See you later!", "Bye! Have a great day!"],
            "default": ["I'm not sure about that.", "Can you rephrase that?", "Sorry, I didn't get that."]
        }
        self.responses.update(self.personalized_responses)
        
        self.rules = {
            "hi": ["hi", "hello", "hey"],
            "how are you": ["how are you", "how are you doing"],
            "bye": ["bye", "goodbye"],
        }
        
        # GUI elements
        self.chat_history = scrolledtext.ScrolledText(root, width=50, height=20, bg="black", fg="white")
        self.chat_history.pack(padx=10, pady=10)
        
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(padx=10, pady=5)
        self.input_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(root, text="Send", command=self.send_message, bg="deepskyblue", fg="white")
        self.send_button.pack(pady=5)
        
        self.input_entry.focus()

    def load_personalized_responses(self):
        try:
            with open("personalized_responses.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_personalized_responses(self):
        with open("personalized_responses.json", "w") as file:
            json.dump(self.personalized_responses, file)

    def match_rule(self, input_text):
        for intent, patterns in self.rules.items():
            for pattern in patterns:
                if pattern in input_text:
                    return intent
        return "default"

    def respond(self, input_text):
        intent = self.match_rule(input_text.lower())
        if intent in self.responses:
            return random.choice(self.responses[intent])
        else:
            return random.choice(self.responses["default"])

    def send_message(self, event=None):
        user_input = self.input_entry.get()
        self.chat_history.insert(tk.END, "You: " + user_input + "\n")
        
        if user_input.lower() == 'quit':
            self.chat_history.insert(tk.END, "Chatbot: Nice chatting with you!\n")
            self.input_entry.delete(0, tk.END)
            self.save_personalized_responses()
            self.root.quit()
        else:
            response = self.respond(user_input)
            self.chat_history.insert(tk.END, "Chatbot: " + response + "\n")
            self.input_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_app = ChatbotApp(root)
    root.mainloop()
