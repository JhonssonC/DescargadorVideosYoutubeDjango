import os
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
import ffmpeg
from djangoDownloader.settings import BASE_DIR
from datetime import datetime
from ytDownloader.forms import VideoForm
from ytDownloader.models import Video
import mimetypes

from pytube import YouTube

# Create your views here.

def index(request):
    data = None
    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            s = Video()
            s.link=form.cleaned_data['enlace']
            s.resoluciones=form.cleaned_data['resluciones']
            s.nombre=form.cleaned_data['titulo']
            s.extension=((form.cleaned_data['resluciones'].split(":"))[-1]).strip()
            #print (s)
            
            
            s.save()
            
            fecha_time = s.created_at.strftime("%d-%m-%y %H%M%S")
            filepath = BASE_DIR.__str__() + "\\videos\\"+ str(fecha_time)
            os.mkdir(filepath)
            
            mimetype=((((form.cleaned_data['resluciones'].split(":"))[1]).split(";"))[0]).strip()

            #print(mimetype)
            #print(s.extension)

            url = YouTube(str(form.cleaned_data['enlace']))
            
            video = url.streams.filter(
                resolution=mimetype, 
                mime_type=s.extension, 
                progressive="False").first()

            if not video:
                print ("No progresive = 'False'")
                video = url.streams.filter(
                resolution=mimetype, 
                mime_type=s.extension).first()
                
            archivo = s.nombre+"."+s.extension.split("/")[1]
            
            if video is not None:
                
                if video in url.streams.filter(only_video=True):
                    onlyAudio = url.streams.filter(only_audio=True).first().download(output_path=filepath, filename="only_audio_"+s.nombre+".mp3")
                    onlyVideo = video.download(output_path=filepath, filename="only_video_"+archivo)
                    #print ("a", onlyAudio)
                    #print ("v", onlyVideo)
                    video_file = ffmpeg.input(onlyVideo)
                    audio_file = ffmpeg.input(onlyAudio)
                    print("path_u", os.path.join(filepath, archivo))
                    ffmpeg.concat(video_file, audio_file, v=1, a=1).output("videos\\"+ str(fecha_time) + "\\"+archivo).run()
                else:                     
                    print("Audio & Video")
                    video.download(output_path=filepath, filename=archivo)
                

                myfile = os.path.join(filepath, archivo)
                # print (myfile)
                path_to_file = os.path.realpath(myfile)
                print (path_to_file)
                path = open(path_to_file, 'rb')
                response = HttpResponse(path, content_type='application/video')
                response['Content-Disposition'] = "attachment; filename=%s" % archivo
                return response
            else:
                print("Video no encontrado")
                return None

    else:
        form = VideoForm()
        return render(request, "downloader.html", {"form": form, "data": data})


def getResolution(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        print('is ajax')
        resoluciones=[]
        if request.method == 'POST':
            data = request.POST
            print(data)
            print(str(data['enlace']))
            url = YouTube(url=str(data['enlace'])) 
            
            streams = url.streams
            print(streams)
            
            for resolucion in url.streams:

                if resolucion.resolution:# and str(resolucion.resolution) not in ("480p", "240p", "144p"):
                    resoluciones.append({'resolucion':str(resolucion.resolution), 'peso':resolucion._filesize_mb, 'format':str(resolucion.mime_type)})
                    
                print(resolucion, '\n')
            
            print (resoluciones)
            titulo=""
            if(url.title):
                print (url.title)
                titulo = url.title
            

        return JsonResponse({'options': resoluciones, 'title': titulo}, status=200)
    
    else:
        return HttpResponseBadRequest('Invalid request')