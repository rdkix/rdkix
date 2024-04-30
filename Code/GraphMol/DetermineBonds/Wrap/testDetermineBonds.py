#
#  Copyright (C) 2022 Greg Landrum
#   @@ All Rights Reserved @@
#
#  This file is part of the RDKix.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the RDKix source tree.

import glob
import os
import unittest

from rdkix import Chem, RDConfig
from rdkix.Chem import rdDetermineBonds


class TestCase(unittest.TestCase):

  def testVdWConnectivity(self):
    testDir = os.path.join(RDConfig.RDBaseDir, 'Code', 'GraphMol', 'DetermineBonds', 'test_data',
                           'connectivity')
    for fn in glob.glob(os.path.join(testDir, 'test*.xyz')):
      mol = Chem.MolFromXYZFile(fn)
      self.assertIsNotNone(mol)
      smi = mol.GetProp('_FileComments')
      omol = Chem.MolFromSmiles(smi)
      self.assertIsNotNone(omol)

      rdDetermineBonds.DetermineConnectivity(mol, useHueckel=False)
      mol = Chem.RemoveAllHs(mol, sanitize=False)
      self.assertEqual(mol.GetNumAtoms(), omol.GetNumAtoms())
      self.assertEqual(mol.GetNumBonds(), omol.GetNumBonds())
      for aid1 in range(mol.GetNumAtoms()):
        for aid2 in range(aid1 + 1, mol.GetNumAtoms()):
          if omol.GetBondBetweenAtoms(aid1, aid2):
            self.assertIsNotNone(mol.GetBondBetweenAtoms(aid1, aid2))

  def testCtDConnectivity(self):
    testDir = os.path.join(RDConfig.RDBaseDir, 'Code', 'GraphMol', 'DetermineBonds', 'test_data',
                           'connectivity')
    for fn in glob.glob(os.path.join(testDir, 'test*.xyz')):
      mol = Chem.MolFromXYZFile(fn)
      self.assertIsNotNone(mol)
      smi = mol.GetProp('_FileComments')
      omol = Chem.MolFromSmiles(smi)
      self.assertIsNotNone(omol)

      rdDetermineBonds.DetermineConnectivity(mol, useHueckel=False, useVdw=False)
      mol = Chem.RemoveAllHs(mol, sanitize=False)
      self.assertEqual(mol.GetNumAtoms(), omol.GetNumAtoms())
      self.assertEqual(mol.GetNumBonds(), omol.GetNumBonds())
      for aid1 in range(mol.GetNumAtoms()):
        for aid2 in range(aid1 + 1, mol.GetNumAtoms()):
          if omol.GetBondBetweenAtoms(aid1, aid2):
            self.assertIsNotNone(mol.GetBondBetweenAtoms(aid1, aid2))

  @unittest.skipUnless(rdDetermineBonds.hueckelEnabled(), "YAeHMOP support not enabled")
  def testHueckelConnectivity(self):
    testDir = os.path.join(RDConfig.RDBaseDir, 'Code', 'GraphMol', 'DetermineBonds', 'test_data',
                           'connectivity')
    for fn in glob.glob(os.path.join(testDir, 'test*.xyz')):
      mol = Chem.MolFromXYZFile(fn)
      self.assertIsNotNone(mol)
      smi = mol.GetProp('_FileComments')
      omol = Chem.MolFromSmiles(smi)
      self.assertIsNotNone(omol)
      charge = Chem.GetFormalCharge(omol)

      rdDetermineBonds.DetermineConnectivity(mol, useHueckel=True, charge=charge)
      mol = Chem.RemoveAllHs(mol, sanitize=False)
      self.assertEqual(mol.GetNumAtoms(), omol.GetNumAtoms())
      self.assertEqual(mol.GetNumBonds(), omol.GetNumBonds())
      for aid1 in range(mol.GetNumAtoms()):
        for aid2 in range(aid1 + 1, mol.GetNumAtoms()):
          if omol.GetBondBetweenAtoms(aid1, aid2):
            self.assertIsNotNone(mol.GetBondBetweenAtoms(aid1, aid2))

  def testVdWBonds(self):
    testDir = os.path.join(RDConfig.RDBaseDir, 'Code', 'GraphMol', 'DetermineBonds', 'test_data',
                           'connectivity')
    for fn in glob.glob(os.path.join(testDir, 'test*.xyz')):
      mol = Chem.MolFromXYZFile(fn)
      self.assertIsNotNone(mol)
      smi = mol.GetProp('_FileComments')
      omol = Chem.MolFromSmiles(smi)
      self.assertIsNotNone(omol)
      charge = Chem.GetFormalCharge(omol)

      rdDetermineBonds.DetermineBonds(mol, useHueckel=False, charge=charge)
      mol = Chem.RemoveAllHs(mol, sanitize=False)
      self.assertEqual(mol.GetNumAtoms(), omol.GetNumAtoms())
      self.assertEqual(mol.GetNumBonds(), omol.GetNumBonds())
      for aid1 in range(mol.GetNumAtoms()):
        for aid2 in range(aid1 + 1, mol.GetNumAtoms()):
          if omol.GetBondBetweenAtoms(aid1, aid2):
            self.assertIsNotNone(mol.GetBondBetweenAtoms(aid1, aid2))

  # FIX: this is problematic...
  # def testHueckelBonds(self):
  #   testDir = os.path.join(RDConfig.RDBaseDir, 'Code', 'GraphMol', 'DetermineBonds', 'test_data',
  #                          'connectivity')
  #   for fn in glob.glob(os.path.join(testDir, 'test*.xyz')):
  #     mol = Chem.MolFromXYZFile(fn)
  #     self.assertIsNotNone(mol)
  #     smi = mol.GetProp('_FileComments')
  #     omol = Chem.MolFromSmiles(smi)
  #     self.assertIsNotNone(omol)
  #     charge = Chem.GetFormalCharge(omol)

  #     try:
  #       rdDetermineBonds.DetermineBonds(mol, useHueckel=True, charge=charge)
  #     except ValueError:
  #       print(fn)
  #       print(' ', smi)
  #       print(' ', Chem.MolToSmiles(mol))

  #     mol = Chem.RemoveAllHs(mol, sanitize=False)
  #     self.assertEqual(mol.GetNumAtoms(), omol.GetNumAtoms())
  #     self.assertEqual(mol.GetNumBonds(), omol.GetNumBonds())
  #     for aid1 in range(mol.GetNumAtoms()):
  #       for aid2 in range(aid1 + 1, mol.GetNumAtoms()):
  #         if omol.GetBondBetweenAtoms(aid1, aid2):
  #           self.assertIsNotNone(mol.GetBondBetweenAtoms(aid1, aid2))


if __name__ == '__main__':  # pragma: nocover
  unittest.main()
