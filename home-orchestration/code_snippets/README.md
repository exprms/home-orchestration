# Code Snippets

This repo contains useful code snippets

- **`csv2md.py`**
- ...

## csv2md.py

A Python function that filters a CSV file for specified tags and writes the results to a Markdown table. 
The csv table requires the following columns
- id
- left
- right
- info_left
- *tag_1*
- *tag_2*
- ... 

The output is a markdown table with the 4 four columns filter for the given tags. 

My personal use case for this file:
- i am collecting german-czech vocabs in an .ods file. There i am tagging the words, e.g. *restaurant*, *color*, *months*,...
- i am also using obsidian for learning czech
- so i want to create obsidian-md files in my vault, that gives me a nice vocab table to a given topic. Makes learning easier.


If you check `utils.py`, here you can see a column-map. The column names on the left side are required in the csv file and will be printed in the markdown. The names on the right side  are the column names in the generetaed markdown file. You can individualize your csv headers there.

**utils.py**
```
column_map: dict=Field(
        default={
            "id":"id",
            "right":"neměcký",
            "left":"český",
            "info_left":"info",
            }
        )
```

**Create a `.env` file in your directory:**
```
CSV_SOURCE=<path to your csv>
MD_PATH=<path to output directory>
```

**Call the function**
```bash
python csv2md.py  <tag1> <tag2> <tag3> ...
```

## Requirements
- pandas

