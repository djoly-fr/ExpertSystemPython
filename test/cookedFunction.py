#cooking function
#http://pyke.sourceforge.net/about_pyke/cooking_functions.html


from functools import partial

def foo(cooked, standard):
    print "foo called with cooked: %s, standard: %s" % (cooked, standard)
#print "My name is %s and weight is %d kg!" % ('Zara', 21)

foo('a', 'b')

# i cook
cooked1 = partial(foo, 'cooked_value1')
cooked1('value2')

# cook function call graph   le premier param est une fonction
def bar (child_fun, a):
    print "bar called with:", a
    return child_fun(a)

bar_float = partial(bar, float)
print bar_float('123')

bar_min = partial(bar, min)
print bar_min((3,2,5))

bar_cooked1 = partial(bar, cooked1)
bar_cooked1('abc')

bar_bar_min = partial(bar, bar_min)
bar_bar_min((3,2,5))