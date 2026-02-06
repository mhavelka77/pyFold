from io import StringIO
import json
import asyncio
import numpy as np
from Bio.PDB.StructureBuilder import StructureBuilder
from Bio.PDB import PDBIO

### CONSTANTS
AA_DISTANCE = 3.8  # Angstroms
REPULSION_DIST = 3.0  # Angstroms - minimum allowed distance between any two residues
SPRING_K = 2.0  # Bond spring stiffness
REPULSION_K = 2.0  # Steric repulsion strength
HYDRO_K = 0.02  # Hydrophobic attraction strength
STEP_SIZE = 0.1  # Force scaling per timestep
TEMPERATURE = 0.05  # Random thermal noise magnitude


class Residue:
    def __init__(self, x, y, z, code, hydrophobic=0):
        self.position = np.array([x, y, z], dtype=float)
        self.code = code
        self.hydrophobic = hydrophobic


class Chain:
    def __init__(self, seq):
        self.seq = seq
        self.residues = []

        for i in range(len(seq)):
            self.residues.append(
                Residue(i * AA_DISTANCE, 0, 0, seq[i], np.random.randint(2))
            )

    def __iter__(self):
        for residue in self.residues:
            yield residue

    def __str__(self) -> str:
        sb = StructureBuilder()
        sb.init_structure("toy_fold")
        sb.init_model(0)
        sb.init_chain("A")

        for i, residue in enumerate(self, 1):
            sb.init_residue(residue.code, "H" if residue.hydrophobic else " ", i, " ")

            pos = residue.position
            sb.init_atom("N", pos + np.array([-1.46, 0, 0]), 0.0, 1.0, " ", " N  ")
            sb.init_atom("CA", pos, 0.0, 1.0, " ", " CA ")
            sb.init_atom("C", pos + np.array([1.51, 0, 0]), 0.0, 1.0, " ", " C  ")
            sb.init_atom("O", pos + np.array([1.51, 1.23, 0]), 0.0, 1.0, " ", " O  ")

        writer = PDBIO()
        writer.set_structure(sb.get_structure())
        buf = StringIO()
        writer.save(buf)
        return buf.getvalue()

    def calculate_timestep(self):
        n = len(self.residues)
        forces = [np.zeros(3) for _ in range(n)]

        # 1. Backbone springs - keep neighbors at AA_DISTANCE apart
        for i in range(n - 1):
            diff = self.residues[i + 1].position - self.residues[i].position
            dist = np.linalg.norm(diff)
            if dist == 0:
                continue
            direction = diff / dist
            force = SPRING_K * (dist - AA_DISTANCE) * direction
            forces[i] += force
            forces[i + 1] -= force

        # 2. Steric repulsion + 3. Hydrophobic attraction (all pairs)
        for i in range(n):
            for j in range(i + 2, n):
                diff = self.residues[j].position - self.residues[i].position
                dist = np.linalg.norm(diff)
                if dist == 0:
                    continue
                direction = diff / dist

                # Repulsion - push apart if too close
                if dist < REPULSION_DIST:
                    repel = REPULSION_K * (REPULSION_DIST - dist) * direction
                    forces[i] -= repel
                    forces[j] += repel

                # Hydrophobic attraction - pull hydrophobic pairs together
                if self.residues[i].hydrophobic and self.residues[j].hydrophobic:
                    forces[i] += HYDRO_K * direction
                    forces[j] -= HYDRO_K * direction

        # Apply forces + thermal noise
        for i in range(n):
            self.residues[i].position += forces[i] * STEP_SIZE
            self.residues[i].position += (np.random.rand(3) - 0.5) * TEMPERATURE


### Main folding function called from webserver
async def fold(seq, steps):
    yield json.dumps({"status": "starting", "message": "Folding initiated..."}) + "\n"

    chain = Chain(seq)

    # Perform X steps of folding simulation based on forces
    for i in range(steps):
        chain.calculate_timestep()
        yield (
            json.dumps(
                {
                    "status": "folding",
                    "step": i + 1,
                    "total_steps": steps,
                    "pdb": str(chain),
                }
            )
            + "\n"
        )
        await asyncio.sleep(0)
    yield json.dumps({"status": "completed", "pdb": ""}) + "\n"
