from ursina import *

class GameHUD(Entity):
    def __init__(self,):
        super().__init__(parent=camera.ui)
      
        self.bar = Entity(parent=self, model='quad', color=color.red,scale=(0.38, 0.03), origin=(0.5, -0.5),position=(0.75, -0.45))
        
        self.hp_text = Text(text='HP: 100/100', parent=self,origin=(0.5, -0.5),position=(0.75, -0.42), scale=1)
        self.score_text = Text(text='Score: 0', parent=self,origin=(0.5, -0.5),position=(0.75, -0.39), scale=1)    
        self.exp_text = Text(text='Exp: 0', parent=self,origin=(0.5, -0.5),position=(0.75, -0.36), scale=1)
        self.level_text = Text(text='Level: 0', parent=self,origin=(0.5, -0.5),position=(0.75, -0.33), scale=1)

    def update_health(self, current_hp, max_hp):
        ratio = current_hp / max_hp
        self.bar.scale_x = 0.38 * max(0, min(1, ratio))  # clamp tra 0 e 1
        self.hp_text.text = f"HP: {int(current_hp)}/{max_hp}"

    def update_score(self, amount):
        self.score_text.text = f"Score: {amount}"

    def update_exp(self, amount):
        self.exp_text.text = f"Exp: {amount}"

    def update_level(self, amount):
        self.level_text.text = f"Level: {amount}"