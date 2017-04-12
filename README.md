# To extract a chain from a mmcif file.

This is realized by manipulating the atom_site category so that only
the atoms matching the specified chain ID (auth_asym_id) are retained.
All other categories are not changed so the output mmcif is inconsistent.

use --output-for-ngl to generate output mmcif for NGL viewer.
In such a case, only the atom_site category is written to the mmcif file.
Otherwise NGL viewer will not display the mmcif.

Only the 1st model is considered.

By default, water molecules are removed. Use --keep-water option to keep them).