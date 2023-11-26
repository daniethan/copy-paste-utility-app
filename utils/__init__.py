import os
from typing import Any, Generator
import pandas as pd


INPUT_DIR = r"D:\projects\side-projects\mcq-extraction-2-xl\resources\completed\latest"


def get_input_files(in_dir: str) -> Generator[str, None, None]:
    return (
        os.path.join(in_dir, filename)
        for filename in os.listdir(in_dir)
        if os.path.isfile(os.path.join(in_dir, filename))
    )


FILES = {os.path.basename(fpath): fpath for fpath in get_input_files(INPUT_DIR)}


def extract_df(excel_file: str) -> pd.DataFrame:
    # Load the Excel file into a Pandas DataFrame
    df = pd.read_excel(excel_file)

    # Replace empty strings with None
    df.replace("", None, inplace=True)

    # Identify rows with missing explanations
    missing_explanations = df[df["Explanation"].isnull()]
    # print(missing_explanations.head())
    return missing_explanations


def fetch_incomplete_MCQ(df: pd.DataFrame) -> Generator[dict[str, Any], Any, None]:
    # Iterate through rows with missing explanations and generate/fetch explanations
    for index, row in df.iterrows():
        question = row["Question"]

        # Collect options dynamically by iterating through columns
        options = {
            col_name: value
            for col_name, value in row.items()
            if col_name.startswith("Option") and isinstance(value, str)
        }

        correct_answer = (
            row["Correct Answer"] if isinstance(row["Correct Answer"], str) else ""
        )

        yield {
            "i": index,
            "Question": question,
            "Options": options,
            "Correct Answer": ", ".join(correct_answer.split()).strip(", "),
        }


def set_explanation_detail(
    df: pd.DataFrame,
    index: int,
    explanation: str,
) -> None:
    df["Explanation"] = df["Explanation"].astype(str)
    df.at[index, "Explanation"] = explanation
    # return df


def save_changes(df: pd.DataFrame) -> None:
    # Save the updated DataFrame back to the Excel file
    df.to_excel("updated_file.xlsx", index=False)


def pretty_print_dict(d: dict):
    pretty_dict = ""
    for k, v in d.items():
        pretty_dict += f"\n{k}: "
        if type(v) == dict:
            for value in v:
                pretty_dict += f"\n {value}: {v[value]}"
            else:
                pretty_dict += "\n"
        else:
            pretty_dict += f"{v}\n"

    return pretty_dict.strip()
