# PII Redaction Tool for Word Documents (.docx)

## Approach

This tool uses a **hybrid detection strategy** to identify and replace PII in `.docx` files:

- **Regex patterns** handle structured identifiers with known formats — emails, phone numbers, PAN, Aadhaar, SSN, credit cards, dates of birth, IP addresses, and physical addresses (e.g., `Plot No.`, `Flat No.`).
- **spaCy NER** (`en_core_web_sm`) handles unstructured text — it dynamically discovers full person names and organisation names that regex alone cannot reliably catch.
- **Faker library** generates consistent synthetic replacements — the same original value always maps to the same fake value throughout the entire document, preserving referential integrity.

Redaction runs in **two passes**: a full document scan first to build a name/org inventory, then a second pass to apply all replacements across paragraphs and table cells.

---

## Precision — What We Chose NOT to Redact

Some numeric identifiers that look sensitive were **deliberately excluded**:

- **Order numbers, Ticket numbers, Application numbers** — not redacted. These are transactional reference codes, not personal identifiers tied to an individual's identity.
- **Financial figures** (e.g., `₹12,34,56,789`, share quantities) — not redacted, though the broad Aadhaar/credit card regex can partially collide with them (see false positives below).
- **Single-token organisation abbreviations** (e.g., `BSE`, `SEBI`, `RBI`) — whitelisted and not redacted, as they are statutory bodies, not PII.

This is a **precision-first design choice**: it's better to leave a borderline identifier untouched than to corrupt legally significant reference numbers in a financial document.

---

## Recall — What We Catch

| PII Type | Detection Method | Coverage |
|---|---|---|
| Email | Regex | High — standard RFC format |
| Phone | Regex | High — handles `+91`, ISD codes, dashes, spaces |
| PAN | Regex | Exact — fixed alphanumeric pattern |
| Aadhaar | Regex | High — 12-digit with optional spaces |
| SSN | Regex | Exact — `NNN-NN-NNNN` format |
| Credit Card | Regex | High — 13–16 digit groups |
| Date of Birth | Regex | High — `DD/MM/YYYY`, `DD-MM-YYYY`, `DD.MM.YYYY` |
| IP Address | Regex | High — standard IPv4 |
| Physical Address | Regex | Partial — triggers on `Plot/Flat/Gat/Survey No.` prefix |
| Person Names | spaCy NER | Moderate — requires ≥ 2 tokens; misses single-word names |
| Organisation Names | spaCy NER | Moderate — context-dependent; generic orgs may be missed |

---

## Known False Positives / Negatives

**False Positives (over-redaction):**
- Large financial numbers (e.g., `12,34,56,789`) can partially match the Aadhaar regex
- Generic two-word capitalized phrases (e.g., `Equity Shares`, `Lead Manager`) may occasionally be tagged as person names by spaCy

**False Negatives (missed PII):**
- Single-word names (e.g., `Rajesh`) are **intentionally skipped** — the false positive rate on common nouns is too high
- Names inside embedded images or scanned content are invisible to `python-docx`
- Abbreviated or non-standard phone formats not matching the regex pattern may be missed

---

## Tradeoffs

- **spaCy small model (`en_core_web_sm`):** Fast and lightweight, but less accurate than larger models on ambiguous or domain-specific names.
- **Exclusion whitelist:** Prevents over-redaction of regulatory terms like *SEBI*, *RBI*, *Board of Directors* — but a person whose name overlaps with a whitelisted word may be missed.
- **Broad phone regex:** Catches most formats but risks colliding with financial numbers.
- **Two-pass design:** Ensures all names are discovered before redaction begins, but reads the full document twice.
- **No image/scanned content support:** `python-docx` only reads XML text nodes — scanned pages are silently skipped.

---

## Extending to a New PII Type

Adding a new PII type takes **one step** — add an entry to the `regex_patterns` list in [`src/redactor.py`](src/redactor.py):

```python
{'type': 'PASSPORT', 'pattern': re.compile(r'\b[A-PR-WY][1-9]\d\s?\d{4}[1-9]\b')}
```

Then add a replacement branch in `get_fake_value()`:

```python
elif piiType == 'PASSPORT':
    replacement = '[REDACTED_PASSPORT]'
```

No other changes needed — the two-pass pipeline picks it up automatically.

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

## Project Structure

```
├── main.py              # CLI entry point
├── src/redactor.py      # Core redaction logic (PIIDetectionAndRedaction class)
├── requirements.txt     # Dependencies
├── input_docs/          # Place source .docx files here
└── output_docs/         # Redacted files saved here
```