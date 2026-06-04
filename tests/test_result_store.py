import time
from unittest.mock import patch

import pytest

from utils.result_store import ResultStore


@pytest.mark.unit
def test_put_returns_string():
    store = ResultStore()
    token = store.put({'data': 1})
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.unit
def test_put_returns_unique_tokens():
    store = ResultStore()
    tokens = {store.put({'n': i}) for i in range(10)}
    assert len(tokens) == 10


@pytest.mark.unit
def test_get_returns_payload():
    store = ResultStore()
    payload = {'qr': b'bytes', 'x': 42}
    token = store.put(payload)
    assert store.get(token) == payload


@pytest.mark.unit
def test_get_unknown_token_returns_none():
    store = ResultStore()
    assert store.get('nonexistent') is None


@pytest.mark.unit
def test_get_expired_entry_returns_none():
    store = ResultStore(ttl=10)
    token = store.put({'data': 1})
    future = time.monotonic() + 11
    with patch('utils.result_store.time.monotonic', return_value=future):
        assert store.get(token) is None


@pytest.mark.unit
def test_fifo_eviction_at_cap():
    store = ResultStore(max_entries=3)
    t1 = store.put({'n': 1})
    store.put({'n': 2})
    store.put({'n': 3})
    store.put({'n': 4})
    assert store.get(t1) is None


@pytest.mark.unit
def test_eviction_keeps_recent_entries():
    store = ResultStore(max_entries=2)
    t1 = store.put({'n': 1})
    t2 = store.put({'n': 2})
    t3 = store.put({'n': 3})
    assert store.get(t2) is not None or store.get(t3) is not None
