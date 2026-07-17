import logging
from typing import Callable, Dict, List

logger = logging.getLogger("app")

class EventDispatcher:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, handler: Callable) -> None:
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.info(f"Subscribed handler {handler.__name__ if hasattr(handler, '__name__') else str(handler)} to event: {event_name}")

    def dispatch(self, event_name: str, *args, **kwargs) -> None:
        handlers = self._subscribers.get(event_name, [])
        if not handlers:
            logger.info(f"No handlers registered for event: {event_name}")
            return
            
        logger.info(f"Dispatching event '{event_name}' to {len(handlers)} handlers")
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error executing handler for event {event_name}: {str(e)}", exc_info=True)

event_dispatcher = EventDispatcher()
