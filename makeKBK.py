import numpy as np
from chess import *
import pickle

kbkbtm=kbkwtm=0
KBK=np.empty((2,64,64,64),dtype='int16')
KBK.fill(-2000)
for wk in sqrs:
	for bk in sqrs:
		if (wk!=bk) and not isKMove(wk,bk):
			for wb in sqrs:
				if wb not in (wk,bk):
					KBK[1,wk,bk,wb]=0;kbkbtm+=1
					if bk not in bMoves(wb,wk):
						KBK[0,wk,bk,wb]=0;kbkwtm+=1
print(kbkbtm)
print(kbkwtm)
with open('KBK.pkl','wb') as file:
	pickle.dump(KBK,file)
