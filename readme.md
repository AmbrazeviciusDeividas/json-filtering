This is python script which filters whatever data you need from any size of JSON file and outputs what you need from the file.

# Usage

where you will see ``[]`` it means that you need to inset specific fields, what - you will get inside these brackets.

### Commands need to be runned

``python3 filter.py json_file.json -o filtered_.json --include-line-number --skip-parse-errors``

``--include-line-number`` - optional, but it shows in which line it finded your filtered data

``--skip-parse-error`` - optional, but recomended - script does not stop if it finds some errors
