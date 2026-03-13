# Personal-Information-Detection-And-Redaction
In today’s digital landscape, the protection of sensitive information is a growing concern,especially with the increasing exchange of documents containing Personally Identifiable Information (PII). This project proposes a robust system for the automated detection and redaction of PII from PDF documents using a hybrid approach involving regular expressions, contextual validation, and PDF processing techniques. The system is designed to identify critical data types such as Aadhaar numbers, PAN numbers, phone numbers, and email addresses, ensuring accuracy through additional validation, particularly for Aadhaar patterns. Built using Flask for the web interface and PyMuPDF (Fitz) for precise PDF manipulation, the system allows users to upload a document, view detected PII, choose which elements to redact, and download a clean, redacted version. Unlike conventional detection-only systems or manual redaction tools, this project offers end-to-end privacy preservation, combining accuracy, user control, and security. This solution is especially useful in contexts where sensitive data must be shared without compromising confidentiality, such as legal, financial, and governmental documentation.

SOFTWARE REQUIREMENTS :
Operating System :  Windows 11       

Coding Language :  Python   3.10.7, Html, CSS    

Libraries/Frameworks :  Flask, PyMuPDF (fitz), re (Regular Expressions) 

Web Server :  Flask development server 

HARDWARE REQUIREMENTS 

System  :intel i5 or above

project:
app.py
templates
|
--select_pii.html
--uploads.html
