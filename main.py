from testes import Teste
from servidor import Servidor
import combinacao


continueMain = True
continueTeste = True
continueConexao = True
while(continueTeste):
    print("iniciando testes\n")
    mTeste = Teste()
    mTeste.start()

    while(continueConexao):
        mServidor = Servidor()
        mServidor.verificar_comando()

        if (mServidor.comando=="linear"): #com um drone apenas
            print("linear")
            combinacao.combinacao1(mTeste.mcs[0])
        if (mServidor.comando=="zigzag"): #com um drone apenas
            print("zigzag")
            combinacao.arco(mTeste.mcs[0], mTeste.mcs[1])
        if (mServidor.comando=="loop"):
            print("loop")
            combinacao.esquadrilha(mTeste.mcs[0], mTeste.mcs[1])

        entrada = input("")

    for sync in mTeste.scfs:
        sync.close_link()
