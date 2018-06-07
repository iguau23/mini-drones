from testes import Teste
from servidor import Servidor
import combinacao
import time
import os

class Main():
    def start(self):

        continueMain = True
        continueTeste = True
        inMaintenance = True



        while(continueTeste):
            mServidor = Servidor()
            Servidor.push_status("Disponível")
            mServidor.verificar_prepara()
            duration = 1  # second
            freq = 440  # Hz
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
            print("iniciando testes\n")
            Servidor.push_status("Preparando drone...")
            mTeste = Teste()
            mTeste.start()

            Servidor.push_status("Pronto! Aguardando comando")

            mServidor.verificar_comando(mTeste)

            mServidor.setExecutando(True)

            if (mServidor.comando=="demo"): #com um drone apenas
                Servidor.push_status("Executando demo")
                if(len(mTeste.mcs)==1):
                    print("demo")
                    mTeste.setThreadEmergencial()
                    combinacao.combinacao1(mTeste.mcs[0])
                elif(len(mTeste.mcs)==2):
                    print("demo")
                    mTeste.setThreadEmergencial()
                    combinacao.combinacao1(mTeste.mcs[1])
                else:
                    print("numero insuficiente")
            if (mServidor.comando=="espiral"):
                Servidor.push_status("Executando Espiral")
                print("espiral")
                if (len(mTeste.mcs)==2):
                    mTeste.setThreadEmergencial()
                    combinacao.circulo(mTeste.mcs[0], mTeste.mcs[1])
                else:
                    print("numero insuficiente")
            if (mServidor.comando=="esquadrilha"):
                Servidor.push_status("Executando Esquadrilha")
                print("esquadrilha")
                mTeste.setThreadEmergencial()
                if (len(mTeste.mcs)==2):
                    mTeste.setThreadEmergencial()
                    combinacao.esquadrilha(mTeste.mcs[0], mTeste.mcs[1])
                else:
                    print("numero insuficiente")

            mServidor.setExecutando(False)
            Servidor.push_status("Aguardando")


            #zera o pouso emergencial
            for mc in mTeste.mcs:
                mc.setStopMotion(False)

            while(inMaintenance):
                maintenanceInput = input("tecle enter se estiver pronto")
                if(maintenanceInput == ""):
                    inMaintenance = False



            for sync in mTeste.scfs:
                sync.close_link()

if __name__ =='__main__':
    main = Main()
    try:
        main.start()
    except (KeyboardInterrupt, SystemExit):
        Servidor.push_status("Aguardando")
