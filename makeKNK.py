import numpy as np
from chess import *
import pickle

knkbtm=knkwtm=0
KNK=np.empty((2,64,64,64),dtype='int16')
KNK.fill(-2000)
for wk in sqrs:
	for bk in sqrs:
		if (wk!=bk) and not isKMove(wk,bk):
			for wn in sqrs:
				if wn not in (wk,bk):
					KNK[1,wk,bk,wn]=0;knkbtm+=1
					if bk not in nMoves(wn):
						KNK[0,wk,bk,wn]=0;knkwtm+=1
print(knkbtm)
print(knkwtm)
with open('KNK.pkl','wb') as file:
	pickle.dump(KNK,file)
