from random import randint, choice
import numpy as np
from time import sleep
from tqdm import tqdm
import pygame as pg
import threading as th
from time import sleep

class Matrix(object):
	def __init__(self):
		super(Matrix, self).__init__()
		self.table = [0,0,0,0,0,0,0,0,0]


	def CheckIfWinner(self):
		t = self.table
		if [1,1,1] in [t[:3],t[3:6],t[6:]]:
			return True
		elif [2,2,2] in [t[:3],t[3:6],t[6:]]:
			return False

		# t = t[0]+t[1]+t[2]

		if [1,1,1] in [[t[0],t[3],t[6]],
		[t[1],t[4],t[7]],
		[t[2],t[5],t[8]],
		[t[0],t[4],t[8]],
		[t[2],t[4],t[6]]]:
			return True

		elif [2,2,2] in [[t[0],t[3],t[6]],
		[t[1],t[4],t[7]],
		[t[2],t[5],t[8]],
		[t[0],t[4],t[8]],
		[t[2],t[4],t[6]]]:
			return False 


		return None


	def GetIndexFree(self):
		idx = []
		for index,value in enumerate(self.table):
			if value == 0:
				idx.append(index)
		return idx 


	def GetState(self):
		return str(self.table)


	def AddMove(self, move=0, player=0, random=False):
		if random:
			move 			= choice(self.GetIndexFree())
		self.table[move] 	= player



import pygame as pg
def Render():
	# usar thread para executar essa funcao
	# table sao as jogadas no tabuleiro, por exemplo [0,0,0,0,0,0,0,0,0] 0=vazio, 1=X, 2=O
	global table, posClick, vict, deft, epsilon, epochAct
	table = []
	epochAct = vict = deft = 0
	# pos = []
	pg.init()
	screen = pg.display.set_mode((900,600))
	back   = pg.image.load('sprites/back.png')
	_x     = pg.image.load('sprites/_x.png')
	_o     = pg.image.load('sprites/_o.png')

	while True:
		# sleep(0.2)
		posClick = None
		screen.blit(back, (0,0))
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				exit()
			if ev.type == pg.ACTIVEEVENT:
				pass
			if ev.type == pg.MOUSEBUTTONDOWN:
				x,y = pg.mouse.get_pos()
				if x not in range(157,443) and y not in range(157,443):
					pass
				else:
					if x in range(157,253) and y in range(157,251):
						posClick = 0
					elif x in range(253,347) and y in range(157,251):
						posClick = 1
					elif x in range(347,443) and y in range(157,251):
						posClick = 2
					elif x in range(157,253) and y in range(251,347):
						posClick = 3
					elif x in range(253,347) and y in range(251,347):
						posClick = 4
					elif x in range(347,443) and y in range(251,347):
						posClick = 5
					elif x in range(157,253) and y in range(347,443):
						posClick = 6
					elif x in range(253,347) and y in range(347,443):
						posClick = 7
					elif x in range(347,443) and y in range(347,443):
						posClick = 8
		for p, v in enumerate(table):
			if v != 0:
				x = p%3*97+157+18
				y = p//3*95+157+19
				if v == 1:
					screen.blit(_x,(x,y))
				else:
					screen.blit(_o,(x,y))

		myfont = pg.font.SysFont(pg.font.get_fonts()[8], 20)
		eps = myfont.render('EPSILON: ' + str(round(epsilon, 4)), True, (200, 200, 200))
		epo = myfont.render('EPOCH: ' + str(epochAct), True, (200, 200, 200))
		vic = myfont.render('VICTORIES: ' + str(vict), True, (200, 200, 200))
		deF = myfont.render('DEFEATS: ' + str(deft), True, (200, 200, 200))
		screen.blit(eps,(620,100))
		screen.blit(epo,(620,140))
		screen.blit(vic,(620,180))
		screen.blit(deF,(620,220))
		# screen.blit(textsurface,(int(screen_size[0]/2-textsurface.get_rect().size[0]/2),105))




		pg.display.update()
	# screen.fill((10,25,10))





def Step(matrix, action):
	indexFree 	= matrix.GetIndexFree()
	matrix.AddMove(action, 1, False)
	w 			= matrix.CheckIfWinner()
	done 		= w != None

	if action in indexFree:
		reward 		= 5
	if action not in indexFree:
		reward 		= -30
		done 		= True
	elif w != None:
		if w:
			reward = 20
		else:
			reward = -20

	return matrix, matrix.GetState(), done, reward







def ChooseOneEmptySpace():
	pass


def RandomAction():
	return randint(0,8)


def DrawTicTacToe(matrix):
	def a(matrix,index):
		if matrix[index] == 0:
			return ' '
		elif matrix[index] == 1:
			return 'X'
		else:
			return 'O'
	print('-'*20)
	print('|{}|{}|{}|'.format(a(matrix,0),a(matrix,1),a(matrix,2)))
	print('|{}|{}|{}|'.format(a(matrix,3),a(matrix,4),a(matrix,5)))
	print('|{}|{}|{}|'.format(a(matrix,6),a(matrix,7),a(matrix,8)))


def Test(Q):

	while True:
		M 					= Matrix()		   	   # TicTacToe table
		# DrawTicTacToe(M.table)
		table = M.table
		sleep(2)

		while True:
			state  = M.GetState()
			action = np.argmax(Q[state])  # Exploitation

			M.AddMove(action,player=1,random=False)
			table = M.table
			# DrawTicTacToe(M.table)
			w = M.CheckIfWinner()
			sleep(1.25)
			if w == True:
				break

			if len(M.GetIndexFree()) != 0:
				M.AddMove(player=2,random=True)
				table = M.table
				# DrawTicTacToe(M.table)
				w = M.CheckIfWinner()
				sleep(1.25)
				if w == False:
					M 					= Matrix()		   	   # TicTacToe table
					M.AddMove(player=2,random=True)
					table = M.table
					# DrawTicTacToe(M.table)


def TestManual(Q):
	global table, posClick
	posClick = None
	thd = th.Thread(target=Render)
	thd.start()
	while True:
		M 					= Matrix()		   	   # TicTacToe table
		table = M.table
		# DrawTicTacToe(M.table)
		# sleep(2)

		# Render()
		while True:
			state  = M.GetState()
			action = np.argmax(Q[state])  # Exploitation

			M.AddMove(action,player=1,random=False)
			table = M.table
			# Render()
			# DrawTicTacToe(M.table)
			w = M.CheckIfWinner()
			sleep(1.25)
			if w == True:
				break

			if len(M.GetIndexFree()) != 0:
				while not posClick:
					pass
				M.AddMove(posClick,player=2,random=False)
				# Render()
				table = M.table
				# DrawTicTacToe(M.table)
				w = M.CheckIfWinner()
				sleep(1.25)
				if w == False:
					M 					= Matrix()		   	   # TicTacToe table
					table = M.table
					while not posClick:
						pass
					M.AddMove(posClick,player=2,random=False)
					# M.AddMove(int(input("> Action:")),player=2,random=False)
					# Render()
					table = M.table
					# DrawTicTacToe(M.table)
					sleep(1.25)
				elif len(M.GetIndexFree()) == 0:
					break
			else:
				break


def main():
	global table, posClick, vict, epsilon, deft, epochAct
	Q 					= {}				   # Q-Table 
	M 					= Matrix()		   	   # TicTacToe table

	epsilon 			= 50
	epoch 				= 500000
	decrementEpsilon 	= epsilon/epoch
	gamma 				= 0.2
	alpha 				= 0.1
	epochAct = vict = deft = 0
	# posClick = None
	thd = th.Thread(target=Render)
	thd.start()
	sleep(2)
	# while epsilon > 0:
	turn = 1
	for c in tqdm(range(epoch)):
		epochAct = c
		done 			= False
		turn = 0 if turn == 1 else 1
		# print(epsilon)
		# table = M.table
		# sleep(1)
		M = Matrix()
		if turn:
			M.AddMove(player=2,random=True)
		while not done:
			state = M.GetState()
			table = M.table
			# sleep(0.25)
			# sleep(1)
			# print(str([state[-2],state[-5],state[-8]]))
			if state not in Q:
				Q[state] = [0,0,0,0,0,0,0,0,0]
			
			if randint(0,100) < epsilon:
				action = RandomAction()            # Exploration
			else:
				action = np.argmax(Q[state])  # Exploitation

			M, next_state, done, reward = Step(M, action)
			table = M.table
			# sleep(0.25)
			# sleep(1)
			# if str([int(state[-2]),int(state[-5]),int(state[-8])]) == '[1, 1, 1]':
				# print(done)
			# if(done):
				# M = Matrix()
				# table = M.table
				# sleep(1)
			# elif len(M.GetIndexFree()) != 0:
				# M.AddMove(player=2,random=True)
				# if M.CheckIfWinner == False:
					# reward = -20
				# M_copy = M
				# M_copy.AddMove(player=2,random=True)
				# if M_copy.CheckIfWinner() == False:
					# print(1)
					# reward = -500
			if done:
				if M.CheckIfWinner() == True:
					vict += 1
				# pass
				# M = Matrix()

			elif len(M.GetIndexFree()) != 0:
				M.AddMove(player=2,random=True)
				table = M.table
				# sleep(0.25)
				if M.CheckIfWinner() == False:
					deft += 1
					# M = Matrix()
					# M.AddMove(player=2,random=True)
					reward = -20
				if len(M.GetIndexFree()) == 0:
					done = True

			if next_state not in Q:
				Q[next_state] = [0,0,0,0,0,0,0,0,0]
			
			s, a, ns = state, action, next_state
			


			# update qtable value with Bellman equation
			# qtable[state][action] = reward + gamma * max(qtable[next_state])


			# old_value = Q[s][a]
			next_max = np.max(Q[ns])
			# new_value = old_value + alpha * (reward + gamma * next_max - old_value)
			new_value = reward + gamma * next_max
			Q[s][a] = new_value


			# if len(M.GetIndexFree()) == 0:
				# M.AddMove(player=2,random=True)
			# else:
				# M = Matrix()		   	   # TicTacToe table
				# M.AddMove(player=2,random=True)
				# table = M.table
				# sleep(1)
				# break
				# epsilon = 0

		epsilon -= decrementEpsilon
	# c = 0
	# for k in Q.keys():
		# print(k,' > ',Q[k])
		# c += 1
	# print(c)
	# Test(Q)
	TestManual(Q)



if __name__ == '__main__':
  main()