import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog,messagebox
import sqlite3
from threading import Thread
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Tk, simpledialog, messagebox, Label
from PIL import Image, ImageTk
import time
Host = "127.0.0.1"
Port = 9090



class client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        #msg = tkinter.Tk()
        #msg.withdraw()
        
        self.window =tk.Tk()
        self.window.geometry('950x600')  
        self.window.title("Chat Application: AUTHENTIFICATION")
        self.window.iconbitmap('Goo.ico')
        # ###################### background Image ########
        self.bg_frame = Image.open('images\\bg12.webp')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.place(relx=0.5, rely=0.5, anchor='center')

        # ############ login frame #########
        self.lgn_frame = Frame(self.window, bg='black', width='950', height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.txt = 'WELCOME'
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 20, 'bold'), bg='#040405', fg='white')
        self.heading.place(relx=0.1, rely=0.1, anchor='w')

        # ################ left side image ########
        self.side_image = Image.open('images\\bg6NEW.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405', width=600, height=525)
        self.side_image_label.image = photo
        self.side_image_label.place(x=-100, y=100)

        # ###################### sign in Image ########
        self.sign_in_image = Image.open('images\\fste-umi.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405', width=150, height=150)
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=700, y=130)  

        self.sign_in_label = Label(self.lgn_frame, text='Sign In', bg='#040405', fg='white',
                                   font=('yu gothic ui', 17, 'bold'))
        self.sign_in_label.place(x=750, y=240)

        ########## username ###########
        self.username_label = Label(self.lgn_frame, text='Username', bg='#040405',
                                    font=('yu gothic ui', 13, 'bold'), fg='#4f4e4d')
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg='#040405', fg='#6b6a69',
                                    font=('yu gothic ui', 12, 'bold'))
        self.username_entry.place(x=580, y=335, width=270)
        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.username_line.place(x=550, y=359)

        ########## password ###########
        self.password_label = Label(self.lgn_frame, text='Password', bg='#040405',
                                    font=('yu gothic ui', 13, 'bold'), fg='#4f4e4d')
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame,show="*",highlightthickness=0, relief=FLAT, bg='#040405',
                                    fg='#6b6a69', font=('yu gothic ui', 13, 'bold'))
        self.password_entry.place(x=580, y=416, width=270)
        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.password_line.place(x=550, y=440)

        ######## login button ############
        self.lgn_button = Image.open('images\\bg14.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405', width=500, height=80)
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=500, y=460)  

        self.login = Button(self.lgn_button_label, text='Login', font=('yu gothic ui ', 13, 'bold'),command=self.on_login,
                            width=30, bd=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.login.place(relx=0.4, rely=0.5, anchor='center')
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=('yu gothic ui', 11, 'bold'), background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)

        ######## Button ###########
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=('yu gothic ui', 11, 'bold'), background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)
        self.signup_button = Image.open('images/Python_2.png')
        photo = ImageTk.PhotoImage(self.signup_button)
        self.signup_button_label = Button(self.lgn_frame, image=photo, bg='#040405',command=self.enregistrer,width=111, height=35, activebackground='#3047ff', cursor='hand2', bd=0)
        self.signup_button_label.image = photo
        self.signup_button_label.place(x=670, y=555)  

       
        self.window.mainloop()

    def on_login(self):
        # Obtenez le nom d'utilisateur et le mot de passe lorsque le bouton de connexion est pressé
        username = self.username_entry.get()
        password = self.password_entry.get()
       
        self.username = username  # Définissez les attributs de l'objet client
        self.password = password
        self.sock.send("USERNAME".encode("utf-8"))
        self.sock.send(self.username.encode("utf-8"))
        response = self.sock.recv(1024).decode("utf-8")
        if response != "PASSWORD":
            print("Échec de l'authentification. Vérifiez votre nom d'utilisateur et votre mot de passe.")
            self.sock.close()
            exit(1)
        # Envoyer le mot de passe au serveur
        self.sock.send(self.password.encode("utf-8"))
        # Attendre la réponse du serveur pour l'autorisation
        auth_response = self.sock.recv(1024).decode("utf-8")
        if auth_response != "AUTHORIZED":
           error_message = "Échec de l'authentification. Vérifiez votre nom d'utilisateur et votre mot de passe."
           print(error_message)
            # Afficher une boîte de dialogue d'erreur
           messagebox.showerror("Erreur d'authentification", error_message)
           self.sock.close()
           exit(1)
        self.window.destroy()
        self.gui_donne = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        recevoir_thread = threading.Thread(target=self.recevoir)

        gui_thread.start()
        recevoir_thread.start()

    def change_username(self):
        new_username = simpledialog.askstring("Change Username", "Enter new username:")
        if new_username:
            self.sock.send(f"CHANGE_USERNAME,{new_username}".encode("utf-8"))
            result = self.sock.recv(1024).decode("utf-8")
            self.username=new_username
            messagebox.showinfo("le nom a été modifier avec succé",result)

    def enregistrer(self):
        self.fenetre = tkinter.Tk()
        self.fenetre.title("Création de compte")
        self.fenetre.geometry("400x500")
        self.fenetre.config(bg="black")
        self.fenetre.iconbitmap('Goo.ico')
        #Création des étiquettes et des zones de saisie
        self.label_nom = tk.Label(self.fenetre, text="Nom :",bg='#040405',
                                            font=('yu gothic ui', 13, 'bold'), fg='#4f4e4d')
        self.label_nom.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.label_nom.place(x=20,y=145)
        self.entry_nom = tkinter.Entry(self.fenetre, highlightthickness=0, relief=FLAT, bg='#040405', fg='#6b6a69',
                                            font=('yu gothic ui', 12, 'bold'))
        self.entry_nom.place(x=170,y=150)
        self.entry_noml= Canvas(self.fenetre, width=400, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.entry_noml.place(x=20,y=178)
        self.label_prenom = tkinter.Label(self.fenetre, text="Prénom :",bg='#040405', font=('yu gothic ui', 13, 'bold'), fg='#4f4e4d')
        self.label_prenom.place(x=20,y=200)
        self.entry_prenom = tkinter.Entry(self.fenetre,highlightthickness=0, relief=FLAT, bg='#040405', fg='#6b6a69', font=('yu gothic ui', 12, 'bold'))
        self.entry_prenom.place(x=170,y=200)
        self.entry_prenoml= Canvas(self.fenetre, width=400, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.entry_prenoml.place(x=20,y=230)
        self.label_password = tkinter.Label(self.fenetre, text="Mot de passe :",bg='#040405',
                                            font=('yu gothic ui', 13, 'bold'), fg='#4f4e4d')
        self.label_password.place(x=20,y=250)
        self.entry_password = tkinter.Entry(self.fenetre, show="*",highlightthickness=0, relief=FLAT, bg='#040405', fg='#6b6a69',
                                            font=('yu gothic ui', 12, 'bold'))
        self.entry_password.place(x=170,y=250)
        self.entry_passwordl= Canvas(self.fenetre, width=400, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.entry_passwordl.place(x=20,y=280)

        self.bouton_enregistrer = tkinter.Button(self.fenetre, text="Enregistrer",command=self.enregistre,font=('yu gothic ui ', 13, 'bold'),
                                    bd=0, bg="#3498DB", cursor='hand2', activebackground='#3047ff', fg='white')
        self.bouton_enregistrer.grid(row=3, column=0, columnspan=2,pady=200,)
        self.bouton_enregistrer.place(x=140,y=350)
        
        self.fenetre.mainloop()



  



    def enregistre(self):
        username = self.entry_nom.get()
        password = self.entry_password.get()
        prenom =self.entry_prenom.get()
        self.username = username
        self.password = password
        self.prenom = prenom
        # Envoyer le nom d'utilisateur au serveur
        self.sock.send("SASS".encode("utf-8"))
        time.sleep(0.2)
        self.sock.send(self.username.encode("utf-8"))
        time.sleep(0.2)
        self.sock.send(self.prenom.encode("utf-8"))
        # Attendre la réponse du serveur pour le mot de passe
        time.sleep(0.2)
        self.sock.send(self.password.encode("utf-8"))
        # Fermer la fenêtre de connexion après avoir obtenu les informations d'identification
        sass = self.sock.recv(1024).decode("utf-8")
        if sass == "enregistre":
           messagebox.showinfo("compte crée ",'vous avez créer votre compte avec succès')
        self.fenetre.destroy()


        
    def enligne(self):
        self.sock.send("enligne".encode('utf-8'))

    def request_history(self):
        self.sock.send("REQUEST_HISTORY".encode('utf-8'))

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chat Application")
        #self.win.geometry("600x600")
        self.win.geometry("600x600")
        self.win.config(bg="#ffa500")
        self.win.iconbitmap('Goo.ico')
        self.win.resizable(height=False,width=False)
        # Créer une étiquette pour afficher le nom d'utilisateur
        username_label = tkinter.Label(self.win, text=f"WELCOME, {self.username}!", bg="#c0c0c0", fg="black", font=("Helvetica", 14, "bold"))
        username_label.pack(fill="x")
        self.chat_label = tkinter.Label(self.win,bg="#ffa500")
        self.chat_label.configure(font="arial 12")
        self.chat_label.pack(padx=20,pady=5)

              #########  boutton option 
        self.btn_option = tkinter.Button(self.win, text="deconnexion", command=self.deconnexion,font=('yu gothic ui ', 13, 'bold'),
                             bd=0, bg="#c0c0c0", cursor='hand2', activebackground='#3047ff', fg='black')
        
        self.btn_option.config(font="arial 12")

        # Ajouter la marge en ajustant les valeurs de x et y
        x_position = 0
        y_position = 40
        margin_x = 300
        margin_y = 0
        self.btn_option.place(x=x_position + margin_x, y=y_position + margin_y)


           # Zone de texte pour afficher les messages
        self.text_area = ScrolledText(self.win, wrap="word", font=("Helvetica", 12), bg="#ECF0F1", state="disabled")
        self.text_area.pack(expand=True, fill="both", padx=10, pady=20)

        self.msg_label = tkinter.Label(self.win,text="Message",bg="#ffa500")
        self.msg_label.config(font="arial 12")
        self.msg_label.pack(padx=20,pady=5)
        
        self.saisit = tkinter.Text(self.win, height=0,width=45,font=("Helvetica", 12), bg="#ECF0F1",)
        self.saisit.pack(expand=True, padx=5, pady=(9, 10))
        x_position = 70
        y_position = 273
        margin_x = 0
        margin_y = 280
        self.saisit.place(x=x_position + margin_x, y=y_position + margin_y)

        self.btn_envoie = tkinter.Button(self.win, text="Envoyez", command=self.ecrire,font=('yu gothic ui ', 13, 'bold'),
                             bd=0, bg="#3498DB", cursor='hand2', activebackground='#3047ff', fg='white')
        self.btn_envoie.config(font="arial 12")
        self.btn_envoie.pack(padx=40,pady=5)
        x_position = 80
        y_position = 235
        margin_x = 400
        margin_y = 315
        self.btn_envoie.place(x=x_position + margin_x, y=y_position + margin_y)
        self.gui_donne = True 
        self.win.protocol("WM_DELETE_WINDOW",self.stop)
        #### bouton de l'historique ########
        self.btn_historique = tkinter.Button(self.win, text="historique", command=self.request_history,font=('yu gothic ui ', 13, 'bold'), bd=0, bg="#c0c0c0", cursor='hand2', activebackground='#3047ff', fg='black')
        
        self.btn_historique.config(font="arial 12")

        # Ajouter la marge en ajustant les valeurs de x et y
        x_position = 15
        y_position = 40
        
        margin_x = 72
        margin_y = 0
        self.btn_historique.place(x=x_position + margin_x, y=y_position + margin_y)
         #### bouton onligne ############
        self.btn_onligne = tkinter.Button(self.win, text="enligne", command=self.enligne,font=('yu gothic ui ', 13, 'bold'), bd=0, bg="#c0c0c0", cursor='hand2', activebackground='#3047ff', fg='black')
        
        self.btn_onligne.config(font="arial 12")

        # Ajouter la marge en ajustant les valeurs de x et y
        x_position = 15
        y_position = 40
        
        margin_x = 5
        margin_y = 0
        self.btn_onligne.place(x=x_position + margin_x, y=y_position + margin_y)
        ######### BUTTON CHANGEMENT DE NOM ########3
        self.btn_name = tkinter.Button(self.win, text="changer de nom", command=self.change_username,font=('yu gothic ui ', 13, 'bold'), bd=0, bg="#c0c0c0", cursor='hand2', activebackground='#3047ff', fg='black')
        
        self.btn_name.config(font="arial 12")

        # Ajouter la marge en ajustant les valeurs de x et y
        x_position = 15
        y_position = 40
        
        margin_x = 155
        margin_y = 0
        self.btn_name.place(x=x_position + margin_x, y=y_position + margin_y)
        

        self.win.mainloop()
    

    def ecrire(self):
        message = f"{self.username}: {self.saisit.get(('1.0'),'end')}"
            # Message normal
        self.sock.send(message.encode('utf-8'))
        self.saisit.delete('1.0','end')
        #pour la deconnexion
    def deconnexion(self):
        # Arrêtez le thread de réception
        self.running = False
        self.stop()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def recevoir(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                if message == "SURNOM":
                    self.sock.send(self.username.encode("utf-8"))
                    print("donne")
                    
                else :
                    if self.gui_donne:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end",message)
                        self.text_area.yview("end")
                        self.text_area.config(state="disabled")

            except ConnectionAbortedError:
                print("erreur donne")
                break
            except:
                print("Erreur")
                self.sock.close()
                break



            
client = client(Host,Port)