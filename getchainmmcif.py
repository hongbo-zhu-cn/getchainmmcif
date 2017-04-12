#!/usr/bin/env python

# 2017_04_11
# to extract certain chain from a mmcif file
# only manipunate the atom_site category is not enough
# NGL viewer does not play the cif file.

# python lib
import sys
import argparse

# pdbx lib
from pdbx.reader.PdbxReader import PdbxReader
from pdbx.writer.PdbxWriter import PdbxWriter


def getchainmmcif(ciffn, chid, outciffn, keepwater=False, ngl=False):
    """
    Manipulate the atom_site category in mmcif file, where atom coordinates
    are stored, so that only the specified chain is retained.
    NOTE: If there are multiple models as in NMR structure, only the 1st model 
          is considered.

    @param ciffn: mmcif file name
    @param type: string

    @param chid: chain id (chain id can consist of more than 1 letter)
    @param type: string

    @param outciffn: output mmcif file name
    @param type: string

    @param keepwater: if HOH molecules should be retained in the output
    @param type: Boolean

    @param ngl: if the output is for ngl viewer. If True, only atom_site is output
    @param type: Boolean
    """
    
    # read cif file and put into a container
    fh = open(ciffn)
    xreader = PdbxReader(fh) # handle exceptions when necessary!
    cifdata = []
    xreader.read(cifdata)    # read cif content and put into cifdata
    fh.close()
    
    # only manipulate the atom_site category
    blk = cifdata[0]         # only consider the 1st data block 
    atom_site = blk.getObj('atom_site')  # handle exceptions when necessary!
    # PDB chain id is author specified chain id in cif: atom_site.auth_asym_id
    chididx = atom_site.getAttributeIndex('auth_asym_id')        # chain id
    mdididx = atom_site.getAttributeIndex('pdbx_PDB_model_num')  # model id
    resnidx = atom_site.getAttributeIndex('label_comp_id')       # residue name (3 letter)
    # To keep only the 1st model, we get the model id of the atom on the 1st row (row 0)
    mdid1st = atom_site.getRow(0)[mdididx]
        
    # keep only rows with specified chain id in the 1st model
    if keepwater:
        newrowlist = [r for r in atom_site.getRowList() \
                      if r[chididx] == chid and r[mdididx] == mdid1st]
    else:
        newrowlist = [r for r in atom_site.getRowList() \
                      if r[chididx] == chid and r[mdididx] == mdid1st and r[resnidx] != 'HOH']

    if ngl:
        buf = []
        buf.append('#')
        buf.append('loop_')
        buf.extend( [('_atom_site.%s' % (a,)) for a in atom_site.getAttributeList() ] )
        buf.extend( [' '.join(r) for r in newrowlist])
        outfh = open(outciffn, 'w')
        outfh.writelines('\n'.join(buf))
        outfh.close()
        
    
    else:
        atom_site.setRowList(newrowlist)  # manipulate the atom_site category

        # write the manipulated container
        # this output is recognized by PyMOL or Chimera but not NGL
        outfh = open(outciffn, 'w')
        xwriter = PdbxWriter(outfh)
        xwriter.write(cifdata)
        outfh.close()
    
    return



if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Extract a chain from mmcif file.')
    argparser.add_argument('-i', type=str, metavar='input mmcif', help='input mmcif')
    argparser.add_argument('-c', type=str, metavar='chain identifier', help='chain ID to extract')
    argparser.add_argument('-o', type=str, metavar='output mmcif', help='output mmcif')
    argparser.add_argument('--keep-water', dest='keepwater', action='store_true', 
                           help='keep water molecules in the output')
    argparser.add_argument('--output-for-ngl', dest='ngl', action='store_true', 
                           help='write output for NGL viewer')

    argparser.set_defaults(keepwater=False)
    argparser.set_defaults(ngl=False)
    
    args = argparser.parse_args()

    getchainmmcif(args.i, args.c, args.o, args.keepwater, args.ngl)
    
