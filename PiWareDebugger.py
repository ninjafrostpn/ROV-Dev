import socket, threading

print """TYPE_OPTIONS = 0
TYPE_MOTOR_1 = 1
TYPE_MOTOR_2 = 2
TYPE_MOTOR_3 = 3
TYPE_LIGHTS = 4
TYPE_CAM_X = 5
TYPE_CAM_Y = 6"""

def sending():
    while True:
        commandtype, value = input(">> ")
        command = commandtype << 5
        command |= 31 & value
        if command < 256:
            data = chr(command)
            s.send(data)
        else:
            print "Invalid command"

addr = ("139.166.166.21", 8080)
homeaddr = ("127.0.0.1", 9001)
piaddr = ("192.168.0.30", 9001)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

broken = True
while broken:
    try:
        s.connect(homeaddr)
        broken = False
        print "Connected up :)"
    except:
        print "Nope"
sender = threading.Thread(target=sending)
sender.start()
