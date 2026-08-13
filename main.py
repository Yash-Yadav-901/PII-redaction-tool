import sys
from src.redactor import PIIDetectionAndRedaction

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.docx> [output.docx]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "Redacted_Output.docx"
    
    redactor = PIIDetectionAndRedaction()
    redactor.process_file(input_file, output_file)