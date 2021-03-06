import pytest
import asyncio

from aioreactive.testing import VirtualTimeEventLoop
from aioreactive.operators.from_iterable import from_iterable
from aioreactive.operators.distinct_until_changed import distinct_until_changed
from aioreactive.core import run, subscribe, AnonymousAsyncObserver


class MyException(Exception):
    pass


@pytest.yield_fixture()
def event_loop():
    loop = VirtualTimeEventLoop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_distinct_until_changed_different():
    xs = from_iterable([1, 2, 3])
    result = []

    async def asend(value):
        result.append(value)

    ys = distinct_until_changed(xs)

    await run(ys, AnonymousAsyncObserver(asend))
    assert result == [1, 2, 3]


@pytest.mark.asyncio
async def test_distinct_until_changed_changed():
    xs = from_iterable([1, 2, 2, 1, 3, 3, 1, 2, 2])
    result = []

    async def asend(value):
        result.append(value)

    ys = distinct_until_changed(xs)

    await run(ys, AnonymousAsyncObserver(asend))
    assert result == [1, 2, 1, 3, 1, 2]
