import yt_dlp
from ytdlp.postprocessors import SquareCoverPP


# inject custom postprocessor into yt_dlp.postprocessor to be accessible through globals() of get_postprocessor
yt_dlp.postprocessor.SquareCoverPP = SquareCoverPP
