import numpy as np
import pandas as pd

def gamma_strength(price, flip_level, sensitivity=0.02):
    """
    Returns a signal from -1 to 1 based on distance from the flip.
    Sensitivity: how fast the signal reaches 'max strength' (0.02 = 2% away).
    """
    if flip_level == 0 or pd.isna(flip_level):
        return 0.0
    
    # Calculate % distance from the flip
    dist = (price - flip_level) / flip_level
    
    # Use tanh to 'squish' the distance into a -1 to 1 range
    # Dividing by sensitivity controls how 'steep' the curve is
    strength = np.tanh(dist / sensitivity)
    
    return strength



