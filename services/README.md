# Recommendation Backend Implementation

This directory contains the implementations of various backend components used to power the recommendations demo.

* [batch_recommendation_service/](./batch_recommendation_service/) contains the implementation of an endpoint that serves precomputed batch recommendations by fetching them from Tecton.
* [real_time_recommendation_service/](./real_time_recommendation_service/) contains the implementation of an endpoint that computes recommendations in real time by performing candidate generation, filtering, and ranking with an ML model.
* [recommender_model_service/](./recommender_model_service/) contains the implementation of an endpoint that hosts a trained TabNet model to provide real-time inference capabilities.