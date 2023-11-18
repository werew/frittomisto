"""
Test async utilities
"""
import asyncio
from frittomisto.asyncio import make_sync


@make_sync
async def async_increment(n: int) -> int:
    """
    An async function can be run synchronously
    """
    await asyncio.sleep(0.001)
    return n+1

def test_make_sync() -> None:
    """
    Test make_sync
    """
    assert async_increment(1) == 2
