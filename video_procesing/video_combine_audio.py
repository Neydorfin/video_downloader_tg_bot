import moviepy.editor as mpe


def combine_audio(video, audio, output):
    output = f"resources/video/{output}.mp4"
    my_clip = mpe.VideoFileClip(video)
    audio_background = mpe.AudioFileClip(audio)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output)
