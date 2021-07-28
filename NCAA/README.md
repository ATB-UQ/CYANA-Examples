# CYANA-Examples
Example use of ATB CYANA library files for a non-canonical amino acid containing tripeptide 

Files must be located in the same file when CYANA starts

  - Example.cya
      - Structure calculation file
     
  - Example.lib
      - Residue library file generated from the ATB 
      - Non-canonical amino acid code UT9Y
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/Residue_library_file

  - Example.seq
      - Sequence file
      - Calling ncAA amino acid code UT9Y in position 2
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/Sequence_file

  - init.cya
      - Initialisation file
      - Use command 'read lib./Example.lib append' to append residue library file Example.lib to the standard CYANA library file 
      - CYANA wiki entry: http://www.cyana.org/wiki/index.php/CYANA_Macro:_init
      
Non-canonical amino acid library file accessed from the ATB https://atb.uq.edu.au/molecule.py?molid=516192 

