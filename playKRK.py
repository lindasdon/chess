import numpy as np
from chess import *
import pickle

with open('KRK.pkl','rb') as file:
	KRK=pickle.load(file)
curloss=-500
while True:
	wins=0
	nullct=len([wr for col in KRK for wk in col for bk in wk for wr in bk \
	if wr==-1000])
	if not nullct:
		break
	for wk in sqrs:
		for bk in sqrs:
			for wr in sqrs:
				if KRK[1][wk][bk][wr]==curloss:
					for s in kMoves(wk):
						if KRK[0][s][bk][wr]==-1000:
							KRK[0][s][bk][wr]=-curloss
					for s in rMoves(wr,wk,bk):
						if KRK[0][wk][bk][s]==-1000:
							KRK[0][wk][bk][s]=-curloss
	for wk in KRK[0]:
		for bk in wk:
			for wr in bk:
				if wr==-curloss:
					wins+=1
	print(f"{wins} wins of {-curloss}")
	losses=0
	for wk in sqrs:
		for bk in sqrs:
			for wr in sqrs:
				if KRK[0][wk][bk][wr]==-curloss:
					for s in kMoves(bk):
						if KRK[1][wk][s][wr]==-1000:
							hasMove=False
							for s1 in kMoves(s):
								if KRK[0][wk][s1][wr]==-1000:
									hasMove=True;break
							if not hasMove:
								KRK[1][wk][s][wr]=curloss+1
	for wk in KRK[1]:
		for bk in wk:
			for wr in bk:
				if wr==curloss+1:
					losses+=1
	print(f"{losses} losses of {curloss+1}")
	curloss+=1
with open('KRK.pkl','wb') as file:
	pickle.dump(KRK,file)
