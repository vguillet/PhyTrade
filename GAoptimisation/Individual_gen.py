
class Individual:
    def __init__(self):
        import random

        # RSI parameters:
        self.rsi_1_timeframe = random.randint(2, 100)

        self.rsi_1_spline_smoothing_factor = random.uniform(0.0, 2.0)

        # SMA parameters:
        self.sma_1_timeperiod_1 = random.randint(2, 100)
        self.sma_1_timeperiod_2 = random.randint(2, 100)

        self.sma_2_timeperiod_1 = random.randint(2, 100)
        self.sma_2_timeperiod_2 = random.randint(2, 100)

        self.sma_3_timeperiod_1 = random.randint(2, 100)
        self.sma_3_timeperiod_2 = random.randint(2, 100)

        self.sma_1_spline_smoothing_factor = random.uniform(0.0, 2.0)
        self.sma_2_spline_smoothing_factor = random.uniform(0.0, 2.0)
        self.sma_3_spline_smoothing_factor = random.uniform(0.0, 2.0)

        # OC parameters:
        self.oc_avg_gradient_spline_smoothing_factor = random.uniform(0.0, 2.0)

        # Volume parameters:
        self.volume_amplification_factor = random.uniform(0.0, 3.0)

        self.volume_spline_smoothing_factor = random.uniform(0.0, 2.0)

        # Volatility parameters:
        self.volatility_timeframe = random.randint(2, 100)
        self.volatility_amplification_factor = random.uniform(0.0, 3.0)

        self.volatility_spline_smoothing_factor = random.uniform(0.0, 2.0)

        # Spline weights:
        self.rsi_1_spline_weight = random.uniform(0.0, 10.0)

        self.sma_1_spline_weight = random.uniform(0.0, 10.0)
        self.sma_2_spline_weight = random.uniform(0.0, 10.0)
        self.sma_3_spline_weight = random.uniform(0.0, 10.0)

        self.oc_avg_gradient_spline_weight = random.uniform(0.0, 10.0)



