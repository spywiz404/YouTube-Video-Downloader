import re
from flask import Flask, render_template,request,send_file
from pytube import YouTube
from io import BytesIO

yt=""
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home(lst=[]):
    if(request.method=='POST'):
        global yt
        url=request.form['url']
        # print("================================")
        # print(url)
        # print('================================')
        # playlist=Playlist(url)
        # print(playlist.video_urls)
        try:
            yt=YouTube(url)
        except:
            return render_template('error.html',output="Invalid URL please check url",background_image="static/download.jpg",color="rgb(200, 0, 0)")
        print("Title : ",yt.title)
        try:
            ys=yt.streams
            l=[stream.resolution for stream in ys.filter(progressive=True).all()]
            return render_template('index.html',background_image="static/Background.jpg",lst=l)
        except Exception as e:
            return render_template('error.html',output="Unable to fetch Resolutions",background_image="static/download.jpg",color="rgb(200, 0, 0)")
            
    return render_template('index.html',background_image="static/Background.jpg",lst=lst)
@app.route('/error',methods=['GET','POST'])
def download_file():
    if(request.method=='POST'):
        # url=request.form['url']
        # print("\n================\n")
        # print(url)
        # print(request.form)
        # print("\n================\n"))
        global yt
        ys=yt.streams.get_by_resolution(request.form['Choose resolution'])
        try:
            buffer=BytesIO()
            ys.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=yt.title, mimetype="video/mp4")
        except:
            return render_template('error.html',output="Video Download failed",background_image="static/download.jpg",color="rgb(200, 0, 0)")
if __name__=="__main__":
    app.run(debug=True)