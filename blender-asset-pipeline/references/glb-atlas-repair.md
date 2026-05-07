# GLB Atlas Repair Reference

Use this reference when converting vertex-colored Blender/FBX assets into textured GLB/OBJ outputs, or when textures appear stretched, sliding, duplicated, black, or mismatched.

## GLB Structure

A binary GLB v2 contains:

- 12-byte header: magic `glTF`, version, total length.
- JSON chunk.
- Optional binary chunk.

The JSON describes:

- `scenes`, `nodes`, `meshes`, `materials`
- `accessors` for typed views of data
- `bufferViews` for byte ranges inside `buffers`
- `images`, `textures`, `samplers`

When rewriting GLB:

1. Read JSON and BIN chunks.
2. Copy only referenced nodes, meshes, materials, accessors, bufferViews, images, textures, and samplers.
3. Compact the BIN chunk and remap all indices.
4. Pad JSON and BIN chunks to 4-byte boundaries.
5. Update `buffers[0].byteLength`.

## Reading Accessors

Accessor values are read from:

```text
bufferView.byteOffset + accessor.byteOffset + i * stride
```

Use:

- `componentType 5126`: float32
- `5125`: uint32
- `5123`: uint16
- `5121`: uint8

Common types:

- `SCALAR`: 1 component
- `VEC2`: 2 components
- `VEC3`: 3 components
- `VEC4`: 4 components

Respect `bufferView.byteStride` when present.

## Baking Vertex Colors to a Safe Atlas

If existing UVs overlap, do not bake into the existing UV layout. Use a generated atlas:

1. Count triangles across all primitives.
2. Choose an atlas size: start at 512, increase to 1024/2048 for many triangles.
3. Build a square grid of cells.
4. For each source triangle:
   - Duplicate its 3 vertices into new `POSITION`, `NORMAL`, and `TEXCOORD_0` arrays.
   - Assign triangle UVs to a unique cell, leaving a small margin.
   - Rasterize interpolated `COLOR_0` into that cell.
5. Dilate colored pixels into blank margins to reduce mip/filter seams.
6. Encode the atlas as PNG.
7. Attach PNG to GLB as an embedded image.
8. Set `material.pbrMetallicRoughness.baseColorTexture`.
9. Delete `COLOR_0` from primitives.

This produces larger geometry because vertices are no longer shared, but it avoids incorrect texture overlap.

## Material Notes

For GLB:

```json
"pbrMetallicRoughness": {
  "baseColorFactor": [1, 1, 1, 1],
  "baseColorTexture": { "index": 0 },
  "metallicFactor": 0
}
```

For OBJ/MTL:

```text
newmtl Mat_Standard
map_Kd ModelName.png
Kd 1 1 1
d 1
illum 1
```

If `assimp export` writes `map_Kd *0`, replace it with the real PNG filename.

## Alternative Mesh Detection

`alt###` nodes often indicate variants. A robust heuristic:

- Only consider collapsing when an entity has exactly two mesh nodes and both names match `alt\d+`.
- Compute each mesh bounding box.
- If overlap divided by the smaller volume is high, and volumes are not wildly different, treat them as alternatives.
- Keep the first variant by default unless the user asks for all variants.

Do not collapse multi-part assets such as eyes, transparent layers, double-sided wings, skeleton parts, teeth, or named body parts.

## Validation Snippets

Mass import validation:

```bash
for f in output/*.glb output/*.obj; do assimp info "$f" >/dev/null || exit 1; done
```

Expected atlas GLB properties:

- No `indices` on primitives if using per-triangle duplicated geometry.
- No `COLOR_0`.
- Has `POSITION`, `NORMAL`, `TEXCOORD_0`.
- `POSITION.count === TEXCOORD_0.count`.
- `POSITION.count % 3 === 0`.
- Has one or more embedded images/textures.
