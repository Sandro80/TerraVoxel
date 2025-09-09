from ursina import *

class Tree(Entity):
    def __init__(self, audio_manager, model_name='tree',  texture_model=None, position=(0,0,0), scale=1,minimap= None, traceable = False):
        super().__init__(
            model=f'assets/models/{model_name}.obj',
            #texture=f'assets/models/{texture_model}.png',
            position=position,
            scale=scale
        )

        self.minimap=minimap
        if texture_model:  # Se è specificata, la carico
            self.texture = f'assets/models/{texture_model}'
            
        self.audio_manager = audio_manager
        self.traceable = traceable
      
        if self.bounds:
            size = Vec3(1, self.bounds.size.y, 1)
            offset = self.bounds.center  # Posizione corretta del collider
            self.collider = BoxCollider(self, size=size, center=offset)

            # Debug visivo
            """self.debug_collider = Entity(
                parent=self,
                model='cube',
                scale=size,
                position=offset,
                color=color.rgba(255, 0, 0, 100),
                wireframe=True
            )"""
        else:
            print(f"⚠️ Bounds non disponibili per il modello: {model_name}")
    
    def reset_collider(self):
        if self.bounds:
            size = Vec3(1, self.bounds.size.y, 1)
            offset = self.bounds.center  # Posizione corretta del collider
            self.collider = BoxCollider(self, size=size, center=offset)

    def on_hit(self):
        self.audio_manager.play_sound('axe_hit_tree')
        # Altri effetti: cambiare colore, far cadere legna, ecc.