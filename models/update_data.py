import os
import re
import pandas as pd
from datetime import datetime


def remove_outer_inverted_commas(text):
    """
  Removes inverted commas (") from the beginning and end of a string, if present.

  Args:
    text: The string to process.

  Returns:
    The string with the outer inverted commas removed, if present. Otherwise, the original string.
  """

    # Use regular expressions to match and remove outer inverted commas
    pattern = r'^"(.*?)"$'
    match = re.match(pattern, text)

    if match:
        return match.group(1)  # Return the inner content
    else:
        return text  # No change if no outer inverted commas


def get_labeled_files(files):
    labeled_files = {"DELIVERED": [],
                     "EXCEPTIONS": [],
                     "RETURNED": [],
                     "PICKUP": []}

    for file in files:
        if ("DELIVERED" in file.upper()):
            labeled_files['DELIVERED'].append(file)
        elif ("EXCEPTIONS" in file.upper()):
            labeled_files['EXCEPTIONS'].append(file)
        elif ("RETURNED" in file.upper()):
            labeled_files['RETURNED'].append(file)
        elif ("PICKUP" in file.upper()):
            labeled_files['PICKUP'].append(file)

    return labeled_files


def process_dataframe(df, status):
    df = df.rename(columns={'Card ID': 'CARD_ID', 'User contact': "USER_CONTACT", "User Mobile": "USER_CONTACT",
                            "Timestamp": "TIMESTAMP", "Comment": "COMMENT"})
    # appling regex only to object types columns
    df[df.select_dtypes(include=['object']).columns.values] = df.select_dtypes(include=['object']).map(
        remove_outer_inverted_commas)
    df["USER_CONTACT"] = df["USER_CONTACT"].astype('int64')

    # pick up last 9 digits of contant number
    df["USER_CONTACT"] = df["USER_CONTACT"].map(lambda x: str(x)[-9:])
    df["STATUS"] = status

    def parse_flexible_format(timestamp):
        for fmt in (
        '%d-%m-%Y %I:%M %p', '%d-%m-%Y %I:%M%p', '%d-%m-%Y %H:%M', '%Y-%m-%dT%H:%M:%SZ'):  # Add more formats if needed
            try:
                return datetime.strptime(timestamp, fmt)
            except ValueError:
                pass  # Try the next format
        raise ValueError(f"Unrecognized timestamp format: {timestamp}")

        # Apply the appropriate parsing function based on the format

    df['TIMESTAMP'] = df['TIMESTAMP'].apply(parse_flexible_format)
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    return df



