from django.test import override_settings
import pytest

from idempotency_key import locks


def test_single_thread_lock():
    obj = locks.ThreadLock()
    assert obj.acquire() is True
    assert obj.acquire() is False
    obj.release()
    assert obj.acquire() is True
    obj.release()


@override_settings(IDEMPOTENCY_KEY={"LOCK": {"LOCATION": "Redis://localhost"}})
def test_multi_process_lock_only_host():
    obj = locks.MultiProcessRedisLock()
    assert obj.acquire() is True
    assert obj.acquire() is False
    obj.release()
    assert obj.acquire() is True
    obj.release()


@override_settings(IDEMPOTENCY_KEY={"LOCK": {"LOCATION": "Redis://localhost:6379/1"}})
def test_multi_process_lock_host_and_port():
    obj = locks.MultiProcessRedisLock()
    assert obj.acquire() is True
    assert obj.acquire() is False
    obj.release()
    assert obj.acquire() is True
    obj.release()


@override_settings(IDEMPOTENCY_KEY={"LOCK": {"LOCATION": ""}})
def test_multi_process_lock_empty_string_must_be_set():
    with pytest.raises(ValueError):
        locks.MultiProcessRedisLock()


@override_settings(IDEMPOTENCY_KEY={"LOCK": {"LOCATION": None}})
def test_multi_process_lock_null_must_be_set():
    with pytest.raises(ValueError):
        locks.MultiProcessRedisLock()
