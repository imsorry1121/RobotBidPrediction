require(randomForest)
set.seed(1)
bid.train = read.csv("../result/featureTrain2015615_1548.csv")
bid.test = read.csv("../result/featureTest2015615_1548.csv")
bid.test.ans = read.csv("../result/test.csv")

bid.train$outcome = as.factor(bid.train$outcome)
bid.test$outcome = NULL
f = outcome~.
rf = lapply(1:5, function(j) randomForest(f, bid.train, ntree = 140, mtry = 9))
model = do.call(combine, rf)
pred = predict(model, bid.test, type='prob')
bid.test.ans$prediction = pred[,2]
write.csv(bid.test.ans[,-c(2,3)], paste("../result/", format(Sys.time(), "%Y.%m.%d.%H.%M.%S"), ".predict.csv", sep=""), row.names=F)

