require(e1071)
require(randomForest)
require(C50)
require(nnet)

set.seed(1)
bid.train = read.csv("../result/featureTrain.csv", header = F)
bid.test = read.csv("../result/featureTest.csv", header = F)
bid.train.ans = read.csv("../result/train.csv")
bid.test.ans = read.csv("../result/test.csv")


names(bid.train) = names(bid.test) = c('id', 'bidNum', 'auctionNum', 'bidNumPerAuction', 'bidNumPerAuctionEntropy', 'bidPropPerAuction', 'bidOverlapNum', 'bidOverlapNormNum', 'bidOverlapPerAuction', 'bidOverlapPerAuctionNorm', 'countryNum', 'countryNumEntropy', 'deviceNum', 'deviceNumEntropy', 'ipNum', 'ipShared')
bid.train$outcome = as.factor(bid.train.ans$outcome)
#bid.test$outcome = bid.test.ans$outcome
bid.train$id = bid.test$id = NULL
f = outcome~.
rf = lapply(1:10, function(j) randomForest(f, bid.train, ntree = 130, mtry = 3))
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
