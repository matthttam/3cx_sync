from pathlib import Path
import platformdirs
from pydantic import BaseModel, Field
from sync.strategy.mapping import MappingField, JSONMappingConfig, JSONMappingConfig, MappingModel
from typing import ClassVar

class ExtensionMappingField(MappingField):
    field: str = Field(default="", description="3CX field for the mapped field")
    header: str = Field(default="", description="CSV header for the mapped field")
    key: bool = Field(default=False, description="Whether this field is a unique key")
    update: bool = Field(default=False, description="Whether this field should be updated")
    static: bool = Field(default=False, description="Whether this field should use a static.")
    static_value: str = Field(default="", description="Value to use if set to static.")


class ExtensionMappingModel(MappingModel):
    csv_path: Path = Field(default=None, description="Path to the CSV file")
    mappings: list[ExtensionMappingField] = Field(
        default_factory=lambda: ExtensionMappingModel.default_mappings.copy(), description="List of Field mappings"
    )

    default_mappings: ClassVar[list[ExtensionMappingField]] = [
            ExtensionMappingField(field="Number", header="Number", key=True),
            ExtensionMappingField(field="FirstName", header="FirstName", update=True),
            ExtensionMappingField(field="LastName", header="LastName", update=True),
            ExtensionMappingField(field="EmailAddress", header="EmailAddress", update=True),
            ExtensionMappingField(field="VMPIN", header="FirVMPINVMPINtName", update=False),
            ExtensionMappingField(field="VMEmailOptions", header="VMEmailOptions", update=False),
            ExtensionMappingField(field="OutboundCallerID", header="OutboundCallerID", update=False),
            ExtensionMappingField(field="SendEmailMissedCalls", header="SendEmailMissedCalls", update=False),
            ExtensionMappingField(field="Enabled", header="Enabled", update=True),
            ExtensionMappingField(field="EnableHotdesking", header="EnableHotdesking", update=False),
            ExtensionMappingField(field="RecordCalls", header="RecordCalls", update=False),
            ExtensionMappingField(field="RecordExternalCallsOnly", header="RecordExternalCallsOnly", update=False),
            ExtensionMappingField(field="VMEnabled", header="VMEnabled", update=False),
            ExtensionMappingField(field="WebMeetingFriendlyName", header="WebMeetingFriendlyName", update=False),
        ]
    

class ExtensionMappingConfig(JSONMappingConfig):
    DEFAULT_FILENAME = "csv_extension_mapping.json"
    MAPPING_MODEL = ExtensionMappingModel

    def get_update_fields(self) -> list[str]:
        """Returns all ExtensionMappingField field values that are set to update."""
        return [mapping.field for mapping in self._model.mappings if mapping.update]

    def get_mapping_dictionary(self) -> dict:
        """Returns a dictionary of 3CX field with the CSV header"""
        return {mapping.field: mapping.header for mapping in self._model.mappings}

class GroupMapping(MappingField):
    group_id: int = Field(default=None, description="3CX group id for the mapping")
    group_name: str = Field(defaults="3CX group name for the mapping")
    header: str = Field(default="", description="CSV header for the mapping")


class GroupMappingConfig(MappingModel):
    path: str = Field(default="", description="Path to the CSV file")
    mappings: list[GroupMapping] = Field(default_factory=list, description="List of Field mappings")


class GroupMapping(JSONMappingConfig):
    DEFAULT_FILENAME = "csv_group_mapping.json"
    MAPPING_MODEL = GroupMappingConfig
