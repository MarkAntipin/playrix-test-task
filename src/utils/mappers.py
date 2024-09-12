def from_gridly_to_google_sheets(
    *,
    gridly_record: dict,
    column_names_mapping: dict[str, str],
) -> dict:
    """
    Gridly record:
    {
        "id": "Accept_Button",
        "cells":
        [
            {
                "columnId": "column1",
                "value": "None"
            },
            {
                "columnId": "column2",
                "sourceStatus": "readyForTranslation",
                "value": "Принять"
            },
            {
                "columnId": "column3",
                "dependencyStatus": "upToDate",
                "value": "Accept"
            },
            {
                "columnId": "column4",
                "value": "0"
            },
            {
                "columnId": "column5",
                "value": "1"
            },
            {
                "columnId": "column6",
                "value": "None"
            }
        ]
    },

    Google Sheets record:
    {
        "Record ID": "Accept_Button",
        "Character": "None",
        "Russian": "Принять",
        "English (United States)": "Accept",
        "Character limit": 0,
        "Version": 1,
        "NarrativeComment": "None"
    }

    Mapping:
    {
        "column1": "Character",
        "column2": "Russian",
        "column3": "English (United States)",
        "column4": "Character limit",
        "column5": "Version",
        "column6": "NarrativeComment"
    }
    """
    return {
        column_names_mapping[cell['columnId']]: cell['value']
        for cell in gridly_record['cells']
    }


def from_google_sheets_to_gridly(
    *,
    google_sheets_record: dict,
    column_names_mapping: dict[str, str],
    id_column_name: str
) -> dict:
    """
    Google Sheets record:
    {
        "Record ID": "Accept_Button",
        "Character": "None",
        "Russian": "Принять",
        "English (United States)": "Accept",
        "Character limit": 0,
        "Version": 1,
        "NarrativeComment": "None"
    }

    Gridly record:
    {
        "id": "Accept_Button",
        "cells":
        [
            {
                "columnId": "column1",
                "value": "None"
            },
            {
                "columnId": "column2",
                "sourceStatus": "readyForTranslation",
                "value": "Принять"
            },
            {
                "columnId": "column3",
                "dependencyStatus": "upToDate",
                "value": "Accept"
            },
            {
                "columnId": "column4",
                "value": "0"
            },
            {
                "columnId": "column5",
                "value": "1"
            },
            {
                "columnId": "column6",
                "value": "None"
            }
        ]
    }

    Mapping:
    {
        "Character": "column1",
        "Russian": "column2",
        "English (United States)": "column3",
        "Character limit": "column4",
        "Version": "column5",
        "NarrativeComment": "column
    }
    """
    return {
        'id': google_sheets_record[id_column_name],
        'cells': [
            {
                'columnId': column_names_mapping[column_name],
                'value': str(column_value) if column_value is not None else None
            }
            for column_name, column_value in google_sheets_record.items()
            if column_name in column_names_mapping
        ]
    }
