from enum import Enum


class MemoryTypes(Enum):
    FREE = 'free'
    USED = 'used'
    TOTAL = 'total'

    @property
    def label_string(self):
        return self.value
