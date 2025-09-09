from ursina import *
import math

class DayNightCycle(Entity):
    def __init__(self, player, day_length=60, shadow_scale=Vec3(50,50,50), **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.day_length = day_length
        self.time_of_day = 0  # 0 = alba, 0.5 = tramonto, 1 = notte

        # Sole
        self.sun = DirectionalLight(shadows=True)
        self.sun.shadow_map_resolution = (1024, 1024)
        self.sun.look_at(Vec3(1, -1, -1))

        # Luna
        self.moon = DirectionalLight(shadows=False)
        self.moon.look_at(Vec3(-1, -1, -1))
        self.moon.color = color.rgb(180, 200, 255)
        self.moon.enabled = False

        # Luce ambientale
        self.ambient = AmbientLight()
        self.ambient.color = color.rgb(200, 200, 200)

        # Bounding box per le ombre
        self.shadow_bounds = Entity(model='cube', scale=shadow_scale, visible=False)
        self.sun.update_bounds(self.shadow_bounds)

    def update(self):
        # Avanza il tempo
        self.time_of_day += time.dt / self.day_length
        if self.time_of_day > 1:
            self.time_of_day = 0

        # Rotazione sole
        angle = self.time_of_day * math.tau
        self.sun.look_at(Vec3(math.sin(angle), -1, math.cos(angle)))

        # Ombre centrate sul player
        self.shadow_bounds.position = self.player.position
        self.sun.update_bounds(self.shadow_bounds)

        # Giorno
        if 0 <= self.time_of_day < 0.5:
            self.sun.enabled = True
            self.moon.enabled = False
            self.sun.color = color.rgb(255, 244, 214)
            self.sun._light.intensity = lerp(1.0, 0.3, self.time_of_day * 2)
            self.ambient.color = color.rgb(200, 200, 200)

        # Notte
        else:
            self.sun.enabled = False
            self.moon.enabled = True
            moon_angle = angle + math.pi
            self.moon.look_at(Vec3(math.sin(moon_angle), -1, math.cos(moon_angle)))
            self.moon._light.intensity = 0.4
            self.ambient.color = color.rgb(80, 80, 120)
