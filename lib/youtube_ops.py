# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import youtube_dl

_URL_FORMAT = 'https://www.youtube.com/watch?v={}'
_TARGET_FORMAT_ID = 18


def get_youtube_info(video_id, format_id=_TARGET_FORMAT_ID, proxy=None):
    assert isinstance(video_id, str), "video_id must be string"
    assert len(video_id) == 11, 'video_identifier must have length 11'

    target_url = _URL_FORMAT.format(video_id)

    ydl_opts = {'forceurl': True}
    if proxy:
        ydl_opts['proxy'] = proxy

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        resp = ydl.extract_info(target_url, download=False)
        infos = resp['formats']
        for info in infos:
            # 18 - 360p or 240p h264 encoded video (with audio)
            if info['format_id'] == str(format_id):
                return info['url'], info['width'], info['height']
        raise youtube_dl.DownloadError('There is no format_id=={}'.format(format_id))
