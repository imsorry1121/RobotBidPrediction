require(e1071)
require(randomForest)
require(C50)
require(nnet)
require(pROC)
set.seed(1)

bid.train = read.csv("../result/featureTrain2015615_1548.csv")
bid.test = read.csv("../result/featureTest2015615_1548.csv")
bid.test.ans = read.csv("../result/test.csv")
bid.train$outcome = as.factor(bid.train$outcome)

bid.test$outcome = NULL
f = outcome~.
k = 10
tp = 1/k
n.grid = seq(140, 160, 10)
t.grid = seq(7, 11, by = 1)
adata = bid.train
bid.k = split(adata, f = rep_len(1:k, nrow(adata)))
p = data.frame()
for (n in n.grid)
{	for (t in t.grid)
	{	print(c(n, t))
		pp = data.frame()
		for (i in 1:k)
		{	set.seed(1)
			atrain = do.call(rbind, bid.k[setdiff(1:k, i)])
			atestx = subset(bid.k[[i]], select = -outcome)
			atesty = bid.k[[i]]$outcome
			model = do.call(combine, lapply(1:10, function(j) randomForest(f, atrain, ntree = n, mtry = t)))
			pred = predict(model, atestx, type='prob')
			p.auc = auc(atesty, pred[,2])
			pp = rbind(pp, p.auc)
		}
		p = rbind(p, c(n, t, mean(pp[,1])))
	}
}
names(p) = c("ntree", "mtry", "meanAUC") 
print(p[p[,3]==max(p[,3]),])
