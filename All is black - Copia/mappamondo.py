import json
import os
import time
from PIL import Image

class Mappamondo:
    def __init__(self, file_salvataggio="chunks_visitati.json", cartella_mappe="maps"):
        self.chunks_visitati = set()
        self.current_chunk = None
        self.chunks_esplorati = 0
        self.file_salvataggio = file_salvataggio
        self.cartella_mappe = cartella_mappe

        # Crea la cartella mappe se non esiste
        os.makedirs(self.cartella_mappe, exist_ok=True)

        self.carica_chunks()  # carica eventuali dati salvati

    def aggiorna_chunk(self, chunk_x, chunk_z):
        """Aggiorna il chunk corrente, registra se è nuovo e salva subito."""
        new_chunk = (chunk_x, chunk_z)
        if new_chunk != self.current_chunk:
            self.current_chunk = new_chunk
            if new_chunk not in self.chunks_visitati:
                self.chunks_visitati.add(new_chunk)
                self.chunks_esplorati += 1
                self.salva_chunks()  # salvataggio automatico

    def stampa_mappa_chunk(self):
        """Stampa una mappa testuale dei chunk visitati."""
        if not self.chunks_visitati:
            print("Nessun chunk visitato.")
            return

        xs = [c[0] for c in self.chunks_visitati]
        zs = [c[1] for c in self.chunks_visitati]
        min_x, max_x = min(xs), max(xs)
        min_z, max_z = min(zs), max(zs)

        for z in range(max_z, min_z - 1, -1):
            riga = ""
            for x in range(min_x, max_x + 1):
                if (x, z) == self.current_chunk:
                    riga += "P"  # posizione attuale
                elif (x, z) in self.chunks_visitati:
                    riga += "#"  # chunk visitato
                else:
                    riga += "."
            print(riga)

    def salva_chunks(self):
        """Salva i chunk visitati su file JSON."""
        with open(self.file_salvataggio, "w") as f:
            json.dump(list(self.chunks_visitati), f)

    def carica_chunks(self):
        """Carica i chunk visitati da file JSON."""
        try:
            with open(self.file_salvataggio, "r") as f:
                self.chunks_visitati = set(tuple(c) for c in json.load(f))
        except FileNotFoundError:
            self.chunks_visitati = set()

    def genera_mappa_png(self):
        """Genera e salva la mappa in una cartella dedicata con nome univoco."""
        if not self.chunks_visitati:
            return None

        xs = [c[0] for c in self.chunks_visitati]
        zs = [c[1] for c in self.chunks_visitati]
        min_x, max_x = min(xs), max(xs)
        min_z, max_z = min(zs), max(zs)

        width = max_x - min_x + 1
        height = max_z - min_z + 1

        img = Image.new("RGB", (width, height), (0, 0, 0))
        for (cx, cz) in self.chunks_visitati:
            img.putpixel((cx - min_x, max_z - cz), (0, 255, 0))

        if self.current_chunk:
            px, pz = self.current_chunk
            img.putpixel((px - min_x, max_z - pz), (255, 0, 0))

        img = img.resize((width*10, height*10), Image.NEAREST)

        # Nome file con timestamp
        filename = f"mappa_{int(time.time())}.png"
        filepath = os.path.join(self.cartella_mappe, filename)
        img.save(filepath)

        return filepath