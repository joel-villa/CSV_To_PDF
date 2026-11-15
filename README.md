# A CSV to PDF Converter

## OOPs

- main()
  - Settings 
    - Construct with path to settings.json & default_settings.json
    - Map of row number to fonts
  - Converter (.csv, .pdf, settings.json)
    - Loop through columns, loop through rows, use settings.json
    - Writer (may be overkill):
      - constructor takes in a path to a pdf file
      - Methods:
        - write_line(Font, text)
  - CLI
    - Ask for path, allow to edit setting.json with ':e'
    - Path given -> call converter, done
    - ':e':
      - ':q' to go back
      - Show column ordering (change with 'o')
      - Show column fonts (change with 'f')
