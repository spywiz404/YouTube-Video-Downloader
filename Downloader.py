from flask import Flask, render_template,request
from pytube import YouTube

app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html',background_image="static/Background.jpg")
@app.route('/download',methods=['GET','POST'])
def download_file():
    if(request.method=='POST'):
        url=request.form['url']
        print(url)
        try:
            yt=YouTube(url)
        except:
            return render_template('download.html',output="Invalid URL please check url",background_image="static/download.jpg",color="rgb(200, 0, 0)")
        print("Title : ",yt.title)
        ys=yt.streams.get_lowest_resolution()
        try:
            ys.download('./video')
            return render_template('download.html',output="Video Download Successful",background_image="static/download.jpg",color="rgb(9, 253, 53)")
        except:
            return render_template('download.html',output="Video Download failed",background_image="static/download.jpg",color="rgb(200, 0, 0)")
if __name__=="__main__":
    app.run(debug=True)