from enum import Enum


class ErrorType(Enum):
    INVALID_FOLDER = "Invalid Folder"
    PROCESSING_ERROR = "Processing Error"
    DATABASE_ERROR = "Database Error"
    EXPORT_ERROR = "Export Error"
    STYLING_ERROR = "Styling Error"
    EVENT_ERROR = "Event Error"
    DISPLAY_ERROR = "Display Error"
    UNKNOWN_ERROR = "Unknown Error"
