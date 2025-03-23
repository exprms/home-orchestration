#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 07:12:53 2025

@author: bernd
"""

import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def convert_ods_to_csv(input_file, output_file):
    # Read the .ods file
    df = pd.read_excel(input_file, engine='odf')

    # Write the DataFrame to a .csv file
    df.to_csv(output_file, index=False, sep=';')

    print(f"Converted '{input_file}' to '{output_file}'")

if __name__ == "__main__":
    # Example usage
    input_file = os.getenv('ODS_SOURCE')
    output_file = os.getenv('CSV_SOURCE')
    
    convert_ods_to_csv(input_file, output_file)