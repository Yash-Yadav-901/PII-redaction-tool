### Fully Automated PII Redaction Pipeline for Word Documents (.docx)


1. Project Overview & Approach
The Fully Automated PII Redaction Tool is a robust Python utility designed to scan unstructured and semi-structured Word documents (.docx), detect sensitive Personal Identifiable Information (PII) across 9 distinct categories, and replace them with consistent synthetic placeholders (using the Faker library) while preserving the underlying XML layout, styling, and table integrity.

Hybrid Technical Approach
Rule-Based Pattern Matching (Regex): Used for structured identifiers where strict alphanumeric formats apply (e.g., Email addresses, Phone numbers, Social Security Numbers, Credit Cards, Dates of Birth, IP Addresses, PAN, Aadhaar, and specialized location prefixes like Plot/Gat/Tower).

Natural Language Processing (NER & Linguistics): Utilizes spaCy (en_core_web_sm) combined with custom regex boundary triggers to dynamically discover unstructured personal names and corporate entities in running text and complex tables.

Referential & Contextual Integrity: Uses an internal memory dictionary (pii_mapping) so that every unique instance of a specific individual or company name is mapped to the exact same synthetic placeholder throughout the entire document. It also implements an Exclusion Dictionary to whitelist key statutory, legal, and issuer terms (e.g., SEBI, RoC) to prevent false-positive over-redactions.

2. Tech Stack Used
Python 3.x: Core scripting language.

python-docx: For precise, low-level manipulation of paragraphs, runs, and table cells inside Word documents without corrupting file layouts.

spaCy (en_core_web_sm): For Named Entity Recognition (NER) targeting PERSON and ORG categories.

Faker: For generating realistic synthetic replacement data (names, companies, addresses, emails, dates).

Regular Expressions (re): For fast and accurate structural pattern matching.

3. Tradeoffs & Limitations
Scanned Documents & Image-Based Content (The Image Tradeoff):

Limitation: Word documents that consist entirely of flattened images, scanned ID cards (such as scanned identification cards embedded as graphics), or non-selectable text layers cannot be parsed natively by text-extraction tools like python-docx because the text lives inside pixel matrices rather than XML text nodes.

Tradeoff: The current pipeline targets structural XML text blocks (paragraphs and tables). To handle image-heavy or scanned documents, an Optical Character Recognition (OCR) layer would need to be chained upstream.

Contextual Whitelisting vs. Over-Redaction:

To prevent the script from destroying legal prose, common regulatory terms are whitelisted. While this ensures high precision, highly unique corporate or proprietary nouns can occasionally trigger false matches if they mirror personal naming conventions.

4. Step-by-Step Instructions: How to Run the Script
Follow these command-line instructions to set up your environment and execute the redaction tool locally.

Step 1: Open Terminal and Navigate to Project Directory
Open your command prompt or terminal and ensure you are inside your project folder:


cd \piiredactiontool\scalerai
Step 2: Activate Your Virtual Environment
Activate your Python virtual environment:


venv\Scripts\activate
Step 3: Install Required Dependencies
Ensure all packages (python-docx, faker, spacy) are installed:

pip install -r requirements.txt
python -m spacy download en_core_web_sm
Step 4: Run the Redaction Script
Execute main.py by providing the path to your source Word document and your target output file path wrapped securely in double quotes:

python main.py "input_docs\Red Herring Prospectus (2).docx" "output_docs\Redacted_Output.docx"
Step 5: Verify Output
Upon successful execution, the terminal will confirm the file creation, and you can open output_docs/Redacted_Output.docx to review your completely redacted, layout-preserved document.