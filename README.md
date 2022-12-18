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