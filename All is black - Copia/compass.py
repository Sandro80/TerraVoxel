from ursina import *

class Compass(Entity):
    def __init__(self, player_camera,position, **kwargs):
        super().__init__(parent=camera.ui, scale=0.1, position=(-0.75, 0.4), **kwargs)
        self.player_camera = player_camera
        self.position = position

        self.bg = Entity(parent=self, model='quad',texture='compass_bg.png',scale=2,z=-0.01,)

        # Indicatore direzione (freccia)
        self.arrow = Entity(parent= self,model='quad',texture='assets/arrow.png', scale=0.7, rotation_z=0,z=0.01)

        self.bg.render_queue = 0
        self.arrow.render_queue = 1
        self.arrow.always_on_top = True

    def update(self):
        direction = self.player_camera.forward.normalized()
        angle = math.degrees(math.atan2(direction.x, direction.z))
        self.bg.rotation_z = -angle  # ruota la bussola
        self.arrow.rotation_z = 0   # freccia sempre verso l’alto