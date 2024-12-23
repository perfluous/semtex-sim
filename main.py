from PyPDF2 import PdfReader

# Define the path to the PDF file
file_path = 'sim/Units/Compressor/Documentation/Papers/Review of curren tech in hydrogen compression.pdf'
output_file_path = 'extracted_text.txt'

# Initialize the PdfFileReader object and extract the text
with open(file_path, 'rb') as file:
    pdf_reader = PdfReader(file)
    text_content = ""
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text_content += page.extract_text()

# Write the extracted content to a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(text_content)
