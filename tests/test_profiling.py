"""
Test profiling utilities
"""
import pytest
from frittomisto.profiling import pp_start, pp_stop, pp_get, pp_stats


def test_profile_rounds() -> None:
    """
    Test profile
    """
    pp_start("outer")
    for _ in range(10):
        pp_start("inner")
        for _ in range(10):
            pp_start("innermost")
            pp_stop("innermost")
        pp_stop("inner")
    pp_stop("outer")

    assert pp_get("outer").name == "outer"
    assert pp_get("outer").rounds == 1

    assert pp_get("inner").name == "inner"
    assert pp_get("inner").rounds == 10

    assert pp_get("innermost").name == "innermost"
    assert pp_get("innermost").rounds == 100

    assert pp_get("outer").tot_time >= pp_get("inner").tot_time
    assert pp_get("inner").tot_time >= pp_get("innermost").tot_time

    pp_stats()


def test_profile_restart() -> None:
    """
    Test starting a perf counter twice
    """
    pp_start("test_profile_restart")
    with pytest.raises(RuntimeError):
        pp_start("test_profile_restart")

    pp_start("test_profile_restart", allow_restart=True)
    pp_stop("test_profile_restart")
    assert pp_get("test_profile_restart").rounds == 1


def test_profile_restop() -> None:
    """
    Test stopping a perf counter twice
    """
    pp_start("test_profile_restop")
    pp_stop("test_profile_restop", allow_restop=True)
    pp_stop("test_profile_restop", allow_restop=True)
    with pytest.raises(RuntimeError):
        pp_stop("test_profile_restop")

    assert pp_get("test_profile_restop").rounds == 1
