# Setup
- Install requirements from requirements.txt
- For each dataset, the download urls are listed in the setup directory, along with a download.sh script to download all of them. Run those scripts

# Experiments
The corresponding jupyter notebooks for experiments can be found in the experiments directory. 

## NYC Taxi Cab trip data

The data contains individual trips from a starting location id, to a destination location id, along with fare details. We want to answer the following questions

- How related are all the centrality measures to nodes ranked by revenue
- Can we use Top K Closeness centrality to find the top revenue generating taxi pick up zones
- Can we use Top K Closeness centrality to find nodes as well as their neighbors that generate top revenue/trip count
  
## Wikipedia Clickstream

The dataset contains clickstream data for the Wikipedia website. Each row is a source and destination page name that any user visited, as well as the type of source link, and the number of times users visited the particular destination from source. We want to answer the following questions

- How related is top k closeness centrality to the other centrality measures.
- Can we use Top K Closeness Centrality to find the top visited destinations, for the sample usecase of caching pages more optimally 
