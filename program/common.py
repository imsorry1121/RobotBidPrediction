from math import log
# ps is a list
def entropy(ps):
	l = len(ps)
	s = sum(ps)
	result = float()
	if l == 0:
		return 0
	elif l==1:
		return 1
	else:
		if s!=1:
			for i in range(len(ps)):
				ps[i] = float(ps[i])/s
		result = float()
		for p in ps:
			result = result + p*log(p)
		return -result/log(l)

def overlap(target, l):
	count = 0
	for i in range(len(l)-1):
		if target==l[i] and target==l[i+1]:
			count = count+1
	return count

def multiprocess():
	s = time()
	nprocs = 8
	procList = list()
	q = mp.Queue()
	result = list()
	for i in range(nprocs):
		p = mp.Process(target=f, args=([3], q))
		p.start()
		procList.append(p)
	for i in range(nprocs):
		result += q.get()
	for p in procList:
		p.join()
	e = time()
	print (result)
	print (e-s)


def f(num, q):
	q.put(num)

if __name__ == "__main__":
	ratios = [0.2,0.1,0.1,0.4,0.2]
	ratios2 = [0.3,0.3,0.3]
	print(entropy(ratios))
	print(entropy(ratios2))