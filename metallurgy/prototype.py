from collections import Counter
from math import gcd
from numbers import Number
from string import ascii_uppercase
from typing import List


class Prototype:
    """A crystal structure prototype, defining positions of atoms in a unit cell.

    :group: structures

    Attributes
    ----------

    name
       Name of the structure (e.g. Strukturbericht A1).
    lattice
       Lattice vectors the shape of the unit cell.
    basis
       Basis vectors defining positions of atoms in the unit cell.

    """

    def __init__(
        self,
        name: str,
        lattice: List[List[Number]],
        basis: List[dict],
        space_group: str,
    ):
        self.name = name
        self.lattice = lattice
        self.basis = basis
        self.original_basis = basis
        self.space_group = space_group

    @property
    def num_atoms(self) -> int:
        """Return the number of atoms in the unit cell
        :group: structures
        """
        return len(self.basis)

    @property
    def elements(self) -> list:
        """Return list of unique elements in the unit cell
        :group: structures
        """
        return list(self.element_counts.keys())

    @property
    def element_counts(self) -> dict:
        """Return count of each unique element in the unit cell
        :group: structures
        """
        return Counter(b["element"] for b in self.basis)

    @property
    def composition(self) -> dict:
        """Return percentage of each unique element in the unit cell
        :group: structures
        """
        total = self.num_atoms
        counts = self.element_counts
        return {e: counts[e] / total for e in counts}

    @property
    def num_elements(self) -> int:
        """Return the number of unique elements in the unit cell
        :group: structures
        """
        return len(self.elements)

    @property
    def formula(self) -> str:
        counts = self.element_counts
        divisor = gcd(*counts.values())

        formula_str = ""
        for element, label in zip(counts.keys(), ascii_uppercase):
            formula_str += label
            number = int(counts[element] / divisor)
            if number > 1:
                formula_str += str(number)

        return formula_str

    def __repr__(self) -> str:
        return self.name
