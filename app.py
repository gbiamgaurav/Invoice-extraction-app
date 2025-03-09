
import os
import streamlit as st 
from utils import *
from dotenv import load_dotenv
import json  # Import json module

# Load the env variables
load_dotenv()

def main():
    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot")

    # Upload Invoices (PDF files or Image Files)
    uploaded_files = st.file_uploader("Upload Invoices (PDF or Images) here", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

    submit = st.button("Extracted Data")

    if submit:
        if uploaded_files:
            with st.spinner("Extracting data, please wait..."):
                data_list = []
                for uploaded_file in uploaded_files:
                    try:
                        if uploaded_file.type == "application/pdf":
                            raw_data = get_pdf_text(uploaded_file)
                        else:
                            # Assume image formats (jpg, jpeg, png)
                            raw_data = get_image_text(uploaded_file)

                        # Call the extraction function
                        llm_extracted_data = extracted_data(raw_data)

                        # Extract the content from the AIMessage object
                        if hasattr(llm_extracted_data, 'content'):
                            llm_extracted_data = llm_extracted_data.content
                        else:
                            st.error("Unexpected response format from the model.")
                            continue

                        # Display the extracted data in the app
                        st.write("Extracted Data:")
                        st.text(llm_extracted_data)  # Display the extracted data

                        # Process the extracted data 
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

                    except Exception as e:
                        st.error(f"An error occurred while processing {uploaded_file.name}: {e}")

            # Create a DataFrame from the collected data
            df = pd.DataFrame(data_list)

            if not df.empty:
                st.write("Extracted Invoice Data:")
                st.dataframe(df)  # display the dataframe

                # Download as CSV
                data_as_csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download data as CSV",
                    data_as_csv,
                    "extracted_data.csv",
                    "text/csv",
                    key="download-tools-csv",
                )

                # Download as JSON
                data_as_json = df.to_json(orient='records').encode('utf-8')
                st.download_button(
                    "Download data as JSON",
                    data_as_json,
                    "extracted_data.json",
                    "application/json",
                    key="download-tools-json",
                )

                st.success("Extraction Completed!")
            else:
                st.warning("No data extracted. Please check the input files.")
        else:
            st.warning("Please upload at least one PDF or Image file.")

# Invoking the main function
if __name__ == "__main__":
    main()