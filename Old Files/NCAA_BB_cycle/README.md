# CYANA-Examples
Example use of ATB CYANA library files for an all ALA heptaptide cyclised through a backbone peptide bond

Files must be located in the same file when CYANA starts

  - Example.cya
      - Structure calculation file
      - Distance constraints in the form of restraints.upl and .lol form the backbone peptide bond
     
   - Example.seq
      - Sequence file
      - Includes link statement to eliminate steric repulsion between covalently bound atoms
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/Sequence_file

  - init.cya
      - Initialisation file
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/CYANA_Macro:_init

  - restraints.lol
      - Distance restraints to cyclise the heptapeptide with a backbone peptide bond
      - Lower distances 1 and 2 atom bonds apart 
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/Distance_restraint_file

  - restraints.upl
      - Distance restraints to cyclise the heptapeptide with a backbone peptide bond
      - Upper distances 1 and 2 atom bonds apart 
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/Distance_restraint_file
