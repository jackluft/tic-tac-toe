
# oct 23, 2019
# jack luft
# tic/tac/toc project-server
# Need to add tried game and whne you win the Progam doesnt close it correctly not yet [Done]
import socket
import threading
import time
import pickle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 5689
s.bind((host,port))
print("Waiting for connectiotns............")
s.listen(2)
client = []
play = ["p1","p2"]
board = [" "," "," "," "," "," "," "," "," "]
index = 0
moves = []
def respond(conn):
    global board
    while True:
        go = True
        data = conn.recv(1024).decode('UTF-8')
        if not data:
            break

        formats = data.split(":")
        Id = formats[0]
        user = int(formats[1])
        if Id == 'p1':
            char = 'X'
        else:
            char = 'O'


        board[user] = char
        moves.append(user)
        if((board[0]== 'O' and board[1] == 'O'and  board[2] == 'O' ) or (board[3]=='O' and board[4]=='O' and board[5] == 'O' ) or (board[6]=='O' and board[7]=='O' and board[8] == 'O' )or (board[0] == 'O' and board[4]=='O' and board[8] == 'O') or (board[2] == 'O' and board[4]=='O' and board[6] == 'O') or (board[2] == 'O' and board[5]=='O' and board[8] == 'O') or (board[1] == 'O' and board[4]=='O' and board[7] == 'O') or (board[0] == 'O' and board[3]=='O' and board[6] == 'O')):
            print("O won!!!!")
            for c in client:
                data = "O won the game!!!\nX lost :("
                c.send(data.encode('UTF-8'))
            break


        if((board[0]== 'X' and board[1] == 'X'and  board[2] == 'X' ) or (board[3]=='X' and board[4]=='X' and board[5] == 'X' ) or (board[6]=='X' and board[7]=='X' and board[8] == 'X' )or (board[0] == 'X' and board[4]=='X' and board[8] == 'X') or (board[2] == 'X' and board[4]=='X' and board[6] == 'X') or (board[2] == 'X' and board[5]=='X' and board[8] == 'X') or (board[1] == 'X' and board[4]=='X' and board[7] == 'X') or (board[0] == 'X' and board[3]=='X' and board[6] == 'X')):
            print("X won!!!!!")
            for c in client:
                data = "X won the game!!!\nO lost :("
                c.send(data.encode('UTF-8'))
            break

        if((board[0] == 'X' or board[0] == 'O') and (board[1] == 'X' or board[1] == 'O') and (board[2] == 'X' or board[2] == 'O') and (board[3] == 'X' or board[3] == 'O') and (board[4] == 'X' or board[4] == 'O') and (board[5] == 'X' or board[5] == 'O') and (board[6] == 'X' or board[6] == 'O') and (board[7] == 'X' or board[7] == 'O') and (board[8] == 'X' or board[8] == 'O')):
            print("Game is Tied!!")

            for c in client:
                print("Going to send to "+str(c))
                data = "Game is Tied"
                c.send(data.encode('UTF-8'))
            board = [" "," "," "," "," "," "," "," "," "]
            go = False

        if go == True:
            print("As Pickled: "+str(data))
            print("Has Not Picled: "+str(data))
            for c in client:
                if c != conn:
                    data = pickle.dumps(board)
                    c.send(data)


    conn.close()
    client.remove(conn)


while True:
    if index == 2:
        for c in client:
            data = "start"
            c.send(data.encode('UTF-8'))
    conn, adr = s.accept()
    print("Connection from: "+str(adr))
    if index >=2:
        index = 0
        board = [" "," "," "," "," "," "," "," "," "]
        client = []
    client.append(conn)
    conn.send(play[index].encode('UTF-8'))
    threading.Thread(target=respond,args=(conn,)).start()
    index = index +1


