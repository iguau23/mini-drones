from testes import Teste
from servidor import Servidor
import combinacao


continueMain = True
continueTeste = True
while(continueTeste):
    print("iniciando testes\n")
    mTeste = Teste()
    mTeste.start()

    continueConexao = True
    while(continueConexao):
        mServidor = Servidor()
        mServidor.verificar_comando(mTeste)

        if (mServidor.comando=="demo"): #com um drone apenas
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
        if (mServidor.comando=="espiral"): #com um drone apenas
            print("espiral")
            if (len(mTeste.mcs)==2):
                mTeste.setThreadEmergencial()
                combinacao.circulo(mTeste.mcs[0], mTeste.mcs[1])
            else:
                print("numero insuficiente")
        if (mServidor.comando=="esquadrilha"):
            print("esquadrilha")
            mTeste.setThreadEmergencial()
            if (len(mTeste.mcs)==2):
                mTeste.setThreadEmergencial()
                combinacao.esquadrilha(mTeste.mcs[0], mTeste.mcs[1])
            else:
                print("numero insuficiente")


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
    # while ((entrada != 'y') and (entrada!= 'n')):
    #     entrada = input("deseja fazer novos testes?[y]es ou [n]o: ")
    # if (entrada == 'y'):
    #     continueTeste = True
    # else:
    #     continueTeste = False
