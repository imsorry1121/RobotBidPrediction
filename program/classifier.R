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
bid.test.ans$outcome = as.factor(bid.test.ans$outcome)
bid.train$id = bid.test$id = NULL

f = outcome~.

bid.svm = svm(f, bid.train, type = 'C-classification', probability = T, kernel = 'sigmoid')
pred = predict(bid.svm, bid.test)