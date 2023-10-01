from tkinter import *
import pandas
import random

# ---------------------------- Variables ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
timer = None
the_count = None
current_card = {}
to_learn = {}

# ---------------------------- Word List SETUP ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- Next Card / Word ------------------------------- #
def select_correct():
    to_learn.remove(current_card)
    df = pandas.DataFrame(to_learn)
    df.to_csv('data/words_to_learn.csv', index=False, header=True)
    next_card()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #
# Create window
window = Tk()
window.title("Language Flashcards")
window.config(width=800, height=800, padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# Create Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

# Canvas title
card_title = canvas.create_text(400, 150, text="Title", fill="black", font=('Ariel', 40, "italic"))

# Canvas word
card_word = canvas.create_text(400, 263, text="Word", fill="black", font=('Ariel', 60, "bold"))

# Create buttons
# wrong button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

# right button
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=select_correct)
right_button.grid(row=1, column=1)

# Initial card draw
next_card()

# Window loop
window.mainloop()
