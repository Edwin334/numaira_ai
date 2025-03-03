import os
import sys
import logging
from config import Config
from utils.logging import setup_logging
from utils.document_processing.processor import process_files_with_selected_data, find_changes

# Load configuration
config = Config()
for key, value in config.get_env_vars().items():
    os.environ[key] = value

# Set up logging
logger = setup_logging(level=logging.ERROR)  # Only show ERROR logs

def main(docx_data=None, excel_data=None):
    """Main entry point."""
    # If no paths provided, try to get them from command line
    if docx_data is None or excel_data is None:
        if len(sys.argv) != 3:
            print("Usage: python main.py <docx_file> <excel_file>")
            sys.exit(1)
        docx_data = sys.argv[1]
        excel_data = sys.argv[2]
    
    try:
        # Process files to find matches
        # results = process_files(docx_path, excel_path) uncomment if reading the excel file directly; if using excel list data, use the current one below
        results = process_files_with_selected_data(docx_data, excel_data)
        
        # Print results if running as script
        if __name__ == "__main__":
            if results:
                print(f"\nFound {len(results)} changes:")
                for i, (orig, mod, conf) in enumerate(results, 1):
                    print(f"\nChange {i} (confidence: {conf:.1%}):")
                    print("Original:", orig)
                    print("Modified:", mod)
        
        # Update document with changes
        #output_path = docx_data.replace('.docx', '_updated.docx')
        changes_made = find_changes(results)
        return {
            "status": "success",
            "data": {
                "number_of_changes": changes_made,
                "results": [
                    {
                        "original_text": orig,
                        "modified_text": mod,
                        "confidence": float(conf)
                    } for orig, mod, conf in results
                ]
                #,
                #"output_file_path": output_path
            }
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if __name__ == "__main__":
            sys.exit(1)
        raise e

if __name__ == "__main__":
    main()
