import socket
import sys 
from random import randint
import time

from CONSTANTE import*
from lancer_partie import lancer_partie

#Initialisation du socket
connecteur_reseau = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connecteur_reseau.settimeout(TIME)  #création du timeout socket
connecteur_reseau.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

try:
    #Liaison du socket
    connecteur_reseau.bind((HOST,PORT))
    connecteur_reseau.listen(1)  #Le serveur écoute
    print(f"Serveur démarré sur {HOST} : {PORT}")
    print(f"Timeout global : {TIME}s")
    while True:
        try:
            print(" Serveur de Jeu lancé ... Attente du joueur")
            connexion , adresse = connecteur_reseau.accept()  #Connection avec le joueur
            #connexion.settimeout(TIME)
            print(f"\nJoueur connecté à l'adresse IP : {adresse[0]}, port {adresse[1]}")
            correcte = True
            connexion.send(str(correcte).encode(encoding=ENCO))
            while correcte:
                message_serveur ="Vous étes connecté sur le serveur de JEU PLUS OU MOIN, j'ai choisi un nb entre 1 et 10.\n Voulez vous jouer <T> Oui o <F> Non"
                connexion.send(message_serveur.encode(encoding=ENCO))
                time.sleep(TIME_L)  #Envoit de message_serveur au client
                reponse = connexion.recv(1024).decode(ENCO)
                try:
                    if reponse == "T":
                        correcte = False
                        connexion.send(f"Lancement du jeux".encode(encoding=ENCO))
                        time.sleep(TIME_L)
                        #connexion.send(str(correcte).encode(encoding = ENCO))
                        #print(correcte)
                        lancer_partie(connexion)  #Fonction pour lancer la partie de PLUS ou MOIN
                    elif reponse == "F":
                        correcte = False
                        connexion.send("Fermeture de la connexion".encode(encoding=ENCO))
                        time.sleep(TIME_L)
                        print("Fermeture de la connexion")
                        time.sleep(TIME_L)
                        #connexion.send(correcte.encode(encoding=ENCO))
                        connexion.shutdown(socket.SHUT_WR)
                        connexion.close()
                        print("Fermeture de connexion faite")
                    else:
                        connexion.send(f"Commande incorrecte".encode(encoding=ENCO))
                        connexion.send(str(correcte).encode(encoding=ENCO))
                except OSError as e:
                    print(f"Erreur lors de la fermeture")
                    try:
                        correcte = False
                        connexion.close() #Fermeture en cas d'erreur 
                        print("Fermeture forcée faite")
                    except:
                        pass
                    

        #EXCEPTION si le timeout est dépassé
        except socket.timeout:
            print("Timeout atteint : aucun joueur ne s''est connecté à temps")
            print("Reprise de l'attente")

        #EXCEPTION si le client se déconnecte sur serveur
        except ConnectionResetError:
            print("Le client a fermé la connexion de maniére inattendue")

#EXCEPTION s'il il ya un Ctrl+C dans le terminal
except KeyboardInterrupt:
    print("\nArrêt du serveur ...")
    connecteur_reseau.close()
    print("Serveur arrêté proprement")

#EXCEPTION s'il y a une erreur quelconque avec le serveur
except Exception as e:
    print(f"Erreur inatendue : {e}")


         
