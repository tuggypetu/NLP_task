
Instructions
----------------------------------------------------------------------------------------------------------------------------

1. Explaining how I approached the solution

    Steps I took to approach the solution:
   
    i. Firstly I read the Objective.docx and Text Analysis.docx files to understand what was the problem statement.
   
    ii. I tried to explore the data.
    - The excel files using pandas
    - The txt word files on vscode
    - Read few articles from the links
   
    iii. Wrote some data scraper code to extract title and text from artilce. Looked through all text for any issues.
    - Some links had error Page not found
    - on some texts had to be removed using regex
   
    iv. Created python class for reading the stopwords, positive words, and negative words data. 
    -  Few complexities and data processing to extract words
   
    v. Created python class to extract metrics from article text
    - nltk library used to generate tokens
    - data preprocessing and stopwords removed from tokens.
    - nltk Syllable tokenizer used for calculating syllables
    - code for calculating metrics based on instructed Text Analysis.docx file
   
    vi. Output metrics appended to dataframe and saved as output.csv

Various complexities were included in the code that are not mentioned in detail.

----------------------------------------------------------------------------------------------------------------------------

2. How to run the .py file to generate output

    The file to run is main.py in the code folder.

-- Create a Virtual Environment:

  - Open a terminal.
  - Navigate to the directory with the main.py file in the code folder:

  - Create a virtual environment inside the project directory. You can use venv: (in terminal)

          python3 -m venv venv

  - Activate the virtual environment:
  
  + On Windows: (in terminal)

          venv\Scripts\activate
  
  + On macOS and Linux: (in terminal)

          source venv/bin/activate

-- Install Dependencies:

    -Install requirements.txt file, you can install the dependencies using pip: (in terminal)

            pip install -r requirements.txt

-- Run main.py Python File: (in terminal)

            python main.py

    - The output.csv file will be generated and saved in the preceeding directory! It takes about 5-10 minutes for the code to run.

-- Deactivate the Virtual Environment: (in terminal)

            deactivate

----------------------------------------------------------------------------------------------------------------------------

3. Include all dependencies required

    The dependencies required are:

        Python>=3.7.7
        beautifulsoup4==4.10.0
        nltk==3.7
        pandas==1.3.5
        Requests==2.31.0
        openpyxl==3.0.9

----------------------------------------------------------------------------------------------------------------------------
