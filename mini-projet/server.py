import socket
import threading 
import sqlite3
from threading import Thread
import time
import json

Host = "127.0.0.1"
Port = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((Host,Port))

server.listen()

clients = []
surnoms = []



def brodcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def register_user(client):
    try:
        username=client.recv(1024).decode("utf-8")
        print(username)
        time.sleep(0.1)
        password=client.recv(1024).decode("utf-8")
        print(password)
        time.sleep(0.1)
        prenom= client.recv(1024).decode("utf-8")
        conn = sqlite3.connect('sass.db')
        cursor = conn.cursor()
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return "USERNAME_TAKEN"
        # Insérer le nouvel utilisateur dans la base de données
        cursor.execute("INSERT INTO users (username, prenom,password) VALUES (?, ?,?)", (username, password,prenom))
        conn.commit()
        conn.close()
        return "REGISTRATION_SUCCESS"
    except Exception as e:
        print(f"Erreur lors de l'inscription de l'utilisateur : {e}")
        return "REGISTRATION_FAILED"

def change_nom(client,message):
                print("changer nom")
                parts = message.split(",")
                new = parts[1]
                print(f"{new}")
                index = clients.index(client)
                old_username = surnoms[index]

                conn = sqlite3.connect('sass.db')
                cursor = conn.cursor()
                # Changer le nom d'utilisateur dans la base de données
                cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new,old_username))
                conn.commit()
                print(new)
                surnoms[index] = new
                print(surnoms[index])
                # Diffuser le changement de nom d'utilisateur à tous les clients
                brodcast(f"{old_username} a changé de nom en {new}\n")
                client.send(f'vous avez change le nom avec succés'.encode('utf-8'))
                conn.close()
                


def handle(client): ### pour la reception de message 
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print("message:",message)
            if message == "REQUEST_HISTORY":
                send_history_to_client(client)
                continue
            elif message.startswith("CHANGE_USERNAME"):
                print("condition verifier ")
                change_nom(client,message)
                continue
            elif   message =="enligne":
                client.send(f'users online: {surnoms}\n'.encode('utf-8')) 
                continue
            ####### chat privé ######
            elif "@" in message:
                print("private message")
                infos=message.split("@")
                print(infos)
                destnom=infos[1]
                message=f'{infos[0]}(pv){infos[2]}'
                print(destnom)
                destsock=clients[surnoms.index(destnom)]
                destsock.send(message.encode("utf-8"))
                client.send(message.encode("utf-8"))
                continue
            else:
                username1 = surnoms[clients.index(client)]
            data = message.split(":")    
            conn = sqlite3.connect('sass.db')
            cursor = conn.cursor()
            query = "INSERT INTO messages (message, username) VALUES (?, ?)"
            cursor.execute(query, (data[1], username1))
            print("Message en registre dans la base de donné")
            conn.commit()
            conn.close()
            
            brodcast(message)


        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = surnoms[index]
            surnoms.remove(username)
            print(f"{username} s'est déconecté")
            break

def create_user_table():   ###### connexion et la creation  de la table message
    conn = sqlite3.connect('sass.db')
    c = conn.cursor()

    # Créer la table users
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT  NOT NULL,
            username TEXT NOT NULL
        )
    ''')
    print("TABLE USER CREER ")
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    print("users donne")
    conn.commit()
    conn.close()
create_user_table()


def add_message(username1,message):
    conn = sqlite3.connect('sass.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (message,username) values (?,?)",username1,message)
    print("donnnne")
    conn.commit()
    conn.close()

     
def send_history_to_client(client_socket):
    try:
        conn = sqlite3.connect('sass.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, message FROM messages")
        history = cursor.fetchall()

        # Supprimer tous les caractères de nouvelle ligne de chaque deuxième élément de la paire
        history_cleaned = [(item[0], item[1].replace('\n', '')) for item in history]
        conn.close()
        fichier_json = json.dumps(history_cleaned)
        client_socket.send("voici votre historique des messages\n".encode("utf-8"))
        client_socket.send(fichier_json.encode())
    

    except Exception as e:
        print(f"Erreur lors de la récupération de l'historique depuis la base de données: {e}")

def validate_user(username, password):
    conn = sqlite3.connect('sass.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(username)=? AND password=?", (username.lower(), password))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        print(f"Utilisateur {username} autorisé.")
    else:
        print(f"Échec de l'autorisation pour {username}.")

    return user_data is not None

def recevoir():
    while True:
        client, address = server.accept()
        print(f"Connecté avec {str(address)}")
        # Envoyer un message d'authentification au client
        auth_message = client.recv(1024).decode("utf-8")
        if auth_message == "USERNAME":
            username = client.recv(1024).decode("utf-8")
            client.send("PASSWORD".encode("utf-8"))   # Envoyer un message d'authentification au client
            # Recevoir le mot de passe du client
            password = client.recv(1024).decode("utf-8")
            print(f"Tentative de connexion pour l'utilisateur : {username}")
           
            if validate_user(username, password):
                print(f"Authentification réussie pour {username}.")      # Vérifier le nom d'utilisateur et le mot de passe
                client.send("AUTHORIZED".encode("utf-8"))
               
                surnoms.append(username)
                clients.append(client)  # Ajouter l'utilisateur à la liste des clients
                send_message = f"{username} est connecté\n"
                print(send_message)
                brodcast(send_message)
                thread = threading.Thread(target=handle, args=(client,)) # Démarrer un thread pour gérer les messages du client
                thread.start()
            else:
                print(f"Échec de l'authentification pour {username}.")
                client.send("UNAUTHORIZED".encode("utf-8"))
        elif auth_message == "SASS":
               if register_user(client):
                client.send("enregistre".encode("utf-8"))
                client.close()


create_user_table()
print("Attente de connexion....")
recevoir() 