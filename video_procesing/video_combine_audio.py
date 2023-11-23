import moviepy.editor as mpe


class VideoMaker:
    @staticmethod
    def combine_audio(video, audio, output):
        """
            Комбинирует видео и аудио, сохраняя результат в новом файле.

            Args:
                video (str): Путь к видеофайлу.
                audio (str): Путь к аудиофайлу.
                output (str): Имя для сохраняемого файла.

            Returns:
                None
        """
        output = f"resources/video/{output}.mp4"
        # загрузка видео
        video_clip = mpe.VideoFileClip(video)
        # загрузка звука
        audio_clip = mpe.AudioFileClip(audio)
        # используется конец видеоклипа
        end = video_clip.end
        # установка начала и конца аудиоклипа в параметрах `start` и `end`
        audio_clip = audio_clip.subclip(0, end)
        # добавить звук к видео
        final_clip = video_clip.set_audio(audio_clip)
        # сохранить готовый клип
        final_clip.write_videofile(output)
