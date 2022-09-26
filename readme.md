## Tiger Archive File System

Tools and APIs for manipulating tiger files.

`TAFS` is a proprietary file format developed by [Crystal Dynamics][1] for
their games such as the [Tomb Raider][2] series.

This project is based upon some openly available reverse-engineered information
about this file format and my own findings.

Crystal Dynamics, Inc. is not in any way associated with this project's
development.

The goal is just to be able to change some gameplay elements by modifying some
game resources (also known as 'modding' in video games communities).

No game files (either modified or original) would ever be redistributed along
with this project.

#### Features

- [ ] Update archives with the modified resources.
- [ ] List resources without extracting any data.
- [ ] Extract resources to a known workable format.
- [ ] Remove modified resources from the archives.

#### Resources Directory Layout

The extracted resources are organized this way,

```
res:                                                           <-(Content root)
    v3_lara_aviatrix:                                          <-(Object level)
        400.dds                                                     <-.(Assets)
        401.dds                                                       |
        402.dds                                                       |
        403.dds                                                       |
        421.dds                                                       |
        422.dds                                                       |
        424.dds                                                       |
        425.dds                                                       |
        592.mesh                                                      |
    v3_lara_aviatrix.drm                                             <-(Object)
    .
    .
    .
        .
        .
        .
```

One can modify the game assets but leave the filenames and the directory layout
as is. Otherwise, the changes will not take effect or the update will fail.

If you want to rename asset files in your creative workspace, just symlink
asset files outside the `res` directory.

Make sure you clean up (move or delete) any extracted but unmodified assets
before updating the archives with the modified assets. Otherwise, It'll just
waist cpu time and disk space for no gains whatsoever.

`<obj_name>.drm` files are only needed if you have modified assets in the
`<obj_name>` directory or both should be cleaned up altogether.

If you happen to get some modified assets from somewhere else, You'll just have
to carefully reorganize them as such to make use of these tools.

#### Licensing, Copyright, and Attribution

`Copyright 2022 Nikhil Saxena (nik6ena)`

This project is released under the terms of the GNU GPL3.

You may read the terms & permissions as made available in the [license][gpl3]
file.

[gpl3]: licenses/gpl-3.0.md
[1]: https://en.wikipedia.org/wiki/Crystal_Dynamics
[2]: https://en.wikipedia.org/wiki/Tomb_Raider
