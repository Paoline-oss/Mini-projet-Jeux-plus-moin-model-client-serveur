import sys, socket
from CONSTANTE import*

connexion=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connexion.settimeout(TIME)  #création du timeout socket
#connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


try:
    connexion.connect((HOST,PORT))
    connexion.settimeout(TIME)
    correcte = bool(connexion.recv(1024).decode(ENCO))
    #print(correcte)
    while correcte == True:
        print(connexion.recv(1024).decode(ENCO))
        print("Entrez la réponse")
        reponse = input()
        connexion.send(reponse.encode(encoding = ENCO)) #Envoit de la réponse du client
        if reponse == "T":
            continuer = True
            correcte = False
            print(connexion.recv(1024).decode(ENCO))
        elif reponse == "F" :
            continuer = False
            correcte = False
            print(connexion.recv(1024).decode(ENCO))
            print(f"Fermeture de la connexion coté client")
            connexion.shutdown(socket.SHUT_WR)
            connexion.close()

        else : 
            print(connexion.recv(1024).decode(ENCO))
            continuer = False
        try:
            while continuer :
                message = connexion.recv(1024).decode(ENCO)
                print(message) #print("Faite proposition ...")
                proposition = str(input())
                connexion.send(str(proposition).encode(encoding = ENCO))

                if not proposition.isdigit():
                    print(connexion.recv(1024).decode(ENCO))
                    continue

                if "compris entre" in message:
                    continue

                if "trouvé" in message:
                    print(f"GAGNER\n")
                    continuer = False
                    break



        except ValueError:
            print(connexion.recv(1024).decode(ENCO))

        except socket.timeout:
            print("Timeout atteint : aucune réponse de la part du joueur")
            print("Reprise de l'attente d'une réponse")



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



