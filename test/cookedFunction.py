#cooking function

from functools import partial

def foo(cooked, standard):
    print "foo called with cooked: %s, standard: %s" % (cooked, standard)
#print "My name is %s and weight is %d kg!" % ('Zara', 21)

foo('a', 'b')

# i cook
cooked1 = partial(foo, 'cooked_value1')
cooked1('value2')