import logging
import time
import cflib.crtp
import trajetorias as tr
import threading
import paralelo
import combinacao

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.log import LogConfig

COMB1 = '1'
COMB2 = '2'
COMB3 = '3'
ESQUADRILHA = '4'
CIRCULOS = '5'
TESTBATTERY = '9'
TESTSUBIDA = '0'
SELECT = '123'
FINALIZA_TESTE = '99'
SAIR = 's'

class Teste():
    def __init__(self):
        URI1 = 'radio://0/10/2M/E7E7E7E7E1'
        URI2 = 'radio://0/20/2M/E7E7E7E7E2'
        URI3 = 'radio://0/30/2M/E7E7E7E7E3'
        URI4 = 'radio://0/40/2M/E7E7E7E7E4'
        self.uris = [URI1, URI2, URI3, URI4]

    def pouso_emergencial(self):
        stop = False
        while(stop==False):
            entrada = input("pouso emergencial - Drone (1), (2), (3) OU (4): ")
            if(entrada == ""): # se vazio, sai
                break

            try:
                entrada = int(entrada)
            except:
                entrada = 0
            if(entrada  in self.selected):
                n = self.selected.index(entrada)
                if(n!=-1):
                    self.mcs[n].setStopMotion(True)
                    print("pouso emergencial %d acionado" %entrada)

            #verifica se todos os motores foram pausados
            stop = True
            for mc in self.mcs:
                if(mc.getStopMotion()==False):
                    stop = False

    def setThreadEmergencial(self):
        #inicia a thread para o pouso emergencial
        threadEmergencial = threading.Thread(target=self.pouso_emergencial)
        threadEmergencial.setDaemon(True)
        threadEmergencial.start()

    def setVerificaBateria(self):
        time.sleep(0.5)
        self.lg_battery = LogConfig(name='Battery', period_in_ms=100)
        self.lg_battery.add_variable('pm.vbat', 'float')
        try:
            self.cfs[0].log.add_config(self.lg_battery)
            #This callback will receive the data
            self.lg_battery.data_received_cb.add_callback(self.stab_log_data)
            # Start the logging
            self.lg_battery.start()
        except AttributeError:
            print('Could not add Stabilizer log config, bad configuration.')

    def testeSubida(self, mc):
        mc.take_off()
        time.sleep(2)
        mc.land()

    def testeSubida2(self, mc1, mc2):
        thread1 = threading.Thread(target=self.testeSubida, args=(mc1,))
        thread1.setDaemon(True)

        thread2 = threading.Thread(target=self.testeSubida, args=(mc2,))
        thread2.setDaemon(True)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    def testeBateria(self, cf):
        time.sleep(0.5)
        lg_stab = LogConfig(name='Battery', period_in_ms=100)
        lg_stab.add_variable('pm.vbat', 'float')
        try:
            cf.log.add_config(lg_stab)
            #This callback will receive the data
            lg_stab.data_received_cb.add_callback(self.stab_log_data)
            # Start the logging
            lg_stab.start()
        except AttributeError:
            print('Could not add Stabilizer log config, bad configuration.')
        time.sleep(0.3)
        lg_stab.stop()
        time.sleep(0.3)

    def stab_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        print('\n[%d][%s]: %s' % (timestamp, logconf.name, data))
        tensao = float(str(data)[12:16])
        if(tensao<=3.5):
            print("FALHA! A tensão na bateria é: %f" %tensao)


    def selectDrone(self):
        self.cfs = []
        self.scfs = []
        self.mcs = []
        self.selected = []
        message = 'Quais drones deseja controlar? (1, 2, 3, 4 ou combinacao delas):'

        while(len(self.selected)==0):
            user_input_numbers = input(message)
            if(user_input_numbers.find('1')!=-1):
                self.selected.append(1)
            if(user_input_numbers.find('2')!=-1):
                self.selected.append(2)
            if(user_input_numbers.find('3')!=-1):
                self.selected.append(3)
            if(user_input_numbers.find('4')!=-1):
                self.selected.append(4)
            if(len(self.selected)==0):
                print("comando invalido")

            try:
                for i in self.selected:
                    cf = Crazyflie(rw_cache='./cache')
                    self.cfs.append(cf)
                    sync = SyncCrazyflie(self.uris[i-1], cf=cf)
                    sync.open_link()
                    self.mcs.append(MotionCommander(sync))
                    self.scfs.append(sync)
            except:
                print("Exception: Too many packets lost\n")
                self.selected = []


    def start(self):
        cflib.crtp.init_drivers(enable_debug_driver=False)
        factory = CachedCfFactory(rw_cache='./cache')
        self.selectDrone()

        selectedTest = 'start'
        while(selectedTest != '99'):
            self.isAlive = True
            messageTest = ("\nQual teste você deseja fazer?\n"
                          "(1) Combinacao1\n"
                          "(2) Combinacao2\n"
                          "(3) Combinacao3\n"
                          "(4) Esquadrilha\n"
                          "(5) Círculos\n"
                          "(9) bateria\n"
                          "(0) subida\n"
                          "(123) selecionar drone\n"
                          "(99) finalizar teste\n")
            selectedTest = input(messageTest)

            #Verifica se não houve perda de conexão
            for cf in self.cfs:
                if (cf.link == None):
                    print("conexao com o drone perdida")
                    selectedTest = SELECT
                    break


            if (selectedTest == COMB1):
                self.setThreadEmergencial()
                combinacao.combinacao1(self.mcs[0])
            elif(selectedTest == COMB2):
                self.setThreadEmergencial()
                combinacao.combinacao2(self.mcs[0], self.mcs[1])
            elif(selectedTest == COMB3):
                self.setThreadEmergencial()
                combinacao.combinacao3(self.mcs[0], self.mcs[1], self.mcs[2])
            elif(selectedTest == ESQUADRILHA):
                self.setThreadEmergencial()
                combinacao.esquadrilha(self.mcs[0], self.mcs[1])
            elif(selectedTest == CIRCULOS):
                self.setThreadEmergencial()
                combinacao.circulo(self.mcs[0], self.mcs[1])
            elif(selectedTest == TESTBATTERY):
                if(len(self.selected)>1):
                    d = int(input("selecione o drone: "))
                    n = self.selected.index(d)
                    self.testeBateria(self.cfs[n])
                else:
                    self.testeBateria(self.cfs[0])
                time.sleep(0.5)
            elif(selectedTest == TESTSUBIDA):

                if(len(self.selected)==1):
                    self.testeBateria(self.cfs[0])
                    self.testeSubida(self.mcs[0])
                else:
                    print("bateria drone ", self.selected[0])
                    self.testeBateria(self.cfs[0])

                    print("bateria drone ", self.selected[1])
                    self.testeBateria(self.cfs[1])
                    self.testeSubida2(self.mcs[0], self.mcs[1])
            elif(selectedTest == SELECT):
                for sync in self.scfs:
                    sync.close_link()
                self.selectDrone()
            elif(selectedTest == SAIR):
                for sync in self.scfs:
                    sync.close_link()
                print("\n===============================================================================\n"
                      "     Obrigado por terem utilizado o nosso mini-drones tests!\n"
                      "                      Espero que tenham gostado!\n"
                      "===============================================================================\n")
                break

            #zera o pouso emergencial
            for mc in self.mcs:
                mc.setStopMotion(False)



if __name__ == '__main__':
    teste = Teste()
    teste.start()