import numpy as np
from chess import *
import pickle

with open('KQK.pkl','rb') as file:
	KQK=pickle.load(file)
qcapts=mates=stmates=0
for wk in sqrs:
	for bk in sqrs:
		for wq in sqrs:
			if KQK[1][wk][bk][wq]==-1000:
				if isKMove(bk,wq) and not isKMove(wk,wq):
					KQK[1,wk,bk,wq]=0;qcapts+=1
				else:
					hasMove=False
					for s in kMoves(bk):
						if KQK[0][wk][s][wq]==-1000:
							hasMove=True;break
					if not hasMove:
						if KQK[0][wk][bk][wq]==-1000:
							KQK[1][wk][bk][wq]=0;stmates+=1
						else:
							KQK[1][wk][bk][wq]=-500;mates+=1
print(f"qcapts: {qcapts}, stmates: {stmates}, mates: {mates}")
with open('KQK.pkl','wb') as file:
	pickle.dump(KQK,file)
