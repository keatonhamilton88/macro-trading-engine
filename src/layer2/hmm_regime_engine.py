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


    def describe_states(features, states):

        df = features.copy()
        df["state"] = states
    
        summary = df.groupby("state").mean()
    
        return summary

    summary = describe_states(features, states)

    print("\nState Characteristics:")
    print(summary)


    def label_states(states):

        STATE_LABELS = {
            0: "risk_on",
            1: "risk_off",
            2: "neutral",
            3: "stress"
        }
    
        return states.map(STATE_LABELS)



    def apply_persistence_filter(states, window=3):

        filtered = states.copy()
    
        for i in range(window, len(states)):
            if len(set(states.iloc[i-window:i])) == 1:
                filtered.iloc[i] = states.iloc[i]
            else:
                filtered.iloc[i] = filtered.iloc[i-1]
    
        return filtered


    def fit(self, features: pd.DataFrame):
        # 'Winsorize' or clip the PCA signals to 3 standard deviations
        # This prevents the Gaussian HMM from 'stretching' to fit outliers
        X = features.dropna().clip(lower=features.mean()-3*features.std(), 
                                    upper=features.mean()+3*features.std(), 
                                    axis=1).values
        self.model.fit(X)
        self.fitted = True

    
