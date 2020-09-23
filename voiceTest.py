import time
import tkinter.messagebox
import speech_recognition as sr

import threading

from tkinter import *
from textChatbot import chat

DIMS="500x500"

class ChatInterface(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        #Default background setting
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        #Menu bar
        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
        
        #File
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        
        #Clear chat option
        file.add_command(label="Clear Chat", command=self.clear_chat)
        
        #Exit chatbot option
        file.add_command(label="Exit",command=self.chatexit)

        #Preferences option
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Preferences", menu=options)

        #Fonts
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default",command=self.font_change_default)
        font.add_command(label="System",command=self.font_change_system)

        #Theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Theme", menu=color_theme)
        color_theme.add_command(label="Default",command=self.color_theme_default)
        color_theme.add_command(label="Blue",command=self.color_theme_dark_blue) 
        color_theme.add_command(label="Hacker",command=self.color_theme_hacker)
        
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="About", menu=help_option)
        help_option.add_command(label="About Chatbot", command=self.msg)
        
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        #Scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        #Contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
            bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
            width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        #Frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        #Entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        #self.users_message = self.entry_field.get()

        #Frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        #Send button
        self.send_button = Button(self.send_button_frame, text="Speak", width=5, relief=GROOVE, bg='white',
            bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
            activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=8)
        self.master.bind("<Return>", self.send_message_insert)

                
        self.last_sent_label(date="No messages sent.")
        
        t2 = threading.Thread(target=self.speechToText)
        t2.start()
        
            
    def speechToText(self):
        r = sr.Recognizer()

        while(True):

            with sr.Microphone() as source:
                print('Listenting...')
                try:
                    inputAudio = r.listen(source)
                    inputText = r.recognize_google(inputAudio)

                    print(inputText.lower())
                    return inputText.lower()

                except:
                    print("Not")

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def msg(self):
        tkinter.messagebox.showinfo("NLP - Neural Network based chatbot")

    def about(self):
        tkinter.messagebox.showinfo("Chatbot by AI")
    
    def send_message_insert(self, message):
        
        user_input = self.speechToText()
        
        print("I heard: " + user_input)
        pr1 = "You : " + user_input + "\n"

        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        
        response = chat(user_input)
        pr = "Bot : " + response + "\n"
        
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0,END)

    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFsFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    #Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    #Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"    
    
    #Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    #Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()    

root=Tk()
ob = ChatInterface(root)
root.geometry(DIMS)
root.title("Chatbot-NLP")

img = PhotoImage(file = 'img/bot.png') 
root.iconphoto(False, img)

root.mainloop()

