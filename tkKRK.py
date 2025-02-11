import tkinter as tk
import asyncio
from async_tkinter_loop import async_handler,async_mainloop
from tkinter import messagebox,simpledialog
import numpy as np
import pickle
from chess import *

with open('KRK.pkl','rb') as file:
	KRK=pickle.load(file)
board=np.empty((8,8),dtype='object')
col=None;wk=None;bk=None;wr=None;newPos=True
root=tk.Tk()
root.title("Board")
root.geometry('560x630')
for r in range(len(board)):
	root.rowconfigure(r,minsize=70,weight=1)
root.rowconfigure(8,minsize=70,weight=1)
for f in range(len(board[r])):
	root.columnconfigure(f,minsize=70,weight=1)
for r in range(len(board)):
	for f in range(len(board[r])):
		cell=tk.Label(root,bg=('goldenrod','dark blue')[(r+f)%2],\
			width=70,height=70)
		cell.grid(row=r,column=f,sticky='nsew')
		cell.config(font=('Arial',48,'bold'))
		board[r,f]=cell
txtLabel=tk.Label(root,bg='white',fg='black',height=40,text='')
txtLabel.grid(row=8,column=1,columnspan=7,sticky='nsew')
def highlightMovePossible(s:int):
	board[7-s//8,s%8].config(highlightbackground='white',\
	highlightcolor='white',highlightthickness=5)
	board[7-s//8,s%8].bind('<Button-1>',selectSqrToMove)
def selectSqrToMove(event):
	global col,wk,bk,wr
	for r in range(len(board)):
		for f in range(len(board[r])):
			board[r,f].unbind('<Button-1>')
			board[r,f].config(highlightthickness=0,bg=('goldenrod',\
			'darkblue')[(r+f)%2])
	global sqrMoved
	sqrMoved=(7-event.widget.grid_info()['row'])*8 + \
		event.widget.grid_info()['column']
	board[7-sqrMoved//8,sqrMoved%8].config(text=\
		board[7-pceMoved//8,pceMoved%8]['text'])
	board[7-pceMoved//8,pceMoved%8].config(text='')
	if sqrMoved==wr:
		wr=-1
		txtLabel.config(text='DRAW')
	if pceMoved==wk:
		wk=sqrMoved
	elif pceMoved==bk:
		bk=sqrMoved
		messagebox.showinfo('',f'bk={bk}')
	else:
		wr=sqrMoved
	if txtLabel['text']!='DRAW':
		col=0 if col else 1
		global newPos
		newPos=True
def selectPieceMoved(event):
	for r in range(len(board)):
		for f in range(len(board[r])):
			board[r,f].config(bg=('goldenrod','darkblue')[(r+f)%2],\
			highlightthickness=0)
	event.widget.config(bg='lightgreen')
	global pceMoved
	pceMoved=(7-event.widget.grid_info()['row'])*8+\
		event.widget.grid_info()['column']
	if pceMoved==wk:
		for s in kMoves(wk):
			if KRK[1,s,bk,wr]>-2000:
				highlightMovePossible(s)
	elif pceMoved==wr:
		for s in rMoves(wr,wk):
			if KRK[1,wk,bk,s]>-2000:
				highlightMovePossible(s)
	elif pceMoved==bk:
		if isKMove(bk,wr) and not isKMove(wk,wr):
			highlightMovePossible(wr)
		for s in kMoves(bk):
			if KRK[0,wk,s,wr]>-2000:
				highlightMovePossible(s)
async def get_newPos():
	global newPos
	while not newPos:
		await asyncio.sleep(1)
	newPos=False
async def my_routine():
	global col, wk, bk, wr, newPos
	newPos=True
	while True:
		await get_newPos()
		while col not in (0,1):
			col=simpledialog.askstring("Color to move",'Which color is to move?')
			col='WB'.index(col.upper())
		while wk not in sqrs:
			wk=simpledialog.askinteger("WK",'What square has wk?')
		board[7-wk//8,wk%8].config(text='K',fg='white')
		while bk not in sqrs:
			bk=simpledialog.askinteger("BK",'What square has bk?')
		board[7-bk//8,bk%8].config(text='K',fg='black')
		while wr not in sqrs:
			wr=simpledialog.askinteger("WR",'What square has wr?')
		board[7-wr//8,wr%8].config(text='R',fg='white')
		txtLabel.config(font=('Arial',10),text=str(KRK[col,wk,bk,wr])+': ',\
			wraplength=500,justify='center')
		if col:
			for s in kMoves(bk):
				if (wr==s) and not isKMove(wk,s):
					txtLabel.config(text=txtLabel['text']+'KxR(0) ')
				else:
					scr=KRK[0][wk][s][wr]
					if scr>-2000:
						txtLabel.config(text=txtLabel['text']+f'K{s}({scr}) ')
		else:
			for s in kMoves(wk):
				scr=KRK[1][s][bk][wr]
				if scr>-2000:
					txtLabel.config(text=txtLabel['text']+f'K{s}({scr}) ')
			for s in rMoves(wr,wk):
				scr=KRK[1][wk][bk][s]
				if scr>-2000:
					txtLabel.config(text=txtLabel['text']+f'R{s}({scr}) ')
		pces=[[board[7-wk//8,wk%8],board[7-wr//8,wr%8]],[board[7-bk//8,bk%8]]]
		for pce in pces[col]:
			pce.bind('<Button-1>',selectPieceMoved)
startButton=tk.Button(root,text='Start',command=async_handler(my_routine))
startButton.grid(row=8,column=0,sticky='nsew')
async_mainloop(root)
