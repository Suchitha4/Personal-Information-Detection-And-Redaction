from flask import Flask, request, render_template, send_file, redirect, url_for
import fitz  # PyMuPDF for text positioning
import os
import re

app = Flask(__name__)

# Aadhaar validation
def validate_aadhaar_detection(text, match_start, match_end):
    """Validate Aadhaar detection by checking the next non-space character."""
    next_index = match_end
    while next_index < len(text) and text[next_index].isspace():
        next_index += 1
    # Ensure the next non-space character is NOT a digit
    if next_index < len(text) and text[next_index].isdigit():
        return False
    return True

# PII Detection Logic
def detect_pii_with_validation(text):
    """Detect PII with extra Aadhaar validation."""
    patterns = {
        'Aadhaar': r'\b\d{4}\s\d{4}\s\d{4}\b',
        'PAN': r'\b[A-Z]{5}\d{4}[A-Z]\b',
        'Phone Number': r'\b\d{10}\b',
        'Email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    }

    detected_pii = {}
    for key, pattern in patterns.items():
        matches = [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, text)]
        valid_matches = []
        for match_start, match_end, match_value in matches:
            if key == 'Aadhaar' and not validate_aadhaar_detection(text, match_start, match_end):
                continue  # Skip invalid Aadhaar matches
            valid_matches.append(match_value)
        if valid_matches:
            detected_pii[key] = valid_matches

    return detected_pii

# Redaction Logic
def redact_pdf(input_path, output_path, pii_to_redact):
    """Redact selected PII in the PDF and save as a new file."""
    pdf_document = fitz.open(input_path)

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        text = page.get_text()

        # Detect PII on the page
        detected_pii = detect_pii_with_validation(text)
        if detected_pii:
            for pii_type, values in detected_pii.items():
                # Only redact selected PII
                if pii_type not in pii_to_redact:
                    continue
                for value in values:
                    areas = page.search_for(value)  # Locate the text position
                    for area in areas:
                        # Draw a black rectangle over the PII
                        page.add_redact_annot(area, fill=(0, 0, 0))
                        page.apply_redactions()

    # Save the redacted PDF
    pdf_document.save(output_path)
    pdf_document.close()

# Flask Routes
@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    input_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(input_path)

    # Extract text and detect PII
    text = ""
    pdf_document = fitz.open(input_path)
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()

    detected_pii = detect_pii_with_validation(text)

    return render_template('select_pii.html', pii_types=list(detected_pii.keys()), input_file=file.filename)

@app.route('/redact', methods=['POST'])
def redact_file():
    pii_to_redact = request.form.getlist('pii_types')  # Get selected PII types
    input_file = request.form['input_file']
    input_path = os.path.join('uploads', input_file)
    output_path = os.path.join('uploads', 'redacted_' + input_file)

    # Redact the selected PII types
    redact_pdf(input_path, output_path, pii_to_redact)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
