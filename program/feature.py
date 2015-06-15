import common as cm
import numpy as np
from math import floor
# feature extracion

def feature_extract(g, bidder, ipBidderList):
	features = basic(g,bidder)+bid_per_auction(g, bidder)+bid_override(g, bidder)+bidder_ratio_in_auction(g, bidder)+country(g, bidder)+device(g, bidder)+ip(g, ipBidderList, bidder)+time(g, bidder)
	return features

# categories 
def basic(g, bidder):
	return [bid_total(g,bidder),  auction_total(g, bidder)]

# bid_per_auction mean, max, min, std, entropy
def bid_per_auction(g, bidder):
	values = list(g.node[bidder]['auctionDistri'].values())
	return cm.stats(values)

def bid_override(g, bidder):
	bidOverrideNum = 0
	bidOverrideNormNum = 0
	bidOverrideNumAuction = 0
	bidOverrideNormNumAuction = 0
	bidOverrideRatioDistri = dict()
	edges = g.edges(bidder)
	auctionNum = len(edges)
	if auctionNum ==0:
		return [0]*9
	# print(edges)
	for (b, a) in edges:
		bidderRecord = g.node[a]["bidders"]
		count = cm.overlap(bidder, bidderRecord)
		bidOverrideNum = bidOverrideNum+count
		bidOverrideRatioDistri[a] = count
		if count>0:
			bidOverrideNumAuction = bidOverrideNumAuction+1
	if bidOverrideNum==0:
		return [0]*9
	else:
		for auction in bidOverrideRatioDistri.keys():
			bidOverrideRatioDistri[auction] = bidOverrideRatioDistri[auction]/bidOverrideNum
		bidOverrideNormNum = bidOverrideNum/bid_total(g, bidder)
		bidOverrideNormNumAuction = bidOverrideNumAuction/auctionNum
		return [bidOverrideNum, bidOverrideNormNum, bidOverrideNumAuction, bidOverrideNormNumAuction]+cm.stats(list(bidOverrideRatioDistri.values()))

def bidder_ratio_in_auction(g, bidder):
	ratios = list(g.node[bidder]['auctionRatios'].values())
	return cm.stats(ratios)

def country(g, bidder):
	# country per bidder
	featureBidder = country_per_bidder(g, bidder)
	# country per auction
	featureAuction = country_per_auction(g, bidder) 
	return featureBidder+featureAuction

def device(g, bidder):
	# device per bidder
	# device per auction
	return device_per_bidder(g, bidder)+device_per_auction(g, bidder)

def ip(g, ipBidderList, bidder):
	# ip per bidder
	# ip per auction
	return ip_per_bidder(g, ipBidderList, bidder)+ip_per_auction(g, bidder)

def time(g, bidder):
	return bid_by_hour(g, bidder)




# basic
# feature 1: Bidder's number of total bid
def bid_total(g, bidder):
	# edges = g.edges(bidder)
	# total = int()
	# for (bidder, auction) in edges:
	# 	total = total+g.edge[bidder][auction]["num"]
	# return total
	return sum(g.node[bidder]['auctionDistri'].values())

# feature 2: Bidder's number of bidded auctions
def auction_total(g, bidder):
	return len(g.edges(bidder))

# bid per auction
# feature 1: bid_per_auction_mean, Bidder's average bid numbers in auctions
# feature 2: bid_per_auction_max, Bidder's max bid numbers in auctions
# feature 3: bid_per_auction_min, Bidder's min bid numbers in auctions
# feature 4: bid_per_auction_std, Bidder's std bid numbers in auctions
# feature 5: bid_per_auction_entropy, Bidder's entropy of bid numbers in auctions

# bidder ratio in auction
# feature 1: bidder_ratio_per_auction_mean, average Bidder in every auction's ratio 
# feature 2: bidder_ratio_per_auction_max
# feature 3: bidder_ratio_per_auction_min
# feature 4: bidder_ratio_per_auction_std
# feature 5: bidder_ratio_per_auction_entropy

# bid overlap per auction
# feature 1:



# bid override
# bid_override_per_bidder, bid_override_per_auction


# country
# country per bidder, num, enttropy
def country_per_bidder(g, bidder):
	countryDistri = g.node[bidder]["countryDistri"]
	countryNum = len(countryDistri)
	# print(list(countryDistri.values()))
	countryEntropy = cm.entropy(list(countryDistri.values()))
	return [countryNum, countryEntropy]

# country per auction, mean, max, min, std, entropy
def country_per_auction(g, bidder):
	# [{'bids':{'bid_id':attrDict}]
	entropys = list()
	for edge in list(g.edge[bidder].values()):
		countryDistriAuction = dict()
		for (bid, attrs) in edge['bids'].items():
			country = attrs['country']
			countryDistriAuction[country] = countryDistriAuction.get(country,0)+1
		entropy = cm.entropy(list(countryDistriAuction.values()))
		entropys.append(entropy)
	return cm.stats(entropys)


# device
# device per bidder, entropy, device num
def device_per_bidder(g, bidder):
	deviceDistri = g.node[bidder]["deviceDistri"]
	deviceNum = len(deviceDistri)
	deviceEntropy = cm.entropy(list(deviceDistri.values()))
	return [deviceNum, deviceEntropy]

# device per auction, mean, max, min, std, entropy
def device_per_auction(g, bidder):
	entropys = list()
	for edge in list(g.edge[bidder].values()):
		deviceDistriAuction = dict()
		for (bid, attrs) in edge['bids'].items():
			device = attrs['device']
			deviceDistriAuction['device'] = deviceDistriAuction.get(device,0)+1
		entropy = cm.entropy(list(deviceDistriAuction.values()))
		entropys.append(entropy)
	return cm.stats(entropys)

# ip
# ip per bidder: ip num, ip entropy, ip share num
def ip_per_bidder(g, ipBidderList, bidder):
	# ips is a list
	ipDistri = g.node[bidder]["ipDistri"]
	ipNum = len(ipDistri)
	ipEntropy = cm.entropy(list(ipDistri.values()))
	ipShareNum = 0
	for ip in ipDistri.keys():
		if len(ipBidderList[ip])>1:
			ipShareNum = ipShareNum+1
	return [ipNum, ipEntropy, ipShareNum]

# ip per auction: mean, max, min, std, entropy
def ip_per_auction(g, bidder):
	entropys = list()
	for edge in list(g.edge[bidder].values()):
		ipDistriAuction = dict()
		for (bid, attrs) in edge['bids'].items():
			ip = attrs['ip']
			ipDistriAuction['ip'] = ipDistriAuction.get(ip,0)+1
		entropy = cm.entropy(list(ipDistriAuction.values()))
		entropys.append(entropy)
	return cm.stats(entropys)


# bid distribution by hour, 4 hours, 6 hours
def bid_by_hour(g, bidder):
	hourList = g.node[bidder]['hourList']
	# hourTuple = [(a, hourDistri[a]) for a in sorted(hourDistri.keys())]
	# total = float(sum(hourDistri.values()))
	total = sum(hourList)
	if total==0:
		return [0]*49
	else:
		bidRatioPerHour = list()
		# bid per hour
		for bid in hourList:
			bidRatioPerHour.append(bid/total)
		bidRatioPer4Hour = cm.sumWithDistance(bidRatioPerHour, 4)
		bidRatioPer6Hour = cm.sumWithDistance(bidRatioPerHour, 6)
		bid_by_hour_feature = bidRatioPerHour+cm.stats(bidRatioPerHour)+bidRatioPer4Hour+cm.stats(bidRatioPer4Hour)[1:]+bidRatioPer6Hour+cm.stats(bidRatioPer6Hour)[1:]
		return bidRatioPerHour+cm.stats(bidRatioPerHour)+bidRatioPer4Hour+cm.stats(bidRatioPer4Hour)[1:]+bidRatioPer6Hour+cm.stats(bidRatioPer6Hour)[1:]



