
import os 
from pathlib import Path 
from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pypdf import PdfReader
import pandas as pd 
import re, ast 
from PIL import Image 
import pytesseract
from dotenv import load_dotenv
load_dotenv()


model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


# Function to extract text from images
def get_image_text(image_file):
  # Open the image file
  image = Image.open(image_file)
  # Use the tessaract to do OCR on the image
  text = pytesseract.image_to_string(image)
  return text


# Function to extract text from PDF files
def get_pdf_text(pdf_doc):
  text = ""
  pdf_reader = PdfReader(pdf_doc)
  for page in pdf_reader.pages:
    text += page.extract_text()
  return text 


# Function to extract data from text
def extracted_data(pages_data):
  template = """Extract all the following values: Invoice no., Description, Quantity, Date,    Unit price, Amount, Total, GST, email, phone number, Address from this data: {pages}.\n

  Expected Output: remove any dollar symbols {{'Invoice no.': '1001329', 'Description': 'Office Chair', 'Quantity': '2', 'Date': '5/4/2023', 'Unit price': '1100.00', 'Amount': '2200.00',
  'Email': 'abc@gmail.com', 'Phone number': '9999999999', 'Address': 'India'}}"""


  prompt_template = PromptTemplate(template=template, input_variables=["pages"])


  # Prepare the formatted input
  formatted_input = prompt_template.format(pages=pages_data)

  # Call the model using the invoke method with the correct input
  full_response = model.invoke(input=formatted_input)

  return full_response


def create_docs(user_pdf_list):
  data_list = []

  # Define the Dataframe structure
  for filename in user_pdf_list:
    print(f"Processing: {filename}")
    raw_data = get_pdf_text(filename)

    # Call he extraction function
    llm_extracted_data = extracted_data(raw_data)

    # Extract the content from the AIMessage Object
    if hasattr(llm_extracted_data, 'content'):
      llm_extracted_data = llm_extracted_data.content 
    else:
      print("Unexpected response format form the model.")
      continue

    print(llm_extracted_data) 


    invoices = llm_extracted_data.split("\n\n")
    for invoice in invoices:
      invoice_data = {}
      lines = invoice.strip().split("\n")
      for line in lines:
        if ": " in line:
          key, value = line.split(": ", 1)
          invoice_data[key.strip()] = value.strip()
      if invoice_data:
        data_list.append(invoice_data)

    print("----------------Done-------------------")


  # Create a Dataframe from the collected data
  df = pd.DataFrame(data_list)
  return df