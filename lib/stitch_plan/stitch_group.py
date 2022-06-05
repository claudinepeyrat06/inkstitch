# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .stitch import Stitch


class StitchGroup:
    """A collection of Stitch objects with attached instructions and attributes.

    StitchGroups will later be combined to make ColorBlocks, which in turn are
    combined to make a StitchPlan.  Jump stitches are allowed between
    StitchGroups, but not between stitches inside a StitchGroup.  This means
    that EmbroideryElement classes should produce multiple StitchGroups only if
    they want to allow for the possibility of jump stitches to be added in
    between them by the stitch plan generation code.
    """

    def __init__(self, color=None, stitches=None, trim_after=False, stop_after=False,
                 tie_modus=0, force_lock_stitches=False, stitch_as_is=False, tags=None):
        self.color = color
        self.trim_after = trim_after
        self.stop_after = stop_after
        self.tie_modus = tie_modus
        self.force_lock_stitches = force_lock_stitches
        self.stitch_as_is = stitch_as_is
        self.stitches = []

        if stitches:
            self.add_stitches(stitches)

        if tags:
            self.add_tags(tags)

    def __add__(self, other):
        if isinstance(other, StitchGroup):
            return StitchGroup(self.color, self.stitches + other.stitches)
        else:
            raise TypeError("StitchGroup can only be added to another StitchGroup")

    def __len__(self):
        # This method allows `len(patch)` and `if patch:
        return len(self.stitches)

    def add_stitches(self, stitches):
        for stitch in stitches:
            self.add_stitch(stitch)

    def add_stitch(self, stitch):
        if not isinstance(stitch, Stitch):
            # probably a Point
            stitch = Stitch(stitch)

        self.stitches.append(stitch)

    def reverse(self):
        return StitchGroup(self.color, self.stitches[::-1])

    def add_tags(self, tags):
        for stitch in self.stitches:
            stitch.add_tags(tags)

    def add_tag(self, tag):
        for stitch in self.stitches:
            stitch.add_tag(tag)
