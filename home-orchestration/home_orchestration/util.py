from pydantic import BaseModel
from typing import List, Optional

# data laoding: ==============================

class FieldMapper(BaseModel):
    name: str
    columns: list[str]
    
class CSVFileMapper(FieldMapper):
    json_columns: FieldMapper
     
    @property
    def source_column_names(self) -> list[str]:
        return self.columns + self.json_columns.columns
    
    @property
    def target_column_names(self) -> list[str]:
        return self.columns + [self.json_columns.name]  
    

