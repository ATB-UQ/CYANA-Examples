# CYANA-Examples
Example use of ATB CYANA library files for a tetrapeptide with methylated N- and C-terminals

Files must be located in the same file when CYANA starts

  - Example.cya
      - Structure calculation file
     
  - Example.lib
      - Residue library file generated from the ATB 
      - N-terminal amino acid code C0GM
      - C-terminal amino acid code PZHU

  - Example.seq
      - Sequence file
      - Calling N-terminal C0GM and C-terminal PZHU 

  - init.cya
      - Initialisation file
      - Use command 'read lib./Example.lib append' to append residue library file Example.lib to the standard CYANA library file 

C-terminal amino acid library file was accessed from the ATB https://atb.uq.edu.au/molecule.py?molid=714149
N-terminal amino acid library file was accessed from the ATB 
