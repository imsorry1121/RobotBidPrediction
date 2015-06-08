import numpy as np
from sklearn.metrics import roc_auc_score

def main():
	y_true = np.array([0,0,1,1])
	y_pred = np.array([0,0,0,0])
	score = roc_auc_score(y_true, y_pred)
	print (score)

if __name__ =="__main__":
	main()
