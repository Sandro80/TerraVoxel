from ursina import *

class SkyAmbient():
    def __init__(self, world_bounds, chunk_size, **kwargs):

        max_dist_axis = (world_bounds *2 +1 ) * chunk_size +chunk_size +chunk_size /2 
 
        # Dimensione del cielo
        sky_size = max_dist_axis 
        half_size = sky_size / 2

        # Facce del cubo
        sky_front  = Entity(model='quad', texture='assets/Daylight Box_front.bmp', position=(0,0,-half_size),  scale=(sky_size, sky_size), rotation=(0,0,0), double_sided=True)
        sky_back   = Entity(model='quad', texture='assets/Daylight Box_back.bmp', position=(0,0,half_size),  scale=(sky_size, sky_size), rotation=(0,180,0), double_sided=True)
        sky_left   = Entity(model='quad', texture='assets/Daylight Box_left.bmp', position=(-half_size,0,0),  scale=(sky_size, sky_size), rotation=(0,90,0), double_sided=True)
        sky_right  = Entity(model='quad', texture='assets/Daylight Box_right.bmp', position=(half_size,0,0),  scale=(sky_size, sky_size), rotation=(0,-90,0), double_sided=True)
        sky_top    = Entity(model='quad', texture='assets/Daylight Box_top.bmp', position=(0,half_size,0),  scale=(sky_size, sky_size), rotation=(90,0,0), double_sided=True)