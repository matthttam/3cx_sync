from sync.schema import CSVUser, SourceSchema
from pydantic import BaseModel


class TestSyncSchema:

    def test_csv_user_optional_id(self):
        csv_user = CSVUser(Id=None)
        assert csv_user.Id is None

    def test_source_schema_default_comparison_behavior(self):
        class ModifiedComparisonClass(SourceSchema, BaseModel):
            prop_a: str
            prop_b: str
            prop_c: str

        modified_comparison_a = ModifiedComparisonClass(
            prop_a="a", prop_b="b", prop_c="c")
        modified_comparison_b = ModifiedComparisonClass(
            prop_a="a", prop_b="b", prop_c="c")
        assert modified_comparison_a == modified_comparison_b
        modified_comparison_b.prop_a = "TEST"
        assert modified_comparison_a != modified_comparison_b

        # Set it to only compare properties b and c

    def test_source_schema_comparison_properties_behavior(self):
        class ModifiedComparisonClass(SourceSchema, BaseModel):
            prop_a: str
            prop_b: str
            prop_c: str
        ModifiedComparisonClass._comparison_properties = ["prop_b", "prop_c"]
        modified_comparison_a = ModifiedComparisonClass(
            prop_a="a", prop_b="b", prop_c="c")
        modified_comparison_b = ModifiedComparisonClass(
            prop_a="TEST", prop_b="b", prop_c="c")
        assert modified_comparison_a == modified_comparison_b
        modified_comparison_b.prop_b = "TEST"
        assert modified_comparison_a != modified_comparison_b


class TestSyncCSV:
    pass


class testSync:
    pass
