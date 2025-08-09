import pandas as pd
import os

class PreProcess:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path, encoding='utf-8', engine='python')
        self.cleaned_text = ""

    def handle_float_nans(self):
        float_columns = ['EventId', 'ProcessId', 'ParentProcessId']
        for col in float_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(-1)

    def remove_nans(self):
        self.df.fillna('', inplace=True)

    def normalize_text(self):
        def normalize(value):
            return str(value).replace(',', ' ').replace('\n', ' ').replace('\r', '').strip()
        for col in self.df.select_dtypes(include='object').columns:
            self.df[col] = self.df[col].map(normalize)


    def select_columns(self):
        columns_to_keep = [
            'TimeCreated', 'EventId', 'ProcessId', 'ParentProcessId',
            'Image', 'CommandLine', 'ParentImage', 'ParentCommandLine',
            'CurrentDirectory', 'User', 'IntegrityLevel'
        ]
        self.df = self.df[columns_to_keep]

    def rows_to_paragraphs(self):
        def row_to_paragraph(row):

            return (
                f"On {row['TimeCreated']}, Event ID {row['EventId']} occurred. "
                f"Process '{row['Image']}' (PID: {row['ProcessId']}) was launched using the command: {row['CommandLine']}. "
                f"It was spawned by '{row['ParentImage']}' (PID: {row['ParentProcessId']}) with command: {row['ParentCommandLine']}. "
                f"The process ran in directory '{row['CurrentDirectory']}' under user '{row['User']}' "
                f"with an integrity level of '{row['IntegrityLevel']}'."
            )
        self.df['log_paragraph'] = self.df.apply(row_to_paragraph, axis=1)

    def create_megastring(self):
        self.cleaned_text = '\n'.join(self.df['log_paragraph'].tolist())

    def run_pipeline(self):
        self.handle_float_nans()
        self.remove_nans()
        self.normalize_text()
        self.select_columns()
        self.rows_to_paragraphs()
        self.create_megastring()