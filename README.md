### Fully Automated PII Redaction Pipeline for Word Documents (.docx)

#### 1. Project Overview & Approach
The Fully Automated PII Redaction Tool is a robust Python utility designed to scan unstructured and semi-structured Word documents (.docx), detect sensitive Personal Identifiable Information (PII) across 9 distinct categories, and replace them with consistent synthetic placeholders (using the `Faker` library) while preserving the underlying XML layout, styling, and table integrity.

**Hybrid Technical Approach:**
* **Rule-Based Pattern Matching (Regex):** Used for structured identifiers where strict alphanumeric formats apply (e.g., Email addresses, Phone numbers, Social Security Numbers, Credit Cards, Dates of Birth, IP Addresses, PAN, Aadhaar, and specialized location prefixes like Plot/Gat/Tower).
* **Natural Language Processing (NER & Linguistics):** Utilizes spaCy (`en_core_web_sm`) combined with custom regex boundary triggers to dynamically discover unstructured personal names and corporate entities in running text and complex tables.
* **Referential & Contextual Integrity:** Uses an internal memory dictionary (`pii_mapping`) so that every unique instance of a specific individual or company name is mapped to the exact same synthetic placeholder throughout the entire document. It also implements an Exclusion Dictionary to whitelist key statutory, legal, and issuer terms (e.g., SEBI, RoC) to prevent false-positive over-redactions.

---

#### 2. Tech Stack Used
* **Python 3.x:** Core scripting language.
* **`python-docx`:** For precise, low-level manipulation of paragraphs, runs, and table cells inside Word documents without corrupting file layouts.
* **spaCy (`en_core_web_sm`):** For Named Entity Recognition (NER) targeting `PERSON` and `ORG` categories.
* **`Faker`:** For generating realistic synthetic replacement data (names, companies, addresses, emails, dates).
* **Regular Expressions (`re`):** For fast and accurate structural pattern matching.

---

#### 3. Tradeoffs & Limitations
* **Scanned Documents & Image-Based Content (The Image Tradeoff):**
  * *Limitation:* Word documents that consist entirely of flattened images, scanned ID cards (such as scanned identification cards embedded as graphics), or non-selectable text layers cannot be parsed natively by text-extraction tools like `python-docx` because the text lives inside pixel matrices rather than XML text nodes.
  * *Tradeoff:* The current pipeline targets structural XML text blocks (paragraphs and tables). To handle image-heavy or scanned documents, an Optical Character Recognition (OCR) layer would need to be chained upstream.
* **Contextual Whitelisting vs. Over-Redaction:**
  * To prevent the script from destroying legal prose, common regulatory terms are whitelisted. While this ensures high precision, highly unique corporate or proprietary nouns can occasionally trigger false matches if they mirror personal naming conventions.

---

#### 4. Step-by-Step Instructions: How to Run the Script

Follow these command-line instructions to set up your environment and execute the redaction tool locally.

---

**Step 1: Clone the Repository**

Open your terminal (Command Prompt or PowerShell on Windows) and clone the project:

```cmd
git clone <your-repo-url>
cd "piiredactiontool scalerai"
```

---

**Step 2: Create a Virtual Environment**

Create an isolated Python virtual environment to avoid dependency conflicts:

```cmd
python -m venv venv
```

---

**Step 3: Activate the Virtual Environment**

```cmd
# On Windows (Command Prompt)
venv\Scripts\activate

# On Windows (PowerShell)
venv\Scripts\Activate.ps1

# On macOS / Linux
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

---

**Step 4: Install Dependencies**

Install all required Python packages from the requirements file:

```cmd
pip install -r requirements.txt
```

> **Note:** This installs `python-docx`, `Faker`, and `spaCy >= 3.8.0`.  
> spaCy 3.8+ is required for **Python 3.13** compatibility (older versions fail to compile).

---

**Step 5: Download the spaCy Language Model**

The NER engine requires the `en_core_web_sm` English model. Download it with:

```cmd
python -m spacy download en_core_web_sm
```

> If you're on a network with SSL restrictions, install the model wheel directly:
> ```cmd
> pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
> ```

---

**Step 6: Place Your Input Document**

Copy the `.docx` file you want to redact into the `input_docs/` folder:

```
input_docs/
└── YourDocument.docx
```

---

**Step 7: Run the Redaction Tool**

Execute the tool from the project root, passing the input file path and (optionally) the desired output file path:

```cmd
# Basic usage — output saved as "Redacted_Output.docx" in the project root
python main.py "input_docs/YourDocument.docx"

# Custom output path
python main.py "input_docs/YourDocument.docx" "output_docs/Redacted_YourDocument.docx"
```

---

**Step 8: Collect Your Redacted Output**

The redacted file will be saved to the path you specified (or `Redacted_Output.docx` by default). Check the `output_docs/` folder:

```
output_docs/
└── Redacted_YourDocument.docx
```

---

#### 5. PII Categories Detected

| Category | Detection Method | Example |
|---|---|---|
| Email Address | Regex | `john.doe@example.com` → `synth@fake.com` |
| Phone Number | Regex | `+91 98765 43210` → `[fake number]` |
| PAN Number | Regex | `ABCDE1234F` → `[REDACTED_ID]` |
| Aadhaar Number | Regex | `1234 5678 9012` → `[REDACTED_ID]` |
| SSN | Regex | `123-45-6789` → `[REDACTED_ID]` |
| Credit Card | Regex | `4111 1111 1111 1111` → `[REDACTED_ID]` |
| Date of Birth | Regex | `15/08/1990` → `[fake date]` |
| IP Address | Regex | `192.168.1.1` → `[fake IP]` |
| Physical Address | Regex | `Plot No. 12, Andheri` → `[fake address]` |
| Person Names | spaCy NER | `Rajesh Kumar` → `[fake name]` |
| Organisation Names | spaCy NER | `ABC Enterprises Ltd` → `[fake company]` |

---

#### 6. Project Structure

```
piiredactiontool scalerai/
│
├── main.py                  # Entry point — accepts CLI arguments
├── requirements.txt         # Python dependencies
├── .gitignore               # Git exclusions (venv, docs, secrets)
├── README.md                # This file
│
├── src/
│   ├── __init__.py
│   └── redactor.py          # Core PIIDetectionAndRedaction class
│
├── input_docs/              # Place your source .docx files here
└── output_docs/             # Redacted output files are saved here
```