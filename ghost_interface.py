from abc import ABC, abstractmethod


class AlgorithmInterface(ABC):

    @abstractmethod
    def getNextStep(self):
        pass
