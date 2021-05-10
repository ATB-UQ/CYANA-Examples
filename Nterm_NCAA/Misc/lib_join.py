import json
import sys
from os.path import basename, dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cyana_lib import CyanaLib
from gen_restraints import restraints


def join_libs(lib_a, lib_b, linking_bond_a, linking_bond_b, atom_mapping):
    restraints_str, warnings = restraints(lib_a, lib_b, linking_bond_a, linking_bond_b, atom_mapping)
    lib_a.remove_atoms_to_chains_end(*linking_bond_a)
    lib_b.remove_atoms_to_chains_end(*linking_bond_b)
    return restraints_str, warnings


if __name__=="__main__":
    # cyana_lib_a = CyanaLib(open("testing/met.lib").read(), residue_id=1)
    # cyana_lib_b = CyanaLib(open("testing/met.lib").read(), residue_id=2)
    # atom_mapping = dict([(8, 8), (7, 9), (9, 7), (12, 6), (11, 15), (10, 14)])
    # restraints_str, warnings = join_libs(cyana_lib_a, cyana_lib_b, (8, 9), (7, 8), atom_mapping)
    # open("testing/met_a.lib", "w").write(cyana_lib_a.write())
    # open("testing/met_b.lib", "w").write(cyana_lib_b.write())
    # open("testing/restraints.cya", "w").write(restraints_str)
    # print("\n".join(warnings))

    # lib_file_a = "testing/disulfide_template.lib"#sys.argv[1]
    # lib_file_b = "testing/disulfide_template.lib"#sys.argv[2]
    # args_file = "testing/args.json"#sys.argv[3]

    lib_file_a = sys.argv[1]
    lib_file_b = sys.argv[2]
    args_file = sys.argv[3]
    with open(args_file) as fh:
        args = json.load(fh)
    res_id_a, res_id_b, linking_bond_a, linking_bond_b, atom_mapping_list = \
        args["res_id_a"], args["res_id_b"], args["linking_bond_a"], args["linking_bond_b"], args["atom_mapping"]
    cyana_lib_a = CyanaLib(open(lib_file_a).read(), residue_id=res_id_a)
    cyana_lib_b = CyanaLib(open(lib_file_b).read(), residue_id=res_id_b)
    atom_mapping = dict(atom_mapping_list)
    restraints_str, warnings = join_libs(cyana_lib_a, cyana_lib_b, linking_bond_a, linking_bond_b, atom_mapping)
    open("{}_a.lib".format(basename(lib_file_a).split(".")[0]), "w").write(cyana_lib_a.write())
    open("{}_b.lib".format(basename(lib_file_b).split(".")[0]), "w").write(cyana_lib_b.write())
    open("restraints.cya", "w").write(restraints_str)
    print("\n".join(warnings))
