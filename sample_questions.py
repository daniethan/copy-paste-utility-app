import os
from typing import Any, Generator
import pandas as pd

QUESTIONS = [
    "Question: What is the primary purpose of a firewall in computer networks?\nOptions:\nA) To encrypt data transmissions\nB) To prevent unauthorized access\nC) To boost network speed\nD) To detect hardware failures\nCorrect Answer: B) To prevent unauthorized access\nProvide a precise and concise rationale for the correct answer.",
    "Question: How does encryption contribute to data security?\nOptions:\nA) It slows down data transmission\nB) It protects data from unauthorized access\nC) It increases hardware failures\nD) It hampers network speed\nCorrect Answer: B) It protects data from unauthorized access\nExplain briefly the role of encryption in data security.",
    "Question: What is the purpose of a VPN in networking?\nOptions:\nA) To expose network vulnerabilities\nB) To ensure slow network connections\nC) To create secure, private connections\nD) To enhance hardware failures\nCorrect Answer: C) To create secure, private connections\nProvide a concise rationale for VPN's role in networking.",
    "Question: Why is multi-factor authentication essential?\nOptions:\nA) It decreases security risks\nB) It simplifies access control\nC) It adds an extra layer of security\nD) It limits network access\nCorrect Answer: C) It adds an extra layer of security\nBriefly explain the importance of multi-factor authentication.",
    "Question: How do intrusion detection systems contribute to network security?\nOptions:\nA) They slow down network performance\nB) They prevent all types of attacks\nC) They identify and respond to suspicious activities\nD) They boost network speed\nCorrect Answer: C) They identify and respond to suspicious activities\nExplain the role of intrusion detection systems in network security.",
    "Question: What is the primary function of an antivirus program?\nOptions:\nA) To introduce malware\nB) To protect against malware\nC) To encrypt data transmissions\nD) To enhance hardware failures\nCorrect Answer: B) To protect against malware\nProvide a brief rationale for the necessity of antivirus programs.",
    "Question: Why is regular software patching important in network security?\nOptions:\nA) It increases vulnerability\nB) It enhances system performance\nC) It reduces security risks\nD) It impacts network speed\nCorrect Answer: C) It reduces security risks\nBriefly explain the significance of regular software patching in network security.",
    "Question: What role does a proxy server play in network security?\nOptions:\nA) It exposes IP addresses\nB) It hides IP addresses\nC) It reduces network performance\nD) It boosts network speed\nCorrect Answer: B) It hides IP addresses\nExplain the purpose of a proxy server in network security.",
    "Question: How does a DDoS attack impact network operations?\nOptions:\nA) It enhances network speed\nB) It overloads systems, causing disruption\nC) It reduces the risk of data breaches\nD) It improves hardware performance\nCorrect Answer: B) It overloads systems, causing disruption\nBriefly explain the impact of a DDoS attack on network operations.",
    "Question: Why is access control essential for network security?\nOptions:\nA) It restricts authorized access\nB) It facilitates unrestricted access\nC) It complicates network management\nD) It slows down hardware performance\nCorrect Answer: A) It restricts authorized access\nProvide a concise rationale for the importance of access control in network security.",
]

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
    df: pd.DataFrame, index: pd.Index, explanation: str
) -> pd.DataFrame:
    df.at[index, "Explanation"] = explanation
    return df


def save_changes(df: pd.DataFrame) -> None:
    # Save the updated DataFrame back to the Excel file
    df.to_excel("updated_file.xlsx", index=False)
