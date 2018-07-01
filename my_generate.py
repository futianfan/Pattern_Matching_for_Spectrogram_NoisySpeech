
a = [0, [[1],2,3],[4,[5,6]],7]
#a = [0,1,2,3]


def flatten_append(lst):
	results = []
	if isinstance(lst,int):
		results.append(lst)
		return results
	for sublst in lst:
		results.extend(flatten_append(sublst))
	return results
	
r = flatten_append(a)
print(r)

def flatten_append(lst):
	results = []
	try:
		lst + 1
	except TypeError:
		for sublst in lst:
			results.extend(flatten_append(sublst))
	else:
		results.append(lst)
	return results

r = flatten_append(a)
print(r)


def ccount(n):
	for i in range(n):
		yield i
print(list(ccount(10)))



########################  right generator code  ########################

def flatten(lst):
	#print('call')
	if isinstance(lst,int):
		yield lst
	else:
		for sublst in lst:
			### ************* ####
			b = flatten(sublst)   
			for j in b:
				yield j
			### **** ####
for j in flatten(a):
	print(j)  ### wrong


########################  right generator code  ########################

########################################################################################################################################################################
########################################################################################################################################################################

########################  wrong generator code  ########################

def flatten(lst):
	if isinstance(lst,int):
		yield lst
	else:
		for sublst in lst:
			### **** ####
			flatten(sublst)
			### **** ####
for j in flatten(a):
	print(j)  ### wrong

########################  wrong generator code  ########################


########################  right generator code using try,except,else ########################
def flatten_try_except(lst):
	try: 
		lst + 1
	except TypeError: 
		for sublst in lst:
			b = flatten_try_except(sublst)
			for j in b:
				yield j
	else: 
		yield lst

for j in flatten_try_except(a):
	print(j)
print(list(flatten_try_except(a)))

########################  right generator code  try,except,else ########################





