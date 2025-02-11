import numpy as np
from chess import *
import pickle

with open('KQK.pkl','rb') as file:
	KQK=pickle.load(file)
curloss=-500
while True:
	wins=0
	nullct=len([wq for col in KQK for wk in col for bk in wk for wq in bk \
	if wq==-1000])
	if not nullct:
		break
	for wk in sqrs:
		for bk in sqrs:
			for wq in sqrs:
				if KQK[1][wk][bk][wq]==curloss:
					for s in kMoves(wk):
						if KQK[0][s][bk][wq]==-1000:
							KQK[0][s][bk][wq]=-curloss
					for s in qMoves(wq,wk,bk):
						if KQK[0][wk][bk][s]==-1000:
							KQK[0][wk][bk][s]=-curloss
	for wk in KQK[0]:
		for bk in wk:
			for wq in bk:
				if wq==-curloss:
					wins+=1
	print(f"{wins} wins of {-curloss}")
	losses=0
	for wk in sqrs:
		for bk in sqrs:
			for wq in sqrs:
				if KQK[0][wk][bk][wq]==-curloss:
					for s in kMoves(bk):
						if KQK[1][wk][s][wq]==-1000:
							hasMove=False
							for s1 in kMoves(s):
								if KQK[0][wk][s1][wq]==-1000:
									hasMove=True;break
							if not hasMove:
								KQK[1][wk][s][wq]=curloss+1
	for wk in KQK[1]:
		for bk in wk:
			for wq in bk:
				if wq==curloss+1:
					losses+=1
	print(f"{losses} losses of {curloss+1}")
	curloss+=1
with open('KQK.pkl','wb') as file:
	pickle.dump(KQK,file)
