
class BaseCollector:
    def __init__(self):
        pass


from functools import partial
from timeit import default_timer as timer
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import ValidationError
from opulence.common.base_fact import BaseFact
from opulence.common.types import BaseSet
from opulence.common.exceptions import InvalidCollectorDefinition, CollectorRuntimeError

from timeit import default_timer as timer


# from opulence.common.collectors.exceptions import CollectorRuntimeError
# from opulence.common.collectors.exceptions import InvalidCollectorDefinition
# from opulence.common.models.collect_item import CollectItemModel
# from opulence.common.models.collect_item import CollectItemResponseModel
# from opulence.common.models.fact import BaseFact
# from opulence.common.modules import BaseModule
# from opulence.common.types import BaseSet


class BaseConfig(BaseModel):
    name: str

class CollectorResponse:
    def __init__(self):
        self.errors = []
        self.facts = []
        self.duration: float = 0.0
        self._start_time = timer()

    def set_response(self, facts, errors):
        self.facts = facts
        self.errors = errors
        self.duration = timer() - self._start_time

class BaseCollector:

    config: Optional[BaseConfig] = None

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

    # def json(self):
    #     callbacks = []
    #     for t in self._callbacks.keys():
    #         if isinstance(t, BaseSet):
    #             callbacks.append(t.json())
    #         else:
    #             callbacks.append({"type": "Single", "params": [t.__name__]})
    #     return {"name": self.config.name, "allowed_types": callbacks}

    @staticmethod
    def _sanitize_output(fn):
        try:
            output = fn()
            if output:
                for out in output:
                    if isinstance(out, BaseFact):
                        yield out
        except Exception as err:
            logger.error(f"Error while executing {fn}: {err}")
            raise CollectorRuntimeError(err) from err

    def _prepare_callbacks(
        self, input_fact: Union[List[BaseFact], BaseFact]
    ) -> Iterator[Callable]:
        for cb_type, cb in self._callbacks.items():
            if isinstance(cb_type, BaseSet):
                _set = cb_type.select_from(input_fact)
                if _set:
                    yield partial(cb, _set)
            else:
                for fact in input_fact:
                    if cb_type == type(fact):
                        yield partial(cb, fact)

    def _execute_callbacks(self, callbacks):
        facts = []
        errors = []
        for cb in callbacks:
            try:
                facts.extend(list(self._sanitize_output(cb)))
            except CollectorRuntimeError as err:
                errors.append(str(err))
        return facts, errors

    def collect(self, facts: List[BaseFact]) -> Iterator[BaseFact]:
        callbacks = self._prepare_callbacks(facts)

        response = CollectorResponse()

        facts, errors = self._execute_callbacks(callbacks)
        response.set_response(facts=facts, errors=errors)
        return response