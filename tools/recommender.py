"""Recommender Tool for Answerable

The recommender loads the specified model to make the recommendations.
"""

import importlib


def recommend(user_qa, feed, model_name):
    try:
        model = importlib.import_module("." + model_name, "models")
        return model.recommend(user_qa, feed)
    except ModuleNotFoundError:
        log.abort(f"Model {model_name} not present")
