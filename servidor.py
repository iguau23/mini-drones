import requests
import time
import threading


URL_POP = 'https://3vkeycenej.execute-api.us-east-1.amazonaws.com/prod/CIAB-2018-DroneCommandQueue?droneId=drone1&operation=POP&secret=dr0neRulez2A5T7U'
URL_PEEK = 'https://3vkeycenej.execute-api.us-east-1.amazonaws.com/prod/CIAB-2018-DroneCommandQueue?droneId=drone1&operation=PEEK&secret=dr0neRulez2A5T7U'

URL_PUSH_STATUS = 'https://3vkeycenej.execute-api.us-east-1.amazonaws.com/prod/CIAB-2018-DroneCommandQueue?operation=PUSH&secret=dr0neRulez2A5T7U&droneId=status&command='

class Servidor():
    def __init__(self):
        self.cancelar_prepara = False
        self.comando = "empty"
        self.cancelarConexao = False
        self.executando = False

    def setExecutando(self, value):
        self.executando = value;
        #r = request.get()

    def solicitar_conexao(self):
        print("conectado")
        #joga fora o primeiro comando que estiver na pilha
        r = requests.get(URL_POP)

        r = requests.get(URL_POP)
        while(r.text=='empty'):
            if(self.cancelarConexao==True):
                break

            #Verifica se não houve perda de conexão
            for cf in self.mTeste.cfs:
                if (cf.link == None):
                    print("conexao com o drone perdida")
                    self.cancelarConexao = True

            r = requests.get(URL_POP)
            time.sleep(1)

        self.comando = r.text

    def cancela_comando(self):

        while(not self.cancelarConexao):
            entrada = input("digite \'cancela\' para cancelar: ")
            if(entrada=='cancela'):
                self.cancelarConexao = True
                break

    def verificar_comando(self, mTeste):
        self.mTeste = mTeste
        threadComando = threading.Thread(target=self.solicitar_conexao)
        threadComando.setDaemon(True)

        threadCancela = threading.Thread(target=self.cancela_comando)
        threadCancela.setDaemon(True)

        threadComando.start()
        threadCancela.start()

        threadComando.join()

    def verificar_prepara(self):
        threadEsperaPrepara = threading.Thread(target=self.espera_prepara)
        threadEsperaPrepara.setDaemon(True)

        threadContinua = threading.Thread(target=self.cancela_prepara)
        threadContinua.setDaemon(True)

        threadEsperaPrepara.start()
        threadContinua.start()

        threadEsperaPrepara.join()

    def espera_prepara(self):
        print("esperando prepara")
        #joga fora o primeiro comando da pilha
        r = requests.get(URL_POP)

        r = requests.get(URL_POP)
        while(r.text!= "preparar"):
            if(self.cancelar_prepara):
                break
            r = requests.get(URL_POP)
            time.sleep(1)

    def cancela_prepara(self):
        while(not self.cancelar_prepara):
            entrada = input("tecle ENTER para continuar: \n")
            if(entrada==""):
                self.cancelar_prepara = True
                break


    def push_status(command):
        r = requests.get(URL_PUSH_STATUS + command)
