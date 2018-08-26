# GenerativeArt
Some artistic effects from programming.

Saving .gif to mp4:

Requirement - ffmpeg

command: 
ffmpeg -i filename.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
