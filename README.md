# LIB_TRACE

Bitmap -> shapes for LiveCode 9.6.3:
- **Outline tracing:** follows the edge of every shape in a 1-bit grid (or any image's
  mask) and returns polygon points LiveCode graphics take directly. Clockwise, each
  outline closed on its first point, outlines separated by an empty line.
- Grid to 3D map has moved to LIB_MAP (`Map.Pieces`), with stitching and pathfinding.

Pure handlers (data in, data out). Grids are LIB_BIT's format: lines of `0`/`1`.

```
start using stack "<path>/LIB_TRACE/livecode/lib_trace.livecodescript"
put Trace.MaskToGrid(the maskData of image "logo", the width of image "logo", the height of image "logo") into tGrid
set the points of graphic "outline" to Trace.Offset(Trace.Contours(tGrid), the left of image "logo" - 1, the top of image "logo" - 1)
```

| Handler | Does |
|---|---|
| `Trace.Contours(grid)` | every outline as points |
| `Trace.MaskToGrid(maskData, width, height [, threshold])` | an image's mask -> grid |
| `Trace.Offset(points, dx, dy)`, `Trace.Scale(points, factor)` | place and size points |

## Tests

`python3 tests/run_tests.py`: 9 checks in real LiveCode 9.6.3 through LIB_MCP. All pass.

## From the owner's bitmap tracer

`~/projects/xtalk_py/corpus/originals/BITMAPVECTORTRACER_Livecode_Stack_Script.txt`: the radial-sweep tracer (`doTrace`/`radialSweep`) and
`textToMap`, made pure. Differences from the original:
- the sweep table is built in, not read from a custom property
- an angle of 360 is treated as 0 (it would have found no table entry)
- a step limit stops a bad outline from looping forever
- `textToMap` (with its undefined `i` fixed) became LIB_MAP's `Map.Pieces`

Inner holes in a shape (a ring's inside edge) are not traced yet: a scan only starts
outlines where a row goes from empty to filled. Next: trace holes, simplify points
(fewer, longer edges), and meshify (outline -> extruded 3D mesh for xt3d).

Part of the family of separate libraries listed in `~/projects/LIB_MCP/README.md`.
