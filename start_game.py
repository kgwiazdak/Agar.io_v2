from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import database
import game


def game_settings(nick):
    def submit(color, new_nick):
        game_root.destroy()
        game.start_new_game(new_nick, color)

    root.destroy()
    game_root = Tk()
    game_root.title("Game settings")
    game_root.geometry("500x220")
    Label(game_root, text="Settings", font=("Helvetica", 20)).pack()
    Label(game_root, text="Choose Your color").pack()

    colors = [
        ("Red", "red"),
        ("Green", "green"),
        ("Blue", "blue")
    ]

    v = Variable()
    v.set("red")
    for text, color in colors:
        Radiobutton(game_root, text=text, variable=v, value=color).pack()
    Label(game_root, text='Custom nick', font=('calibre', 10, 'bold')).pack()
    new_nick = Entry(game_root, font=('calibre', 10, 'normal'))
    new_nick.insert(0, nick)
    new_nick.pack()
    Button(game_root, text="Submit", command=lambda: submit(v.get(), new_nick.get())).pack()


def sign_in():
    def check_entry():
        if not (
                first_name.get() and last_name.get() and email.get() and password.get() and password_again.get() and nick.get()):
            messagebox.showerror(title="Error", message="Fields must not be empty")
            return False
        if password.get() != password_again.get():
            messagebox.showerror(title="Error", message="Password does not match, try again")
            password.delete(0, END)
            password_again.delete(0, END)
            return False
        return True

    def submit():
        if not check_entry():return

        database.sign_in(
            first_name.get(),
            last_name.get(),
            email.get(),
            password.get(),
            nick.get()
        )
        game_settings(nick.get())
        top.destroy()


    top = Toplevel(root)
    top.title("Sign in")
    top.geometry("300x200")
    i = 0
    title_label = Label(top, text="Sign in to Agar.io v2", font=("Helvetica", 20))
    i += 1
    title_label.grid(row=i, column=1)
    i += 1

    first_name_text = Label(top, text='First name', font=('calibre', 10, 'bold'))
    first_name = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    first_name_text.grid(row=i, column=0)
    first_name.grid(row=i, column=1)

    last_name_text = Label(top, text='Last name', font=('calibre', 10, 'bold'))
    last_name = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    last_name_text.grid(row=i, column=0)
    last_name.grid(row=i, column=1)

    email_text = Label(top, text='E-mail', font=('calibre', 10, 'bold'))
    email = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    email_text.grid(row=i, column=0)
    email.grid(row=i, column=1)

    password_text = Label(top, text='Password', font=('calibre', 10, 'bold'))
    password = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    password_text.grid(row=i, column=0)
    password.grid(row=i, column=1)

    password_again_text = Label(top, text='Password (again)', font=('calibre', 10, 'bold'))
    password_again = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    password_again_text.grid(row=i, column=0)
    password_again.grid(row=i, column=1)

    nick_text = Label(top, text='Nick', font=('calibre', 10, 'bold'))
    nick = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    nick_text.grid(row=i, column=0)
    nick.grid(row=i, column=1)

    Button(top, text="Submit", command=submit).grid(row=i + 1, column=1)


def log_in():
    def check_entry():
        if not (email.get() and password.get()):
            messagebox.showerror(title="Error", message="Fields must not be empty")
            return False
        return True

    def submit():
        if not check_entry():
            return

        nick = database.log_in(
            email.get(),
            password.get(),
        )
        if nick:
            top.destroy()
            game_settings(nick[0])
        else:
            messagebox.showerror(title="Error", message="Password and e-mail does not match")
            password.delete(0, END)
            email.delete(0, END)

    top = Toplevel(root)
    top.title("Log in")
    top.geometry("300x200")
    i = 0
    title_label = Label(top, text="Log in to Agar.io v2", font=("Helvetica", 20))
    i += 1
    title_label.grid(row=i, column=1)
    i += 1

    email_text = Label(top, text='E-mail', font=('calibre', 10, 'bold'))
    email = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    email_text.grid(row=i, column=0)
    email.grid(row=i, column=1)

    password_text = Label(top, text='Password', font=('calibre', 10, 'bold'))
    password = Entry(top, font=('calibre', 10, 'normal'))
    i += 1
    password_text.grid(row=i, column=0)
    password.grid(row=i, column=1)

    Button(top, text="Log in", command=submit).grid(row=i + 1, column=1)


root = Tk()

root.geometry("500x550")
root.title("Agar.io v2")

title_label = Label(root, text="Agar.io v2", font=("Helvetica", 50))
title_label.pack()

Label(root, text="").pack()

img = ImageTk.PhotoImage(Image.open("/Users/kgwiazda/PycharmProjects/python/resources/agarIo.png"))
label = Label(root, image=img)
label.pack()

Label(root, text="").pack()

button1 = Button(root, text="Sign in", command=sign_in)
button1.pack()
button2 = Button(root, text="Log in", command=log_in)
button2.pack()
button3 = Button(root, text="Start as guest", command=lambda: game.start_new_game("Nick"))
button3.pack()

root.mainloop()
