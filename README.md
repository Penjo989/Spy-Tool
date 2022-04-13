# Spy Tool
A network tool for performing simple second layer attacks with a simple gui.

## Table of Contents
- Introduction

  - How this project came to be
  - The spy, HQ and communicator
  - What does the tool do
  
- Features
    - Perform a brute-force attack on a wpa2-psk secured wireless network
    - Connect multiple spies to a single communicator
    - Command a spy to start an arp poisoning attack between any 2 stations
    - Command a spy to start capturing the traffic between any 2 stations
    - Command a spy to scan the local network it's in
    - Control a spy's shell from the hq's gui
    
- Security And Encryption
    - The Data Transfer Protocol
    - The Authentication Proccess

- Known Issues

- Future Plans

## Introduction
### How this project came to be

When I first started this project, my goal was to make a graphical network tool that would allow you to initiate a basic second-layer attack(for example Arp poisoning) over the internet by controlling a “spy” computer in the desired network. When I finished my first version of my project that could do all that I felt like the project didn’t have much use and I decided to expand it by turning it into a tool that can perform an entire attack with a simple gui/ui. I started reading about the wpa/wpa2 protocols and about their vulnerabilities and I decided to implement into my tool an automatic wpa2-psk brute-force attack. 
After writing code that could brute force a wpa2-psk secured network I felt that If I had added only this feature to my project it will not be able to perform a full attack. When I was coding the brute force attack’s code, I came across a Linux tool named tmux and I realized that if I could make my program open a tmux tab and capture the output of it without stopping my main code I could essentially make a synthetic shell and so I added that to my project too.

### The spy, the HQ and the communicator
The final project consists of 3 parts:
- the spy – which is the program ran on the computer that is connected(or close by) to the desired local network.
- the communicator – which is the server that the spy connects to and sends and receives it’s information and commands(the communicator is essential because of port forwarding) 
- the HQ – which is the program that the user runs on his pc and controls/monitors the attack.

### What does the tool do
When the spy is first executed it will ask the user on which interface he would like to operate, if the given interface is not connected to the internet the program will offer him to brute-force the psk of the network of his choice using a dictionary of his choice. After connecting the spy to the internet, the user will connect to the desired communicator. The user could then launch the hq on his PC, connect to the same communicator and communicate with the spy with an encryption protocol similar to the wpa2-psk protocol, the user will be able to operate a shell on the spy, scan the spy’s network and perform Arp poisoning and mitm attacks with a simple gui.

## Features
Note: the entire wpa2-psk brute-force attack, the Arp spoofs, the mitm attacks and the scans were written in python with scarce use of external tools.
### Perform a brute-force attack on a wpa2-psk secured wireless network

When the spy is given a interface it checks if it’s connected to the internet by sending a ping to a chosen address (defaulted to google.com) and checks if there is a response, after checking the connection, if the spy isn’t connected and the user wants to brute force an access point’s psk the program starts an attack made up of 4 parts:
- The spy enters monitor mode using air-crack, starts sniffing for beacons (using scapy) of the given ssid and extracts the bssid of the AP and simultaneously starts switching channels.
** **
The function that handles a sniffed packet:
```python
def packetHandler(self, pkt):
    if pkt.haslayer(Dot11):  # refers to 802.11 protocol
        if pkt.type == 0 and pkt.subtype == 8:#checks if is a beacon
            if pkt.info.decode("utf-8") == self.ssid:  # pkt.info = ssid
                self.bssid = pkt.addr2
                self.apChannel = self.freqToChannel(pkt[RadioTap].Channel)
                self.isWPA2 = Dot11EltRSN in pkt
                    return True
        return False
```
- The spy creates a thread sending de-auth frames to the stations connected to the AP and simultaneously sniffs  for a 4 way hand-shake made with the AP.

```python
def deAuthThread(self):
    timer = Timer(self.sniffTimeOut)
    dot11 = Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=self.bssid, addr3=self.bssid)
    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
    timer.start()
    while not timer.isOver() and (self.handshake == None or self.handshake.isValid == False):
        try:
            sendp(packet, inter=0.1, iface=self.interface, verbose=False)#sends de-auth packet
        except Exception as e:
            print(e)

```
- After the four way handshake was captured the spy extracts the anonce, snonce, mic and macs of the station and the AP(although it already knows the ap’s mac - bssid)

```python
def getNonce(self, pkt):
    return pkt[Raw].load[13:45]

def getMic(self, pkt):
    return binascii.hexlify(pkt[Raw].load)[154:186]

```


- Finally the spy starts going over a dictionary and for each psk it does the following – turns the psk into a pmk using the pbkdf2 function and the ssid as salt,  turns the pmk into the ptk , generates the mic from the snonce and compares the generated mic to the sniffed mic.

```python 
def calcPMK(self, PSK):
    PMK = hashlib.pbkdf2_hmac('sha1', PSK.encode('ascii'), self.ssid.encode('ascii'), 4096, 32)
    return PMK
```


```python
def calcPTK(self, PMK, data):
    blen = 64
    i = 0
    R = b""
    pke = b"Pairwise key expansion"
    while i <= ((blen * 8 + 159) / 160):
        hmacsha1 = hmac.new(PMK, pke + chr(0x00).encode() + data + chr(i).encode(), hashlib.sha1)
        i += 1
        R = R + hmacsha1.digest()

    return R[:blen]
```

When I ran this attack on my laptop it went over about `300` passwords a second.

### Connect multiple spies to a single communicator 
A single communicator can handle multiple spies conecting to it and allow a HQ to link to them seemlessly
![ezgif-3-85636aff16](https://user-images.githubusercontent.com/53350057/163164751-6544daea-d6c9-4a59-b15b-89aa76e30fa3.gif)

### Command a spy to start an arp poisoning attack between any 2 stations
After connecting to the internet the spy opens a thread for Arp poisoning that is given a set of `station links`  to spoof and sends fake Arp answers for each link (with a default interval of 1 second).
When a HQ links to a spy he can send commands to the spy to add or remove a station link from the arp poisoning thread.

![ezgif-3-09379ba2af](https://user-images.githubusercontent.com/53350057/163182114-7a4d3c1b-ca07-4369-a502-65493b27aed5.gif)


The green line between 2 stations indicates that the spy is performing a arp spoof attack on them.

Note: by writing 'performing a arp spoof attack on them' I mean that the spy is convincing each station that the spy's mac is the other station's mac, so the spy is basically forcing their traffic to go through 
itself.

### Command a spy to start capturing the traffic between any 2 stations
Simmilar to the arp posoning thread, after connecting to the internet the spy opens a thread for capturing traffic between 2 stations - that is given a set of `station links` aswell.
When a HQ links to a spy he can send commands to the spy to add or remove a station link from the mitm thread.

![ezgif-3-e62de6df3c](https://user-images.githubusercontent.com/53350057/163183520-193b7eb3-56a9-4bd3-9b05-58204dfece09.gif)

The red line between 2 stations indicates that the spy is capturing the traffic between them.

### Command a spy to scan the local network it's in
The spy has a scanner object that can perform a quick arp scan on it's local network, when a HQ is controlling a spy it has a scan button that can tell the spy to perform a new scan.

![ezgif-3-8d6799b0a9](https://user-images.githubusercontent.com/53350057/163190091-cbed68f3-72c7-4a7d-bfae-3514bced922e.gif)

### Control a spy's shell from the hq's gui


The spy and the HQ are mostly graphics and socket networking therefore I will only explain how the encryption protocol (which is very similar to the wpa2-psk protocol) works. 
After a spy/socket connects to the communicator’s socket, they send the communicator their name(which is entered by the user). After the communicator receives the name he generates their key from the password of the communicator using the pbkdf2 function with 100000 iterations and the name as salt, he then sends a random number 32-bit  integer to the hq/spy. On the other side the hq/spy receives the number and sends back the same number but encrypted using their key, the communicator checks if the encrypted number that he received is legit by decrypting it, If it is - they start to communicate using that key.

Known issues:
1.	After disconnecting from a communicator the hq fails to connect to it’s spies
2.	Due to frequent de-auth frames being sent the spy accidently disconnects stations from aps while they are authenticating which sometimes causes the handshake that is captured to be made up of 2 different sessions(not sure if this is correct).
3.	Sometimes the spy is disconnected from the communicator without getting notified.


Future plans: 
1.	Add a function that will distinguish between wired and wireless interfaces
2.	Add a function that detects the os type and version
3.	Add an organized ui class to the spy
4.	Add a data collection class
5.	Replace the synthetic shell with an actual ssh tunnel
6.	Rewrite the networking
7.	Enable more dynamic Arp spoofs
8.	Allow the user to choose a subnet mask
9.	Improve gui
