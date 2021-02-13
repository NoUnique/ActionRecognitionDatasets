# -*- coding: utf-8 -*-
"""
    Audioset dataset parser.
    
    Author : HyoSang Kim (hyo_sang.kim@samsung.com)
"""

from lib.parser.parser_base import Parser

NUM_HEADER_LINES = 3


class AudiosetParser(Parser):
    def _parse_annotation(self, annotation_filepath):
        annotations = set()
        if self.annotation_type == 'csv':
            with open(annotation_filepath, 'r') as f:
                reader = self.lib.reader(f, delimiter=',')
                # skip headers
                for i in range(0, NUM_HEADER_LINES):
                    next(reader)
                for row in reader:
                    if len(row) < 4:  # (YTID,  start_seconds,  end_seconds,  *positive_labels)
                        continue
                    video_id, start_time, end_time = row[0], row[1], row[2]
                    annotations.add((video_id, start_time, end_time))
        elif self.annotation_type == 'json':
            pass
        else:
            pass
        return annotations
