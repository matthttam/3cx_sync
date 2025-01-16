from app.widgets import Checkbox, ExtensionMappingFieldSet

import pytest
from unittest.mock import MagicMock
from tkinter import Entry, Button


class TestCheckbox:
    def test_initial_state(self):
        checkbox = Checkbox()
        assert checkbox.checked is False  # Initially, checkbox should be unchecked

    def test_check(self):
        checkbox = Checkbox()
        checkbox.check()
        # After checking, checkbox should be checked
        assert checkbox.checked is True

    def test_uncheck(self):
        checkbox = Checkbox(value=True)  # Create a checkbox initially checked
        checkbox.uncheck()
        # After unchecking, checkbox should be unchecked
        assert checkbox.checked is False

    def test_toggle(self):
        checkbox = Checkbox(value=True)  # Create a checkbox initially checked
        checkbox.toggle()  # Toggle the checkbox
        # After toggling, checkbox should be unchecked
        assert checkbox.checked is False
        checkbox.toggle()  # Toggle the checkbox again
        # After toggling again, checkbox should be checked
        assert checkbox.checked is True


class TestExtensionMappingFieldSet:

    @pytest.fixture
    def field_set(self):
        yield ExtensionMappingFieldSet(
            header=MagicMock(spec=Entry),
            field=MagicMock(spec=Entry),
            static=MagicMock(spec=Checkbox),
            update=MagicMock(spec=Checkbox),
            key=MagicMock(spec=Checkbox),
            delete=MagicMock(spec=Button),
        )

    def test_initialization(self, field_set):
        # Check if the attributes are properly set
        assert field_set.header is not None
        assert field_set.field is not None
        assert field_set.update is not None
        assert field_set.key is not None

    def test_is_tuple(self):
        assert issubclass(ExtensionMappingFieldSet, tuple)
        assert hasattr(ExtensionMappingFieldSet, "_fields")
