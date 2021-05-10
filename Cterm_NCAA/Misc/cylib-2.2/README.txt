CyLib 2.0  (27.07.2016)
---------

Copyright (c) 2015-16 by Peter Guentert. All rights reserved.



NAME

    cylib -- Convert MOL2 or PDB molecular topology descriptions into CYANA residue library


SYNOPSIS

    cylib [-help] [-aa] [-n] [-c] [-fba atom] [-lba atom] [-sc] [-nic] [-np] [-info] [-o lib-file] topology-file


DESCRIPTION

    CYLIB is an algorithm for converting molecular topology descriptions in MOL2 format or from the PDB
    Chemical Component Dictionary into CYANA residue library entries.

    The CYANA structure calculation algorithm uses torsion angle molecular dynamics for the efficient
    computation of three-dimensional structures from NMR-derived restraints. For this, the molecules have
    to be represented in torsion angle space with rotations around covalent single bonds as the only
    degrees of freedom. The molecule must be given a tree structure of torsion angles connecting rigid
    units composed of one or several atsoms with fixed relative positions. Setting up CYANA residue
    library entries therefore involves, besides straightforward format conversion, the non-trivial step
    of defining a suitable tree structure of torsion angles, and to re-order the atoms in a way that is
    compatible with this tree structure. This can be done manually for small numbers of ligands but the
    process is time-consuming and error-prone. An automated method is necessary in order to handle the
    large number of different potential ligand molecules to be studied in drug design projects. CyLib is
    an algorithm for this purpose.
    
    The input topology-file must be either in MOL2 format (with extension .mol2) or in the mmCIF format
    of the PDB Chemical Component Dictionary (with extension .cif).

    The following options are available:

    -help  help
    -aa    molecule is an amino acid; add N- and C-terminal overlap atoms
    -n     add N-terminal overlap atoms
    -c     add C-terminal overlap atoms
    -nc    add N- and C-terminal overlap atoms
    -fba   specify first atom of the backbone.
    -lba   specify last atom of the backbone.
    -sc    treat all rings as rigid.
    -nic   use non-ideal cartesian coordinates
    -np    do not add pseudo atoms
    -info  print details of the running program to the screen
    -fr    set output filename to residue name
    -o     write output CYANA residue entry to the given file
           (default: name of input file, but with extension .lib)


FILES

    cylib         script to start CyLib
    cylib.Linux   executable for Linux, called by cylib
    cylib.Darwin  executable for Mac, called by cylib

    *.mol2        example MOL2 input files
    *.cif         example input files from the PDB Chemical Component Dictionary
    *.lib         example output files produced by CyLib from the corresponding .cif file


EXAMPLES

    Convert PDB Chemical Component Dictionary entry MND.cif into CYANA library entry MND.lib:

        cylib MND.cif

    Convert PDB Chemical Component Dictionary entry PYH.cif for an unatural amino acid:

        cylib -aa PYH.cif

    Convert PDB Chemical Component Dictionary entry 002.cif for a general (not amino acid) molecule
    with specification of the first and last backbone atom:

        cylib -fba C1 -lba C23 002.cif


REFERENCE

    When reporting results obtained with CyLib, please cite this publication:

    Maden Yilmaz, E. & Güntert, P. NMR structure calculation for all small molecule
    ligands and non-standard residues from the PDB Chemical Component Dictionary.
    J. Biomol. NMR 63, 21-37 (2015).


BUGS

    A small number of CIF files from the PDB Chemical Component Dictionary cannot be converted
    correctly. See the publication for details.


LICENSE

    The CYLIB 2.0 Software License is a legal agreement, governed by the laws of
    Switzerland, between an end user (the "Licensee"), either an individual or an entity,
    and Dr. Peter Guentert (the "Licensor"). The program package CYLIB 2.0 (copyright (c)
    2015-16 by Peter Guentert), comprising all computer programs, source code, license keys,
    documentation, example data and other files delivered to the Licensee, as well as any
    copies, modifications or derivative works made by the Licensee, are hereinafter referred
    to collectively as the "Software". A derivative work is any software that contains one
    or several parts of the Software in original or modified form. If the Licensor provides
    the Licensee with updates of the Software, these will become part of the Software and
    will be controlled by this license.

     1. The Licensor grants to the Licensee a non-exclusive, non-transferable, permanent
        license to install and use the Software on computer systems located at the site of
        the Licensee's organization. However, a violation of any of the clauses of this
        license agreement by the Licensee shall terminate automatically and with immediate
        effect the Licensee's right to install, use or store the Software in any form. Use
        of the Software is restricted to the Licensee and to direct collaborators who are
        members of the organization of the Licensee at the site of the Licensee and who
        accept the terms of this license. The Licensee shall neither use the Software to
        produce other software that duplicates functionality of the Software nor translate
        source code of the Software into another programming language.

     2. The Licensor retains at all times ownership of the Software delivered to the
        Licensee. Any modifications or derivative works based on the Software are considered
        part of the Software, and ownership thereof is retained by the Licensor. All parts
        of the Software must carry the copyright notice, will be controlled by this license,
        and will be promptly destroyed by the Licensee upon termination of this license.

     3. The Licensee shall not use the Software for any purpose (research or otherwise) that
        is supported by a "for profit" organization without prior written authorization from
        the Licensor.
        [This Article does not apply to Licensees who have obtained a Commercial License.]

     4. The Licensee shall not disclose in any form the Software or any modifications or
        derivative works based on the Software to third parties without prior written
        authorization from the Licensor.

     5. The Licensee agrees that the Software has been developed in connection with academic
        research projects and is provided "as is". The Licensor disclaims all warranties
        with regard to the Software or any of its results, including any implied warranties
        of merchantability or fitness for a particular purpose. In no event shall the
        Licensor be liable for any damages, however caused, including, without limitation,
        any damages arising out of the use of the Software, loss of use of the Software, or
        damage of any sort to the Licensee.

     6. The Licensee agrees that any reports or publications of results obtained with the
        Software will acknowledge its use by the literature citation: Maden Yilmaz, E. &
        Güntert, P. NMR structure calculation for all small molecule ligands and
        non-standard residues from the PDB Chemical Component Dictionary.  J. Biomol. NMR
        63, 21-37 (2015).
