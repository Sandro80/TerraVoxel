
from ursina import *
from collections import deque

class Animal(Entity):
    def __init__(self, nome,audio_manager, model_name='',  texture_model=None, posizione=(0,0,0),
                 salute=100, suono_colpito=None, minimap= None,  traceable = True, exp = 10, drop_items=None,  **kwargs):
        
        super().__init__(
            model=f'assets/models/animals/{model_name}.gltf',
            position=posizione,
            collider='box',
            **kwargs
        )


        if texture_model:  # Se è specificata, la carico
            self.texture = f'assets/models/animals/{texture_model}'

        self.rotation_y = random.uniform(0, 360)  
        self.nome = nome
        self.salute = salute
        self.audio_manager = audio_manager  # istanza di AudioManager
        self.suono_colpito = suono_colpito  # chiave del suono da riprodurre
        self.velocita = 2
        self.minimap = minimap
        self.traceable= traceable
        self.exp = exp
        
        # Lista di drop possibili [(model, texture, scale), ...]
        self.drop_items = drop_items or []
        self.movement_cellsxz = []


        # Variabili per il movimento
        self.path = []
        self.path_index = 0
        self.wait_timer = random.uniform(1, 3)

        """if self.bounds:
            size = Vec3(1, self.bounds.size.y, 1)
            offset = self.bounds.center  # Posizione corretta del collider
            self.collider = BoxCollider(self, size=size, center=offset)

            # Debug visivo
            self.debug_collider = Entity(
                parent=self,
                model='cube',
                scale=size,
                position=offset,
                color=color.rgba(255, 0, 0, 100),
                wireframe=True
            )
        else:
            print(f"⚠️ Bounds non disponibili per il modello: {model_name}")"""
  
     # ---------------------------
    # PATHFINDING BFS
    # ---------------------------
    def find_path(self, start, goal):
        """Trova un percorso tra start e goal usando BFS."""
        walkable = set(self.movement_cellsxz)
        queue = deque([start])
        came_from = {start: None}

        directions = [
            (1,0), (-1,0), (0,1), (0,-1),  # ortogonali
            (1,1), (1,-1), (-1,1), (-1,-1) # diagonali
        ]

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            for dx, dz in directions:
                neighbor = (current[0] + dx, current[1] + dz)
                if neighbor in walkable and neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)

        if goal not in came_from:
            return []

        # Ricostruisci il percorso
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    # ---------------------------
    # SCELTA NUOVA DESTINAZIONE
    # ---------------------------
    def scegli_nuova_destinazione(self):
        if not self.movement_cellsxz:
            return
        start = (int(self.x), int(self.z))
        goal = random.choice(self.movement_cellsxz)
        self.path = self.find_path(start, goal)
        self.path_index = 0


     # ---------------------------
    # MOVIMENTO FRAME-BY-FRAME
    # ---------------------------
    def muovi(self, dt):
        # Se stiamo aspettando
        if self.wait_timer > 0:
            self.wait_timer -= dt
            return

        # Se non abbiamo un percorso, scegline uno
        if not self.path or self.path_index >= len(self.path):
            self.wait_timer = random.uniform(1, 3)
            self.scegli_nuova_destinazione()
            return

        # Prossima cella
        cella = self.path[self.path_index]
        target_pos = Vec3(cella[0] + 0.5, self.y, cella[1] + 0.5)

        direzione = target_pos - self.position
        distanza = direzione.length()

        if distanza < 0.05:
            # Passa alla cella successiva
            self.path_index += 1
        else:
            # Rotazione graduale verso la direzione di marcia
            angolo_target = math.degrees(math.atan2(direzione.x, direzione.z))
            self.rotation_y = self.rotation_y + (angolo_target - self.rotation_y) * min(10 * dt, 1)

            # Movimento fluido
            direzione = direzione.normalized()
            self.position += direzione * self.velocita * dt



    def prendi_danno(self, quantita, attaccante=None):
        self.salute -= quantita
        print(f"{self.nome} ha {self.salute} punti vita rimanenti")

        if self.suono_colpito:
            self.audio_manager.play_sound(self.suono_colpito)

        if hasattr(self.parent, 'modified'):
            self.parent.modified = True

        if self.salute <= 0:
            self.morire(attaccante)

        print(self.movement_cellsxz)

    def lasciaOggetti(self):
        pass

  

    def morire(self, killer=None):
        if killer and hasattr(killer, "add_exp"):
            killer.add_exp(self.exp)  # assegna exp al player
            print(f"{killer} ha guadagnato {self.exp} EXP!")

        if self in self.parent.animali:
            print(f"{self.nome} è morto.")
            self.parent.animali.remove(self)
        if self in self.minimap.tracked:
            self.minimap.tracked.remove(self)
        
        if hasattr(self.parent, 'modified'):
            self.parent.modified = True

        destroy(self)
