import requests
import time
import threading


URL_POP = 'https://3vkeycenej.execute-api.us-east-1.amazonaws.com/prod/CIAB-2018-DroneCommandQueue?droneId=drone1&operation=POP&secret=dr0neRulez2A5T7U'
URL_PEEK = 'https://3vkeycenej.execute-api.us-east-1.amazonaws.com/prod/CIAB-2018-DroneCommandQueue?droneId=drone1&operation=PEEK&secret=dr0neRulez2A5T7U'

class Servidor():
    def __init__(self):
        self.comando = "empty"
        self.cancelarConexao = False

    def solicitar_conexao(self):
        print("conectado")
        r = requests.get(URL_POP)
        while(r.text=='empty'):
            if(self.cancelarConexao==True):
                break
            r = requests.get(URL_POP)
            time.sleep(1)
        self.comando = r.text

    def cancela_comando(self):
        entrada = input("digite \'cancela\' para cancelar: ")
        if(entrada=='cancela'):
            self.cancelarConexao = True

    def verificar_comando(self):
        threadComando = threading.Thread(target=self.solicitar_conexao)
        threadComando.setDaemon(True)

        threadCancela = threading.Thread(target=self.cancela_comando)
        threadCancela.setDaemon(True)

        threadComando.start()
        threadCancela.start()

        threadComando.join()
