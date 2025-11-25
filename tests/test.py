import asyncio
import time
from typing import Any, AsyncGenerator, Callable
from dependency_injector.containers import DeclarativeContainer, providers
from dependency_injector import providers
from dependency_injector.wiring import Provide
from contextlib import asynccontextmanager


async def function(app: Any, boolean: bool = False):
    print(boolean)
    print(app)
    await asyncio.sleep(3)
    return


class AAA:
    a = "aaaaa"


class Container(DeclarativeContainer):
    configuration = providers.Configuration()

    a = providers.Factory(AAA)

    f = providers.Callable(function, app=a)


di = Container()
di.init_resources()

call = di.f()
time.sleep(5)
asyncio.run(call)

# в данном случае все реально работает
