from PIL import Image
import yt_dlp.postprocessor


class SquareCoverPP(yt_dlp.postprocessor.PostProcessor):
    """
    Crop thumbnail images to look like album covers
    """

    def run(self, info):
        file_ext = info["ext"]
        file_name = info["filepath"][: -len(file_ext) - 1]
        thumbnail_file = f"{file_name}.jpg"
        self.__crop(thumbnail_file, thumbnail_file)
        return [], info

    def __crop(self, thumbnail_file: str, cover_file: str):
        img = Image.open(thumbnail_file)
        width, height = img.size
        side = min(width, height)
        left = (width - side) / 2
        right = left + side
        top = (height - side) / 2
        bottom = top + side
        img_square = img.crop((left, top, right, bottom))
        img_square.save(cover_file)
