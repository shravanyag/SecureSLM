import os
import time
from SyntheticData import SyntheticData

class SyntheticBatchProcessor:
    def __init__(self, folder_path, output_path, api_key, endpoint, deployment_name):
        self.folder_path = folder_path
        self.output_path = output_path
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_name = deployment_name

    def process_all_files(self):
        # Loop over all folders inside the parent folder
        for child_folder in os.listdir(self.folder_path):
            child_path = os.path.join(self.folder_path, child_folder)
            
            # Proceed only if it's a directory
            if os.path.isdir(child_path):
                for filename in os.listdir(child_path):
                    if filename.endswith(".csv"):
                        file_path = os.path.join(child_path, filename)
                        
                        print(f"🔍 Processing: {filename} in {child_folder}")
                        sd = SyntheticData(file_path)
                        sd.generate_cleaned_text()
                        sd.generate_response(
                            api_key=self.api_key,
                            endpoint=self.endpoint,
                            deployment_name=self.deployment_name
                        )
                        sd.save_to_csv(self.output_path, append=True)
