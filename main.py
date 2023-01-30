from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
flip_timer = None

#----------------------words-----------------------
try:
    words_data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_data = pd.read_csv("data/french_words.csv")
    
words_data_dict = words_data.to_dict(orient="records")
random_word = {}

#----------------------function--------------------
def update_word():
    global random_word, flip_timer
    if flip_timer != None:
        window.after_cancel(flip_timer)
    random_word = random.choice(words_data_dict)
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(lang_word, text="French", fill="black")
    canvas.itemconfig(q_word, text=random_word["French"])
    flip_timer = window.after(3000, reveal)

def reveal():
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(lang_word, text="English", fill="white")
    canvas.itemconfig(q_word, text=random_word["English"])

def remove_known_word():
    words_data_dict.remove(random_word)
    pd.DataFrame(words_data_dict).to_csv("data/words_to_learn.csv", index=False)
    update_word()
    
#----------------------UI--------------------------
window = Tk()
window.title("Let's learn French!")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

# canvas
canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 270, image=card_front_img)
lang_word = canvas.create_text(400, 150, text="", font=("Arial", 32, "italic"), fill="black")
q_word = canvas.create_text(400, 250, text="", font=("Arial", 64, "bold"), fill="black")
update_word()
canvas.grid(row=0, column=0, columnspan=2)

# button
wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=update_word)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=remove_known_word)
right_button.grid(row=1, column=1)

window.mainloop()
