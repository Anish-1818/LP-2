import nltk
nltk.download("all", quiet=True)

import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import random
import datetime

# --- NLP Setup ---
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    return [lemmatizer.lemmatize(word=word, pos=get_wordnet_pos(tag)) for word, tag in tagged_tokens]

# --- Rules ---
rules = {
    # Greetings & Farewells
    ('hello', 'hi', 'hey', 'greeting', 'wassup'):
        ["Hello there! 😊 Welcome to our cafe. How can I make your day better?",
         "Hi! 👋 What would you like today?",
         "Hey! So glad you stopped by!"],
    ('thank', 'thanks', 'appreciate'):
        ["You're most welcome! 🙏", "No problem at all—enjoy your time here! ☕", "Always happy to help!"],
    ('bye', 'goodbye', 'exit', 'quit', 'see you'):
        ["Goodbye! 👋 Hope to see you again soon.", "Farewell! 🌟 Have a wonderful day!", "Bye! Take care! Come back anytime."],

    # Cafe Specific
    ('menu', 'offer', 'serve', 'selection', 'list'):
        ["Here's what we offer: ☕ Coffees, 🍵 Teas, 🥐 Pastries, 🥪 Sandwiches. Feel free to ask for details!"],
    ('coffee', 'brew', 'drip', 'filter', 'cup'):
        ["We have a variety of freshly brewed coffees! From espresso to pour-over, what's your mood today? ☕"],
    ('latte', 'cappuccino', 'espresso', 'americano', 'mocha', 'macchiato', 'flat white'):
        ["Absolutely! We make all of those! ❤️ Milk alternatives available too—oat, almond, soy."],
    ('tea', 'chai'):
        ["We serve black, green, herbal teas, and chai latte. 🍵 Would you like something warm or iced?"],
    ('food', 'eat', 'hungry', 'snack', 'pastry', 'cake', 'muffin', 'croissant', 'bite'):
        ["We’ve got fresh pastries 🥐, cakes 🎂, sandwiches 🥪, and snacks. Check the display or ask me for recommendations!"],
    ('wifi', 'internet', 'wi-fi', 'network', 'password'):
        ["Yes, we offer free WiFi! 📶 Network: CafeConnect_Guest, Password: enjoyyourcoffee"],
    ('pay', 'payment', 'card', 'cash', 'credit', 'upi', 'gpay', 'paytm', 'phonepe', 'scan'):
        ["We accept cash 💵, cards 💳, and UPI (GPay, PhonePe, Paytm). Pay your way!"],
    ('special', 'deal', 'offer', 'discount', 'promotion', 'combo'):
        ["We’ve got some seasonal specials 🌸—ask at the counter or check the board!"],
    ('vegan', 'vegetarian', 'gluten-free', 'allergy', 'dairy-free', 'milk', 'soy', 'oat', 'almond'):
        ["We cater to dietary needs! 🌱 We offer oat/almond/soy milk, and vegetarian options. Please inform us about allergies!"],
    ('restroom', 'bathroom', 'toilet', 'washroom', 'loo'):
        ["The restroom is at the back 👉 past the counter and to your left."],
    ('book', 'reservation', 'reserve', 'table'):
        ["We don’t usually take reservations, but for large groups feel free to call ahead 📞."],
    ('music', 'song', 'playlist', 'volume'):
        ["Enjoying the vibe? 🎶 We play a cozy playlist. If it’s too loud/quiet, let the staff know!"],
    ('sandwich',):
        ["Grea choice sir! We serve variety of Sandwiches like Cheese Grilled Sandwich, Chocolate sandwich, Club Toast, And many more. Just refer the menu pls."],
    # General Info
    ('hour', 'open', 'close', 'time', 'timing'):
        ["We’re open daily 🕗 8 AM to 8 PM."],
    ('location', 'address', 'where', 'find'):
        ["Find us at 📍 15 Cafe Lane, Koregaon Park, Pune."],
    ('help', 'assist', 'support', 'question'):
        ["Sure! 😊 I can help with menu, hours, location, WiFi, or any other cafe-related questions!"]
}

# --- Response Generator ---
def get_response(user_input):
    lemmas = preprocess_text(user_input)
    for keywords, responses in rules.items():
        if any(keyword in lemmas for keyword in keywords):
            if 'bye' in lemmas or 'quit' in lemmas or 'exit' in lemmas:
                root.after(1000, close_app)  # Schedule app to close
            return random.choice(responses)
    return random.choice([
        "Hmm 🤔 I'm not sure about that. Could you ask about coffee, food, WiFi, hours, or location?",
        "I'm still learning! Try asking me about our menu, opening hours, or available drinks.",
        "I can answer questions about our cafe ☕. What would you like to know?"
    ])

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def send_message():
    user_input = user_entry.get().strip()
    if not user_input:
        return
    chat_window.insert(tk.END, f"You [{timestamp()}]: {user_input}\n")
    response = get_response(user_input)
    chat_window.insert(tk.END, f"Bot [{timestamp()}]: {response}\n\n")
    chat_window.see(tk.END)
    if 'bye' in user_input.lower() or 'exit' in user_input.lower() or 'quit' in user_input.lower():
        user_entry.config(state=tk.DISABLED)
        send_button.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

def close_app():
    messagebox.showinfo("Cafe Chatbot", "Thank you for chatting! Goodbye!")
    root.destroy()

# --- GUI ---
root = tk.Tk()
root.title("☕ Cafe Chatbot")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12), state=tk.NORMAL)
chat_window.pack(padx=10, pady=10)
chat_window.insert(tk.END, "Bot: 👋 Welcome to our Cafe Assistant! Ask me anything.\n(Type 'bye' to exit)\n\n")

user_entry = tk.Entry(root, width=50, font=("Arial", 12))
user_entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(side=tk.LEFT, padx=10, pady=(0,10))

user_entry.bind("<Return>", lambda event: send_message())  # Send on Enter

root.mainloop()
