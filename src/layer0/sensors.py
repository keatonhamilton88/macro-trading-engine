from features import z_score
import pandas as pd

class SensorLibrary:

    @staticmethod
    def equity_risk_appetite(spy):
        return z_score(spy)
    
    @staticmethod
    def bond_momentum(tlt):
        return z_score(tlt)
    @staticmethod
    def gold_safety(gld):
        return z_score(gld)
    
    
