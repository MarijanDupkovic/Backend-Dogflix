import os
import subprocess

from Videos.models import VideoItem

def convert_480p(source):
    new_file_name = source.split('.')[0] + '_480p.mp4' 
    
    
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run = subprocess.Popen(cmd,shell=True)
    run.wait()
    file_name = os.path.basename(source)
    video = VideoItem.objects.get(video_file__icontains=file_name)
    new_path = 'videos/{}'.format(os.path.basename(new_file_name))
    video.video_file_480p = new_path
    video.save()
    print("Converting to 480px finished!")
    
def convert_720p(source):
    new_file_name = source.split('.')[0] + '_720p.mp4'
    
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run = subprocess.Popen(cmd,shell=True)
    run.wait()

    file_name = os.path.basename(source)

    video = VideoItem.objects.get(video_file__icontains=file_name)
    new_path = 'videos/{}'.format(os.path.basename(new_file_name)) 
    video.video_file_720p = new_path
    video.save() 
    print("Converting to 720px finished!")
    
def convert_1080p(source):
    new_file_name = source.split('.')[0] + '_1080p.mp4' 
    file_name = os.path.basename(source)

    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run = subprocess.Popen(cmd,shell=True)
    run.wait()

    video = VideoItem.objects.get(video_file__icontains=file_name) 
    new_path = 'videos/{}'.format(os.path.basename(new_file_name))
    video.video_file_1080p = new_path
    video.save()
    print("Converting to 1080px finished!")