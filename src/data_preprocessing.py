import pandas as pd
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = Path(__file__).parent.parent

DATA_PATH = project_root / "data"/ "raw"
OUTPUT_PATH = project_root / "data"/ "processed"

cols_to_keep = [
    "linkedinProfileUrl", "firstName", "lastName", "companyName",
    "linkedinCompanyUrl", "linkedinJobTitle", "linkedinJobDateRange",
    "companyIndustry", "linkedinHeadline", "location"
]

def preprocess_data():
    try:
        logger.info("Starting preprocessing of data")
        logger.info("Reading data from csv")
        df = pd.read_csv(DATA_PATH / "linkedin_leads.csv")

        logger.info("Preprocessing data")
        df = df[cols_to_keep]
        df = df.dropna(subset=["companyName"])

        df["linkedinJobTitle"] = df["linkedinJobTitle"].fillna("Unknown Job Title")
        df["linkedinCompanyUrl"] = df["linkedinCompanyUrl"].fillna("")
        df["linkedinJobDateRange"] = df["linkedinJobDateRange"].fillna("")

        logger.info("Saving data to csv")
        df.to_csv(OUTPUT_PATH / "linkedin_leads_processed.csv", index=False)

        logger.info("Preprocessing completed")
    except Exception as e:
        logger.error("Error occurred during preprocessing: {}".format(e))
        raise e

if __name__ == "__main__":
    preprocess_data()



    
    