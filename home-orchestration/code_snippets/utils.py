#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 09:13:55 2025

@author: bernd
"""
import hashlib
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()

class ExportConfig(BaseModel):
    column_map: dict=Field(
        default={
            "id":"id",
            "right":"neměcký",
            "left":"český",
            "info_left":"info",
            }
        )
    csv_path: str=Field(default=os.getenv('CSV_SOURCE'))
    dest_path: str=Field(default=os.getenv('MD_PATH'))
    
    @property
    def cols(self):
        return list(self.column_map.keys())
    
    @property
    def col_names(self):
        return list(self.column_map.values())
    
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
        mdh = "## Vocabel \n \nFilter Tags:\n- "
        if len(self.tags)>0: 
            mdh += '\n- '.join(self.sorted) 
        else:
            mdh += '- ALL'
        return mdh
    
    @property
    def tagstring(self):
        return '-'.join(self.sorted)
    
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
