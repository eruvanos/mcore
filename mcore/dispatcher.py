from collections import defaultdict


class Dispatcher:
    def __init__(self):
        self._listeners = defaultdict(list)

    def emit(self, event):
        for listener in self._listeners[type(event)]:
            listener(event)

    def connect(self, event_type, listener):
        self._listeners[event_type].append(listener)


class AsyncDispatcher:
    def __init__(self):
        self._listeners = defaultdict(list)

    async def emit(self, event):
        for l in self._listeners[type(event)]:
            await l(event)

    def connect(self, event_type, listener):
        self._listeners[event_type].append(listener)
