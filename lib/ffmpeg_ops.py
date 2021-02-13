# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import time
import json
import subprocess


# TODO: fix a bug of probe_resolution not working with direct_url
def probe_resolution(video):
    # probe the resolution of video
    command = [
        'ffprobe',
        '-loglevel', 'quiet',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=height,width',
        '-print_format', 'json',
        '-show_format',
        video,
    ]

    output = subprocess.check_output(command,
                                     shell=True,
                                     stderr=subprocess.STDOUT)

    vmeta = json.loads(output)
    width = int(vmeta['streams'][0]['width'])
    height = int(vmeta['streams'][0]['height'])
    return width, height


_X264_PRESET_LIST = ['placebo', 'veryslow', 'slower', 'slow', 'medium',
                     'fast', 'faster', 'veryfast', 'superfast', 'ultrafast']


def get_timestr(start_time=None, end_time=None):
    def _convert_to_sec(string):
        try:
            return float(string)
        except ValueError:
            try:
                tgt_t = time.strptime(string, '%H:%M:%S')
                std_t = time.strptime('00:00:00', '%H:%M:%S')
                return time.mktime(tgt_t) - time.mktime(std_t)
            except:
                raise ValueError("cannot convert timestamp")

    command_time = []
    if start_time is not None:
        sec = _convert_to_sec(start_time)
        command_time.extend(['-ss',
                             '{:02d}:{:02d}:{:04.1f}'.format(int(sec / 3600),
                                                             int(sec / 60),
                                                             sec % 60.0)])
    if start_time is not None and end_time is not None:
        duration = float(end_time) - float(start_time)
        sec = _convert_to_sec(duration)
        command_time.extend(['-t',
                             '{:02d}:{:02d}:{:04.1f}'.format(int(sec / 3600),
                                                             int(sec / 60),
                                                             sec % 60.0)])
    return command_time

def encode_video(video, output_filename, width, height,
                 start_time=None, end_time=None, x264_preset='veryfast',
                 resize=True, min_size=256):
    # apply custom settings if it exists
    command_time = get_timestr(start_time, end_time)

    command_scale = []
    if resize:
        if width >= height:
            new_height = min_size
            new_width = int(1. * width / height * min_size)
            new_width = int(new_width / 2) * 2
        else:
            new_width = min_size
            new_height = int(1. * height / width * min_size)
            new_height = int(new_height / 2) * 2
        command_scale.extend([
            '-filter:v', 'scale={}:{}'.format(new_width, new_height)])

    assert isinstance(x264_preset, str), "x264_preset must be string"
    if x264_preset not in _X264_PRESET_LIST:
        raise ValueError("{} is not supported x264 preset".format(x264_preset))

    command = [
        'ffmpeg',
        '-threads', '1',
        '-loglevel', 'panic',
        ] + command_time + [
        '-i', '"{}"'.format(video),
        ] + command_scale + [
        '-codec:v', 'libx264',
        '-preset', x264_preset,
        '-tune', 'fastdecode',
        '-codec:a', 'aac',
        output_filename,
    ]

    output = subprocess.check_output(' '.join(command),
                                     shell=True,
                                     stderr=subprocess.STDOUT)
    return output

def encode_audio(video, output_filename,
                 start_time=None, end_time=None):
    # apply custom settings if it exists
    command_time = get_timestr(start_time, end_time)

    command = [
        'ffmpeg',
        '-threads', '1',
        '-loglevel', 'panic',
        ] + command_time + [
        '-i', '"{}"'.format(video),
        '-vn',
        '-codec:a', 'aac',
        output_filename,
    ]

    output = subprocess.check_output(' '.join(command),
                                     shell=True,
                                     stderr=subprocess.STDOUT)
    return output
