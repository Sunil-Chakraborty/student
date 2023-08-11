import fitz  # PyMuPDF
import requests
from urllib.parse import urlparse
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the PDF file path
pdf_filename = "Book3.pdf"
pdf_path = os.path.join(current_directory, pdf_filename)
# Load the PDF file

pdf_document = fitz.open(pdf_path)
#response = requests.get(pdf_document, timeout=10)  # Timeout set to 10 seconds

# Iterate through each page of the PDF
for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    links = page.get_links()

    # Iterate through each link on the page
    for link in links:
        link_url = link.get("uri")
        parsed_url = urlparse(link_url)
        if parsed_url.scheme in ["http", "https"]:
            response = requests.get(link_url)
            if response.status_code == 200:
                # Extract the filename from the URL
                filename = link_url.split("/")[-1]
                
                # Save the content to a separate file
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {link_url}")

# Close the PDF document
pdf_document.close()
