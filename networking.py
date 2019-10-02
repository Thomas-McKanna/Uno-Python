import pygame
import cardanim.constants as c
import json
from struct import pack, unpack
import select
from cardanim.shared_objects import SharedObjects
import time
import threading
import socket
import sys

players = None #list of players
playersDone = False #specifies when the other thread has finished fetching client data
PID = None        #personal ID for this client
threadStop=False  #inter-thread message to stop when the game is being closed

HOST = '127.0.0.1' #hardcoded host and port for now
PORT = 8000

#provided receive function
def recv_json(server_socket):
    header = server_socket.recv(8)   
    size = unpack('<I', header[4:8])[0]
    if not(header.startswith(b"JSON")):
        raise "Invalid JSON format (Missive)"
    if size < 0 or size > 1024 * 1024:
        raise "Incoming JSON is too large: " + str(size)
    # read incoming size from socket, then remove the trailing newline
    body = server_socket.recv(size)[:-1]
    # parse into json
    return json.loads(body)

#provided send function
def send_json(server_socket, msg_payload):
    if msg_payload[-1] != "\n":
        msg_payload += "\n"
    prefix = "JSON".encode("utf-8")
    size = pack("<I", len(msg_payload))
    message = msg_payload.encode("utf-8")    
    server_socket.sendall(prefix + size + message)
    return recv_json(server_socket)

#provided send function, except it does not read immediately after sending
def send_json_norec(server_socket, msg_payload):
    if msg_payload[-1] != "\n":
        msg_payload += "\n"
    prefix = "JSON".encode("utf-8")    
    size = pack("<I", len(msg_payload))    
    message = msg_payload.encode("utf-8")
    server_socket.sendall(prefix + size + message)
    return
    
#class for a text box, only really used to get username as of now    
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = c.COLOR_INACTIVE
        self.text = text
        self.txt_surface = SharedObjects.get_font().render(text, True, self.color)
        self.active = False    
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        
#used for the initial turn order sending        
def turnSend(turn, turnOrder):
  global serv   
  turnInfo = json.dumps({
        "messageType": "game-state",
        "data": {
            "state": {
                "turn": turn,
                "order": turnOrder
            }
        }
  })
  #print(turnInfo)
  send_json_norec(serv, turnInfo)

#used for the initial turn order sending  
def turnRec():
  global serv   
  while True:
    ready_to_read, ready_to_write, in_error = \
     select.select(
        [serv],
        [],
        [],
        1)
    if len(ready_to_read)==1:
      break              
  turnInfo = recv_json(serv)
  while turnInfo.get('messageType') != 'game-state':
        if turnInfo.get('messageType') == 'error':
            raise Exception(json_response.get('data'))
        if turnInfo.get('messageType') == 'disconnect':
            return
        else:            
            while True:
              ready_to_read, ready_to_write, in_error = \
               select.select(
                  [serv],
                  [],
                  [],
                  1)
              if len(ready_to_read)==1:
                break              
            turnInfo = recv_json(serv)
  return turnInfo

  
#returns the next player whose turn it should be
def getNextPlayer(id, turnOrder):
  index=turnOrder.index(id)
  if index==-1:
    raise exception("Invalid player ID")
  index+=1
  if index >= len(turnOrder):
    index=0
  return turnOrder[index]
  
  
#check for messages from the current player  
def checkMoves():
  global serv   
  ready_to_read, ready_to_write, in_error = \
               select.select(
                  [serv],
                  [],
                  [],
                  0)
  if len(ready_to_read)==1:
    message = recv_json(serv)    
    if message.get('messageType')=="game-state": #ignore messages not about game state
      if "msgType" in message.get("data")["state"]: 
        if message.get("data")["state"]["msgType"]=="move": #make sure the 'msgType' is move, so that other game state messages
          return message.get("data")                        #not about moves do not break the main loop
  return None
  
#send move to other players  
def sendMove(t,turn):  
  global serv, PID  
  move = json.dumps({
        "messageType": "game-state",
        "data": {
            "state": {
                "msgType": "move",
                "turn": turn, #next player
                "type": t,    #either 'draw' or 'play', specifing drawing a card or playing a card
                "sender": PID #designates who sent the message
            }
        }
  })
  send_json_norec(serv, move)
  
  
  
#separate thread function, used to connect clients and maintain connection  
def serverConnect(serv,screenNameInput):
    global players
    global playersDone
    global PID
    global threadStop   
    id = screenNameInput.text
    
    data = json.dumps({
        "messageType": "connect",
        "data": {
            "game": "default",
            "clientType": "client",
            "configuration": {
                "id": id,
            }
        }
    })
    send_json_norec(serv, data)
    while True: 
      ready_to_read, ready_to_write, in_error = \
               select.select( #this prevents the program from crashing if a connecting client disconnects before game is made
                  [serv],
                  [],
                  [],
                  1)      
      if threadStop:
        return
      if len(ready_to_read)==1:        
        break      
    json_response = recv_json(serv)
    while json_response.get('messageType') != 'connect':
        if json_response.get('messageType') == 'error':
            raise Exception(json_response.get('data'))
        if json_response.get('messageType') == 'disconnect':
            return
        elif json_response.get('messageType') == 'response':
            print("Message:", json_response.get('data'))
            while True:
              ready_to_read, ready_to_write, in_error = \
               select.select(
                  [serv],
                  [],
                  [],
                  1)
              if threadStop:
                return
              if len(ready_to_read)==1:
                break              
            json_response = recv_json(serv)

    print('Connect:', json_response.get('data'))
    
    print('Telling the game server I am ready')
    game_connect_payload = json.dumps({
        "messageType": "client-info",
        "data": {
            "clientInfo": {
                "id": id
            }
        }
    })
    whois = send_json(serv, game_connect_payload)
    print("response", whois)
    PID = whois.get('data')['id']
    print("I am ",PID)
    time.sleep(3) #wait a while to ensure all clients have connected before requesting client list
    data = json.dumps({
    "messageType": "client-list"
    })
    send_json_norec(serv, data)
    time.sleep(.5) 
    players = recv_json(serv) #keep reading until client list is found
    while players.get('messageType') != 'client-list':
        if players.get('messageType') == 'error':
            raise Exception(players.get('data'))   
        if players.get('messageType') == 'disconnect':
            return            #kill thread
        print("Message:", players)
        players = recv_json(serv)
    playersDone=True      #client list has been read



    while not threadStop:  #maintain connection by requesting client list every 3 seconds
      data = json.dumps({  #to avoid timeout
      "messageType": "client-list"
      })
      send_json_norec(serv, data)
      time.sleep(3)
     


#initial function for establishing connection to server
def connect(clock):
    global players
    global playersDone
    global PID
    global threadStop    
    global serv        
    
    tries=3 #try three times to bind to the matchmaking server
    while True:
      try:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.connect((HOST, PORT))
        break
      except:
        tries-=1
        if tries==0:
          print("Failed to connect to server")
          pygame.quit()
          sys.exit()
        else:
          print("Could not connect to matchmaking server, trying again")          
          time.sleep(1)
    
    
    
    screenNameInput = InputBox(300, 284, 200, 50)    #text box for name
    done = False #use this event handler until player enters name

    while not done:
        for event in pygame.event.get():          
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screenNameInput.rect.collidepoint(event.pos):                    
                    screenNameInput.active = not screenNameInput.active
                else:
                    screenNameInput.active = False                
                screenNameInput.color = c.COLOR_ACTIVE if screenNameInput.active else c.COLOR_INACTIVE
            if event.type == pygame.KEYDOWN:
                if screenNameInput.active:
                    if event.key == pygame.K_RETURN:
                        if (len(screenNameInput.text)>0):
                            done = True                    #valid name, get out of the event handler loop
                    elif event.key == pygame.K_BACKSPACE:
                        screenNameInput.text = screenNameInput.text[:-1]
                    else:
                        screenNameInput.text += event.unicode
                    screenNameInput.txt_surface = SharedObjects.get_font().render(screenNameInput.text, True, screenNameInput.color)

        SharedObjects.get_surface().fill((30, 30, 30)) #fill background
        
        screenNameInput.draw(SharedObjects.get_surface()) #draw input box
        
        #create label text
        SharedObjects.get_surface().blit(SharedObjects.get_font().render("Enter your name:", True, pygame.Color(52, 235, 88)), (290, 180))
        pygame.display.flip() #flip buffer
        clock.tick(c.FPS)
    
    
    
    th = threading.Thread(target = serverConnect, args = (serv, screenNameInput,)) #start connection thread
    th.start()
    screenNameInput.active = False #deselect name box when searching
    screenNameInput.color = c.COLOR_INACTIVE
    while playersDone==False: #sit in this useless event handler until other thread has found a game
      for event in pygame.event.get():    #ignore every event except quit event
        if event.type == pygame.QUIT:   
          threadStop=True                   #tell other thread to die
          pygame.quit()                     #quit out
          sys.exit()      
        print(event)
      SharedObjects.get_surface().fill((30, 30, 30)) #fill background
      
      screenNameInput.draw(SharedObjects.get_surface()) #draw textbox
      #create label text
      SharedObjects.get_surface().blit(SharedObjects.get_font().render("Enter your name:", True, pygame.Color(52, 235, 88)), (290, 180))
      pygame.display.flip()
      clock.tick(c.FPS)

#initalizes opponent name array      
def opponentInit():
  o=[]
  #print(players)
  for thing in players.get('data'):
    if type(thing)==dict:
      if thing['id']!=PID:
        #print("ID: ",thing['id'])
        #print("Name: ",thing['clientInfo']['id'])
        #print("Lobby Leader: ",thing['isLobbyLeader'])
        #print("")
        o=o[:]+[thing['clientInfo']['id']]        
    else:
      print("This should not happen") #sometimes the message would return weird and not be a dictionary, but a string
      print(thing)                    #this is just in case it happens again
      pygame.quit()
      sys.exit() 
  return o
    