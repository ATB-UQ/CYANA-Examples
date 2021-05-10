import numpy as np

RESTRAINTS_LINE_TEMPLATE = "{resid_a:>2} {resname_a:>5} {atom_name_a:>3}   {resid_b:>2} {resname_b:>5} " \
                           "{atom_name_b:>3} {dist_limit:>6.2f} {weight:>5.1f}"
BOND_WEIGHT = 10
SECOND_NEIGHBOUR_WEIGHT = 5
BOND_DELTA = 0.04
SECOND_NEIGHBOUR_DELTA = 0.08


def restraints(lib_a, lib_b, linking_bond_a, linking_bond_b, atom_mapping):
    warnings = []

    joining_bond_distance = calc_joining_bond_distance(lib_a, lib_b, linking_bond_a, linking_bond_b, warnings)
    lower_limits = [
        RESTRAINTS_LINE_TEMPLATE.format(
            resid_a=lib_a.residue_id, resname_a=lib_a.resname, atom_name_a=lib_a.atoms[linking_bond_a[0]]["name"],
            resid_b=lib_b.residue_id, resname_b=lib_b.resname, atom_name_b=lib_b.atoms[linking_bond_b[0]]["name"],
            dist_limit=joining_bond_distance - BOND_DELTA / 2., weight=BOND_WEIGHT,
        )
    ]
    upper_limits = [
        RESTRAINTS_LINE_TEMPLATE.format(
            resid_a=lib_a.residue_id, resname_a=lib_a.resname, atom_name_a=lib_a.atoms[linking_bond_a[0]]["name"],
            resid_b=lib_b.residue_id, resname_b=lib_b.resname, atom_name_b=lib_b.atoms[linking_bond_b[0]]["name"],
            dist_limit=joining_bond_distance + BOND_DELTA / 2., weight=BOND_WEIGHT,
        )
    ]

    second_neighbour_distances = calculate_2nd_neighbour_distances(lib_a, lib_b, linking_bond_a, linking_bond_b,
                                                                   atom_mapping, warnings)
    for (atom_a, atom_b), distance in second_neighbour_distances.items():
        lower_limits.append(
            RESTRAINTS_LINE_TEMPLATE.format(
                resid_a=lib_a.residue_id, resname_a=lib_a.resname, atom_name_a=lib_a.atoms[atom_a]["name"],
                resid_b=lib_b.residue_id, resname_b=lib_b.resname, atom_name_b=lib_b.atoms[atom_b]["name"],
                dist_limit=distance-SECOND_NEIGHBOUR_DELTA/2., weight=SECOND_NEIGHBOUR_WEIGHT,
            )
        )
        upper_limits.append(
            RESTRAINTS_LINE_TEMPLATE.format(
                resid_a=lib_a.residue_id, resname_a=lib_a.resname, atom_name_a=lib_a.atoms[atom_a]["name"],
                resid_b=lib_b.residue_id, resname_b=lib_b.resname, atom_name_b=lib_b.atoms[atom_b]["name"],
                dist_limit=distance+SECOND_NEIGHBOUR_DELTA/2., weight=SECOND_NEIGHBOUR_WEIGHT,
            )
        )
    return "\n".join(lower_limits + upper_limits) + "\n", warnings


def calc_joining_bond_distance(lib_a, lib_b, linking_bond_a, linking_bond_b, warnings):
    joining_bond_distance_a = np.linalg.norm(
        lib_a.atoms[linking_bond_a[0]]["coords"] - lib_a.atoms[linking_bond_a[1]]["coords"])
    joining_bond_distance_b = np.linalg.norm(
        lib_b.atoms[linking_bond_b[0]]["coords"] - lib_b.atoms[linking_bond_b[1]]["coords"])
    if abs(joining_bond_distance_a - joining_bond_distance_b) > 0.001:
        warnings.append(
            "Linking bonds are not equivalent {}={}, {}={}. A restraint distance of {:.2f} will be used".format(
                linking_bond_a, joining_bond_distance_a, linking_bond_b, joining_bond_distance_b,
                joining_bond_distance_a))
    joining_bond_distance = joining_bond_distance_a
    return joining_bond_distance


def calculate_2nd_neighbour_distances(lib_a, lib_b, linking_bond_a, linking_bond_b, atom_mapping, warnings):
    # check types for atom mappings
    for atom_a, atom_b in atom_mapping.items():
        if lib_a.atoms[atom_a]["type"] != lib_b.atoms[atom_b]["type"]:
            warnings.append("CYANA atom types do not match: {} ({}) and {} ({})".format(
                atom_a, lib_a.atoms[atom_a]["type"], atom_b, lib_b.atoms[atom_b]["type"])
            )
    # Restraint distances needed between last atom of lib_a, and atoms bonded to last atom of lib_b i.e. 2nd neighbours across the linking bond.
    # This method assumes that mappings are appropriate, thus 2nd neighbour atom distances in one lib file
    # can be used across the linking bond.
    second_neighbour_distances = {}

    # Find atoms in lib_a which are mapped to be equivalent to 2nd neighbours in lib_b. This can be obtained from the
    # list of atoms connected to the first leaving atom (exluding the last remaining atom and pseudo atoms).
    second_neigbours_for_a = {atom_id: atom for atom_id, atom in lib_a.atoms[linking_bond_a[1]]["conn"].items()
                              if atom_id != linking_bond_a[0] and atom["type"] != "PSEUD"}
    for atom_id, atom in second_neigbours_for_a.items():
        # (last_atom_lib_a, 2nd_neighbour_in_b) = distance(last_atom_lib_a, 2nd_neighbour_in_a)
        second_neighbour_distances[(linking_bond_a[0], atom_mapping[atom_id])] = np.linalg.norm(
            lib_a.atoms[linking_bond_a[0]]["coords"] - atom["coords"]
        )

    # Now, similarly find atoms in lib_b which are mapped to be equivalent to 2nd neighbours in lib_a.
    second_neigbours_for_b = {atom_id: atom for atom_id, atom in lib_b.atoms[linking_bond_b[1]]["conn"].items()
                              if atom_id != linking_bond_b[0]}
    reversed_mapping = {atom_id_b: atom_id_a for atom_id_a, atom_id_b in atom_mapping.items()}
    for atom_id, atom in second_neigbours_for_b.items():
        # (last_atom_lib_b, 2nd_neighbour_in_a) = distance(last_atom_lib_b, 2nd_neighbour_in_b)
        second_neighbour_distances[(reversed_mapping[atom_id], linking_bond_b[0])] = np.linalg.norm(
            lib_b.atoms[linking_bond_b[0]]["coords"] - atom["coords"]
        )
    return second_neighbour_distances