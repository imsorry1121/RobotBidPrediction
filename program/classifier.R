require(e1071)
require(randomForest)
require(C50)
require(nnet)
require(adabag)

set.seed(1)
bid.train = read.csv("../result/featureTrain2015615_1548.csv")
bid.test = read.csv("../result/featureTest2015615_1548.csv")
bid.test.ans = read.csv("../result/test.csv")

bid.train$outcome = as.factor(bid.train$outcome)
bid.test$outcome = NULL
f = outcome~.
#rf = lapply(1:10, function(j) randomForest(f, bid.train, ntree = 50))
#model = do.call(combine, rf)
#v = varImp(model)
#v = cbind(rownames(v), v)
#vnames = v[order(-v[,2]),1]
#topV = vnames[1:80]
#f = as.formula(paste("outcome", paste(topV, collapse=" + "), sep = " ~ "))
rf = lapply(1:10, function(j) randomForest(f, bid.train, ntree = 500))
model = do.call(combine, rf)
pred = predict(model, bid.test, type='prob')
bid.test.ans$prediction = pred[,2]
write.csv(bid.test.ans[,-c(2,3)], 'tempResult.csv', row.names=F)

#bid.tune = tune(svm, f, data = bid.train, kernel = 'radial', range = list(cost = 10^(-2:2), gamma = 10^(-2:2)))
#bid.svm = svm(f, bid.train, type = 'C-classification', probability = T, kernel = 'radial', cost = 100, gamma = 0.01)
#pred = data.frame(attr(predict(bid.svm, bid.test, probability = T), "prob"))
#bid.test.ans$prediction = pred[,2]
#bid.test.ans = bid.test.ans[,-c(2,3)]
#write.csv(bid.test.ans, "tempResult.csv", row.names = F)
