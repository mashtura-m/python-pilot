import importlib
import os
import sys
from datetime import datetime
from os.path import exists

import pandas as pd
'''
This file run a file from any directory runs and saves data into parquet file in output folder
'''

def run_scraper(script_name):
    script_path = os.path.join("/home/user/Documents/Automation/python-pilot-mode", "scripts/scrapers", script_name)
    output_dir = os.path.join("/home/user/Documents/Automation/python-pilot-mode", "output/reports", script_name.removesuffix(".py"))
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script Not Found @ {script_path}")
    #create output dir if not found
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        scraper_module = importlib.util.module_from_spec(spec)
        sys.modules[script_name] = scraper_module
        spec.loader.exec_module(scraper_module)

        if hasattr(scraper_module, 'initParsing'):
            output_df = scraper_module.initParsing()
        else:
            raise AttributeError("Script has no output")

        if not isinstance(output_df, pd.DataFrame):
            raise TypeError('OUTPUT is not a data frame')

        currentTime = datetime.now()
        version = currentTime.strftime("%m%d%h%m")
        output_file = os.path.join(output_dir, f'{script_name}_{version}.parquet')
        output_df.to_parquet(output_file, engine='pyarrow', compression='snappy')

        print(f"Scraper {script_path} ran successfully")

    except Exception as e:
        print(f"Error Found: " + e.__str__())


if __name__ == "__main__":
    script_path = sys.argv[1]
    run_scraper(script_path)
