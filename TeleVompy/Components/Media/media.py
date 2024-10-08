from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
import os
from ...Utils.base_class import BaseClass


class Media(BaseClass):
    def __init__(self, content: str, parse_mode: str):
        """ Initialize a Media (photo, video, audio and document) instance """
        self.show_caption_above_media: bool = None # shoud show media under caption
        self.has_spoiler: bool = None # shoud hide by spoiler photo and video
        self.parse_mode: str = parse_mode # parsing mode (html)
        self.__content = content # caption for the files
        self.__media: list[InputMediaPhoto | InputMediaVideo] = [] # list of photo and video files
        self.__audios: list[InputMediaAudio] = [] # list of audios files
        self.__documents: list[InputMediaDocument] = [] # list of documents files

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

    def files(self) -> dict:
        """ Returns files as a dictionary """
        return {'media': self.__media, 'audios': self.__audios, 'documents': self.__documents}

    def has_files(self) -> bool:
        """ Returns True if any media are exist, False otherwise """
        return any([self.__media, self.__audios, self.__documents])

    def count_files(self) -> int:
        """ Returns total count of files """
        return len(self.__media) + len(self.__audios) + len(self.__documents)

    def update_content(self, content: str = '') -> None:
        """ Updates caption of all files """
        self.__content = content
        self.__update_media_caption()
        self.__update_caption(self.__audios)
        self.__update_caption(self.__documents)

    def __update_media_caption(self) -> None:
        """ Updates caption of first media """
        if len(self.__media):
            self.__media[0].caption = self.__content

    def __update_caption(self, attachment_list: list[InputMediaAudio | InputMediaDocument]) -> None:
        """ Updates caption of last audio or last document """
        if len(attachment_list) > 1:
            attachment_list[-2].caption = ''
            attachment_list[-1].caption = self.__content
        elif len(attachment_list):
            attachment_list[0].caption = self.__content

    def __input_file(self, path: str, filename: str | None) -> FSInputFile:
        """ Returns file object based on the provided path or file_id """
        file = FSInputFile(path=path, filename=filename)
        return file

    def __get_full_path(self, file: str, folder: str = None) -> str:
        """ Returns assets file path based on the assetse path and file type """
        if not folder:
            return file
        dir_path = os.path.join(self.assets_dir, folder)
        return os.path.join(dir_path, file)

    def __get_file(self, file: str, file_id: str, sended_filename: str, assets_dir) -> bool | str | FSInputFile:
        """ Returns file object or file_id based on the provided path or file_id """
        if not file and not file_id:
            return False
        if file_id:
            return file_id
        full_path = self.__get_full_path(file=file, folder=assets_dir)
        return self.__input_file(path=full_path, filename=sended_filename)

    def add_photo(self, file: str = None, file_id: str = None, sended_filename: str = None, use_assets_dir: bool = True, caption: str = '') -> None:
        """ Add photo to medias list """
        # open file
        file = self.__get_file(file=file, file_id=file_id, sended_filename=sended_filename, assets_dir=self.CfgMedia.PHOTO_PATH if use_assets_dir else None)
        if not file:
            return False
        
        # add file
        photo = InputMediaPhoto(media=file, caption=caption, parse_mode=self.parse_mode, show_caption_above_media=self.show_caption_above_media, has_spoiler=self.has_spoiler)
        self.__media.append(photo)
        self.__update_media_caption()
    
    def add_video(self, file: str = None, file_id: str = None, sended_filename: str = None, use_assets_dir: bool = True, caption: str = '', 
                  width: int | None = None, height: int | None = None, duration: int | None = None) -> None:
        """ Add video to medias list """
        # open file
        file = self.__get_file(file=file, file_id=file_id, sended_filename=sended_filename, assets_dir=self.CfgMedia.VIDEO_PATH if use_assets_dir else None)
        if not file:
            return False

        # add file
        video = InputMediaVideo(
            media=file, caption=caption, parse_mode=self.parse_mode, 
            show_caption_above_media=self.show_caption_above_media, has_spoiler=self.has_spoiler,
            width=width, height=height, duration=duration
            )
        self.__media.append(video)
        self.__update_media_caption()

    def add_audio(self, file: str = None, file_id: str = None, sended_filename: str = None, use_assets_dir: bool = True, caption: str = '', duration: int | None = None) -> None:
        """ Add audio to audios list """
        # open file
        file = self.__get_file(file=file, file_id=file_id, sended_filename=sended_filename, assets_dir=self.CfgMedia.AUDIO_PATH if use_assets_dir else None)
        if not file:
            return False

        # add file
        audio = InputMediaAudio(media=file, caption=caption, parse_mode=self.parse_mode, duration=duration)
        self.__audios.append(audio)
        self.__update_caption(self.__audios)

    def add_document(self, file: str = None, file_id: str = None, sended_filename: str = None, use_assets_dir: bool = True, caption: str = '') -> None:
        """ Add document to documents list """
        # open file
        file = self.__get_file(file=file, file_id=file_id, sended_filename=sended_filename, assets_dir=self.CfgMedia.DOCUMENT_PATH if use_assets_dir else None)
        if not file:
            return False

        # add file
        document = InputMediaDocument(media=file, caption=caption, parse_mode=self.parse_mode)
        self.__documents.append(document)
        self.__update_caption(self.__documents)
    