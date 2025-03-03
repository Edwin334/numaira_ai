# Document Processing API Documentation

## Overview
This API provides functionality for processing document content using provided data to update numerical values while maintaining document structure.

## API Metadata
- **Title**: Document Processing API
- **Description**: API for processing and updating documents based on Excel data
- **Version**: 1.0.0

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
`GET /health`

Simple endpoint to verify the API is running.

**Response:**
```json
{
    "message": "hello"
}
```

### Process Documents
`POST /run-syncspace/`

Processes document content using provided data to update numerical values.

#### Request

**Content-Type:** `application/json`

**Body Parameters:**
- `docx_data`: (JSON object, required) - Document content as key-value pairs
  - `data`: Dictionary mapping paragraph IDs to their text content
- `excel_data`: (JSON object, required) - Data structure containing values for updates
  - `data`: List of Excel rows containing mapping data with row headers and values

**Request Structure (Example):**
```json
{
    "docx_data": {
        "data": {
            "paragraph1": "The revenue was $100 million in 2022.",
            "paragraph2": "The cost was $50 million in 2022.",
            "paragraph3": "Other content without matching data."
        }
    },
    "excel_data": {
        "data": [
            {
                "row_header": "Revenue",
                "values": {
                    "2022": 100,
                    "2023": 120
                }
            },
            {
                "row_header": "Cost",
                "values": {
                    "2022": 50,
                    "2023": 60
                }
            }
        ]
    }
}
```

#### Response (Example)

**Success Response (200 OK)**
```json
{
    "status": "success",
    "data": {
        "number_of_changes": 2,
        "results": [
            {
                "original_text": "The revenue was $100 million in 2022",
                "modified_text": "The revenue was $120 million in 2023",
                "confidence": 0.95
            },
            {
                "original_text": "The cost was $50 million in 2022",
                "modified_text": "The cost was $60 million in 2023",
                "confidence": 0.92
            }
        ]
    }
}
```

**Error Response (500 Internal Server Error)**
```json
{
    "status": "error",
    "message": "Error description"
}
```

## Implementation Notes

1. The API only updates text where a match is found between document content and data headers
2. Changes are only counted when:
   - The text has actually changed
   - The confidence score is above 0.1 (10%)
3. For multiple matches in the same text, the confidence is calculated as an average

## Error Handling
- The API returns appropriate HTTP status codes and error messages
- All errors are logged for debugging purposes

## CORS
The API allows cross-origin requests from specified domains with full access to methods and headers:
- http://numaira.app
- https://api.numaira-ai.click
- http://numaira-ai.click
