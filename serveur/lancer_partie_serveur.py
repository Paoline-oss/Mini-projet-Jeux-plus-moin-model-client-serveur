import sys, socket, os
from random import randint
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilitaire.CONSTANTE import TIME, HOST, PORT, ENCO, BORNE_INF, BORNE_MAX


#FONCTION qui correspoond au jeux 
def lancer_partie(connexion):
    #Initialisation du nb mystére, et du nombre d'essaies
    nb_secret = randint(BORNE_INF, BORNE_MAX)
    essais = 0
    continuer = True
    print(f"\nLe nombre secret : {nb_secret} ")
    reponse = "" #Correspond à la variable qui va stocker les messages spécifique du serveur

    try:
        while continuer:
                        try:

                            connexion.send(f"{reponse}\nFaite une proposition entre 1 et 10 non réel".encode(encoding=ENCO)) #ENVOIT du message de la proposition
                            print("Attente de la proposition du joueur")
                            proposition = (connexion.recv(1024).decode(ENCO)).strip() #RECPTION de la réponse du client 
                            connexion.settimeout(TIME)
                            essais += 1  #Incrémentation des essais du client
                            print(f"Client -----> La proposition donnée est {(proposition)}, essais numéro {essais}" )

                            #Vérification de la proposition du client 
                            if not proposition.isdigit(): #Si il n'y pas des caractéres autres que des nombres 
                                connexion.send("Entrer un nombre valide entre 1 et 10".encode(ENCO))
                                continue
        
                            proposition = int(proposition)  #Passage de la proposition obligatoire en entier si le client aurait mit des décimaux 
                            

                            if proposition < BORNE_INF or proposition > BORNE_MAX:
                                reponse ="Le nombre doit être {BORNE_INF} et {BORNE_MAX}" #Changement du message spécifique
                                continue
                                
                            #Si le nombre est plus grand que le nombre secret
                            if int(proposition) < nb_secret:
                                reponse = "PLUS GRAND"  #Changement du message spécifique
                                
                            #Si le nombre est plus grand que le nombre secret
                            elif int(proposition) > nb_secret:
                                reponse ="PLUS PETIT"  #Changement du message spécifique

                            #Le jouer a gagné
                            else:
                                continuer = False
                                message_jeux = "Le nombre {} a été trouvé en {} tentative" .format(nb_secret, essais)
                                connexion.send(message_jeux.encode(encoding=ENCO))  #ENVOIT du message 
                                return
                            
                        #EXCEPTION si le timeout est dépassé
                        except socket.timeout:
                            print("Timeout atteint : aucune réponse de la part du joueur")
                            print("Reprise de l'attente d'une réponse")

                        #EXCEPTION si la proposition est incorrecte
                        except ValueError:
                            connexion.send("Erreur: entré invalide".encode(ENCO)) #ENVOIT du message d'erreur

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