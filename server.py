import pygame
import socket
import time

buttons = {'A':0,'B':0,'X':0,'Y':0,
           'L1':0,'R1':0,'back':0,'start':0,'Center':0,
           'ButtonL':0,'ButtonR':0,'L2':0,'R2':0,
           'Hat_Up':0,'Hat_Down':0,'Hat_R':0,'Hat_L':0}

axiss=[0.,0.,0.,0.,0.,0.]

JSMode = False
text1 = "Mode1 "
# text2 = "Mode2 "

pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

HOST = '192.168.0.236'  # Change this to your computer IP
PORT = 5000 # Change this to your desired port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
  

def getJS(name=''): # this fn for joy
    global buttons , JSMode
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axiss[event.axis] = round(event.value,2)

        elif event.type == pygame.JOYBUTTONDOWN:
            for x,(key,val) in enumerate(buttons.items()):
                if x<=10:
                    if controller.get_button(x): 
                        buttons[key] = 1

            # if buttons['Center'] == 1:
            #     JSMode = not JSMode

        elif event.type == pygame.JOYBUTTONUP:
            for x,(key,val) in enumerate(buttons.items()):
                if x<=10:
                    if event.button == x: 
                        buttons[key] = 0     
                        
        elif event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            if hat_x == 0 and hat_y == 0:
                buttons['Hat_Up'] = 0
                buttons['Hat_Down'] = 0
                buttons['Hat_R'] = 0
                buttons['Hat_L'] = 0
            elif hat_x == 1:
                buttons['Hat_R'] = 1
            elif hat_x == -1:
                buttons['Hat_L'] = 1
            elif hat_y == 1:
                buttons['Hat_Up'] = 1
            elif hat_y == -1:
                buttons['Hat_Down'] = 1
                        
    buttons['ButtonLX'],buttons['ButtonLY'],buttons['ButtonRX'],buttons['ButtonRY'],buttons['L2'],buttons['R2'] = [axiss[0],axiss[1],axiss[3],axiss[4],axiss[2],axiss[5]]
    if name == '':
        return buttons
    else:
        return buttons[name]

def JSMode1(client_socket): # this fn for send data to client
            # if getJS('ButtonLY') == 1 and  getJS('ButtonRY') == 1: # Down Down
            #     print(text1, "LY Down and RY Down")
            #     client_socket.send("LYDown_and_RYDown".encode())
            
            # elif getJS('ButtonLY') == -1 and  getJS('ButtonRY') == -1: # Up Up
            #     print(text1, "LY Up and RY Up")
            #     client_socket.send("LYUp_and_RYUp".encode())

            # elif getJS('ButtonLY') == 1 and  getJS('ButtonRY') == -1: # Down Up
            #     print(text1, "LY Down and RY Up")
            #     client_socket.send("LYDown_and_RYUp".encode())

            # elif getJS('ButtonLY') == -1 and  getJS('ButtonRY') == 1: # Up Down
            #     print(text1, "LY Up and RY Down")
            #     client_socket.send("LYUp_and_RYDown".encode())

            #################################
            # elif getJS('R1') == 1 and getJS('L1') == 1:
            #     print(text1,"R1 and L1")
            #     client_socket.send("R1_L1".encode())

            # elif getJS('R2') == 1 and getJS('L2') == 1:
            #     print(text1,"R2 and L2")
            #     client_socket.send("R2_L2".encode())
            
            #################################
            if getJS('A') == 1:
                print(text1, "A")  
                client_socket.send("A".encode())

            elif getJS('B') == 1:
                print(text1, "B")
                client_socket.send("B".encode())

            elif getJS('X') == 1:
                print(text1, "X")
                client_socket.send("X".encode())

            elif getJS('Y') == 1:
                print(text1, "Y")
                client_socket.send("Y".encode())

            #################################
            elif getJS('R1') == 1:
                print(text1, "R1")
                client_socket.send("R1".encode())

            elif getJS('R2') == 1:
                print(text1, "R2")
                client_socket.send("R2".encode())

            elif getJS('L1') == 1:
                print(text1, "L1")
                client_socket.send("L1".encode())

            elif getJS('L2') == 1:
                print(text1, "L2")
                client_socket.send("L2".encode())

            #################################
            elif getJS('Hat_Up') == 1:
                print(text1, "Hat_Up")
                client_socket.send("Hat_Up".encode())

            elif getJS('Hat_Down') == 1:
                print(text1, "Hat_Down")
                client_socket.send("Hat_Down".encode())

            elif getJS('Hat_L') == 1:
                print(text1, "Hat_L")
                client_socket.send("Hat_L".encode())

            elif getJS('Hat_R') == 1:
                print(text1, "Hat_R")
                client_socket.send("Hat_R".encode())

            #################################
            elif getJS('ButtonLX') == 1:
                print(text1, "ButtonLX")
                client_socket.send("ButtonLX1".encode())

            elif getJS('ButtonLX') == -1:
                print(text1, "ButtonLX-1")
                client_socket.send("ButtonLX-1".encode())

            elif getJS('ButtonLY') == 1:
                print(text1, "ButtonLY1")
                client_socket.send("ButtonLY1".encode())

            elif getJS('ButtonLY') == -1:
                print(text1, "ButtonLY-1")
                client_socket.send("ButtonLY-1".encode())
            

            #################################
            elif getJS('ButtonRX') == 1:
                print(text1, "ButtonRX")
                client_socket.send("ButtonRX1".encode())

            elif getJS('ButtonRX') == -1:
                print(text1, "ButtonRX-1")
                client_socket.send("ButtonRX-1".encode())

            elif getJS('ButtonRY') == 1:
                print(text1, "ButtonRY1")
                client_socket.send("ButtonRY1".encode())

            elif getJS('ButtonRY') == -1:
                print(text1, "ButtonRY-1")
                client_socket.send("ButtonRY-1".encode())

            #################################
            elif getJS('start') == 1:
                print(text1, "start")
                client_socket.send("start".encode())

            elif getJS('back') == 1:
                print(text1, "back")
                client_socket.send("back".encode())

            ##################################
            elif getJS('ButtonL') == 1:
                print(text1, "ButtonL")
                client_socket.send("ButtonL".encode())

            elif getJS('ButtonR') == 1:
                print(text1, "ButtonR")
                client_socket.send("ButtonR".encode())

            ##################################
            elif getJS('Center') == 1:
                print('Center')
                client_socket.send("CT".encode())
            else:
                print("Stop")
                client_socket.send("Stop".encode())

            time.sleep(0.05)

# def JSMode2(client_socket):
#             if getJS('A') == 1:
#                 print("Mode2 A")
#                 client_socket.send("Mode2 A".encode())

#             else:
#                 print("Mode2 Stop")
#                 client_socket.send("Stop".encode())
#             time.sleep(0.05)


def main(client_socket):
    while True:
        # if JSMode:
            JSMode1(client_socket)
        #################################
        # else:
        #     JSMode2(client_socket)
            


print("SERVER START...")
client_socket, addr = server_socket.accept()
main(client_socket)
