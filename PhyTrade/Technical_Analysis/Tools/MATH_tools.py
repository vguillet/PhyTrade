

class MATH:   
    @staticmethod
    def normalise_zero_one(signal):
        
        signal_normalised = []
        
        for i in range(len(signal)):
            signal_normalised.append((signal[i]-min(signal))/((max(signal)-min(signal)) or 1))
        
        return signal_normalised
    
    @staticmethod
    def normalise_minus_one_one(signal):

        signal_normalised = []

        for i in range(len(signal)):
            signal_normalised.append(2*(signal[i] - min(signal)) / ((max(signal) - min(signal)) or 1)-1)

        return signal_normalised

    @staticmethod
    def amplify(signal, amplification_factor):

        signal_amplified = []

        for i in signal:
            signal_amplified.append(i*amplification_factor)

        return signal_amplified
