from time import sleep, ctime

###################### part I ######################

def decorator1(func):
	print('flag ')
	x = 10
	def wrapper():
		print('wrap begin')
		print(func.__name__,ctime())
		func(x)
		print(func.__name__,ctime())
		print('wrap end')
	return wrapper

def decorator2(func):   ### this is wrong 
	print('wrap begin')
	func()
	print('wrap end')
	return func

@decorator1
def foo(x):
	sleep(3)
	print(x**2)


f = foo
#print(ctime())
a = f()
###################### part I ######################
###################### part II ######################

class Coordinate:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __str__(self):
		return "Coordinate: x = " + str(self.x) + ', y = ' + str(self.y)

#def add(a,b):
#	return Coordinate(a.x + b.x , a.y + b.y)

#def sub(a,b):
#	return Coordinate(a.x - b.x , a.y - b.y)


def check_boundary(a):
	return Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)

def decorator3(func):
	def checker(a, b):
		a2 = check_boundary(a)
		b2 = check_boundary(b)
		c = func(a2,b2)
		c = check_boundary(c)
		return c
	return checker

@decorator3 
def add(a,b):
	return Coordinate(a.x + b.x , a.y + b.y)


@decorator3
def sub(a,b):
	return Coordinate(a.x - b.x , a.y - b.y)


one = Coordinate(10,20)
two = Coordinate(30,20)
print(sub(one,two))

###################### part II ######################

###################### part III ######################
from time import ctime, sleep

def decorator4(func):
	def wrapper():
		print(func.__name__, ctime())
		func()
		#return func()   ## ************** ##
	return wrapper

@decorator4
def getInfo():
	return 'haha'

print(getInfo())
###################### part III ######################


###################### part IV ######################
from time import sleep, ctime
def decorator_out(parameter):
	def decorator_inn(func):
		def wrapper(*args, **kwargs):
			print(func.__name__, ctime())
			print(parameter)
			result = func(*args, **kwargs)
			print(ctime())
			return result
		return wrapper
	return decorator_inn

def add(a,b):
	return a + b

@decorator_out('text')
def calculate(*args, **kwargs):
	lst = list(args)
	print('a' in kwargs)
	print(locals())
	return reduce(add, lst)


print(calculate(1,2,3,4, a = 147))

###################### part IV ######################



