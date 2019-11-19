#jack luft
# tic/tac/toe
import socket
import time 
import threading
import pickle
p = [" "," "," "," "," "," "," "," "," "]
dead = False
on = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'jack.luft.ca'
port = 5689
s.connect((host,port))
player = s.recv(1024).decode('UTF-8')
if player == 'p1':
	tern = True
	# player 1 is X
	print("You are X")
	char = 'X'
	Id = "p1"

elif player == 'p2':
	# Player 2 is O
	tern = False
	print("You are O")
	char = 'O'
	Id = "p2"

else:
	print("conenction closed")
	s.close()

print("yes please wait for other player")
data = s.recv(1024).decode('UTF-8')
print(data)



def s_recv():
	global p
	global tern
	global dead
	global on
	while dead == False:

		if tern == False:
			print("Waiting for move......")
			board = s.recv(1024)
			try:
				data = board.decode('UTF-8')
				if (data.startswith("X")):
					print("-----------")
					if(Id == 'p1'):
						print("You Won!!!!!!!")
					elif(Id == 'p2'):
						print("You Lost :(")
					
					dead = True
					on  = False
					break
					print("Thanks for playing!!")

				elif(data.startswith("O")):
					print("-----------")
					if(Id == 'p2'):
						print("You Won!!!!!!!")
					elif(Id == 'p1'):
						print("You Lost :(")
					
					dead = True
					on  = False
					break
					print("Thanks for playing")

				elif(data.startswith('G')):
					print("-----------")
					print(str(data))
					#p = [" "," "," "," "," "," "," "," "," "]

					
					print("Thanks for playing ---sig")
					dead = True
					on = False
					tern = False
					break

			except:
				pass
			if on == True:
				board = pickle.loads(board)
				p = board
			print(p[0]+"|"+p[1]+"|"+p[2])
			print(p[3]+"|"+p[4]+"|"+p[5])
			print(p[6]+"|"+p[7]+"|"+p[8])

			tern = True
	s.close()







def s_send():
	global tern
	global dead
	print(p[0]+"|"+p[1]+"|"+p[2])
	print(p[3]+"|"+p[4]+"|"+p[5])
	print(p[6]+"|"+p[7]+"|"+p[8])
	while dead == False:
		if tern == True:
			
			user = input("Selct where you want to put "+str(char)+" (1-9)")


			while(user != "1" and user != "2" and user != "3" and user != "4" and user != "5" and user != "6" and user != "7" and user != "8" and user != "9"):
				user = input("Selct where you want to put "+str(char)+" (1-9)")
				print("In loop one ")
				#print("IN loop")
			user = int(user)
			while(p[user-1] == 'X' or p[user-1] == 'O'):
				user = int(input("Selct where you want to put "+str(char)+" (1-9)"))
				print("In loop two")
				#print("IN Second loop")

			
			data = Id+":"+str(user-1)
			p[user-1] = char
			print(p[0]+"|"+p[1]+"|"+p[2])
			print(p[3]+"|"+p[4]+"|"+p[5])
			print(p[6]+"|"+p[7]+"|"+p[8])
			print("---------------------")
			print("^Your move^")
			print("----------------")
			s.send(data.encode('UTF-8'))

			#print("Out of loop")
			tern = False

threading.Thread(target=s_send).start()
threading.Thread(target=s_recv).start()


while dead ==False:
	time.sleep(0.1)

print("\nThanks for playing :)")
