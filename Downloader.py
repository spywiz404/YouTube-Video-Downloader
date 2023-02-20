from fastapi import FastAPI,Form,Request
from pytube import YouTube
from io import BytesIO
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

yt=""

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function

@app.get('/')
async def home(request: Request,lst=[]):
    return templates.TemplateResponse('index.html', {"request":request,"background_image": "static/Background.jpg","lst":lst})

@app.post('/')
async def home(request:Request,url:str = Form(),lst=[]):
    if(request.method=='POST'):   
        global yt                   ### using global variable
        try:
            yt=YouTube(url)          
        except:
            return templates.TemplateResponse('error.html',{"request":request,"output":"Invalid URL please check url","background_image":"static/download.jpg","color":"rgb(200, 0, 0)"})
        try:
            ys=yt.streams
            l=[stream.resolution for stream in ys.filter(progressive=True)]
            print(l)
            return templates.TemplateResponse('index.html',{"request":request,"background_image":"static/Background.jpg","lst":l})
        except Exception as e:
            print (e)
            return templates.TemplateResponse('error.html',{"request":request,"output":"Unable to fetch Resolutions","background_image":"static/download.jpg","color":"rgb(200, 0, 0)"})
            
    return templates.TemplateResponse('index.html',context={"request":request,"background_image":"static/Background.jpg","lst":lst})



# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function

@app.post('/download',response_class=StreamingResponse)
async def download_file(request:Request,Choose_resolution:str = Form(...)):
    if(request.method=='POST'):
        global yt
        ys=yt.streams.get_by_resolution(Choose_resolution)
        try:
            buffer=BytesIO()
            ys.stream_to_buffer(buffer,)
            buffer.seek(0)
            file_name=yt.title.encode('ascii',errors='replace').decode('utf-8')
            file_name=file_name.replace('?','')
            return StreamingResponse(
                        buffer,
                        media_type="video/mp4",
                        headers={
                            "Content-Disposition": f"attachment; filename={file_name}"
                        })
        except Exception as e:
            print(e)
            return templates.TemplateResponse('error.html',{"request":request,"output":"Video Download failed","background_image":"static/download.jpg","color":"rgb(200, 0, 0)"})

