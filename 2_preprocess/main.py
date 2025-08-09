from SyntheticBatchProcessor import SyntheticBatchProcessor

processor = SyntheticBatchProcessor(
    folder_path="C:\\Users\\shrav\\Documents\\MTECH\\Sem IV\\SecureSLM\\PreProcessing\\new",
    output_path="new_output.csv",
    api_key="my_key",
    endpoint="https://shrav-mckii6fb-eastus2.cognitiveservices.azure.com/",
    deployment_name="gpt-4o"
)

processor.process_all_files()

#M2tMQ5DGXcyJNY45FQS8syNc9RdDtgSCjPic9Tdb0DYh6AVZCd93JQQJ99BGACHYHv6XJ3w3AAAAACOGpz6C
