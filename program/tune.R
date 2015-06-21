require(randomForest)
require(ROCR)
set.seed(1)

bid.train = read.csv("../result/featureTrain2015615_1548.csv")
bid.test = read.csv("../result/featureTest2015615_1548.csv")
bid.test.ans = read.csv("../result/test.csv")
bid.train$outcome = as.factor(bid.train$outcome)

bid.test$outcome = NULL
f = outcome~.
k = 10
tp = 1/k
n.grid = seq(140, 160, by = 10)
t.grid = seq(5, 9, by = 1)
f.grid = seq(5, 9, by = 1)
adata = bid.train
bid.k = split(adata, f = rep_len(1:k, nrow(adata)))
p = data.frame()
for (n in n.grid)
{	for (t in t.grid)
	{	for (fo in f.grid)
		{	print(c(n, t, fo))
			pp = data.frame()
			for (i in 1:k)
			{	set.seed(1)
				atrain = do.call(rbind, bid.k[setdiff(1:k, i)])
				atestx = subset(bid.k[[i]], select = -outcome)
				atesty = bid.k[[i]]$outcome
				model = do.call(combine, lapply(1:fo, function(j) randomForest(f, atrain, ntree = n, mtry = t)))
				pred = predict(model, atestx, type='prob')
				p.auc = auc(atesty, pred[,2])
				pp = rbind(pp, p.auc)
			}
			p = rbind(p, c(n, t, fo, mean(pp[,1])))
		}
	}
}

names(p) = c("ntree", "mtry", "forests", "meanAUC") 
print(p[p[,4]==max(p[,4]),])
plot(performance(prediction(pred[,2], atesty), 'tpr', 'fpr'))
