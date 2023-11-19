"""
Test cfg utilities
"""
import tempfile
import os
import pytest
from frittomisto.cfg import cfg
from frittomisto.path import cd


def test_cfg() -> None:
    """
    Test reading a config file
    """
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(
            b"""
        [foo]
        bar = 1
        baz = "hello"
        """
        )
        tmp.flush()
        cfg.set_config_file(tmp.name)
        assert cfg["foo"]["bar"] == 1
        assert cfg["foo"]["baz"] == "hello"

def test_find_cfg() -> None:
    """
    Test finding a config file
    """
    cfg_name = "test.toml"
    cfg.set_config_file(None)
    cfg.set_config_names(cfg_name)
    with tempfile.TemporaryDirectory() as tmpdir:
        child_dir = os.path.join(tmpdir, "a/b/c")
        os.makedirs(child_dir)
        with open(os.path.join(tmpdir, cfg_name), "w", encoding="utf-8") as f:
            f.write(
                """
            [foo]
            bar = 1
            baz = "hello"
            """
            )
        with cd("/"):
            with pytest.raises(FileNotFoundError):
                assert cfg["foo"]["bar"] == 1

        with cd(child_dir):
            assert cfg["foo"]["bar"] == 1
            assert cfg["foo"]["baz"] == "hello"


        
