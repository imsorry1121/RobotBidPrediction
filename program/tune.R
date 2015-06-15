require(e1071)
require(randomForest)
require(C50)
require(nnet)

set.seed(1)

bid.train = read.csv("../result/featureTrain2015615_1548.csv")
bid.test = read.csv("../result/featureTest2015615_1548.csv")
bid.test.ans = read.csv("../result/test.csv")
bid.train$outcome = as.factor(bid.train$outcome)

bid.test$outcome = NULL
f = outcome~.
k = 10
tp = 1/k
n.grid = seq(50, 150, 25)
t.grid = seq(5, 15, by = 2)
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
			model = do.call(combine, lapply(1:t, function(j) randomForest(f, atrain, ntree = n)))
			predO = predict(model, atestx, type='prob')
			pred = rep(0, length(predO[,2]))
			pred[predO[,2] > 0.5] = 1
			oct = table(pred, atesty)
			precision = oct[2,2]/(oct[2,1]+oct[2,2])
			acc = (oct[1,1]+oct[2,2])/sum(oct)
			pp = rbind(pp, c(precision, acc))
		}
		p = rbind(p, c(n, t, mean(pp[,1]), mean(pp[,2])))
	}
}
names(p) = c("ntree", "mtry", "meanPrecision", "meanAccuracy") 
print(p[p[,4]==max(p[,4]),])
