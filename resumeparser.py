import csv
import re
import spacy
import sys
import importlib
importlib.reload(sys)
import pandas as pd
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import docx2txt

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def extract_name(my_text):
    nlp = spacy.load('en')
    doc_2 = nlp(my_text)
    for ent in doc_2.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    return name

#Function to extract Phone Numbers from string using regular expressions
def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

#Function to extract Email address from a string using regular expressions
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
    
# Remove duplicate elements from a list
def remove_duplicates(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

resume = str(sys.argv[1])
filename, file_extension = os.path.splitext(resume)
if file_extension == '.docx':
    resume_string = docx2txt.process(resume)
elif file_extension == '.pdf':
    resume_string = convert(resume)
else:
    print('Unsupported format!')

#Removing commas in the resume for an effecient check
resume_string = resume_string.replace(',',' ')
resume_string = resume_string.replace('\n',' ')

with open('techskill.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)
with open('nontechnicalskills.csv', 'r') as f:
    reader = csv.reader(f)
    your_list1 = list(reader)

#Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
s = set(your_list[0])
s1 = your_list
skillindex = []
skills = []
skillsatt = []
 
for word in resume_string.split(" "):
    if word in s:
        skills.append(word)

#Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
s1 = set(your_list1[0])
nontechskills = []
for word in resume_string.split(" "):
    if word in s1:
        nontechskills.append(word)

entities = {}
        
entities["name"] = extract_name(resume_string)
entities["phone"] = extract_phone_numbers(resume_string)
entities["email"] = extract_email_addresses(resume_string)
entities["technical skills"] = remove_duplicates(skills)
entities["nontechnical skills"] = remove_duplicates(nontechskills)

print(entities)
