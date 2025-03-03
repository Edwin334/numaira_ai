import pandas as pd
from typing import List, Dict, Any
from tqdm import tqdm

def excel_to_list(excel_path: str) -> List[Dict[str, Any]]:
    """Convert Excel file to list of metrics with values.
    
    Maps each value cell to its row header (leftmost column) and column header.
    No text parsing or assumptions about content.
    
    Args:
        excel_path: Path to Excel file
        
    Returns:
        List of dicts with structure:
        {
            "row_header": str,  # Value from leftmost column
            "values": Dict[str, float]  # Column header -> value mapping
        }
    """
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)
        
        # Use first column as row headers
        row_header_col = df.columns[0]
        
        # Convert to list of dicts
        metrics = []
        for _, row in df.iterrows():
            # Skip rows with empty header
            if pd.isna(row[row_header_col]) or str(row[row_header_col]).strip() == '':
                continue
                
            row_header = str(row[row_header_col])
            
            # Create mapping of column header -> value
            values = {}
            for col in df.columns[1:]:  # Skip first (header) column
                if not pd.isna(row[col]):
                    try:
                        value = float(row[col])
                        values[str(col)] = value
                    except (ValueError, TypeError):
                        continue
            
            if values:  # Only add if we found some numeric values
                metrics.append({
                    "row_header": row_header,
                    "values": values
                })
        
        return metrics
        '''
        metrics format is for examole:
        [{"row_header": "Revenue",
                        "values":{
                                "2022":100,
                                "2023":120
                                }
        },
        {"row_header": "Cost",
                        "values":{
                                "2022":50,
                                "2023":60
                                }
        }]
        
        '''
        
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return []
