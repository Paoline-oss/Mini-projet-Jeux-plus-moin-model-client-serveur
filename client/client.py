import sys, socket, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilitaire.CONSTANTE import*
from lancer_partie_client import*

#Création du socket
connexion=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Création du timeout socket
connexion.settimeout(TIME)  



try:
    connexion.connect((HOST,PORT)) #Connection au serveur avec une liaison
    connexion.settimeout(TIME)
    correcte = bool(connexion.recv(1024).decode(ENCO)) #Réception d'un booléen pur la validation du choix du client
    while correcte :
        try :
            print(connexion.recv(1024).decode(ENCO)) #Affichage du message d'accueil du serveur
            print("Entrez la réponse")
            reponse = input() 
            connexion.send(reponse.encode(encoding = ENCO)) #Envoit de la réponse du client

            #Si le joueur veut jouer 
            if reponse == "T":
                correcte = False
                print(connexion.recv(1024).decode(ENCO))
                lancer_partie_client(connexion) #Lancement de la fonction pour gérer le jeux

            #Si le joueur ne veut pas jouer 
            elif reponse == "F" :
                correcte = False
                print(connexion.recv(1024).decode(ENCO))
                print(f"Fermeture de la connexion coté client")

                #FERMETURE de la connexion
                connexion.shutdown(socket.SHUT_WR)
                connexion.close()

            #Si le joeur à taper quelque chose qui n'est pas prévue 
            else : 
                print(connexion.recv(1024).decode(ENCO))
                continuer = False

        #EXCEPTION s'il y a une erreur lors de la fermeture, pour faire une fermeture forcé
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
    print("Fermeture du serveur")

except Exception as e:
    print(f"Erreur inatendue : {e}")  

#EXCEPTION s'il il ya un Ctrl+C dans le terminal
except KeyboardInterrupt:
    print(f"\nArrêt de la connexion")
    connexion.send(f"Fermeture du client".encode(encoding=ENCO))
    connexion.close()
    print("Fermeture du socket")

#EXCEPTION erreur lors de la connection
except OSError as e:
    print(e)
    print("La connexion a échoué")
    sys.exit()



