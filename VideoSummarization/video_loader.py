import torch as th
import pandas as pd
import os
import numpy as np
import ffmpeg
import re

class VideoLoader():
    def __init__(self,fname,framerate,size,centercrop):
        self.fname = fname
        self.centercrop = centercrop
        self.size = size
        self.framerate = framerate

    def _get_video_dim(self, video_path):
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams']
                             if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return height, width

    def _get_output_dim(self, h, w):
        if isinstance(self.size, tuple) and len(self.size) == 2:
            return self.size
        elif h >= w:
            return int(h * self.size / w), self.size
        else:
            return self.size, int(w * self.size / h)

    def vidfeat(self):
        video_path = self.fname
        if os.path.isfile(video_path):
            print('Decoding video: {}'.format(video_path))
            try:
                h, w = self._get_video_dim(video_path)
            except Exception as e:
                print('ffprobe failed at: {}'.format(video_path))
                return {'video': th.zeros(1), 'input': video_path}
            height, width = self._get_output_dim(h, w)
            cmd = (
                ffmpeg
                .input(video_path)
                .filter('fps', fps=self.framerate)
                .filter('scale', width, height)
            )
            if self.centercrop:
                x = int((width - self.size) / 2.0)
                y = int((height - self.size) / 2.0)
                cmd = cmd.crop(x, y, self.size, self.size)
            out, _ = (
                cmd.output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run(capture_stdout=True, quiet=True)
            )
            if self.centercrop and isinstance(self.size, int):
                height, width = self.size, self.size
            video = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])
            video = th.from_numpy(video.astype('float32'))
            video = video.permute(0, 3, 1, 2)
        else:
            video = th.zeros(1)
        return {'video': video, 'input': video_path}
