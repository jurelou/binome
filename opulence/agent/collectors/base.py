from functools import partial
import logging

# from opulence.agent.collectors.dependencies import Dependency
from timeit import default_timer as timer
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import ValidationError

from opulence.agent.collectors.exceptions import CollectorRuntimeError
from opulence.agent.collectors.exceptions import InvalidCollectorDefinition
from opulence.common.fact import BaseFact
from opulence.common.types import BaseSet
from opulence.common.utils import make_list

logger = logging.getLogger(__name__)


# class CollectItem(BaseModel):
#     pass


class BaseConfig(BaseModel):
    name: str


class CollectResult(BaseModel):
    collector_config: BaseConfig
    duration: float
    executions_count: int

    # errors: Optional[List[str]] = None
    facts: Optional[List[BaseFact]] = None


class BaseCollector:

    config: Optional[BaseConfig] = None
    # dependencies: Optional[List[Dependency]] = None

    def __init__(self):
        self._callbacks: Dict[Union[BaseFact, BaseSet], Callable] = self.callbacks()

        try:
            self.configure()
        except ValidationError as err:
            raise InvalidCollectorDefinition(str(err)) from err

    def configure(self):
        self.config = BaseConfig(**self.config)

    def callbacks(self) -> Dict[Union[BaseFact, BaseSet], Callable]:
        raise InvalidCollectorDefinition(
            f"Collector {type(self).__name__} does not have any callbacks",
        )

    @staticmethod
    def _sanitize_output(fn):
        try:
            output = make_list(fn())
            if output:
                for out in output:
                    if isinstance(out, BaseFact):
                        yield out
                    else:
                        logger.error(f"Found unknown output from collector: {out}")
        except Exception as err:
            logger.error(f"Error while executing {fn}: {err}")
            raise CollectorRuntimeError(err) from err

    def _prepare_callbacks(
        self, input_fact: Union[List[BaseFact], BaseFact],
    ) -> Iterator[Callable]:
        callbacks = []
        for cb_type, cb in self._callbacks.items():
            if isinstance(cb_type, BaseSet):
                _set = cb_type.select_from(input_fact)
                if _set:
                    callbacks.append(partial(cb, _set))
            else:
                for fact in input_fact:
                    if cb_type == type(fact):
                        callbacks.append(partial(cb, fact))
        return callbacks

    def _execute_callbacks(self, callbacks):
        facts = []
        for cb in callbacks:
            facts.extend(list(self._sanitize_output(cb)))
        return facts or None

    def collect(self, facts: List[BaseFact]) -> Iterator[BaseFact]:
        start_time = timer()

        callbacks = self._prepare_callbacks(facts)
        print("CALLBACKS", callbacks)
        facts = self._execute_callbacks(callbacks)

        return CollectResult(
            collector_config=self.config,
            duration=timer() - start_time,
            executions_count=len(callbacks),
            facts=facts,
        )
