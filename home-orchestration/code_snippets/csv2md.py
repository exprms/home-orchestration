#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 22:32:42 2025

@author: bernd
"""
import pandas as pd
import argparse
import os

from util.base import MDTag
import util.config as cf
import util.custom_logger as cl


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

def dataframe_to_markdown(df: pd.DataFrame, header: str, column_map: dict):
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
        cl.logger.warning("No Entries with given tags - Creating Empty File")
        return "No data available for the specified filters."
    
    df.rename(columns=column_map, inplace=True)
    
    # Convert DataFrame to Markdown
    markdown_table = df.to_markdown(index=False)
        
    # Construct the Markdown content
    markdown_content = f"\n{header}\n\n{markdown_table}"
    
    return markdown_content


def main(csv_file_path: str, dest_path: str, column_map: dict, sortby: str, tagging: MDTag):
    try:
        
        columns = list(column_map.keys())
        
        # Read the DataFrame from the CSV file
        cl.logger.info(f"Read CSV File {csv_file_path}")
        _df = pd.read_csv(csv_file_path, low_memory=False, sep=";")
        
        # Sort the DataFrame by the 'Name' column in ascending order (A-Z)
        df = _df.sort_values(by=sortby, ascending=True)

        # Check if all specified tags exist in the DataFrame's columns
        for tag in tagging.sorted:
            if tag not in df.columns:
                cl.logger.error(f"Tag '{tag}' does not exist in the CSVFile columns.")
                raise TagNotFoundError("Tag not found")

        # Filter the DataFrame based on the specified tags and select columns
        cl.logger.info(f"Looking for entries with trags: {tagging.tagstring}")
        filtered_df = filter_dataframe(df=df, tags=tagging.sorted, columns=columns)

        # Convert the filtered DataFrame to Markdown format
        cl.logger.info("Creating markdown file")
        markdown_content = dataframe_to_markdown(df=filtered_df, header=tagging.md_header, column_map=column_map)        

        # Create a hash from the tags for the filename
        markdown_file_path = dest_path + 'tags-' + tagging.tagstring + ".md"
        
    
        # Write the YAML header and Markdown content to a Markdown file
        with open(markdown_file_path, 'w') as md_file:
            md_file.write(tagging.yaml_header)
            md_file.write(markdown_content)

        cl.logger.info(f"Written markdown to {markdown_file_path}")

    except TagNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    
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
    main(
        csv_file_path=cf.used_conf.csv_path,
        dest_path=cf.used_conf.dest_path,
        column_map=cf.used_conf.column_map,
        sortby=cf.used_conf.sortby,
        tagging=mdtags
        )

    

    
    
