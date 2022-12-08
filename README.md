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
- [reddit-hyperlinks](https://snap.stanford.edu/data/soc-RedditHyperlinks.html)
- [rt-retweet](https://networkrepository.com/rt-retweet-crawl.php)
- [hiv_transmission](https://networks.skewed.de/net/hiv_transmission)

## Web networks
- [Wikipedia Clickstream](https://meta.wikimedia.org/wiki/Research:Wikipedia_clickstream)

## Collaboration networks
- [Astro Physics](https://snap.stanford.edu/data/ca-AstroPh.html)
- [TerroristRel](https://networkrepository.com/TerroristRel.php)

## Road networks
- [roadNet-CA](https://snap.stanford.edu/data/roadNet-CA.html)
- [Euroroads](http://konect.cc/networks/subelj_euroroad/)
- [openflights](https://networkrepository.com/inf-openflights.php)
- [us_roads](https://networks.skewed.de/net/us_roads)