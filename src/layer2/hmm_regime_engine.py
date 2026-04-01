import pandas as pd
import numpy as np
from hmmlearn.hmm import GaussianHMM


class HMMRegimeEngine:

    def __init__(self, n_states=4, covariance_type="full", n_iter=1000):
        self.n_states = n_states
        self.model = GaussianHMM(
            n_components=n_states,
            covariance_type=covariance_type,
            n_iter=n_iter,
            random_state=42
        )
        self.fitted = False

    def fit(self, features: pd.DataFrame):

        X = features.dropna().values
        self.model.fit(X)
        self.fitted = True

    def predict_states(self, features: pd.DataFrame):

        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")

        X = features.dropna().values
        states = self.model.predict(X)

        state_series = pd.Series(
            states,
            index=features.dropna().index,
            name="state"
        )

        return state_series

    def predict_probabilities(self, features: pd.DataFrame):

        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")

        X = features.dropna().values
        probs = self.model.predict_proba(X)

        prob_df = pd.DataFrame(
            probs,
            index=features.dropna().index,
            columns=[f"state_{i}" for i in range(self.n_states)]
        )

        return prob_df

    def get_transition_matrix(self):

        return pd.DataFrame(
            self.model.transmat_,
            columns=[f"to_{i}" for i in range(self.n_states)],
            index=[f"from_{i}" for i in range(self.n_states)]
        )
