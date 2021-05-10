import sys
import numpy as np

class CyanaLib(object):

    def __init__(self, cyana_lib_str, residue_id=0):
        self.header, self.residue_info = cyana_lib_str.split("RESIDUE")
        self.resname, self.n_dihedrals, self.n_atoms, self.first_id, self.last_id = self.residue_info.splitlines()[0].split()
        self.atom_lines, self.dihedral_lines = parse_cyana_lib(cyana_lib_str)
        self.atoms = build_atoms(self.atom_lines)
        self.dihedrals = build_dihedrals(self.dihedral_lines)
        for d in self.dihedrals.values():
            d["atoms"] = []
            for atom_id in d["atom_ids"]:
                if atom_id != 0:
                    d["atoms"].append(self.atoms[atom_id])
        for a in self.atoms.values():
            a["conn"] = {}
            for atom_id in a["conn_ids"]:
                if atom_id != 0:
                    a["conn"][atom_id] = self.atoms[atom_id]
        self.residue_id = residue_id

    def remove_atom(self, atom_id):
        self.atoms[atom_id]["removed"] = True
        self.atoms[atom_id]["index"] = 0
        # re-index all atoms
        sorted_atoms = [a for _, a in sorted(self.atoms.items()) if not "removed" in a]
        for i, a in enumerate(sorted_atoms, start=1):
            a["index"] = i
        # find dihedrals that contain this atom
        dihedrals_to_remove = [id for id, d in self.dihedrals.items()
                               if atom_id in d["atom_ids"]]
        # remove any dihedral containing this atom
        for dihedral_id in dihedrals_to_remove:
            del self.dihedrals[dihedral_id]

    def remove_atoms_to_chains_end(self, keeping_atom_id, removing_atom_id):
        connected_atoms_to_remove = [id for id in self.atoms[removing_atom_id]["conn"].keys() if id != keeping_atom_id]
        self.remove_atom(removing_atom_id)
        self.remove_all_and_connected_atoms(connected_atoms_to_remove)
        # if a dihedral's "last effected atom" (chain_end_id) refers to deleted atom, set it to be keeping_atom_id
        for d in self.dihedrals.values():
            if d["chain_end_id"] != 0 and "removed" in self.atoms[d["chain_end_id"]]:
                d["chain_end_id"] = keeping_atom_id

    def remove_all_and_connected_atoms(self, atoms_to_remove):
        """
        Recursively remove all connected atoms
        """
        connected_atom_ids = []
        for id_to_remove in atoms_to_remove:
            if "removed" in self.atoms[id_to_remove]:
                continue
            connected_atom_ids.extend([id for id, a in self.atoms[id_to_remove]["conn"].items() if not "removed" in a])
            self.remove_atom(id_to_remove)
        if connected_atom_ids:
            self.remove_all_and_connected_atoms(connected_atom_ids)

    def write(self):
        return "\n".join([self.header[:-1], self.write_res_info(), self.write_dihedrals(), self.write_atoms()]) + "\n"

    def write_res_info(self):
        # keep existing last id offset
        last_id_offset = int(self.n_atoms) - int(self.last_id)
        n_atoms = len([a for a in self.atoms.values() if "removed" not in a])
        return "RESIDUE   {resname} {n_dihedrals:>6d} {n_atoms:>4d} {first_id:>4d} {last_id:>4d}".format(
            resname=self.resname, n_dihedrals=len(self.dihedrals), n_atoms=n_atoms, first_id=int(self.first_id),
            last_id=n_atoms-last_id_offset)

    def write_dihedrals(self):
        #   1 OMEGA    0    0    0.0000    2    1    3    4    0
        lines = []
        for i, (_, d) in enumerate(sorted(self.dihedrals.items()), start=1):
            chain_end = self.atoms[d["chain_end_id"]]["index"] if (d["chain_end_id"] != 0) else 0
            lines.append(
                "{index:>4} {static}{i:>4d} {j:>4d} {k:>4d} {l:>4d} {chain_end:>4d}".format(
                    index=i, static=d["line"][5:31], i=d["atoms"][0]["index"], j=d["atoms"][1]["index"],
                    k=d["atoms"][2]["index"], l=d["atoms"][3]["index"], chain_end=chain_end)
            )
        return "\n".join(lines)

    def write_atoms(self):
        #   1 C    C_BYL    0    0.0000   -2.1908    0.0314    0.0905    2    3    0    0    0
        lines = []
        for id, a in sorted(self.atoms.items(), key=lambda x:x[1]["index"]):
            if "removed" in a:
                continue
            bonds = "".join(
                ["{:>5}".format(self.atoms[int(atom_id)]["index"]) if (atom_id != "0") else "    0"
                    for atom_id in a["line"][61:].split()
                 ]
            )
            lines.append(
                "{index:>4} {static}{bonds}".format(index=a["index"], static=a["line"][5:60], bonds=bonds)
            )

        return "\n".join(lines)


def build_atoms(atom_lines):
    atoms = {}
    for i, line in atom_lines.items():
        cols = line.split()
        atoms[i] = {"index": i, "name": cols[1], "type": cols[2], "coords": np.array(list(map(float, cols[5:8]))),
                    "conn_ids": list(map(int, cols[8:])), "line": line}
    return atoms


def build_dihedrals(dihedral_lines):
    dihedrals = {}
    for i, line in dihedral_lines.items():
        cols = line.split()
        dihedrals[i] = {"index": i, "name": cols[1], "atom_ids": list(map(int, cols[5:9])), "chain_end_id":int(cols[-1]), "line":line}
    return dihedrals


def parse_cyana_lib(cyana_lib_str):
    dihedrals = {}
    atoms = {}
    for line in cyana_lib_str.splitlines():
        if not line.strip():
            continue
        cols = line.split()
        if cols[0].isdigit():
            # dihedral line
            if len(cols) == 10:
                dihedrals[int(cols[0])] = line
            # atom line
            if len(cols) == 13:
                atoms[int(cols[0])] = line
    return atoms, dihedrals


if __name__=="__main__":
    cyana_lib = CyanaLib(open("testing/met.lib").read())
    cyana_lib.remove_atoms_to_chains_end(8, 9)
    open("testing/modified_met.lib", "w").write(cyana_lib.write())

    # cyana_lib = CyanaLib(open(sys.argv[1]).read())
    # cyana_lib.remove_atoms_to_chains_end(int(sys.argv[2]), int(sys.argv[3]))
    # print(cyana_lib.write())
