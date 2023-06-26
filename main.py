from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


# --------------------generate word-------------------

to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    orginal_data = pandas.read_csv("data/french_words.csv")
    to_learn = orginal_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_area, text="French", fill="black")
    canvas.itemconfig(word_area, text=current_card["French"], fill="black")
    canvas.itemconfig(old_image, image=card_frond_img)
    timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():

    canvas.itemconfig(old_image, image=card_back_img)
    canvas.itemconfig(title_area, text="English", fill="white")
    canvas.itemconfig(word_area, text=current_card["English"], fill="white")
    window.after(3000, func=next_card)


window = Tk()
window.title("Flash Card")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_frond_img = PhotoImage(file="images/card_front.png")
old_image = canvas.create_image(400, 263, image=card_frond_img)

card_back_img = PhotoImage(file="images/card_back.png")

title_area = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_area = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))


canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, command=next_card)
wrong_btn.config(highlightthickness=0)
wrong_btn.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img, command=is_known)
right_btn.config(highlightthickness=0)
right_btn.grid(row=1, column=1)


next_card()


window.mainloop()

