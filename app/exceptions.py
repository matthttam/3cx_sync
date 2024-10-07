class ConfigSaveError(Exception):
    """Exception raised when there is a failure to save the configuration file."""

    def __init__(self, message="Failed to save the configuration file"):
        self.message = message
        super().__init__(self.message)
