from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import tkinter as tk
import ttkthemes



loginform=ttkthemes.ThemedTk()
loginform.geometry('500x500+700+250')
loginform.title("LOGIN AS ADMINISTRATOR")
loginform.get_themes()
loginform.set_theme('breeze')


loginbackground = Image.open('LOGIN.jpg')
loginphoto = ImageTk.PhotoImage(loginbackground)

loginbackground_label = Label(loginform, image=loginphoto,width=500,height=500)
loginbackground_label.place(x=0,y=0)



def main_admin():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error','Please fill in the box')
    elif usernameEntry.get() == 'user' and passwordEntry.get() == 'password':
        messagebox.showinfo('Login',"You are now login ")
        loginform.destroy()
        import main
    else:
        messagebox.showwarning('Warning','No Error Found')
    



#background_image = Image.open('background.jpg')
#background_photo = ImageTk.PhotoImage(background_image)

#background_label = tk.Label(root, image=background_photo,width=1300,height=1000)
#background_label.place(x=0,y=0)



usernameEntry = Entry (loginform,width=22,font=('arial',15,'italic'))
usernameEntry.place(x=140,y=170)


passwordEntry = Entry (loginform,width=22,font=('arial',15,'italic'),show= "*")
passwordEntry.place(x=140,y=250)



style = ttk.Style()
style.configure("Big.TButton", font=("arial", 15), padding=(9, 10))
submitButton = ttk.Button(loginform, text='Login', width=15, style="Big.TButton", command=main_admin)
submitButton.place(x=170, y=300)










loginform.mainloop()