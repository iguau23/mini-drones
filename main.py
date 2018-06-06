from testes import Teste
from servidor import Servidor
import combinacao
import time


class Main():
    def start(self):
        continueMain = True
        continueTeste = True
        Servidor.push_status("Iniciando...")
        while(continueTeste):
            print("iniciando testes\n")
            Servidor.push_status("Preparando drone...")
            mTeste = Teste()
            mTeste.start()

            continueConexao = True
            while(continueConexao):
                Servidor.push_status("Pronto! Aguardando comando")
                mServidor = Servidor()
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
                Servidor.push_status("Movimento executado")


                #zera o pouso emergencial
                for mc in mTeste.mcs:
                    mc.setStopMotion(False)

                entrada = 'start'

                entrada = input("tecle enter para continuar, ou digite algo para reiniciar conexao:  ")

                if (entrada == ""):
                    continueConexao = True
                else:
                    continueConexao = False


            for sync in mTeste.scfs:
                sync.close_link()
            entrada = 'start'

if __name__ =='__main__':
    main = Main()
    try:
        main.start()
    except (KeyboardInterrupt, SystemExit):
        Servidor.push_status("Movimento executado")
        time.sleep(0.2)
        Servidor.push_status("Iniciando...")
