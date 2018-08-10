class Buffer:
    field = ''
    def addPacket(self,pkt):
        Buffer.field = Buffer.field + pkt
    def printPacket(self):
        print Buffer.field

#  main
packetSize=42
filename='data.txt'
file=open(filename, "rb")
buf = Buffer()
while True:
    packet=file.read(packetSize)
    if packet == '':
        break
    buf.addPacket((packet))
buf.printPacket()

