import os
import re
from datetime import datetime
from pymediainfo import MediaInfo
from settings import ALLOWED_ROOT_FOLDER


def extract_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    metadata = {}
    for track in media_info.tracks:
        if track.track_type == "General":
            # Approx Release Date - Format to DD/MM/YYYY
            approx_release_date = format_date(track.encoded_date)

            # Time - Convert duration to minutes:seconds format
            time = track.duration
            if time:
                minutes = int(time // 60000)
                seconds = int((time % 60000) / 1000)
                time_min = f"{minutes}:{seconds:02d}"
            else:
                time_min = "Unknown"

            # File Size - Convert file size to MB
            file_size_bytes = track.file_size
            if file_size_bytes:
                file_size = round(file_size_bytes / (1024 ** 2), 2)  # convert to MB and round to 2 decimal places
                file_size_mb = f"{file_size} MB"
            else:
                file_size_mb = "Unknown"

            # Created Date - Getting today's date and time and formatting it to YY-MM-DD HH:MM:ss
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            metadata['song'] = track.title_sort
            metadata['album'] = track.album_sorted_by
            metadata['artist'] = track.performer_sorted_by
            metadata['approx_release_date'] = approx_release_date
            metadata['time'] = time_min
            metadata['file_size'] = file_size_mb
            metadata['created_date'] = created_date

    return metadata


def format_date(date_str):
    try:
        # Remove timezone if it exists (e.g., "UTC")
        if date_str and " UTC" in date_str:
            date_str = date_str.replace(" UTC", "")

        # Parse and reformat the date string to YYYY-MM-DD
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return "Invalid Date"


def is_valid_folder(file_path):
    return file_path.startswith(ALLOWED_ROOT_FOLDER)

