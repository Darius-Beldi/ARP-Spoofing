# ARP-Spoofing

## The container structure I used for testing:

```
            MIDDLE------------\
        subnet2: 198.7.0.3     \
        MAC: 02:42:c6:0a:00:02  \
               forwarding        \ 
              /                   \
             /                     \
Poison ARP 198.7.0.1 is-at         Poison ARP 198.7.0.2 is-at 
           02:42:c6:0a:00:02         |         02:42:c6:0a:00:02
           /                         |
          /                          |
         /                           |
        /                            |
    SERVER <---------------------> ROUTER <---------------------> CLIENT
net2: 198.7.0.2                      |                           net1: 172.7.0.2
MAC: 02:42:c6:0a:00:03               |                            MAC eth0: 02:42:ac:0a:00:02
                           subnet1:  172.7.0.1
                           MAC eth0: 02:42:ac:0a:00:01
                           subnet2:  198.7.0.1
                           MAC eth1: 02:42:c6:0a:00:01
                           subnet1 <------> subnet2
                                 forwarding
```

## Prerequisites
Linux based system
Install docker and docker-compose:
```
apt-get install docker docker-compose
```

## How to run

Create a docker image:

    cd Docker
    docker build -t arp_spoofing
    
Start the containers

    docker-compose up -d

Run the spoofing script in a middle bash

    docker-compose exec middle bash
    python3 scripts/arp_spoofing.py

### Clear the iptables for server and router containers 

In separate terminals:

    docker-compose exec server bash
    ip -s -s neigh flush all



    docker-compose exec router bash
    ip -s -s neigh flush all


## Testing

Open another terminal and run the commands: 

    docker-compose exec middle bash
    tcpdump -SntvXX -i any

In the server terminal run this: 
    
    wget http://old.fmi.unibuc.ro
    
In the middle terminal you just opened you should see something like this: 

![image](https://github.com/user-attachments/assets/bd090bd9-5a92-4aa6-8d0c-ba748c6d4cb3)
