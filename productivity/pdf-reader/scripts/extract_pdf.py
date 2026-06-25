import sys
try:
    import pypdf
except ImportError:
    print("Please install pypdf: pip install pypdf")
    sys.exit(1)

def extract_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            text = ""
            for i, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text += f"--- Page {i+1} ---\n{extracted}\n"
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <file.pdf>")
        sys.exit(1)
    print(extract_text(sys.argv[1]))
