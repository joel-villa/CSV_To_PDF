# A CSV to PDF Converter

If you're reading this, I bet you're a very cool person B)

## Running The Program (in Linux)

### 1. Clone the repository in the terminal command line to your desired directory

For notes on installing git: https://git-scm.com/install/linux

```
git clone https://github.com/joel-villa/CSV_To_PDF.git
```

### 2. Install python if necessary 

See: https://docs.python-guide.org/starting/install3/linux/

### 3. Create a virtual python environment inside the CSV_to_PDF folder 

this is where all installed python resources will live

```
cd CSV_to_PDF
python -m venv venv
```

If that doesn't work try...

```
python3 -m venv venv
```

### 4. Load the virtual environment you just created

```
source venv/bin/activate
```

If you get the following error try running this command: `source venv/bin/activate.fish`

```
venv/bin/activate (line 40): 'case' builtin not inside of switch block
case "$(uname)" in
^~~^
```

You should now see in your terminal an indicator that you are using a 
virtual inveronment "(venv)", if you want to exit it without closing the terminal
run `deactivate`

### 5. Load the requirements necessary for the project

```
pip install -r requirements.txt
```

### 6. Run the program!

```
python -m src.main
```

- You should be prompted to paste the path to your .csv file and to create settings 
- A pdf file of the same name as the csv will be created in the same directory that the .csv file lives!
- Hope this helps!
