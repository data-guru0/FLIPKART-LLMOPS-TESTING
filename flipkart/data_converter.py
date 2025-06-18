# Importing pandas library to work with CSV files and dataframes
import pandas as pd

# Importing Document class from LangChain to create structured document objects
from langchain_core.documents import Document

# Defining a class named DataConverter
class DataConverter:
    # Constructor method to initialize the class with the path to the CSV file
    def __init__(self, file_path: str):
        self.file_path = file_path  # Saving the file path to an instance variable

    # Method to convert the CSV data into a list of Document objects
    def convert(self):
        # Reading the CSV file and selecting only the 'product_title' and 'review' columns
        df = pd.read_csv(self.file_path)[["product_title", "review"]]

        # Creating a list of Document objects from each row in the dataframe
        # Each Document contains the review as content and product title as metadata
        docs = [
            Document(page_content=row["review"], metadata={"product_name": row["product_title"]})
            for _, row in df.iterrows()  # Iterating over each row of the dataframe
        ]

        # Returning the list of Document objects
        return docs
