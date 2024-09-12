from src.utils.mappers import from_google_sheets_to_gridly, from_gridly_to_google_sheets


def test_from_gridly_to_google_sheets() -> None:
    # arrange
    gridly_record = {
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
                "value": None
            }
        ]
    }
    column_names_mapping = {
        "column1": "Character",
        "column2": "Russian",
        "column3": "English (United States)",
        "column4": "Character limit",
        "column5": "Version",
        "column6": "NarrativeComment"
    }

    # act
    res = from_gridly_to_google_sheets(
        gridly_record=gridly_record,
        column_names_mapping=column_names_mapping
    )

    assert res == {
        "Character": "None",
        "Russian": "Принять",
        "English (United States)": "Accept",
        "Character limit": "0",
        "Version": "1",
        "NarrativeComment": None
    }


def test_from_google_sheets_to_gridly() -> None:
    # arrange
    google_sheets_record = {
        "Record ID": "Accept_Button",
        "Character": "None",
        "Russian": "Принять",
        "English (United States)": "Accept",
        "Character limit": 0,
        "Version": 1,
        "NarrativeComment": None
    }
    column_names_mapping = {
        "Character": "column1",
        "Russian": "column2",
        "English (United States)": "column3",
        "Character limit": "column4",
        "Version": "column5",
        "NarrativeComment": "column6"
    }

    # act
    res = from_google_sheets_to_gridly(
        google_sheets_record=google_sheets_record,
        column_names_mapping=column_names_mapping,
        id_column_name='Record ID'
    )

    # assert
    assert res == {
        "id": "Accept_Button",
        "cells": [
            {
                "columnId": "column1",
                "value": "None"
            },
            {
                "columnId": "column2",
                "value": "Принять"
            },
            {
                "columnId": "column3",
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
                "value": None
            }
        ]
    }
