# Setup
- Install requirements from requirements.txt
- For each dataset, the download urls are listed in the setup directory, along with a download.sh script to download all of them.
- Make script executable using *chmod +x download.sh*
- Run scripts using *./download.sh*

# Experiments
The corresponding jupyter notebooks for experiments can be found in the experiments directory. 

# Datasets
We want undirected, unweighted networks, with a large number of nodes. A variance in the following metrics is needed 
- density
- average clustering coefficient
- diameter 

## Social networks
<!-- - [reddit-hyperlinks](https://snap.stanford.edu/data/soc-RedditHyperlinks.html) -->
- [rt-retweet](https://networkrepository.com/rt-retweet-crawl.php)
- [digg_reply](https://networks.skewed.de/net/digg_reply)
- [email_enron](https://networks.skewed.de/net/email_enron)

## Collaboration networks
- [ca-AstroPh](https://snap.stanford.edu/data/ca-AstroPh.html)
- [ca-CondMat](https://snap.stanford.edu/data/ca-CondMat.html)
- [ca-HepPh](https://snap.stanford.edu/data/ca-HepPh.html)
- [TerroristRel](https://networkrepository.com/TerroristRel.php)
- [marvel_universe](https://networks.skewed.de/net/marvel_universe)
  
## Road networks
<!-- - [openflights](https://networkrepository.com/inf-openflights.php) -->
- [us_roads/AK](https://networks.skewed.de/net/us_road)
- [us_roads/NH](https://networks.skewed.de/net/us_road)
- [us_roads/VT](https://networks.skewed.de/net/us_road)
- [us_roads/CT](https://networks.skewed.de/net/us_roads)
- [roadNet-CA](https://snap.stanford.edu/data/roadNet-CA.html)
  
# Paper

## Introduction
- Some blurb about utility of network analysis
- Explain degree centrality, the simplest centrality measure
- Explain closeness centrality, and by extension topk closeness centrality
- Choosing a centrality measure for a task can be difficult. There are certain network specific factors that affect performance
- Detail experiments w.r.t time analysis
- Intuitively, degree and closeness centrality for TopK closeness should be related. But again, certain network specific factors will affect this relationship
- Detail experiments w.r.t comparing degree, closeness, topkcloseness BFSCUT and LB variants