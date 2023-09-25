"""Core input set generators for vasp.

Note that this module will ultimately be moved to atomate2.
"""
from dataclasses import dataclass

from atomate2.vasp.sets.base import VaspInputGenerator
from atomate2.vasp.sets.core import StaticSetGenerator
from pymatgen.core.structure import Structure
from pymatgen.io.vasp.outputs import Outcar, Vasprun


@dataclass
class StaticHFSetGenerator(StaticSetGenerator):
    """Generator for static HF calculations."""

    calc_type: str = "static_hf"

    def get_incar_updates(
        self,
        structure: Structure,
        prev_incar: dict = None,
        bandgap: float = 0,
        vasprun: Vasprun = None,
        outcar: Outcar = None,
    ) -> dict:
        """Get updates to the INCAR for a static VASP job.

        Parameters
        ----------
        structure
            A structure.
        prev_incar
            An incar from a previous calculation.
        bandgap
            The band gap.
        vasprun
            A vasprun from a previous calculation.
        outcar
            An outcar from a previous calculation.

        Returns
        -------
        dict
            A dictionary of updates to apply.
        """
        updates = super().get_incar_updates(
            structure, prev_incar, bandgap, vasprun, outcar
        )
        updates["LHFCALC"] = True
        updates["AEXX"] = 1.0
        updates["ALGO"] = "C"
        return updates


@dataclass
class NonSCFHFSetGenerator(VaspInputGenerator):
    """Class to generate VASP non-self-consistent field Hartree-Fock input sets."""

    calc_type: str = "nonscf_hf"

    def get_incar_updates(
        self,
        structure: Structure,
        prev_incar: dict = None,
        bandgap: float = 0,
        vasprun: Vasprun = None,
        outcar: Outcar = None,
    ) -> dict:
        """Get updates to the INCAR for a static VASP job.

        Parameters
        ----------
        structure
            A structure.
        prev_incar
            An incar from a previous calculation.
        bandgap
            The band gap.
        vasprun
            A vasprun from a previous calculation.
        outcar
            An outcar from a previous calculation.

        Returns
        -------
        dict
            A dictionary of updates to apply.
        """
        nb = max(outcar.data["nplwvs_at_kpoints"]) * 2 - 1
        updates = {
            "LHFCALC": True,
            "AEXX": 1.0,
            "ISYM": -1,
            "ALGO": "sub",
            "NELM": 1,
            "NBANDS": nb,
        }

        # ENCUT = $enc
        # SIGMA = 0.0001
        # EDIFF = 1E-6
        # LHFCALC =.TRUE.
        # AEXX = 1.0
        # ISYM = -1
        # ALGO = sub;
        # NELM = 1
        # NBANDS = $nb
        return updates


@dataclass
class NonSCFMP2CBSSetGenerator(VaspInputGenerator):
    """Class to generate VASP non-self-consistent field Hartree-Fock input sets."""

    calc_type: str = "nonscf_hf"

    def get_incar_updates(
        self,
        structure: Structure,
        prev_incar: dict = None,
        bandgap: float = 0,
        vasprun: Vasprun = None,
        outcar: Outcar = None,
    ) -> dict:
        """Get updates to the INCAR for a static VASP job.

        Parameters
        ----------
        structure
            A structure.
        prev_incar
            An incar from a previous calculation.
        bandgap
            The band gap.
        vasprun
            A vasprun from a previous calculation.
        outcar
            An outcar from a previous calculation.

        Returns
        -------
        dict
            A dictionary of updates to apply.
        """
        nb = max(outcar.data["nplwvs_at_kpoints"]) * 2 - 1
        updates = {
            "LHFCALC": True,
            "AEXX": 1.0,
            "ISYM": -1,
            "ALGO": "MP2",
            "LSFACTOR": True,
            "NBANDS": nb,
        }

        # ENCUT = $enc
        # SIGMA = 0.0001
        # LHFCALC =.TRUE.
        # AEXX = 1.0
        # ISYM = -1
        # ALGO = MP2
        # NBANDS = $nb
        # LSFACTOR =.TRUE.
        return updates


@dataclass
class NonSCFMP2NOsSetGenerator(VaspInputGenerator):
    """Class to generate VASP non-self-consistent field Hartree-Fock input sets."""

    calc_type: str = "nonscf_hf"

    def get_incar_updates(
        self,
        structure: Structure,
        prev_incar: dict = None,
        bandgap: float = 0,
        vasprun: Vasprun = None,
        outcar: Outcar = None,
    ) -> dict:
        """Get updates to the INCAR for a static VASP job.

        Parameters
        ----------
        structure
            A structure.
        prev_incar
            An incar from a previous calculation.
        bandgap
            The band gap.
        vasprun
            A vasprun from a previous calculation.
        outcar
            An outcar from a previous calculation.

        Returns
        -------
        dict
            A dictionary of updates to apply.
        """
        nb = max(outcar.data["nplwvs_at_kpoints"]) * 2 - 1
        updates = {
            "LHFCALC": True,
            "AEXX": 1.0,
            "ISYM": -1,
            "ALGO": "MP2NO",
            "LAPPROX": True,
            "NBANDS": nb,
        }

        # ENCUT = $enc
        # SIGMA = 0.0001
        # LHFCALC =.TRUE.
        # AEXX = 1.0
        # ISYM = -1
        # ALGO = MP2NO;
        # NBANDS = $nb
        # LAPPROX =.TRUE.
        return updates


@dataclass
class NonSCFHFNOsSetGenerator(VaspInputGenerator):
    """Class to generate VASP non-self-consistent field Hartree-Fock input sets."""

    calc_type: str = "nonscf_hf"

    def get_incar_updates(
        self,
        structure: Structure,
        prev_incar: dict = None,
        bandgap: float = 0,
        vasprun: Vasprun = None,
        outcar: Outcar = None,
    ) -> dict:
        """Get updates to the INCAR for a static VASP job.

        Parameters
        ----------
        structure
            A structure.
        prev_incar
            An incar from a previous calculation.
        bandgap
            The band gap.
        vasprun
            A vasprun from a previous calculation.
        outcar
            An outcar from a previous calculation.

        Returns
        -------
        dict
            A dictionary of updates to apply.
        """
        nb = max(outcar.data["nplwvs_at_kpoints"]) * 2 - 1
        updates = {
            "LHFCALC": True,
            "AEXX": 1.0,
            "ISYM": -1,
            "ALGO": "MP2NO",
            "LAPPROX": True,
            "NBANDS": nb,
        }

        # ENCUT = $enc
        # SIGMA = 0.0001
        # EDIFF = 1E-6
        # LHFCALC =.TRUE.
        # AEXX = 1.0
        # ISYM = -1
        # ALGO = sub;
        # NELM = 1
        # NBANDS = $nbno
        # NBANDSHIGH = $nbno
        return updates


@dataclass
class VaspDumpCc4sFilesGenerator(VaspInputGenerator):
    """Class to generate input set for dumping cc4s files."""

    calc_type: str = "vasp_cc4s_dump"
    nbfp: int = 6

    def get_incar_updates(
        self,
        structure: Structure,
        prev_incar: dict = None,
        bandgap: float = 0,
        vasprun: Vasprun = None,
        outcar: Outcar = None,
    ) -> dict:
        """Get updates to the INCAR for a static VASP job.

        Parameters
        ----------
        structure
            A structure.
        prev_incar
            An incar from a previous calculation.
        bandgap
            The band gap.
        vasprun
            A vasprun from a previous calculation.
        outcar
            An outcar from a previous calculation.

        Returns
        -------
        dict
            A dictionary of updates to apply.
        """
        outcar.nelect
        nbno = 0
        updates = {
            "LHFCALC": True,
            "AEXX": 1.0,
            "ISYM": -1,
            "ALGO": "CC4S",
            "NBANDS": nbno,
        }

        # ENCUT = $enc
        # SIGMA = 0.0001
        # EDIFF = 1E-5
        # LHFCALC =.TRUE.
        # AEXX = 1.0
        # ISYM = -1
        # ALGO = CC4S
        # NBANDS = $nbno
        # NBANDSHIGH = $nbno
        # ENCUTGW =$egw
        # ENCUTGWSOFT =$egw
        return updates
