import pytest

# Test 1: Math Logic (Linked to LOGI-18)
def test_addition(record_property):
    record_property("test_key", "LOGI-18")
    assert 10 + 5 == 15

# Test 2: List Logic (Linked to LOGI-19 - Intentional Fail)
def test_data_check(record_property):
    record_property("test_key", "LOGI-19")
    names = ["Alice", "Bob"]
    assert "Charlie" in names

# Test 3: Boolean Logic (Linked to LOGI-20)
def test_is_active(record_property):
    record_property("test_key", "LOGI-20")
    status = True
    assert status is True

# Test 4: String Logic (Linked to LOGI-21)
def test_string_match(record_property):
    record_property("test_key", "LOGI-21")
    text = "Automation"
    assert text.startswith("Auto")

