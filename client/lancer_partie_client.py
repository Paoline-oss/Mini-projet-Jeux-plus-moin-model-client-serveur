import sys, socket, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilitaire.CONSTANTE import TIME, HOST, PORT, ENCO

#connexion -> la liason avec le socket
def lancer_partie_client(connexion):
    try:
            continuer = True
            while continuer :
                try:
                    message = connexion.recv(1024).decode(ENCO) #RECEPTION du message de proposition
                    print(message) 
                    proposition = str(input())
                    connexion.send(str(proposition).encode(encoding = ENCO)) #ENVOIT de la proposition en str

                    #Vérification si la proposition est pas que des chiffres 
                    if not proposition.isdigit():
                        print(connexion.recv(1024).decode(ENCO)) #RECEPTION du message d'avertissement
                        continue

                    #Si le chiffre n'est pas compris entre le BORNE_INF et BORNE_MAX
                    if "compris entre" in message:
                        continue

                    #Si le chiffre à été trouvé
                    if "trouvé" in message:
                        print(f"GAGNER\n")
                        continuer = False #CHangement de la variable booléen -> fin de la boucle de jeux
                        print(f"\n Fermeture de la connexion ...")
                        break
                    
                #EXCEPTION si le timeout est dépassé
                except socket.timeout:
                    print("Timeout atteint : aucune réponse de la part du joueur")
                    print("Reprise de l'attente d'une réponse")

                #EXCEPTION si la proposition est incorrecte
                except ValueError:
                    print(connexion.recv(1024).decode(ENCO))

    #EXCEPTION s'il il ya un Ctrl+C dans le terminal
    except KeyboardInterrupt:
         print(f"\n Fermeture de la connexion")
         connexion.close()

    #EXCEPTION si il y a une erreur pendant le jeux
    except Exception as e:
        print(f"Erreur inatendue : {e}")  