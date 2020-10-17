from typing import Type as _Type, Optional, Any
from typing import TypeVar as _TypeVar

import esper

D = _TypeVar('D')


class World(esper.World):

    def __contains__(self, entity):
        return entity in self._entities

    def safe_delete_entity(self, entity: int, immediate=False):
        if entity in self:
            self.delete_entity(entity, immediate=immediate)

    def get(self, entity: int, component_type: _Type[D]) -> Optional[D]:
        for x in self.try_component(entity, component_type):
            return x
        else:
            return None

    def gets(self, entity: int, *component_types: _Type[D]) -> Any:
        return tuple(self.get(entity, component_type) for component_type in component_types)