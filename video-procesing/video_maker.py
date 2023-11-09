import moviepy.editor as mpe


def combine_audio(data):
    output = f"resources/video/{data.title}.mp4"
    my_clip = mpe.VideoFileClip(data.vidname)
    audio_background = mpe.AudioFileClip(data.audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output)
