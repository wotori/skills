---
name: blender-asset-pipeline
description: Work with Blender and 3D asset pipelines involving .blend, .fbx, .glb, .gltf, .obj, materials, vertex colors, UVs, texture baking, model splitting, and format conversion. Use when Codex needs to inspect, convert, repair, split, texture, orient, or validate 3D model assets, especially when Blender headless Python is unavailable or unstable and fallback tools such as assimp or direct GLB manipulation are needed.
---

# Blender Asset Pipeline

Use this skill for local 3D asset work where correctness matters more than a one-shot conversion. Prefer inspecting the actual scene graph, meshes, materials, UVs, vertex colors, transforms, and output validation before making broad assumptions.

## Tool Order

1. Try Blender headless first when `bpy` access is needed:

```bash
blender --background --python script.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python script.py
```

2. If Blender crashes before Python starts, stop treating it as an asset problem. On macOS this can be a Metal/GPU backend startup issue. Use fallback tools.

3. Use `assimp` for inspection and conversion when it supports the format:

```bash
assimp info model.fbx
assimp info scene.blend
assimp dump model.fbx /tmp/model.assxml -s
assimp export scene.blend /tmp/scene.glb -f glb2
assimp export model.glb model.obj -f obj
assimp extract scene.blend
```

4. Use direct GLB editing when conversion output is almost right but needs deterministic fixes. GLB is JSON plus binary buffers; use Node.js `Buffer` or Python `struct` to rewrite accessors, bufferViews, images, materials, and scenes.

## Inspection Workflow

Always inspect both source and output:

- Count meshes, nodes, materials, embedded textures, vertices, faces.
- Compare scene hierarchy between `.blend` and `.fbx` if names live in one file and materials live in another.
- Check whether "textures" are actual images or vertex colors. `assimp info` may show `Textures (embed.): 0` while meshes still have `COLOR_0` and `TEXCOORD_0`.
- Inspect node names like `base`, `eyes`, `transp`, `DblSided`, and `alt###`; they often encode parts, transparency layers, eyes, or alternatives.
- Validate final files with `assimp info` for every output, not just a sample.

## Conversion Patterns

For splitting one packed scene into named models:

1. Use the file with correct names as the naming source, often `.fbx`.
2. Use the file with better materials/geometry as the geometry source, often `.blend`.
3. Export the geometry source to one temporary GLB.
4. Map source mesh nodes to entity names by hierarchy or order.
5. Write one GLB per entity with only used nodes, meshes, materials, accessors, bufferViews, images, textures, and samplers.
6. Add a root transform for orientation fixes rather than baking transforms into vertices unless the target format requires it.
7. Export OBJ/MTL from the final GLB so both formats share the same final geometry and orientation.

For orientation fixes:

- Use a GLB root node rotation for GLB, for example X -90 degrees quaternion `[-0.7071067811865475, 0, 0, 0.7071067811865476]`.
- Verify with bounding boxes after import; do not rely only on visual intuition.

## Texture and Vertex Color Policy

Do not assume vertex colors can be turned into a correct bitmap using existing UVs. Existing UVs may overlap, wrap, or share islands between parts with different vertex colors. That causes sliding, stretched, or duplicated-looking textures.

When baking vertex colors to PNG:

- If existing UVs are non-overlapping and valid, rasterize vertex colors into that UV layout.
- If textures look wrong or overlap is likely, create a new non-overlapping atlas and rewrite `TEXCOORD_0`.
- For robust atlas output, duplicate vertices per triangle, assign each triangle its own atlas cell, bake interpolated vertex colors into that cell, then remove `COLOR_0` and set material `baseColorTexture`.
- Force alpha opaque unless the source specifically needs transparency; vertex color alpha may contain zeros that produce black or transparent artifacts.
- For OBJ, ensure every `newmtl` in `.mtl` has `map_Kd ModelName.png`.

Read `references/glb-atlas-repair.md` for the concrete GLB buffer/accessor workflow and pitfalls from the Everything Library Animals conversion.

## Alternatives vs Parts

Be careful with nodes named `alt###`:

- `alt###` children with strongly overlapping bounding boxes are often alternative versions, not parts. Exporting all of them together creates an apparent duplicate model with a slight offset.
- Keep real parts such as `base`, `eyes`, `transp`, `DblSided`, and small transparent/light layers together.
- For ambiguous `alt###` cases, compare mesh bounding boxes and vertex counts. If two alternatives have large overlap and similar size, choose one or export separate variant files.

## Validation Checklist

Run these checks before finishing:

```bash
find output -name '*.glb' -print0 | xargs -0 -n1 assimp info >/dev/null
find output -name '*.obj' -print0 | xargs -0 -n1 assimp info >/dev/null
```

For GLB outputs, verify:

- `images.length > 0` and `textures.length > 0` when textures are expected.
- Materials have `pbrMetallicRoughness.baseColorTexture`.
- `COLOR_0` is absent after baking to texture to avoid double color multiplication.
- `POSITION`, `NORMAL`, and `TEXCOORD_0` accessor counts match.
- UVs are in `0..1` for generated atlases.
- There are no unexpected duplicate meshes from overlapping `alt###` alternatives.

For OBJ outputs, verify:

- `.obj`, `.mtl`, and `.png` exist together.
- `.mtl` uses real image filenames, not internal names such as `*0`.
- All material blocks that can be used by the OBJ include `map_Kd`.
