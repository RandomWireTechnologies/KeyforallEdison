#!/usr/bin/python

# This is a library for providing access to Kwikset Smartcode Locks via UART
# The h/w interface is 3.3V 9600 baud 8N1 standard UART
# This is more  of a protocol encoder/decoder though

from binascii import hexlify,unhexlify

pkt_count = 0

NO_DATA = ''
LOCK_CMD = 'e703'
UNLOCK_CMD = 'e705'
INIT_CMDS = ('e707','e74d','e702','e70a','e718','e709','e742','e70f')
INIT_DATAS = ('','','','','','','01010101','15031301471205')
PARSE_LOOKUP = {'e709':"parse_initack",'e727':"parse_lockstatus",'e729':"parse_newlockcode",'e742':"parse_error"}

def generate_packet(cmd,data):
    global pkt_count 
    pkt_count += 1
    length = (len(cmd+data)/2)+2
    base_pkt = "%0.2x%0.2x" % (length,pkt_count)+cmd+data
    pkt = "bd"+base_pkt+calculate_crc(base_pkt)
    return pkt

def calculate_crc(pkt):
    crc = int("ff",16)
    #print "Starting crc = %0.2x"%crc
    while len(pkt)>1:
        crc ^= int(pkt[0:2],16)
        #print "After byte 0x%s, CRC = %0.2x, Len=%d"%(pkt[0:2],crc,len(pkt))
        pkt = pkt[2:]        
    return "%0.2x"%crc

def validate_crc(pkt):
    if calculate_crc(pkt) == '00':
        return True
    else:
        return False

def parse_packet(pkt):
    if pkt[0:2] != 'bd':
        print "Bad packet header"
        return False
    if not validate_crc(pkt[2:]):
        print "Bad packet CRC"
        return False
    if ((len(pkt)/2)-2) != int(pkt[2:4],16):
        print "Bad packet length"
        return False
    cmd = pkt[6:10]
    data = pkt[10:-2]
    print "Found cmd=%s & data=%s"%(cmd,data)
    if cmd in PARSE_LOOKUP:
        parse = globals()[PARSE_LOOKUP[cmd]]
        return parse(data)
    return True

def parse_initack(data):
    if data == '64':
        return True
    else:
        return False        

def parse_lockstatus(data):
    code_used = int(data[2:4],16)
    status_bits = int(data[4:6],16)
    if status_bits & 0x80:
        cause = "Remote Control"
    elif status_bits & 0x40:
        cause = "Code %d Entered"%(code_used)
    elif status_bits & 0x20:
        cause = "Automatic Lock"
    else:
        cause = "Manual/Key"
    if status_bits & 0x02:
        lock_state = "Unlocked"
    elif status_bits & 0x01:
        lock_state = "Locked"
    else:
        lock_state = "Unknown"
    
    return (lock_state,cause)
               

def parse_newlockcode(data):
    return data

def parse_error(data):
    return data

def generate_init_packet(num):
    return unhexlify(generate_packet(INIT_CMD[num],INIT_DATA[num]))

def generate_lock_packet():
    return unhexlify(generate_packet(LOCK_CMD,''))

def generate_unlock_packet():
    return unhexlify(generate_packet(UNLOCK_CMD,''))