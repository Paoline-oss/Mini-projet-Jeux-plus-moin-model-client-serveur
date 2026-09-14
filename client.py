import sys, socket
from CONSTANTE import*

connexion=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion.settimeout(TIME)  #création du timeout socket
connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    connexion.connect((HOST,PORT))
    connexion.settimeout(TIME)
    #correcte = bool(connexion.recv(1024).decode(ENCO))
    #print(correcte)
    correcte = True
    while correcte == True:
        message_du_serveur = connexion.recv(1024).decode(ENCO)
        print(message_du_serveur)
        print("Entrez la réponse")
        reponse = input()
        connexion.send(reponse.encode(encoding = ENCO)) #Envoit de la réponse du client
        print(connexion.recv(1034).decode(ENCO)) #print(Lancement du jeux)

        if reponse == "T":
            continuer = bool(connexion.recv(1024).decode(ENCO))
        while continuer :
            print(connexion.recv(1024).decode(ENCO)) #print("Faite proposition ...")
            proposition = input()
            proposition = connexion.recv(1024).decode(ENCO)

            message_jeux = connexion.recv(1024).decode(ENCO)


except ConnectionResetError:
    print("Fermeture du serveur")

except Exception as e:
    print(f"Erreur inatendue : {e}")  

except KeyboardInterrupt:
    print(f"\nArrêt de la connexion")
    connexion.send(f"Fermeture du client".encode(encoding=ENCO))
    connexion.close()
    print("Fermeture du socket")

except OSError as e:
    print(e)
    print("La connexion a échoué")
    sys.exit()



