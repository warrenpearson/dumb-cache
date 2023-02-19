import os
import time

from dumb_cache import DumbCache


def test_default_cache_path():
    cache = DumbCache()
    path = cache.get_cache_path()
    assert path.endswith("cache.sqlite3")


def test_set_cache_path():
    cache = DumbCache()
    cache.set_cache_path("./cache.db")
    path = cache.get_cache_path()
    check_path = "/cache.db"

    assert path.endswith(check_path)


def test_set_absolute_path():
    test_path = "/tmp/cache.db"
    cache = DumbCache()
    cache.set_cache_path(test_path)

    path = cache.get_cache_path()

    assert path == test_path


def test_insert():
    ts = time.time() * 1000
    cache = DumbCache()
    cache.set_cache_path(f"./cache.{ts}.db")

    test_dict = {"one": 1, "two": 2}

    cache.set_cache_data("test_1", test_dict)

    check = cache.get_cache_data("test_1")

    assert len(check.keys()) == 2
    assert check["two"] == 2

    os.remove(cache.get_cache_path())


def test_double_insert():
    ts = time.time() * 1000
    cache = DumbCache()
    cache.set_cache_path(f"./cache.{ts}.db")

    test_dict = {"one": 1, "two": 2}

    cache.set_cache_data("test_1", test_dict)

    test_dict["three"] = 3
    cache.set_cache_data("test_1", test_dict)

    check = cache.get_cache_data("test_1")

    assert len(check.keys()) == 3
    assert check["two"] == 2
    assert (check["three"]) == 3

    os.remove(cache.get_cache_path())


def test_update():
    ts = time.time() * 1000
    cache = DumbCache()
    cache.set_cache_path(f"./cache.{ts}.db")

    test_dict = {"one": 1, "two": 2}

    cache.set_cache_data("test_1", test_dict)

    test_dict["three"] = 3
    cache.update_cache_data("test_1", test_dict)

    check = cache.get_cache_data("test_1")

    assert len(check.keys()) == 3
    assert check["two"] == 2
    assert (check["three"]) == 3

    os.remove(cache.get_cache_path())


def test_empty_cache():
    cache = DumbCache()
    data = cache.get_cache_data("nosuch_key")
    assert data is None
