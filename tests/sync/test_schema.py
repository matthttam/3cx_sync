import pytest
from sync.schema import CSVUser, SourceSchema
from pydantic import BaseModel
from typing import Optional
from threecxapi.components.schemas.pbx import User


class ComparisonClass(SourceSchema, BaseModel):
    prop_a: str
    prop_b: str
    prop_c: str


@pytest.fixture(autouse=True)
def reset_comparison_properties():
    ComparisonClass._comparison_properties = None
    yield


class TestSourceSchema:

    def test_set_comparison_properties(self):
        comparison_class = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")
        assert comparison_class._comparison_properties is None
        ComparisonClass.set_comparison_properties(["prop_b", "prop_c"])
        assert comparison_class._comparison_properties == ["prop_b", "prop_c"]

    def test_set_comparison_properties_invalid(self):
        with pytest.raises(TypeError):
            ComparisonClass.set_comparison_properties(('tuple', 'instead', 'of', 'list'))

    def test_comparison_with_different_types(self):
        instance_a = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")
        instance_b = {"prop_a": "a", "prop_b": "b", "prop_c": "c"}
        assert instance_a != instance_b, "Instances of different types should not be equal"

    def test_source_schema_default_comparison_behavior(self):
        comparison_class_a = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")
        comparison_class_b = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")
        assert comparison_class_a == comparison_class_b
        comparison_class_b.prop_a = "TEST"
        assert comparison_class_a != comparison_class_b

    def test_default_comparison_behavior_with_none_properties(self):
        class DefaultComparisonClass(SourceSchema, BaseModel):
            prop_a: Optional[str] = None
            prop_b: Optional[str] = None

        instance_a = DefaultComparisonClass(prop_a=None, prop_b=None)
        instance_b = DefaultComparisonClass(prop_a=None, prop_b=None)

        assert instance_a == instance_b, "Instances with None properties should be equal"

    def test_source_schema_comparison_properties_behavior(self):
        ComparisonClass.set_comparison_properties(["prop_b", "prop_c"])
        modified_comparison_a = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")
        modified_comparison_b = ComparisonClass(prop_a="TEST", prop_b="b", prop_c="c")
        assert modified_comparison_a == modified_comparison_b
        modified_comparison_b.prop_b = "TEST"
        assert modified_comparison_a != modified_comparison_b

    def test_dynamic_comparison_properties_update(self):
        ComparisonClass.set_comparison_properties(["prop_b", "prop_c"])
        modified_comparison_a = ComparisonClass(
            prop_a="a", prop_b="b", prop_c="c"
        )
        modified_comparison_b = ComparisonClass(
            prop_a="x", prop_b="b", prop_c="c"
        )
        assert modified_comparison_a == modified_comparison_b

        # Update _comparison_properties and retest
        ComparisonClass.set_comparison_properties(["prop_a", "prop_b"])
        assert modified_comparison_a != modified_comparison_b

    def test_empty_comparison_properties(self):
        ComparisonClass.set_comparison_properties([])
        instance_a = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")
        instance_b = ComparisonClass(prop_a="a", prop_b="b", prop_c="c")

        # Assuming empty _comparison_properties falls back to comparing all fields
        assert instance_a == instance_b


class TestCSVUser:
    def test_csv_user(self):
        csv_user = CSVUser(Id=None)
        assert isinstance(csv_user, SourceSchema)
        assert isinstance(csv_user, User)
        assert csv_user.Id is None
