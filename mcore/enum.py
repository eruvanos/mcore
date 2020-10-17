from enum import Enum


class AutoNameEnum(Enum):
    def _generate_next_value_(self, start, count, last):
        return self

    def __repr__(self):
        return self.value