from typing import Sequence
from clease.datastructures import SystemChanges
from .mc_constraint import MCConstraint


class FixedIndices(MCConstraint):
    """Constrain a given set of indices during an MC run.
    Any suggested system changes by the MC algorithm are rejected if
    they invovle an index in the fixed indices.

    Parameters:

    fixed_indices: sequence of integers
        The indices of the atoms object which are to be fixed.
    """

    name = "FixedIndices"

    def __init__(self, fixed_indices: Sequence[int]):
        super().__init__()
        # We use a set for O(1) lookup time
        # Also, every entry is an index, and should therefore be an int.
        # Avoid floating point conversion issues with round
        self.fixed_basis = set(round(idx) for idx in fixed_indices)

    def __call__(self, system_changes: SystemChanges) -> bool:
        """Check if any of the proposed changes are from the fixed basis"""
        return all(change.index not in self.fixed_basis for change in system_changes)
