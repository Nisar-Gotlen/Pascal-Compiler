from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def Print(self):
        pass
