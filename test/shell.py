# pyke test
# http://pyke.sourceforge.net/using_pyke/index.html
from pyke import knowledge_engine

my_engine = knowledge_engine.engine(__file__)
my_engine.activate('bc_related')