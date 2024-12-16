import pandas as pd

# Expected structure
REQUIRED_SHEETS = {
    "Course": ["Course ID", "Course Name"],
    "Topic": ["Topic ID", "Topic Name", "Description"],
    "Resource": ["Resource ID", "Resource Name", "Resource Content", "Module ID", "Module Name", "Sub Module ID"],
    "Learner": ["Learner ID", "Name", "Essay", "Module ID", "Submodule ID"]
}

def validate_excel(filepath):
    try:
        # Load Excel file
        excel_data = pd.ExcelFile(filepath)
        validation_results = {}

        # Check if the number of required sheets is correct
        if len(REQUIRED_SHEETS) != 4:
            return {"status": "error", "message": "Validation failed: Expected 4 sheets in REQUIRED_SHEETS."}

        # Validate each sheet
        for sheet, required_columns in REQUIRED_SHEETS.items():
            if sheet not in excel_data.sheet_names:
                validation_results[sheet] = f"Sheet '{sheet}' is missing."
                continue

            # Load the sheet data
            sheet_data = pd.read_excel(filepath, sheet_name=sheet)

            # Check for missing columns
            missing_columns = [col for col in required_columns if col not in sheet_data.columns]
            if missing_columns:
                validation_results[sheet] = f"Missing columns: {', '.join(missing_columns)}"
                continue

            # Check for empty values in required columns
            empty_columns = []
            for col in required_columns:
                if sheet_data[col].isnull().any() :
                    empty_columns.append(col)

            if empty_columns:
                validation_results[sheet] = f"Columns with empty values: {', '.join(empty_columns)}"
            elif sheet_data.empty:
                validation_results[sheet] = "Sheet is empty."
            else:
                validation_results[sheet] = "Valid."

        # Compile results
        if all(value == "Valid." for value in validation_results.values()):
            return {"status": "success", "message": "Excel file is valid.", "details": validation_results}
        else:
            return {"status": "error", "message": "Excel file validation failed.", "details": validation_results}

    except Exception as e:
        return {"status": "error", "message": "Error reading Excel file.", "details": str(e)}
