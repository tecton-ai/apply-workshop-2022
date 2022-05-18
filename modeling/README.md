# Building a Deep Learning Recommendation Model

The notebooks in this folder walk through building and operationalizing a deep-learning based recommendation model.

* [data.ipynb](./data.ipynb) displays the raw data that is used to train the model
* [train_tabnet.ipynb](./train_tabnet.ipynb) generates training data with Tecton then trains a TabNet model
* [tabnet_batch_inference.ipynb](./tabnet_batch_inference.ipynb) generates features for inference with Tecton, generates predictions about what rating each user will give each movie, then loads those predictions into Snowflake
* [nearest_neighbors_training.ipynb](./nearest_neighbors_training.ipynb) builds an approximate nearest neighbors model that is used to compute the similarity between every movie.
* [nearest_neighbors_inference.ipynb](./nearest_neighbors_inference.ipynb) predicts the 100 nearest neighbors of each movie and loads these predictions into Snowflake
* [online_recommendations.ipynb](./online_recommendations.ipynb) walks through the online workflow of candidate generation, filtering, and ranking movies to recommend to users in real time.