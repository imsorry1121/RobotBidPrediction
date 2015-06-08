from math import log
def entropy(ps):
	s = sum(ps)
	if s!=1:
		for i in range(len(ps)):
			ps[i] = float(ps[i])/s
	result = float()
	for p in ps:
		result = result + p*log(p)
	return -result/log(len(ps))

def overlap(target, l):
	count = 0
	for i in range(len(l-1)):
		if target==l[i] && target==l[i+1]:
			count = count+1
	return count

if __name__ == "__main__":
	ratios = [0.2,0.1,0.1,0.4,0.2]
	ratios2 = [0.3,0.3,0.3]
	print(entropy(ratios))
	print(entropy(ratios2))