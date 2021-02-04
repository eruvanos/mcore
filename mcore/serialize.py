import dataclasses
from datetime import datetime
from json.encoder import JSONEncoder


class EnhancedJSONEncoder(JSONEncoder):
    """
    json.dumps(datetime.today(), cls=EnhancedJSONEncoder)
    """
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
