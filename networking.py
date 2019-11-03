import pygame
import animation.constants as c
import json
from struct import pack, unpack
import select
from animation.shared_objects import SharedObjects
import time
import threading
import socket
import sys
from cardgame.cards import Card, Deck, Hand, ComplexEncoder


players = None #list of players
playersDone = False #specifies when the other thread has finished fetching client data
PID = None        #personal ID for this client
threadStop=False  #inter-thread message to stop when the game is being closed
servConnect=None
turnDir=1 #0:left, 1:right

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
    
    
#used for the initial turn order sending        
def turnSend(turn, turnOrder, deck):
  global serv   
  
  turnInfo = json.dumps({
        "messageType": "game-state",
        "data": {
            "state": {
                "turn": turn,
                "order": turnOrder,
                "deck": deck
            }
        }
  }, cls=ComplexEncoder)
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
def getNextPlayer(id, turnOrder, cardValue):
  global turnDir
  skip=False  
  ind=turnOrder.index(id)
  if (cardValue=="reverse"):
    if len(turnOrder)==2:
      skip=True
    else:
      if turnDir==1:
        turnDir=-1
      else:
        turnDir=1
  elif (cardValue=="skip"):
    skip=True
  if skip:
    ind=ind+2*turnDir
  else:
    ind=ind+turnDir  
  if ind<0:
    ind=ind+len(turnOrder)
  elif ind>=len(turnOrder):
    ind=ind-len(turnOrder)
  return turnOrder[ind]
  
#check for messages from the current player  
def checkMoves():
  global serv   
  global turnDir
  global PID
  ready_to_read, ready_to_write, in_error =\
                select.select(
                  [serv],
                  [],
                  [],
                  0)
  if len(ready_to_read)==1:
    message = recv_json(serv)    
    if message.get('messageType') in ("game-state", "disconnect", "error", "game-finished"):
      print("network checkMove: ",message)
      if message.get('messageType')=="game-state" and message["data"]["state"]["sender"]!=PID:
        if message["data"]["state"]["reverseOrder"]==True:
          if turnDir==1:
            turnDir=-1
          else:
            turnDir=1
      return message                            
  return None
  
#send move to other players  
def sendMove(source,destination,color,value,cardID,nextPlayer):
  """
  Parameters:
  -----------
  source: can be "deck", "discard", or an integer specifying player id
  destination: "discard", or an integer specifying player id
  color: string
  value: string
  nextPlayer: integer specifying player id
  """
  global serv, PID  
  move = json.dumps({
        "messageType": "game-state",
        "data": {
            "state": {
                "source": source,
                "dest": destination,
                "color": color,
                "value": value,
                "cardID": cardID,
                "reverseOrder": (value=="reverse" and destination=="discard"),
                "nextPlayer": nextPlayer,
                "sender": PID #designates who sent the message
            }
        }
  })
  send_json_norec(serv, move)
  
  
  
#separate thread function, used to connect clients and maintain connection  
def serverConnect(screenNameInput):
    global players
    global playersDone
    global PID
    global threadStop   
    global serv
    id = screenNameInput
    
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
      if (serv!=None):
        send_json_norec(serv, data)
      time.sleep(3)
     


#initial function for establishing connection to server
def connect():
    global servConnect
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
          servConnect=0
          return
        else:
          print("Could not connect to matchmaking server, trying again")          
          time.sleep(1)
    
    
   #get player name
    servConnect=1
    

      
      
def sendEndGame():    
    global serv
    endGameMessage = json.dumps({
        "messageType": "game-finished"        
    })  
    send_json_norec(serv, endGameMessage)      
      
      
      
      
      
      
      
      
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
    