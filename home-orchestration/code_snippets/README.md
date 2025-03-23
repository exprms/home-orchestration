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

The output is a markdown table with the 4 four columns filter for the given tags. For more individuality, check `utils.py`, here you can map your custom headers.

Create a `.env` file in your directory:
```
CSV_SOURCE=<path to your csv>
MD_PATH=<path to output directory>
```

Call the function
```bash
python csv2md.py  <tag1> <tag2> <tag3> ...
```

## Requirements
- pandas

