from moviepy.editor import *
from os import listdir, makedirs, path


makedirs('./output', exist_ok=True)
audios = [path.join('./audios/', audio) for audio in listdir('./audios')]
videos = [path.join('./videos/', video) for video in listdir('./videos')]
audio_index = 0


for vide_index, video in enumerate(videos):
    audio_clip = AudioFileClip(audios[audio_index % len(audios)])
    video_clip = VideoFileClip(video)

    video_clip.audio = audio_clip
    video_clip.write_videofile(path.join("./output", f"{vide_index+1}.mp4"), codec="mpeg4")