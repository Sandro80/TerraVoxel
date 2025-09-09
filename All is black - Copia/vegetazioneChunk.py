from ursina import *

class VegetazioneChunk(Entity):
    def __init__(self, posizione=(0,0,0), vegetazioni=[], atlas='assets/VegetazioneAtlas.png'):
        super().__init__(position=posizione, parent=scene)

        vertices = []
        uvs = []
        triangles = []
        count = 0

        for veg in vegetazioni:
            pos, uv_coords, doppio = veg
            base_vertices = [
                Vec3(-0.5, -0.5, 0),
                Vec3(0.5, -0.5, 0),
                Vec3(0.5, 0.5, 0),
                Vec3(-0.5, 0.5, 0)
            ]
            base_uvs = self.get_uv(uv_coords)

            # Trasla i vertici nella posizione desiderata
            vertices += [v + Vec3(*pos) for v in base_vertices]
            uvs += base_uvs
            triangles += [(count, count+1, count+2), (count+2, count+3, count)]
            count += 4

            if doppio:
                base_vertices_2 = [
                    Vec3(0, -0.5, -0.5),
                    Vec3(0, -0.5, 0.5),
                    Vec3(0, 0.5, 0.5),
                    Vec3(0, 0.5, -0.5)
                ]
                vertices += [v + Vec3(*pos) for v in base_vertices_2]
                uvs += base_uvs
                triangles += [(count, count+1, count+2), (count+2, count+3, count)]
                count += 4

        self.model = Mesh(vertices=vertices, uvs=uvs, triangles=triangles, mode='triangle')
        self.texture = atlas
        self.double_sided = True

    def get_uv(self, coords):
        u, v = coords
        step = 1/16
        v = 15 - v
        return [
            Vec2(u*step, v*step),
            Vec2((u+1)*step, v*step),
            Vec2((u+1)*step, (v+1)*step),
            Vec2(u*step, (v+1)*step)
        ]
