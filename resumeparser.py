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
import win32com.client
def convertdoc(filepath):
    doc = win32com.client.GetObject(filepath)
    filetext = doc.Range().Text
    return filetext
#Function converting pdf to string
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
#Function to extract names from the string using spacy
def extract_name(string):
    r1 = str(string)
    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(r1)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            result = ent.text
            break
    return result
#Function to extract Phone Numbers from string using regular expressions
def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]
#Function to extract Email address from a string using regular expressions
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
#Converting pdf to string
#resume_string = convert("C:\\Users\\User\\Desktop\\work\\resume-parser-master\\resume.pdf")
resume_string = convertdoc("C:\\Users\\User\\Desktop\\work\\resume-parser-master\\resume.docx")
resume_string1 = resume_string
#Removing commas in the resume for an effecient check
resume_string = resume_string.replace(',',' ')
#Converting all the charachters in lower case
resume_string = resume_string.lower()
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
# Remove duplicate elements from a list
def remove_duplicates(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
    
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
entities["name"] = extract_name(resume_string1)
entities["phone"] = extract_phone_numbers(resume_string)
entities["email"] = extract_email_addresses(resume_string)
entities["technical skills"] = remove_duplicates(skills)
entities["nontechnical skills"] = remove_duplicates(nontechskills)

print(entities)

