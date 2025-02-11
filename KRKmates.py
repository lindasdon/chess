import numpy as np
from chess import *
import pickle

with open('KRK.pkl','rb') as file:
	KRK=pickle.load(file)
rcapts=mates=stmates=0
for wk in sqrs:
	for bk in sqrs:
		for wr in sqrs:
			if KRK[1][wk][bk][wr]==-1000:
				if isKMove(bk,wr) and not isKMove(wk,wr):
					KRK[1,wk,bk,wr]=0;rcapts+=1
				else:
					hasMove=False
					for s in kMoves(bk):
						if KRK[0][wk][s][wr]==-1000:
							hasMove=True;break
					if not hasMove:
						if KRK[0][wk][bk][wr]==-1000:
							KRK[1][wk][bk][wr]=0;stmates+=1
						else:
							KRK[1][wk][bk][wr]=-500;mates+=1
print(f"rcapts: {rcapts}, stmates: {stmates}, mates: {mates}")
with open('KRK.pkl','wb') as file:
	pickle.dump(KRK,file)
