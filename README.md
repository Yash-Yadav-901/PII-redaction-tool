# PII Redaction Tool for Word Documents (.docx)

## Approach

This tool uses a **hybrid detection strategy** to identify and redact Personally Identifiable Information (PII) from `.docx` files:

- **Regex patterns** handle structured identifiers with known formats — emails, phone numbers, PAN, Aadhaar, SSN, credit cards, dates of birth, IP addresses, and physical addresses (e.g., `Plot No.`, `Flat No.`).
- **spaCy NER** (`en_core_web_sm`) handles unstructured text — it dynamically discovers full person names and organisation names that regex cannot reliably catch.
- **Faker library** generates consistent synthetic replacements — the same original value always maps to the same fake value throughout the document, preserving referential integrity.

Redaction runs in two passes: first a full document scan to build a name/org inventory, then a second pass to apply all replacements across paragraphs and table cells.

---

## Tradeoffs

| Decision | Tradeoff |
|---|---|
| spaCy `en_core_web_sm` (small model) | Fast and lightweight, but less accurate than larger models on ambiguous or domain-specific names |
| Exclusion whitelist for legal/financial terms | Prevents over-redaction of terms like *SEBI*, *RBI*, *Board of Directors* — but a genuinely named person who shares a whitelisted word may be missed |
| Regex for phone numbers | Broad pattern catches most formats but can produce false positives on numeric sequences like share quantities or financial figures |
| Two-pass design | Ensures all names are discovered before redaction starts, but doubles the document read time |
| Image/scanned content not supported | `python-docx` only reads XML text nodes — embedded images or scanned pages are silently skipped |

---

## Known False Positives / Negatives

**False Positives (over-redaction):**
- Large numbers (e.g., `₹12,34,56,789`) can partially match the Aadhaar or credit card regex pattern
- Generic two-word capitalized phrases (e.g., `Equity Shares`, `Lead Manager`) may occasionally be flagged as person names by spaCy

**False Negatives (missed PII):**
- Single-word names (e.g., `Rajesh`) are intentionally excluded — too many false positives with common nouns
- Names that appear only in image-based content or headers/footers outside the XML text layer are not detected
- Informal or abbreviated phone formats not matching the regex may be missed

---

## Setup & Usage

**Requirements:** Python 3.10+, pip

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd "piiredactiontool scalerai"

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the spaCy model
python -m spacy download en_core_web_sm

# 5. Run the tool
python main.py "input_docs/YourDocument.docx" "output_docs/Redacted.docx"
```

> **SSL issues with `spacy download`?** Install the model wheel directly:
> ```bash
> pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
> ```

---

## PII Categories Detected

| Category | Method |
|---|---|
| Email, Phone, PAN, Aadhaar, SSN, Credit Card, DOB, IP, Address | Regex |
| Person names, Organisation names | spaCy NER |

---

## Project Structure

```
├── main.py              # CLI entry point
├── src/redactor.py      # Core redaction logic
├── requirements.txt     # Dependencies
├── input_docs/          # Place source .docx files here
└── output_docs/         # Redacted files saved here
```