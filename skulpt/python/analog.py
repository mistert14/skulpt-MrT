"""
Analog clock. Kostya, IIPP Fall 2013
"""

import simplegui
import codeskulptor
import time
import math

TIME_ZONE = 6

def to_rad(val, maximum):
    return math.radians(val/maximum*360+90)

def draw(canvas):
    cur_time = time.time()
    hour = float(cur_time / 3600) % 12 + 6
    minute = float(cur_time % 3600 / 60)
    second = float(cur_time % 60)
    
    canvas.draw_image(background, (130, 130), (259, 259), (130, 130), (259, 259))
    canvas.draw_image(hour_arrow, (70, 7), (139, 13), (130, 130), (139, 13), to_rad(hour, 12))
    canvas.draw_image(minute_arrow, (98, 6), (195, 11), (130, 130), (195, 11), to_rad(minute, 60))
    canvas.draw_image(second_arrow, (98, 7), (196, 14), (130, 130), (196, 14), to_rad(second, 60))

frame = simplegui.create_frame('Clock', 259, 259, 0)
frame.set_draw_handler(draw)

background = simplegui.load_image(codeskulptor.file2url('assets_clock_background.png'))
hour_arrow = simplegui.load_image(codeskulptor.file2url('assets_clock_hour_arrow.png'))
minute_arrow = simplegui.load_image(codeskulptor.file2url('assets_clock_minute_arrow.png'))
second_arrow = simplegui.load_image(codeskulptor.file2url('assets_clock_second_arrow.png'))

frame.start()
