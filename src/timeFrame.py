from recognition import getFrame
from time import time

t0 = time()
getFrame()
t1 = time()
print 'function vers1 takes %f' %(t1-t0)
