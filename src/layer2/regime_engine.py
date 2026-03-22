import pandas as pd
import numpy as np


class RegimeEngine:

    REGIME_MAP = {

        "risk_on": {
            "growth": 1,
            "risk": -1,
            "dollar": -1
        },

        "risk_off": {
            "growth": -1,
            "risk": 1,
            "dollar": 1
        },

        "inflation": {
            "inflation": 1,
            "rates": 1
        },

        "deflation": {
            "growth": -1,
            "inflation": -1,
            "rates": -1
        }

    }

    @staticmethod
    def compute_scores(features):

        scores = pd.DataFrame(index=features.index)

        for regime, weights in RegimeEngine.REGIME_MAP.items():

            score = 0

            for factor, direction in weights.items():

                if factor in features.columns:
                    score += direction * features[factor]

            scores[regime] = score

        return scores

    @staticmethod
    def classify(scores):

        regime = scores.idxmax(axis=1)

        confidence = (
            scores.max(axis=1) - scores.mean(axis=1)
        ) / scores.std(axis=1)

        return regime, confidence
