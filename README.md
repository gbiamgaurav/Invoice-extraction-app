# Invoice Extraction App

This **Invoice Extraction App** is a simple web application built with **Streamlit** and powered by the **Google Gemini Flash Model**. It automatically extracts key information from invoices (PDF or image formats), such as **Invoice Number, Description, Quantity, Date, Unit Price, Total Amount**, **GST**, **email**, **phone number**, and **address**.

The app provides a user-friendly interface to upload invoices, process them using Google Gemini Flash's advanced NLP capabilities, and display the extracted data in a structured format. Users can also export the extracted information into a **CSV file** for further analysis or record-keeping.

## Note:

- Please set up your API Keys in the .env file, you can use the LLM as per your choice

## Key Features

- **Streamlit-powered web interface** for an intuitive user experience.
- Support for both **PDF** and **image file uploads**.
- **Google Gemini Flash Model** for fast and accurate data extraction.
- Structured output with essential invoice details.
- Option to **export extracted data as CSV**.
- Open-source and easy to deploy.

---

## How It Works

1. **Upload an Invoice**: Users can upload an invoice in either PDF or image format.
2. **Data Extraction**: The app uses the **Google Gemini Flash Model** to analyze the document and extract relevant details such as invoice number, product description, pricing, and contact information.
3. **View Extracted Data**: The app presents the extracted data in a structured, readable format.
4. **Export Data**: You can export the extracted data to a **CSV** file for further use or analysis.

---

## Installation

### Prerequisites

To run this app, you’ll need the following dependencies installed on your local machine:

- Python 3.x
- **Streamlit**: For building the web app interface.
- **Google Gemini Flash Model**: For document processing.
- Additional dependencies like **pypdf**, **Pillow**, and **pytesseract** for handling PDF and image files.

### Steps to Set Up

1. **Clone the repository**:

   ```bash
   git clone https://github.com/gbiamgaurav/Invoice-extraction-app.git
   cd Invoice-extraction-app
   ```

2. **Install the required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```

## Docker Setup

To run the app using Docker, follow these steps:

1. **Build the Docker image**:

   ```bash
   docker build -t invoice-app .
   ```

2. **Run the Docker container**:

   ```bash
   docker run -p 8501:8501 invoice-app
   ```

You can then access the app at `http://localhost:8501` in your web browser.
