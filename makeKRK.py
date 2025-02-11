import numpy as np
from chess import *
import pickle

krkbtm=krkwtm=0
KRK=np.empty((2,64,64,64),dtype='int16')
KRK.fill(-2000)
for wk in sqrs:
	for bk in sqrs:
		if (wk!=bk) and not isKMove(wk,bk):
			for wr in sqrs:
				if wr not in (wk,bk):
					KRK[1,wk,bk,wr]=-1000;krkbtm+=1
					if bk not in rMoves(wr,wk):
						KRK[0,wk,bk,wr]=-1000;krkwtm+=1
print(krkbtm)
print(krkwtm)
with open('KRK.pkl','wb') as file:
	pickle.dump(KRK,file)
