from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from tempfile import NamedTemporaryFile
from main import main as process_documents
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Document Processing API",
    description="API for processing and updating documents based on Excel data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://numaira.app"],
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
    output_file_path: str

class SuccessResponse(BaseModel):
    status: str = "success"
    data: ProcessingResult

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str

class ExcelData(BaseModel):
    data: List[str]

@app.post("/run-syncspace/", 
    response_model=SuccessResponse,
    responses={500: {"model": ErrorResponse}}
)
async def process_documents_endpoint(
    excel_data: ExcelData,
    docx_file: UploadFile = File(...)
):
    tmp_docx_path = None
    #tmp_excel_path = None
    try:
        # Save uploaded DOCX file to a temporary file
        with NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
            shutil.copyfileobj(docx_file.file, tmp_docx)
            tmp_docx_path = tmp_docx.name

        # Process the documents with excel data list
        result = process_documents(tmp_docx_path, excel_data.data)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )
    finally:
        # Ensure temporary file is removed even if an error occurs
        if tmp_docx_path and os.path.exists(tmp_docx_path):
            os.unlink(tmp_docx_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
