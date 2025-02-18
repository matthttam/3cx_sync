import platformdirs
from pydantic import BaseModel, Field
from sync.strategy.mapping import JSONMapping, JSONMappingNew


class ExtensionMapping(BaseModel):
    field: str = Field(default="", description="3CX field for the mapped field")
    header: str = Field(default="", description="CSV header for the mapped field")
    key: bool = Field(default=False, description="Whether this field is a unique key")
    update: bool = Field(default=False, description="Whether this field should be updated")
    static: bool = Field(default=False, description="Whether this field should use a static.")
    static_value: str = Field(default="", description="Value to use if set to static.")


class CSVExtensionMappingModel(BaseModel):
    path: str = Field(default=platformdirs.user_documents_dir(), description="Path to the CSV file")
    mappings: list[ExtensionMapping] = Field(
        default_factory=lambda: CSVExtensionMappingModel.default_mappings(), description="List of Field mappings"
    )

    @classmethod
    def default_mappings(cls):
        return [
            ExtensionMapping(field="Number", header="Number", key=True),
            ExtensionMapping(field="FirstName", header="FirstName", update=True),
            ExtensionMapping(field="LastName", header="LastName", update=True),
            ExtensionMapping(field="EmailAddress", header="EmailAddress", update=True),
            ExtensionMapping(field="VMPIN", header="FirVMPINVMPINtName", update=False),
            ExtensionMapping(field="VMEmailOptions", header="VMEmailOptions", update=False),
            ExtensionMapping(field="OutboundCallerID", header="OutboundCallerID", update=False),
            ExtensionMapping(field="SendEmailMissedCalls", header="SendEmailMissedCalls", update=False),
            ExtensionMapping(field="Enabled", header="Enabled", update=True),
            ExtensionMapping(field="EnableHotdesking", header="EnableHotdesking", update=False),
            ExtensionMapping(field="RecordCalls", header="RecordCalls", update=False),
            ExtensionMapping(field="RecordExternalCallsOnly", header="RecordExternalCallsOnly", update=False),
            ExtensionMapping(field="VMEnabled", header="VMEnabled", update=False),
            ExtensionMapping(field="WebMeetingFriendlyName", header="WebMeetingFriendlyName", update=False),
        ]


class CSVExtensionMapping(JSONMappingNew):
    DEFAULT_FILENAME = "csv_extension_mapping.json"
    DEFAULT_MODEL = CSVExtensionMappingModel


class GroupMapping(BaseModel):
    group_id: int = Field(default=None, description="3CX group id for the mapping")
    group_name: str = Field(defaults="3CX group name for the mapping")
    header: str = Field(default="", description="CSV header for the mapping")


class GroupMappingModel(BaseModel):
    path: str = Field(default=platformdirs.user_documents_dir(), description="Path to the CSV file")
    mappings: list[GroupMapping] = Field(default_factory=list, description="List of Field mappings")


class CSVGroupMapping(JSONMappingNew):
    DEFAULT_FILENAME = "csv_group_mapping.json"
    DEFAULT_MODEL = GroupMappingModel
