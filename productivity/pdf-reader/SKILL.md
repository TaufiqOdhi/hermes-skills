---
name: read-pdf
description: "Extract text from PDF files so you can read them and perform tasks based on user prompts."
version: 1.0.0
author: self
license: MIT
---

# Read PDF Skill

This skill allows the agent to extract text from a PDF file using a simple Python script, so the agent can read the document's content and complete tasks based on the user's prompt.

## Prerequisites

You need the `pypdf` package installed.
```bash
# In your terminal or the agent's environment:
pip install pypdf
```

## Usage

When the user asks you to read a PDF and do a task:

1. Use the provided script to extract the text. If the PDF is expected to be large, output it to a text file.
   ```bash
   python ~/.hermes/skills/productivity/pdf-reader/scripts/extract_pdf.py path/to/document.pdf > /tmp/pdf_output.txt
   ```
2. Read the text (e.g., using `view_file` or `grep` on `/tmp/pdf_output.txt`).
3. Complete the task the user requested based on the extracted content!

## Example

**User:** "Read the `report.pdf` and summarize the key findings."

**Agent Action:**
```bash
python ~/.hermes/skills/productivity/pdf-reader/scripts/extract_pdf.py report.pdf > /tmp/report.txt
```
*(Agent reads `/tmp/report.txt` and generates the summary)*
