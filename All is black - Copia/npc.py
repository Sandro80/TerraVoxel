from ursina import *

class NPC(Entity):
    def __init__(self, name="NPC", position=(0,0,0), model='cube', scale=1,minimap= None,  traceable = True, dialoghi=None,interaction_radius=4):
        super().__init__(
            name=name,
            position=position,
            model=model,               
            scale=scale,
            collider='box'
        )

        self.minimap= minimap
        self.traceable = traceable
        self.dialoghi = dialoghi if dialoghi else ["Ciao!", "Hai bisogno di aiuto?"]
        self.dialogo_index = 0

        self.interaction_radius = interaction_radius

        # Testo visibile sopra l'NPC
        self.text_entity = Text(
            parent= self,
            text='',
            color=color.white,
            scale=1,
            origin=(0,0),
            #background=True,
            enabled=False
        )
        #self.text_entity.parent = self  # così si muove con l'NPC
        self.text_entity.scale = 6 / self.scale_x 
        self.text_entity.z = -1

    def update(self):
        self.text_entity.world_position = self.world_position + Vec3(0, 2.5, 0)
        if self.minimap and self.minimap.player:            
            distanza = distance(self.position, self.minimap.player.position)
            if distanza <= self.interaction_radius:
                target_pos = self.minimap.player.position
                target_pos.y = self.position.y
                direction = (target_pos - self.position).normalized()
                target_angle = math.degrees(math.atan2(direction.x, direction.z))
                self.rotation_y = lerp(self.rotation_y, target_angle + 180, time.dt * 5)  # +180 se il modello è girato

    def parla(self):
        frase = self.dialoghi[self.dialogo_index]
        print(f"{self.name} dice: \"{frase}\"")
        self.text_entity.text = frase
        self.text_entity.enabled = True
       

        # Nasconde il testo dopo qualche secondo
        invoke(self.nascondi_testo, delay=3)

        self.dialogo_index = (self.dialogo_index + 1) % len(self.dialoghi)

    def nascondi_testo(self):
        self.text_entity.enabled = False

    def on_click(self):
        if self.minimap and self.minimap.player:
            distanza = distance(self.position, self.minimap.player.position)
            if distanza <= self.interaction_radius:
                self.parla()
            else:
                print(f"{self.name} ti ignora... sei troppo lontano ({round(distanza, 2)} unità).")
        