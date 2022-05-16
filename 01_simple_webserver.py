from cv2 import findEssentialMat
from fastapi import FastAPI, Form, Request, UploadFile,File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional, List
from matplotlib.pyplot import flag
import uvicorn

from pydantic import BaseModel ,HttpUrl, Field, DirectoryPath


class ItemIn(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    tax : Optional[float] = None

class ItemOut(BaseModel):
    name : str
    price : float
    tax : Optional[float] = None
app = FastAPI()

class ModelInput(BaseException):
    url : HttpUrl
    rate : int = Field(ge =1, le = 10)
    target_dir : DirectoryPath

fake_items_db = [{"item_name" : "foo"},{"item_name" : "bar"},{"item_name" : "baz"},]
templates = Jinja2Templates(directory= './templates')


@app.get("/")
def read_root():
    content = """
    <body>
        <form action = "/files/" enctype="multipart/form-data" method="post" >
            <input name="files" type="file" multiple>
            <input type="submit">
        </form>
        <form action = "/uploadfiles/" enctype="multipart/form-data" method="post">
            <input name = "files" type="file" multiple>
            <input type="submit">
        </form>
    </body>
    """
    return HTMLResponse(content=content)
@app.get("/users/{user_id}")
def get_user(user_id):
    return {"user_id" : user_id}

@app.post("/items/", response_model = ItemOut)
def create_item(item : ItemIn):
    return item

@app.get("/login")
def get_login_form(request : Request):
    return templates.TemplateResponse('login_form.html', context = {"request" : request})

@app.post("/login")
def login(username : str = Form(...), password : str = Form(...)):
    return {"username" : username}

@app.post("/files")
def create_files(files : List[bytes] = File(...)):
    return {"file_sizes" : {len(file) for file in files}}

@app.post("/uploadfiles")
def create_upload_files(files : List[UploadFile] = File(...)):
    return {"filenames" : {len(file.filename) for file in files}}

if __name__ == '__main__':
    uvicorn.run(app , host = "127.0.0.1", port = 8000)