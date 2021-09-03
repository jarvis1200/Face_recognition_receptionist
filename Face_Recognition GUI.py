import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from Face_Recognition import Create_dataset
from Face_Recognition import train_images
from Face_Recognition import Detector
from Face_Recognition import manual_capture
from PIL import Image, ImageTk
import os

names = []

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        for users in os.listdir("dataset"):
            names.append(users)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        #self.resizable(True, True)
        self.geometry("640x540")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f = open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        img = Image.open('pngtree-abstract-trendy-neon-colorful-frame-png-image_2219062.jpg')
        height = (640,540)
        img = img.resize(height)
        img = ImageTk.PhotoImage(img)
        render = tk.Label(self, image=img, bg='#232F3E')
        render.image = img

        render.grid(row=0, column=0, rowspan=5, sticky="nsew")
        label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font, fg="#263942")
        label.grid(row=0)
        button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
        button1.grid(row=1, column=0, ipady=2, ipadx=7)
        button2.grid(row=2, column=0, ipady=2, ipadx=2)
        button3.grid(row=3, column=0, ipady=2, ipadx=32)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.append(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        value = len(names)
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10,
                                                                                        pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"),
                                    bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names, value)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)


    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Auto Capture ", fg="#ffffff", bg="#263942", command=self.capimg)
        self.name_entry = tk.Entry(self,borderwidth=1, width = 5, bg="lightgrey", font='Helvetica 11')
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.mancapbutton = tk.Button(self, text="Manual Capture", fg="#ffffff", bg="#263942", command=self.mancap)
        self.capturebutton.grid(row=2, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=2, column=2, ipadx=5, ipady=4, padx=10, pady=20)
        self.mancapbutton.grid(row=2, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.name_entry.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=10)

    def capimg(self):
        num = self.name_entry.get()
        self.controller.active_name
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will automatically Capture {} pic of your Face.".format(num))
        x = Create_dataset(self.controller.active_name, num)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))


    def mancap(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "Press S to capture the image of your Face.")
        x = manual_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 20:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 20 images!")
            return
        train_images(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        Detector(self.controller.active_name)




app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()


