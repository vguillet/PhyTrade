from abc import ABC, abstractmethod


class ABSTRACT_indicator(ABC):
    @abstractmethod
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        pass
