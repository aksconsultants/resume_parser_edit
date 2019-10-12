# Resume-Parser

## Extracting name, email, phonenumber, skills

Code to parse information such as Name, Email, Phone Number, skillset and the technology associated with it.

## Requirements
Following is the list of python libraries required

    cStringIO
    re
    csv
    pdfminer
    BeautifulSoup
    urllib2
    spacy

Spacy is an Industrial-Strength Natural Language Processing tool which is used here to detect Indian Names in the resume after pip installing spacy make sure that you install 'xx' model which supports foreign languages

    python -m spacy download xx
    

## Usage

    $ python resumeparser.py <file path>

## Sample Output

	{'name': 'Jon Snow', 'phone': ['9933995693'], 'email': ['ashaywalke@iitkgp.ac.in'], 'technical skills': ['python', 'opencv', 'c', 'c++', 'scikit-learn', 'matplotlib', 'numpy', 'matlab', 'algorithms'], 'nontechnical skills': []}

