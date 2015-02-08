from mido import Parser
import binascii
import string
import struct
import sys

class Message():
    def __init__(self, status_byte, note_number, velocity):
        self.status_byte = binascii.hexlify(status_byte)
        self.note_number = binascii.hexlify(note_number)
        self.velocity = binascii.hexlify(velocity)

    def __str__(self):
        return "status_byte= %s, note number= %s, velocity= %s" %\
                (self.status_byte, self.note_number, self.velocity)

def getLength(f):
    
    cont = True
    byte = ""
    while cont:
        b = ord(f.read(1))
        if (b >> 7) & 1 == 0:
            cont = False
                        
        for i in range(6,-1,-1):
            byte += str((b >>i) & 1)

    return int(byte, 2)
                
def parseMessage(f):
    meta_type = f.read(1)
    if meta_type == b'\x2F':
        print "End of Track"
        v_length = getLength(f)
        return False

    v_length = getLength(f)
    message = ""
    print "v_length: ", v_length
    for j in range(v_length):
        message += str(f.read(1))
    print "Meta Event: ", message
    return message

def SysExEv(f):
    message = ""
    while s != b'\XF7':
        s = f.read(1)
        message += s
    return message

msgs = []
with open("darude-sandstorm.mid", "rb") as f:
    f.read(4) #Always start with a header
    struct.unpack(">i", f.read(4))[0] #header length, 6
    fo = struct.unpack(">h", f.read(2))[0] # what type of file is this?
    # if fo == 0:
    #     print "single track"
    # if fo == 1:
    #     print "multitrack"
    # if fo == 2:
    #     print "multisong"

    #how many track chunks are there?
    chunkSize = struct.unpack(">h", f.read(2))[0] 
     
    print "Track chunks: ", chunkSize
    #print "delta timing: ", \
    struct.unpack(">h", f.read(2))[0] #ticks per beat

    for chunkNumber in range(chunkSize):

        MTrk = f.read(4) #chunk header
        if MTrk !="MTrk":
            raise TypeError("Track mark is off at chunk: " + str(chunkNumber))
        
        #number of events in the chunk
        length = struct.unpack(">i", f.read(4))[0]
        print "events in track: ", length
        for i in range(length):
            print "Track Event Number: ", i
            v_time = getLength(f)
            print "current time: ", v_time

            s = f.read(1)
            if s == b'\xFF':
                #Meta Event
                con = parseMessage(f)
                if not con:
                    break
                
            elif s == b'\xF0' or s == b'\xF7':
                #System Exclusive Event
                SysExEv(f)
                
            else:
                #its a Track Event
                #msg = Message(s, f.read(1), f.read(1))
                #msgs.append(msg)
                #print "note: ", msg
                pass