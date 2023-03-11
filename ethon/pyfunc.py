#vasusen-code/thechariotoflight/dronebots
#__TG:ChauhanMahesh__

from typing import Union
from contextlib import contextmanager
from pathlib import Path
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

import numpy as np
import cv2
import subprocess

@contextmanager
def open_video(video_path: Union[Path, str], mode: str='r', *args):
    '''Context manager to work with cv2 videos
        Mimics python's standard `open` function
    Args:
        video_path: path to video to open
        mode: either 'r' for read or 'w' write
        args: additional arguments passed to Capture or Writer
            according to OpenCV documentation
    Returns:
        cv2.VideoCapture or cv2.VideoWriter depending on mode
    Example of writing:
        open_video(
            out_path,
            'w',
            cv2.VideoWriter_fourcc(*'XVID'), # fourcc
            15, # fps
            (width, height), # frame size
        )
    '''
    video_path = Path(video_path)
    if mode == 'r':
        video = cv2.VideoCapture(video_path.as_posix(), *args)
    elif mode == 'w':
        video = cv2.VideoWriter(video_path.as_posix(), *args)
    else:
        raise ValueError(f'Incorrect open mode "{mode}"; "r" or "w" expected!')
    if not video.isOpened(): raise ValueError(f'Video {video_path} is not opened!')
    try:
        yield video
    finally:
        video.release()

def frames(video: Union[Path, cv2.VideoCapture], rgb: bool=False) -> Iterable[np.ndarray]:
    '''Generator of frames of the video provided
    Args:
        video: either Path or Video capture to read frames from
            in former case file will be opened with :py:funct:`.open_video`
        rgb: if True returns RGB image, else BGR - native to opencv format
    Yields:
        Frames of video
    '''
    if isinstance(video, Path):
        with open_video(video) as capture:
            yield from frames(capture, rgb)
    else:
        while True:
            retval, frame = video.read()
            if not retval:
                break
            if rgb:
                frame = frame[:, :, ::-1]
            yield frame

#fastest way to get total number of frames in a video
def total_frames(video_path):
    cap = cv2.VideoCapture(f"{video_path}")
    tf = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
    return tf        
    
#makes a subprocess handy
def bash(cmd):    
    bashCommand = f"{cmd}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) 
    output, error = process.communicate()
    return output, error
    
#to get width, height and duration(in sec) of a video
def video_metadata(file):
    vcap = cv2.VideoCapture(f'{file}')  
    width = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH ))
    height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    fps = vcap.get(cv2.CAP_PROP_FPS),
    frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = round(frame_count / fps)
    data = {'width' : width, 'height' : height, 'fps' : fps, 'frame_count' : frame_count, 'duration' : duration }
    return data
    vcap.release()
    cap.release()
