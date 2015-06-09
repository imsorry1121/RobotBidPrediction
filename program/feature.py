import common as cm
# feature extracion

def feature_extract(g, bidder, ipDistri):
	features = bidder_info(g,bidder)+bid_info(g, bidder)+country_info(g, bidder)+device_info(g, bidder)+ip_info(g, ipDistri, bidder)
	return features


def bidder_info(g, bidder):
	return [bid_num(g, bidder), auction_num(g, bidder), avg_bid_num(g, bidder), auction_distri(g, bidder), auction_ratio(g, bidder)]

# bidder info
# feature 1: Bidder's number of total bid
def bid_num(g, bidder):
	edges = g.edges(bidder)
	total = int()
	for (bidder, auction) in edges:
		total = total+g.edge[bidder][auction]["num"]
	return total

# feature 2: Bidder's number of bidded auctions
def auction_num(g, bidder):
	return len(g.edges(bidder))

# feature 3: Bidder's average bid numbers in auctions
def avg_bid_num(g, bidder):
	return g.node[bidder]["avgBidNum"]

# feature 4: Bidder's auction's bids entropy
def auction_distri(g, bidder):
	ratios = list(g.node[bidder]["auctionDistri"].values())
	return cm.entropy(ratios)

# feature 5: average Bidder in every auction's ratio 
def auction_ratio(g, bidder):
	avgRatio = float()
	ratios = list(g.node[bidder]["auctionRatios"].values())
	l = len(ratios)
	if l ==0:
		return 0
	else:
		avgRatio = sum(ratios)/l
		return avgRatio

# feature 6: 

# bid info
# feature 7, 8, 9, 10: overlap bidding record
def bid_info(g, bidder):
	bidOverlapNum = 0
	bidOverlapNormNum = 0
	bidOverlapNumAuction = 0
	bidOverlapNormNumAuction = 0
	edges = g.edges(bidder)
	auctionNum = len(edges)
	if auctionNum ==0:
		return [0,0,0,0]
	# print(edges)
	for (b, a) in edges:
		bidderRecord = g.node[a]["bidders"]
		count = cm.overlap(bidder, bidderRecord)
		bidOverlapNum = bidOverlapNum+count
		if count>0:
			bidOverlapNumAuction = bidOverlapNumAuction+1
	bidOverlapNormNum = bidOverlapNum/bid_num(g, bidder)
	bidOverlapNormNumAuction = bidOverlapNumAuction/auctionNum
	return [bidOverlapNum, bidOverlapNormNum, bidOverlapNumAuction, bidOverlapNormNumAuction]

# country 
# feature 11, 12: country entropy, country num
def country_info(g, bidder):
	countryDistri = g.node[bidder]["countryDistri"]
	countryNum = len(countryDistri)
	# print(list(countryDistri.values()))
	countryEntropy = cm.entropy(list(countryDistri.values()))
	return [countryNum, countryEntropy]

# device
# feature 13, 14: device entropy, device num
def device_info(g, bidder):
	deviceDistri = g.node[bidder]["deviceDistri"]
	deviceNum = len(deviceDistri)
	deviceEntropy = cm.entropy(list(deviceDistri.values()))
	return [deviceNum, deviceEntropy]

# ip
# feature 15, 16: ip num, shared ip with others
def ip_info(g, ipDistri, bidder):
	ips = g.node[bidder]["ips"]
	ipNum = len(ips)
	ipShareNum = 0
	for ip in ips:
		if len(ipDistri[ip])>1:
			ipShareNum = ipShareNum+1
	return [ipNum, ipShareNum]
