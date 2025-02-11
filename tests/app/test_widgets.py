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

    def test_destroy(self, field_set):
        field_set.destroy()
        field_set.header.destroy.assert_called_once()
        field_set.field.destroy.assert_called_once()
        field_set.static.destroy.assert_called_once()
        field_set.update.destroy.assert_called_once()
        field_set.key.destroy.assert_called_once()
        field_set.delete.destroy.assert_called_once()

    def test_change_row(self, field_set):
        field_set.change_row(row=500)
        field_set.header.grid.assert_called_once_with(row=500, column=0)
        field_set.field.grid.assert_called_once_with(row=500, column=1)
        field_set.static.grid.assert_called_once_with(row=500, column=2)
        field_set.update.grid.assert_called_once_with(row=500, column=3)
        field_set.key.grid.assert_called_once_with(row=500, column=4)
        field_set.delete.grid.assert_called_once_with(row=500, column=5)

    def test_widgets(self, field_set):
        assert field_set._widgets() == [
            field_set.header,
            field_set.field,
            field_set.static,
            field_set.update,
            field_set.key,
            field_set.delete,
        ]
