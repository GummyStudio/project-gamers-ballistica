# Released under the MIT License. See LICENSE for details.
#
"""Various utilities useful for gameplay."""

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs

if TYPE_CHECKING:
    pass


class SharedObjects:
    """Various common components for use in games.

    Category: Gameplay Classes

    Objects contained here are created on-demand as accessed and shared
    by everything in the current activity. This includes things such as
    standard materials.
    """

    _STORENAME = bs.storagename()

    def __init__(self) -> None:
        activity = bs.getactivity()
        if self._STORENAME in activity.customdata:
            raise RuntimeError(
                'Use SharedObjects.get() to fetch the'
                ' shared instance for this activity.'
            )
        self._object_material: bs.Material | None = None
        self._player_material: bs.Material | None = None
        self._pickup_material: bs.Material | None = None
        self._footing_material: bs.Material | None = None
        self._attack_material: bs.Material | None = None
        self._death_material: bs.Material | None = None
        self._region_material: bs.Material | None = None
        self._railing_material: bs.Material | None = None

    @classmethod
    def get(cls) -> SharedObjects:
        """Fetch/create the instance of this class for the current activity."""
        activity = bs.getactivity()
        shobs = activity.customdata.get(cls._STORENAME)
        if shobs is None:
            shobs = SharedObjects()
            activity.customdata[cls._STORENAME] = shobs
        assert isinstance(shobs, SharedObjects)
        return shobs

    @property
    def region_material(self) -> bs.Material:
        """A bascenev1.Material used for non-physical collision shapes
        (regions); collisions can generally be allowed with this material even
        when initially overlapping since it is not physical.
        """
        if self._region_material is None:
            self._region_material = bs.Material()
        return self._region_material
