"""Data ram.

.. note:: The module currently supports DRM version 22."""

#  Copyright 2022 Nikhil Saxena (nik6ena)
#
#  This source file (the source code or "the software") is released
#  under the terms of the GNU GPL3.
#
#  You may read the terms & permissions as made available in the license
#  file or online at <https://www.gnu.org/licenses/gpl-3.0.html>.

from enum import IntEnum
from struct import Struct
from typing import BinaryIO

header = Struct(b'< 3I 12x I 4x')
data = Struct(b'< B 3s B 3s I 4x')


class SectionType(IntEnum):
    ANIMATION = 0x2
    DTP = 0x7
    EMPTY = 0x1
    GENERAL = 0x0
    MATERIAL = 0xA
    MESH = 0xC
    OBJ = 0xB
    PUSH_BUF = 0x4
    PUSH_BUF_WC = 0x3
    SCRIPT = 0x8
    SHADER = 0x9
    TEXTURE = 0x5
    UNKNOWN = 0xD
    WAVE = 0x6


class Section:
    def __init__(self, packed: memoryview):
        self.id = int.from_bytes(packed[:4], 'little')
        self.packed = packed

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @property
    def type(self) -> 'SectionType':
        return SectionType(self.packed[3])


class Drm:
    def __init__(
            self, sects: list[Section], count: int, names: list[str] | None):
        """
        :param sects: DRM sections.
        :param count: DRM sections list length.
        :param names: DRM object names, if exists."""
        self.sects = sects
        self.count = count
        self.names = names


def parse(f: BinaryIO) -> 'Drm':
    """
    :param f: DRM file.
    :return: Parsed DRM."""
    ver, size1, size2, count = header.unpack(f.read(header.size))

    if ver != 22:
        raise ValueError(f'DRM version {ver}')

    # Skip twenty bytes of unknown data per section
    f.seek(header.size + 20 * count)

    names = None

    if size := size1 + size2:
        names = f.read(size).decode('ascii').split('\0')
        names.pop()

    return Drm([Section(memoryview(f.read(data.size))) for _ in range(
        count)], count, names)
