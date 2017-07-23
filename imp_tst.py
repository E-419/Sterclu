import os

#from src.Node import *
#from src.CDS import *
from src.CDS import CDS
#from src.JBNode import *

from tst_imp import n3
n = n3()
n.p()

from imp_tst2 import n1, n2

n = n3()
n.p()


t = CDS.build(os.path.join(os.getcwd(), 'appdata', 'Root.cds'))