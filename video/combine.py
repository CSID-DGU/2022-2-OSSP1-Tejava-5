import moviepy.editor as moviepy

def main(video, audio):
    videoclip = moviepy.VideoFileClip(video)
    audioclip = moviepy.AudioFileClip(audio)

    videoclip.audio = audioclip
    videoclip.write_videofile("../new video.mp4")