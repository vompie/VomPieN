from ...Engine.base_class import BaseClass
from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument


class Media(BaseClass):
    def __init__(self, content: str, parse_mode: str):
        """ Initialize a Media (photo, video, audio and document) instance """
        self.show_caption_above_media: bool = None # shoud show media under caption
        self.has_spoiler: bool = None # shoud hide by spoiler photo and video
        self.parse_mode: str = parse_mode # parsing mode (html)
        self.__content = content # caption for the files
        self.__media: list = [] # list of photo and video files
        self.__audios: list = [] # list of audios files
        self.__documents: list = [] # list of documents files

    def files(self) -> dict:
        """ Returns files as a dictionary """
        return {'media': self.__media, 'audios': self.__audios, 'documents': self.__documents}

    def has_files(self) -> bool:
        """ Returns True if any media are exist, False otherwise """
        return any([self.__media, self.__audios, self.__documents])

    @property
    def media(self) -> list[InputMediaPhoto | InputMediaVideo]:
        """ Returns all media objects """
        return self.__media
    
    @property
    def audios(self) -> list[InputMediaAudio]:
        """ Returns all audios objects """
        return self.__audios
    
    @property
    def documents(self) -> list[InputMediaDocument]:
        """ Returns all docuemnts objects """
        return self.__documents

    def update_content(self, content: str = '') -> None:
        """ Updates caption of all files """
        self.__content = content
        self.__update_media_caption()
        self.__update_audios_caption()
        self.__update_documents_caption()

    def __update_media_caption(self) -> None:
        """ Updates caption of first media """
        if len(self.__media):
            self.__media[0].caption = self.__content

    def __update_audios_caption(self) -> None:
        """ Updates caption of last audio """
        if len(self.__audios) > 1:
            self.__audios[-2].caption = ''
            self.__audios[-1].caption = self.__content
        elif len(self.__audios):
            self.__audios[0].caption = self.__content

    def __update_documents_caption(self) -> None:
        """ Updates caption of last document """
        if len(self.__documents) > 1:
            self.__documents[-2].caption = ''
            self.__documents[-1].caption = self.__content
        elif len(self.__documents):
            self.__documents[0].caption = self.__content

    def __input_file(self, path: str, filename: str | None) -> FSInputFile:
        """ Returns file object based on the provided path or file_id """
        file = FSInputFile(path=path, filename=filename)
        return file

    def __get_file(self, path: str | None, file_id: str | None, filename: str | None, cfg_path: bool | str) -> bool | str | FSInputFile:
        """ Returns file object or file_id based on the provided path or file_id """
        if not path and not file_id:
            return False
        if file_id:
            return file_id
        else:
            full_path = f"{cfg_path}/{path}" if cfg_path else path
            media = self.__input_file(path=full_path, filename=filename)
        return media

    def add_photo(self, path: str | None = None, file_id: str | None = None, filename: str | None = None, use_cfg_path: bool = True, caption: str = '') -> None:
        """ Add photo to medias list """
        if use_cfg_path:
            use_cfg_path = self.CfgMedia.PHOTO_PATH
        file = self.__get_file(path=path, file_id=file_id, filename=filename, cfg_path=use_cfg_path)
        photo = InputMediaPhoto(media=file, caption=caption, parse_mode=self.parse_mode, show_caption_above_media=self.show_caption_above_media, has_spoiler=self.has_spoiler)
        self.__media.append(photo)
        self.__update_media_caption()
    
    def add_video(self, 
                  path: str | None = None, 
                  file_id: str | None = None, 
                  filename: str | None = None, 
                  use_cfg_path: bool = True,
                  width: int | None = None, 
                  height: int | None = None, 
                  duration: int | None = None,
                  caption: str = ''
                ) -> None:
        """ Add video to medias list """
        if use_cfg_path:
            use_cfg_path = self.CfgMedia.VIDEO_PATH
        file = self.__get_file(path=path, file_id=file_id, filename=filename, cfg_path=use_cfg_path)
        video = InputMediaVideo(
            media=file, caption=caption, parse_mode=self.parse_mode, 
            show_caption_above_media=self.show_caption_above_media, has_spoiler=self.has_spoiler,
            width=width, height=height, duration=duration
            )
        self.__media.append(video)
        self.__update_media_caption()

    def add_audio(self, path: str | None = None, file_id: str | None = None, filename: str | None = None, use_cfg_path: bool = True, duration: int | None = None, caption: str = '') -> None:
        """ Add audio to audios list """
        if use_cfg_path:
            use_cfg_path = self.CfgMedia.AUDIO_PATH
        file = self.__get_file(path=path, file_id=file_id, filename=filename, cfg_path=use_cfg_path)
        audio = InputMediaAudio(media=file, caption=caption, parse_mode=self.parse_mode, duration=duration)
        self.__audios.append(audio)
        self.__update_audios_caption()

    def add_document(self, path: str | None = None, file_id: str | None = None, filename: str | None = None, use_cfg_path: bool = True, caption: str = '') -> None:
        """ Add document to documents list """
        if use_cfg_path:
            use_cfg_path = self.CfgMedia.DOCUMENT_PATH
        file = self.__get_file(path=path, file_id=file_id, filename=filename, cfg_path=use_cfg_path)
        document = InputMediaDocument(media=file, caption=caption, parse_mode=self.parse_mode)
        self.__documents.append(document)
        self.__update_documents_caption()
    