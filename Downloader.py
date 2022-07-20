from flask import Flask, render_template,request,url_for,send_file
from pytube import YouTube
from io import BytesIO

app=Flask(__name__)
@app.route('/')
def home():
    lst=['144p','240p','360p','480p','720p','1080p']
    return render_template('index.html',background_image="static/Background.jpg",lst=lst)
@app.route('/download',methods=['GET','POST'])
def download_file():
    if(request.method=='POST'):
        url=request.form['url']
        # print("\n================\n")
        # print(url)
        # print(request.form)
        # print("\n================\n")
        try:
            yt=YouTube(url)
        except:
            return render_template('download.html',output="Invalid URL please check url",background_image="static/download.jpg",color="rgb(200, 0, 0)")
        print("Title : ",yt.title)
        ys=yt.streams
        try:
            ys=yt.streams
            l=[stream.resolution for stream in ys.filter(progressive=True).all()]
            # print(l)
            # ys=yt.streams.get_by_resolution(re)
            if(request.form['Choose resolution'] not in l):
                return render_template('download.html',output="This Resolution not availabe for this video please choose another Resoltion",background_image="static/download.jpg",color="rgb(200, 0, 0)")
            else:
                ys=yt.streams.get_by_resolution(request.form['Choose resolution'])
        except Exception as e:
            print(e)
            return render_template('download.html',output="Unable to fetch Resolutions",background_image="static/download.jpg",color="rgb(200, 0, 0)")
        
        try:
            buffer=BytesIO()
            ys.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=yt.title, mimetype="video/mp4")
            # return render_template('download.html',output="Video Download Successful",background_image="static/download.jpg",color="rgb(9, 253, 53)")
        except:
            return render_template('download.html',output="Video Download failed",background_image="static/download.jpg",color="rgb(200, 0, 0)")
if __name__=="__main__":
    app.run(debug=True)