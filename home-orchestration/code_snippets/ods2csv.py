#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 07:12:53 2025

@author: bernd
"""

import os
import pandas as pd
from dotenv import load_dotenv
import util.custom_logger as cl
load_dotenv()

CHECK_FOR_DUPLICATES = 'left'

def convert_ods_to_csv(input_file, output_file):
    # Read the .ods file
    df = pd.read_excel(input_file, engine='odf')

    cl.logger.info(f"check for duplicates in column {CHECK_FOR_DUPLICATES}")
    duplicates = df[df.duplicated([CHECK_FOR_DUPLICATES], keep=False)].sort_values(by=CHECK_FOR_DUPLICATES, ascending=True)

    if not duplicates.empty:
        cl.logger.warning("Found duplicates: -----------------------------------")
        print(duplicates[['id', CHECK_FOR_DUPLICATES]])
        cl.logger.warning("-----------------------------------------------------")
    else:
        cl.logger.info("No duplicates found")

    # Write the DataFrame to a .csv file
    df.to_csv(output_file, index=False, sep=';')

    cl.logger.info(f"Created csv file: '{output_file}'")

if __name__ == "__main__":
    # Example usage
    input_file = os.getenv('ODS_SOURCE')
    output_file = os.getenv('CSV_SOURCE')
    
    convert_ods_to_csv(input_file, output_file)