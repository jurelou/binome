from functools import partial
from timeit import default_timer as timer
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

from opulence.common import utils
from pydantic import BaseModel
from pydantic import ValidationError
from opulence.common.fact import BaseFact
from opulence.common.types import BaseSet
from opulence.agent.collectors.exceptions import InvalidCollectorDefinition, CollectorRuntimeError
from opulence.agent.collectors.dependencies import Dependency
from timeit import default_timer as timer




class CollectItem(BaseModel):
    pass


class BaseConfig(BaseModel):
    name: str

class CollectResult(BaseModel):
    collector_config: BaseConfig
    duration: float
    executions_count : int
        
    errors: Optional[List[str]] = None
    facts: Optional[List[BaseFact]] = None

class BaseCollector:

    config: Optional[BaseConfig] = None
    dependencies: Optional[List[Dependency]] = None

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
            f"Collector {type(self).__name__} does not have any callbacks"
        )

    @staticmethod
    def _sanitize_output(fn):
        def force_list(data):
            if utils.is_iterable(data):
                return list(data)
            if not utils.is_list(data):
                return [data]
            return data
        try:
            output = force_list(fn())
            if output:
                for out in output:
                    if isinstance(out, BaseFact):
                        yield out
                    else:
                        print(f"Found unknown output from collector: {out}")
        except Exception as err:
            print(f"Error while executing {fn}: {err}")
            # logger.error(f"Error while executing {fn}: {err}")
            raise CollectorRuntimeError(err) from err

    def _prepare_callbacks(
        self, input_fact: Union[List[BaseFact], BaseFact]
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
        errors = []
        for cb in callbacks:
            try:
                facts.extend(list(self._sanitize_output(cb)))
            except CollectorRuntimeError as err:
                errors.append(str(err))
        return facts or None, errors or None

    def collect(self, facts: List[BaseFact]) -> Iterator[BaseFact]:
        start_time = timer()

        callbacks = self._prepare_callbacks(facts)
        facts, errors = self._execute_callbacks(callbacks)

        return CollectResult(
            collector_config=self.config,
            duration=timer() - start_time,
            executions_count=len(callbacks),
            errors=errors,
            facts=facts)
