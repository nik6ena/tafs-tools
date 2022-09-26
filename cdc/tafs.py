"""Tiger Archive File System.

.. note:: The module currently supports TAFS version 3."""

#  Copyright 2022 Nikhil Saxena (nik6ena)
#
#  This source file (the source code or "the software") is released
#  under the terms of the GNU GPL3.
#
#  You may read the terms & permissions as made available in the license
#  file or online at <https://www.gnu.org/licenses/gpl-3.0.html>.

from pathlib import Path
from struct import Struct
from typing import BinaryIO

import cdrm
import drm

MAGIC = 0x54414653
MAGIC_DDS = 0x20534444
MAGIC_DX10 = 0x30315844
MAGIC_DX9 = 0x39444350  # 'PC' D9 -> DirectX 9, PCDX11 -> DX 11
MAGIC_SECT = 0x54434553

header = Struct('< 6I')


class Tafs:
    def __init__(self, f: BinaryIO):
        self.f = f


def parse(f: BinaryIO) -> Tafs:

    return Tafs(f)


class Dist:
    def __init__(self, home: Path):
        """The game distribution.

        :param home: Game installation directory."""
        self.tafs: dict[int, Tafs] = {}
        self.home = home

    def __del__(self):
        for _, tafs in self.tafs:
            tafs.f.close()

    def get_tafs(self, sect: drm.Section) -> Tafs:
        i = sect.packed[4]

        try:
            return self.tafs[i]
        except KeyError:
            if i == 0x10:
                f = 'patch.000.tiger'
            elif i == 0:
                f = 'title.000.tiger'
            elif i == 0x20:
                f = 'patch1.000.tiger'
            elif i == 0x30:
                f = 'patch2.000.tiger'
            else:
                # Not yet figured out. One could search for an equivalent
                # section in every other tiger file present in the home. That
                # will be taken care after implementing the listing feature.
                raise ValueError(i)

        self.tafs[i] = f = parse((self.home / f).open('r+b'))

        return f

    def update(self, res: Path):
        """
        :param res: Directory containing only the modified resources.
        """
        for drm_p in res.glob('*.drm'):
            with drm_p.open('rb') as f:
                sects = drm.parse(f).sects

            for sect_p in drm_p.with_suffix('').iterdir():
                tafs = self.get_tafs(sects[int(sect_p.stem)])
