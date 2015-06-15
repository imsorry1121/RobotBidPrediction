import numpy as np
from datetime import datetime as dt
from time import time
from sklearn.metrics import roc_auc_score
import networkx as nx
import feature as ft
import csv
from math import floor
# 2015.6.9 coded by Ken
day_duration = 4547368124071.8799
time_start = 9631916820392676.0 

def main(testingFile = "../result/featureTest", trainingFile= "../result/featureTrain"):
	s = time()
	print("main")
	biddersTrain, biddersTest, bidders, auctions, ipBidderList, g = createGraph()
	m = time()
	print(m-s)
	testing = getInstances(g, biddersTest, ipBidderList)
	training = getInstances(g, biddersTrain, ipBidderList)

	print(time()-m)
	date = dt.now()
	timeStr = str(date.year)+str(date.month)+str(date.day)+'_'+str(date.hour)+str(date.minute)
	testingFile = testingFile+timeStr+'.csv'
	trainingFile = trainingFile+timeStr+'.csv'
	writeRow(testing, testingFile)
	writeRow(training, trainingFile)



# evaluation
# predictFile and gtFile need the same amount of rows
def evaluate(predictFile="../data/train.csv", gtFile="../data/train.csv", outputFile='../result/score.csv'):
	preds = list()
	gts = list()
	with open(predictFile, 'r') as fi:
		fi.readline()
		for line in fi:
			# print(line.strip().split(',')[1])
			pred = float(line.strip().split(',')[-1])
			preds.append(pred)
	with open(gtFile, 'r') as fi:
		fi.readline()
		for line in fi:
			gt = int(float(line.strip().split(',')[-1]))
			gts.append(gt)
	score = roc_auc_score(gts, preds)
	print("AUC:"+str(score))
	with open(outputFile, 'a') as fo:
		# outputStr = str(time())+": "+str(score)+'\n'
		outputStr = str(dt.now())+": "+str(score)+'\n'
		fo.write(outputStr)
	return score

def createGraph(bidderFile="../data/train.csv", bidderFile2="../data/test.csv", bidFile="../data/bids.csv"):
	s= time()
	g = nx.Graph()
	biddersTrain = initNode(g, bidderFile)
	biddersTest = initNode(g, bidderFile2)
	auctions = initEdge(g, bidFile)
	bidders = biddersTrain+biddersTest
	print("Init Graph Over:"+str(time()-s))
	updateAuction(g, auctions)
	updateBidder(g, bidders)
	ipBidderList = updateIpBidderList(g, bidders)
	print(g.node["ewmzr"])
	print(g.node["8dac2b259fd1c6d1120e519fb1ac14fbqvax8"])
	print("Update Graph Over:"+str(time()-s))
	return biddersTrain, biddersTest, bidders, auctions, ipBidderList, g

	# print(g.nodes())


def initNode(g, bidderFile):
	titles = list()
	bidders = list()
	with open(bidderFile, 'r') as fi:
		titles = fi.readline().strip().split(',')
		if len(titles)==4:
			for line in fi:
				# attrs = {"type": "bidder"}
				data = line.strip().split(',')
				bidder = data[0]
				outcome = data[-1]
				bidders.append(bidder)
				hourList = [0]*24
				g.add_node(bidder, type="bidder", outcome=outcome,ipDistri=dict(),hourList=hourList, auctionDistri=dict(), auctionRatios=dict(), deviceDistri=dict(), countryDistri=dict(), avgBidNum=0)
				for i in range(1,len(data)):
					g.node[bidder][titles[i]] = data[i]
		else:
			for line in fi:
				# attrs = {"type": "bidder"}
				data = line.strip().split(',')
				bidder = data[0]
				outcome = 0
				bidders.append(bidder)
				hourList = [0]*24
				g.add_node(bidder, type="bidder", outcome=outcome, ipDistri=dict(),hourList=hourList, auctionDistri=dict(), auctionRatios=dict(), deviceDistri=dict(), countryDistri=dict(), avgBidNum=0)
				for i in range(1,len(data)):
					g.node[bidder][titles[i]] = data[i]

	return bidders

def initEdge(g, bidFile):
	auctions = list()
	with open(bidFile, 'r') as fi:
		titles = fi.readline().strip().split(',')
		for line in fi:
			data = line.strip().split(',')
			bid = data[0]
			print(bid)
			bidder=data[1]
			auction=data[2]
			merchandise = data[3]
			device = data[4]
			time = float(data[5])
			day = (time-time_start)/day_duration
			hour = floor((day-floor(day))*24)
			# time in day unit
			country = data[6]
			ip = data[7]
			url = data[8]
			bidAttrs = {"device":device, "day":day, 'hour': hour, "country":country, "ip":ip, "url":url}
			# revise bidder information
			# ips = g.node[bidder]["ips"]
			countryDistri = g.node[bidder]["countryDistri"]
			deviceDistri = g.node[bidder]["deviceDistri"]
			ipDistri = g.node[bidder]['ipDistri']
			hourList = g.node[bidder]['hourList']
			# if ip not in ips:
			# 	ips.append(ip)
			# 	g.node[bidder]["ips"] = ips
			hourList[hour] = hourList[hour]+1
			ipDistri[ip] = ipDistri.get(ip, 0)+1
			countryDistri[country] = countryDistri.get(country,0)+1
			deviceDistri[device] = deviceDistri.get(device, 0)+1
			g.node[bidder]['hourList'] = hourList
			g.node[bidder]['ipDistri'] = ipDistri
			g.node[bidder]["countryDistri"] = countryDistri
			g.node[bidder]["deviceDistri"] = deviceDistri
			# add auction
			if g.has_node(auction):
				bidders = g.node[auction]["bidders"]
				bidders.append(bidder)
				g.node[auction]["bidders"] = bidders		
			else:
				g.add_node(auction, type="auction",merchandise=merchandise, bidders=[bidder])
			# bidders = 
			auctions.append(auction)
			# add and revise edge information
			if g.has_edge(auction, bidder):
				num = g.edge[auction][bidder]["num"]+1
				bids = g.edge[auction][bidder]["bids"]
				bids[bid] = bidAttrs
			else:
				num = 1
				bids = {bid:bidAttrs}
			g.add_edge(auction, bidder, num=num, bids=bids)
	return auctions

# bidderDistri: auction bid distribution of bidder, sum =1
def updateAuction(g, auctions):
	# update bidders inform
	for auction in auctions:
		edges = g.edge[auction]
		total = float()
		bidderBidRatio = dict()
		nums = list()
		bidders = list()
		attrs = g.node[auction]
		for (b, attr) in edges.items():
			num = attr["num"]
			total = total + num
			bidders.append(b)
			nums.append(num)
		for i in range(len(bidders)):
			bidderBidRatio[bidders[i]] = nums[i]/total
		attrs["bidderDistri"] = bidderBidRatio
		# g.add_node(auction, )
		g.add_node(auction, attrs)



# auctionRatio: bidder bid ratio in that auction, sum != 1
# auctionDistri: bidder bid distribution of bidding auctions, sum = total bids
# avgBidNum: bidder average number of bid
def updateBidder(g, bidders):
	for bidder in bidders:
		edges = g.edge[bidder]
		if len(edges)==0:
			continue
		auctionRatios = dict()
		auctionDistri = dict()
		total = int()
		# update ratio from auctions
		for (auction, attr) in edges.items():
			auctionRatios[auction] = g.node[auction]["bidderDistri"][bidder]
			num = attr["num"]
			total = total + num
			auctionDistri[auction] = num
		# update distribution 
		# for auction in edges.keys():
		# 	auctionDistri[auction] = auctionDistri[auction]/total
		g.node[bidder]["auctionDistri"] = auctionDistri
		g.node[bidder]["auctionRatios"] =  auctionRatios
		g.node[bidder]["avgBidNum"] = total/len(edges)


def updateIpBidderList(g, bidders):
	ipBidderList = dict()
	for bidder in bidders:
		ips = list(g.node[bidder]["ipDistri"].keys())
		for ip in ips:
			bidders = ipBidderList.get(ip, list())
			bidders.append(bidder)
			ipBidderList[ip] = bidders
	return ipBidderList

def getInstances(g, bidders, ipDistri):
	print('Get instances')
	instances= list()
	for bidder in bidders:
		features = ft.feature_extract(g, bidder, ipDistri)
		outcome = g.node[bidder]['outcome']
		instance = [outcome] + features
		instances.append(instance)
	return instances



def getFeatures(g, bidders, ipDistri, outcomes):
	print("get feature")
	rows = list()
	for bidder in bidders:
		# print(bidder)
		# print(ft.feature_extract(g, bidder, ipDistri))
		row = [bidder] + ft.feature_extract(g, bidder, ipDistri)
		rows.append(row)
	return rows

def writeRow(rows, outputFile):
	titles = ["outcome","bid_total","auction_total", \
	"bid_per_auction_mean","bid_per_auction_max","bid_per_auction_min","bid_per_auction_std","bid_per_auction_entropy" \
	"bidder_ratio_per_auction_mean","bidder_ratio_per_auction_max","bidder_ratio_per_auction_min","bidder_ratio_per_auction_std","bidder_ratio_per_auction_entropy" \
	"bid_override_num","bid_override_norm_num","bid_override_in_auction","bid_override_norm_num_in_auction","bid_override_by_total_bid_override_mean","bid_override_by_total_bid_override_max","bid_override_by_total_bid_override_min","bid_override_by_total_bid_override_std","bid_override_by_total_bid_override_entropy" \
	"country_per_bidder","country_per_bidder_entropy","country_per_auction_entropy_mean","country_per_auction_entropy_max","country_per_auction_entropy_min","country_per_auction_entropy_std", "country_per_auction_entropy_entropy" \
	"device_per_bidder","device_per_bidder_entropy","device_per_auction_entropy_mean","device_per_auction_entropy_max","device_per_auction_entropy_min","device_per_auction_entropy_std", "device_per_auction_entropy_entropy"
	"ip_per_bidder","ip_per_bidder_entropy","ip_share_num","ip_per_auction_entropy_mean","ip_per_auction_entropy_max","ip_per_auction_entropy_min","ip_per_auction_entropy_std","ip_per_auction_entropy_std"\
	]
	with open(outputFile, 'w', newline="") as fo:
		writer =csv.writer(fo)
		writer.writerow(titles)
		for row in rows:
			# print(row)
			writer.writerow(row)


if __name__ == "__main__":
	main()
	# createGraph()
	# evaluate()