from ursina import *
import math, time, random

class LightController(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Luce direzionale principale (sole/luna)
        self.main_light = DirectionalLight(shadows=True)
        self.main_light.look_at(Vec3(1,-1,-1))
        self.main_light.color = color.white
        self.main_light_intensity = 1.0

        # Luce dinamica (torcia/fuoco)
        self.torch_light = PointLight(parent=camera, y=1, z=1, color=color.orange)
        self.torch_light_intensity = 0.8
        self.flicker_speed = 15
        self.flicker_amount = 0.1

        self.time_of_day = 0  # 0 = alba, 0.5 = tramonto, 1 = notte

    def update(self):
        # Ciclo giorno/notte
        self.time_of_day += time.dt * 0.02
        if self.time_of_day > 1:
            self.time_of_day = 0

        # Colore e intensità del sole/luna
        if self.time_of_day < 0.5:  # Giorno
            self.main_light.color = color.rgb(255, 244, 214)
            self.main_light_intensity = lerp(1.0, 0.3, self.time_of_day * 2)
        else:  # Notte
            self.main_light.color = color.rgb(180, 200, 255)
            self.main_light_intensity = lerp(0.3, 1.0, (self.time_of_day - 0.5) * 2)

        self.main_light._light.color = self.main_light.color
        self.main_light._light.intensity = self.main_light_intensity

        # Flicker torcia
        flicker = math.sin(time.time() * self.flicker_speed) * self.flicker_amount
        flicker += (random.random() - 0.5) * self.flicker_amount
        self.torch_light._light.intensity = self.torch_light_intensity + flicker

app = Ursina()

# Ambiente di test
ground = Entity(model='plane', scale=50, texture='white_cube', texture_scale=(50,50), color=color.gray)
cube = Entity(model='cube', scale=2, color=color.azure, y=1)

light_controller = LightController()

app.run()
