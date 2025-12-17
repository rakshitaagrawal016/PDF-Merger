# from fastapi import FastAPI,File,UploadFile
# from pydantic import BaseModel
# from typing import List
# from pypdf import PdfWriter
# from fastapi.responses import HTMLResponses
# app=FastAPI()
# merger = PdfWriter()


# class pdf_list(BaseModel):
    
# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}
# for pdf in pdf_list:
#     merger.append(pdf)

# merger.write("out-basic.pdf")

# @app.get("/mergedFile")
# def returnFile(file:"out-basic.pdf"):
#     return file

from fastapi import FastAPI,File,UploadFile,HTTPException
from typing import List
from pathlib import Path
from pypdf import PdfReader,PdfWriter
import shutil
from pathlib import Path
import shutil
from fastapi.responses import FileResponse
app=FastAPI()
@app.get("/")
def root():
    return {"message":"backend works","yoyo":"djsvn"}

@app.post("/uploads")
async def uploadFile(files:List[UploadFile]=File(...)):
    # return{
    #     "filename":file.name,
    #     "content_type":file.content_type
    # }
    filenames = [file.filename for file in files]
    length=len(files)
    validate(files,length)
    saved_files=copy(files)
    merged_pdf_path=merge_pdf(saved_files)
    return FileResponse(
        path=merged_pdf_path,
        filename="my_document_name.pdf", # The name the user's browser will use for the download
        media_type="application/pdf"     # The MIME type of the file
    )

def validate(files,length):
    if length<2:
        raise HTTPException(status_code=400, detail="Upload at least 2 PDFs")
    for index,file in enumerate(files):
        extension=Path(file.filename).suffix
        if extension.lower()!=".pdf":
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a PDF"
            )
        
def copy(files):
    temp_dir=Path("uploads")
    temp_dir.mkdir(exist_ok=True)
    saved_files=[]
    for index,file in enumerate(files):
        fileName=Path(temp_dir/f"pdf{index}.pdf")
        source=file.file
        with open(fileName,"wb") as buffer:
            shutil.copyfileobj(source,buffer)
        saved_files.append(fileName)
    print("contents copied successfully :)")
    return saved_files

def merge_pdf(saved_files):
    merge=PdfWriter()
    temp_dir=Path("uploads")
    temp_dir.mkdir(exist_ok=True)
    filename=Path(temp_dir/f"merged_pdf.pdf")
    for pdf_path in saved_files:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            merge.add_page(page)
    with open(filename,"wb") as buffer:
        merge.write(buffer)
    return filename
    
