#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 22:32:42 2025

@author: bernd
"""
import pandas as pd
import argparse
import hashlib
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from a .env file
load_dotenv()


class MDTag(BaseModel):
    tags: list[str]
    
    @property
    def sorted(self):
        # remove duplicates
        tmp = list(set(self.tags))
        return sorted(tmp)
    
    @property
    def chksm(self):
        return create_hash_from_tags(self.sorted)
    
    @property
    def yaml_header(self, prefix:str=''):
        yaml_header = f"---\nchksum: {self.chksm}\n"
        if len(self.tags)>0: 
            yaml_header +=  'tags:\n  - ' + '\n  - '.join([f"{prefix}{item}" for item in self.sorted])
        yaml_header += '\n---'
        return yaml_header
    
    @property
    def md_header(self):
        mdh = "##Vocabeln \n \n Filter Tags:"
        if len(self.tags)>0: 
            mdh += '\n- '.join(self.sorted) 
        else:
            mdh += '- ALL'
        return mdh
    
    @property
    def tagstring(self):
        return '-'.join(self.sorted)

class TagNotFoundError(Exception):
    """Custom exception for when a tag is not found in the DataFrame."""
    pass

def filter_dataframe(df: pd.DataFrame, tags:list[str], columns: list[str]):
    """
    Filters the DataFrame for rows that contain any of the specified tags 
    and selects only the specified columns.

    Parameters:
    - df: pd.DataFrame, the DataFrame to filter
    - tags: list of str, the tags to filter by
    - columns: list of str, the columns to select

    Returns:
    - pd.DataFrame: the filtered DataFrame
    """
    if tags==[]:
        return df[columns]
    
    # Create a filter condition for each tag provided
    filter_condition = df[tags].any(axis=1)

    # Apply the filter condition to get the filtered DataFrame
    filtered_df = df[filter_condition][columns]

    return filtered_df

def dataframe_to_markdown(df: pd.DataFrame, header: str):
    """
    Converts the DataFrame to a Markdown formatted string with a specified header.

    Parameters:
    - df: pd.DataFrame, the DataFrame to convert
    - header: str, the header to include in the Markdown

    Returns:
    - str: Markdown formatted string
    """
    # Return a message if the DataFrame is empty
    if df.empty:
        return "No data available for the specified filters."
    
    # Convert DataFrame to Markdown
    markdown_table = df.to_markdown(index=False)
        
    # Construct the Markdown content
    markdown_content = f"{header}\n\n{markdown_table}"
    
    return markdown_content

def create_hash_from_tags(tags: list[str]):
    """
    Creates a hash from the given tags to be used as a filename.

    Parameters:
    - tags: list of str, the tags to hash

    Returns:
    - str: a hexadecimal string of the hash
    """
    if tags==[]:
        str2hash = 'no_filter'
    else:
        # Join tags into a single string and encode it
        str2hash = ','.join(sorted(tags))  # Sort to ensure consistent hashing
    
    hash_object = hashlib.md5(str2hash.encode())
    return hash_object.hexdigest()


def main(csv_file_path: str, dest_path: str, columns: list[str], tagging: MDTag):
    try:
        # Read the DataFrame from the CSV file
        df = pd.read_csv(csv_file_path, low_memory=False, sep=";")

        # Check if all specified tags exist in the DataFrame's columns
        for tag in tagging.sorted:
            if tag not in df.columns:
                raise TagNotFoundError(f"Tag '{tag}' does not exist in the DataFrame columns.")

        # Filter the DataFrame based on the specified tags and select columns
        filtered_df = filter_dataframe(df=df, tags=tagging.sorted, columns=columns)

        # Convert the filtered DataFrame to Markdown format
        markdown_content = dataframe_to_markdown(df=filtered_df, header=tagging.md_header)        

        # Create a hash from the tags for the filename
        markdown_file_path = dest_path + 'tags-' + tagging.tagstring + ".md"

        # Print the Markdown content for debugging
        print(markdown_file_path)
        print("Generated Markdown Content:")
        print(tagging.yaml_header)
        print(markdown_content)

        # Write the YAML header and Markdown content to a Markdown file
        #with open(markdown_file_path, 'w') as md_file:
            
        #    md_file.write(yaml_header)
        #    md_file.write(markdown_content)

        print(f"Filtered DataFrame written to {markdown_file_path}")

    except TagNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    
    source_path = os.getenv('CSV_SOURCE')
    selected_columns = os.getenv('FILTER_COLUMNS').split(',')  
    dest_path = os.getenv('MD_PATH')
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Filter DataFrame by tags and save to Markdown with a hash filename.')
    # parser.add_argument('csv_file', type=str, help='Path to the CSV file containing the DataFrame.')
    parser.add_argument('tags', nargs='*', help='Optional list of tags to filter by (e.g., tag1 tag2 tag3).')

    args = parser.parse_args()

    if not args.tags:
        tags = []
    else:
        tags = args.tags
        
    mdtags = MDTag(tags=tags)

    # Call the main function with parsed arguments
    main(csv_file_path=source_path, dest_path=dest_path, columns=selected_columns, tagging=mdtags)

    

    
    
