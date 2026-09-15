import sys, socket
from random import randint
import time

from CONSTANTE import*


#FONCTION qui correspoond au jeux 
def lancer_partie(connexion):
    #Initialisation du nb mystére, et du nombre d'essaies
    nb_secret = randint(1,10)
    essais = 0
    continuer = True
    print(f"\nLe nombre secret : {nb_secret} ")
    reponse = ""
    try:
        while continuer:
                        try:

                            connexion.send(f"{reponse}\nFaite une proposition entre 1 et 10 non réel".encode(encoding=ENCO))
                            #time.sleep(TIME_L)
                            print("Attente de la proposition du joueur")
                            proposition = (connexion.recv(1024).decode(ENCO)).strip() #Attente de la réponse du client 
                            #connexion.settimeout(TIME)
                            essais += 1  #Incrémentation des essais du client
                            print(f"Client -----> La proposition donnée est {(proposition)}, essais numéro {essais}" )

                            #Vérification de la proposition du client 
                            if not proposition.isdigit(): #Si il n'y pas des caractéres autres que des nombres 
                                connexion.send("Entrer un nombre valide entre 1 et 10".encode(ENCO))
                                #time.sleep(TIME_L)
                                continue
        
                            proposition = int(proposition)  #Passage de la proposition obligatoire en entier si le client aurait mit des décimaux 
                            

                            if proposition < 1 or proposition > 10:
                                reponce ="Le nombre doit être 1 et 10" #Envoi du message à l'utilisateur 
                                #time.sleep(TIME_L)
                                continue
                                
        
                            if int(proposition) < nb_secret:
                                reponse = "PLUS GRAND"
                                
                                #time.sleep(TIME_L)
                            elif int(proposition) > nb_secret:
                                reponse ="PLUS PETIT"
                                
                                #time.sleep(TIME_L)
                            else:
                                continuer = False
                                message_jeux = "Le nombre {} a été trouvé en {} tentative" .format(nb_secret, essais)
                                connexion.send(message_jeux.encode(encoding=ENCO))
                                return
                            #time.sleep(TIME_L)
                            

                        #EXCEPTION si le timeout est dépassé
                        except socket.timeout:
                            print("Timeout atteint : aucune réponse de la part du joueur")
                            print("Reprise de l'attente d'une réponse")

                        #EXCEPTION si la proposition est incorrecte
                        except ValueError:
                            connexion.send("Erreur: entré invalide".encode(ENCO))
        return

    #EXCEPTION si la client coupe la connection avec le serveur
    except ConnectionResetError:
        print("client a fermé la connexion")
        return  #On srot du juex on revient à la connexion avec un client

    #EXCEPTION si il y a une erreur pendant le jeux 
    except Exception as e:
        print(f"Erreur inatendue : {e}")         

    #EXCEPTION s'il il ya un Ctrl+C dans le terminal         
    except KeyboardInterrupt:
        print("\nArrêt du serveur ...")
        connexion.close()
        print("Serveur arrêté proprement")