from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from main import main as process_documents
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json

app = FastAPI(
    title="Document Processing API",
    description="API for processing and updating documents based on Excel data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://numaira.app", "https://api.numaira-ai.click", "http://numaira-ai.click"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define response models
class Change(BaseModel):
    original_text: str
    modified_text: str
    confidence: float

class ProcessingResult(BaseModel):
    number_of_changes: int
    results: List[Change]

class SuccessResponse(BaseModel):
    status: str = "success"
    data: ProcessingResult

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str

class ExcelRow(BaseModel):
    row_header: str = Field(..., description="The header text to match in the document")
    values: Dict[str, float] = Field(..., description="Mapping of years/columns to their values")

class ExcelData(BaseModel):
    data: List[ExcelRow] = Field(
        ...,
        description="List of Excel rows containing mapping data",
        example=[
            {
                "row_header": "Revenue",
                "values": {"2022": 100.0, "2023": 120.0}
            }
        ]
    )

class WordData(BaseModel):
    data: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping paragraph IDs to their text content",
        example={
            "paragraph1": "The revenue was $100 million in 2022.",
            "paragraph2": "The cost was $50 million in 2022."
        }
    )

class DocumentProcessingRequest(BaseModel):
    excel_data: ExcelData = Field(..., description="Excel data containing the mapping information")
    docx_data: WordData = Field(..., description="Word document data to be processed")

    class Config:
        schema_extra = {
            "example": {
                "excel_data": {
                    "data": [
                        {
                            "row_header": "Revenue",
                            "values": {"2022": 100.0, "2023": 120.0}
                        }
                    ]
                },
                "docx_data": {
                    "data": {
                        "paragraph1": "The revenue was $100 million in 2022.",
                        "paragraph2": "The cost was $50 million in 2022."
                    }
                }
            }
        }

@app.get("/health")
async def health_check():
    """健康检查端点，返回简单的'hello'确认API服务正常运行。"""
    return {"message": "hello"}

@app.post("/run-syncspace/", 
    response_model=SuccessResponse,
    responses={500: {"model": ErrorResponse}}
)
async def process_documents_endpoint(
    request: DocumentProcessingRequest
):
    """
    Process documents based on Excel mapping data.
    
    Args:
        request (DocumentProcessingRequest): Combined request containing both Excel and Word data
        
    Returns:
        SuccessResponse: Processing results with changes made
    """
    try:
        # Process the documents with data received directly
        result = process_documents(request.docx_data.data, request.excel_data.data)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
