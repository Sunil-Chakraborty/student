#Text extraction from pdf and jpeg

#views.py


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text 

def extract_text(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']
        pdf_file_path = r"d:/JU_Student/student_app/r.pdf"
        
        # Save the uploaded PDF file to a specific location
        with open(pdf_file_path, 'wb') as file:
            for chunk in pdf_file.chunks():
                file.write(chunk)

        extracted_text = extract_text_from_pdf(pdf_file_path)

        # Provide the file path for the text file
        text_file_path = "d:/JU_Student/student_app/r.txt"

        # Call the function to save the extracted text to the file
        save_text_to_file(extracted_text, text_file_path)

        return HttpResponse("Text extracted successfully and saved to the file.")
    else:
        return HttpResponse("Please upload a PDF file.")

def save_text_to_file(text, file_path):
    with open(file_path, 'w') as file:
        file.write(text)
        

def extract_text_from_image(image_path):

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)    
    return text

# Provide the path to your JPEG image
image_file_path = r"d:\JU_Student\student_app\us.jpg"
extracted_text = extract_text_from_image(image_file_path)


# Provide the path for the output text file
output_file_path = r"d:\JU_Student\student_app\us.txt"

# Write the extracted text to the file
with open(output_file_path, "w") as file:
    file.write(extracted_text)
print(extracted_text)
print("Text extracted from the image and written to the file successfully.")



urls.py




def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text

# Provide the file path of your PDF file
pdf_file_path = r"d:/JU_Student/student_app/tm.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path)
print(extracted_text)

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Provide the path to your JPEG image
image_file_path = r"d:\JU_Student\student_app\us.jpg"
extracted_text = extract_text_from_image(image_file_path)
print(extracted_text)

