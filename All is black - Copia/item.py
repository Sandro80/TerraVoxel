from ursina import *

class Item(Entity):
    def __init__(self, pickable=True, **kwargs):
        super().__init__(**kwargs)
        
        self.pickable = pickable

    def update(self):
        self.rotation_y += 50 * time.dt 

    