# Lab 2.8: A Reusable CNC Digital Twin

Krishna Vamshi Challa

## What I built

A browser-based digital twin (`index.html`, Three.js) that reads the Metalogi MTConnect demo agent and animates a 3D machine from live position data. A small Python proxy (`proxy.py`) forwards requests to the agent so the browser is not blocked by CORS. The same code runs both devices the agent serves, Mazak and OKUMA, with no changes.

## 1. Discover the machine

The twin reads `/probe` once and finds every `Linear` and `Rotary` component under the selected device. For each axis it takes:

- **Position data item:** the `POSITION` or `ANGLE` item, preferring `ACTUAL` in the machine coordinate system. A rotary with only `ROTARY_VELOCITY` is treated as a spindle.
- **Units:** from the data item (`MILLIMETER`, `DEGREE`, `REVOLUTION/MINUTE`), converted to mm and degrees.
- **Coordinate systems:** the `CoordinateSystem` elements and their translations. OKUMA's machine coordinates are offset by about 4.7 m from the base, and the twin subtracts that offset.
- **Direction:** the `Motion` axis vector. OKUMA's X vector is `0.5 0 0` because X reports diameter, so the twin moves it half the reported value.
- **Kinematic chain:** `Motion parentIdRef` and `ComponentRelationship` PARENT/CHILD, which say which axis rides on which.
- **Travel:** `Specification` limits where the probe has them (Mazak B is -30° to 120°), otherwise the range seen in the agent's buffer.

## 2. Visualize motion

The model is assembled part by part from a kit of 17 parts that I modelled in SketchUp (`cnc_twin_parts_kit.skp`, exported to `kit.json`): rail plates, carriages, ram, spindle head, tilting housing, trunnion, rotary table, chuck, headstock and tool. Rail lengths are sized to each axis's travel.

Motion comes from `/sample`, which returns every observation with the agent's timestamp. All axes are played back on one shared clock, slightly behind live, and interpolated between real samples. Linear axes move in true millimetres and rotary axes in true degrees. The twin never extrapolates past real data.

Mazak shows the required three linear (X, Y, Z) and two rotary (B, C2) axes.

## 3. Avoid machine-specific assumptions

Nothing in the code names a device, a data item ID or a fixed axis list. The device comes from the URL (`?device=`) or the dropdown, which is filled from the probe. The layout is decided from the kinematic chain: the chain with the most linear axes carries the tool, and the others carry the work.

| | Mazak | OKUMA |
|---|---|---|
| Axes found | 3 linear, 2 rotary, 1 spindle | 4 linear, 2 rotary, 3 spindles |
| Tool chain | X → Y → Z → C1 | Z1 → X → Y → B → C6 |
| Work chain | B → C2 | C1, and Z4 → C3 → C2 |
| Result | Machining centre, trunnion table | Mill-turn, tilting head, two work spindles |

## Collision check

The work is placed just outside the volume the tool side can reach. Before showing the machine, the twin sweeps every axis through its travel and tests every pair of solids. A live check runs four times a second. Both show in the panel.

## Limitations

- The tool stops just short of the part by design, so it does not show cutting.
- A machine whose probe has no kinematic information is drawn as a plain vertical mill.
- Spindle rotation is slowed down so it is visible.
- The Metalogi feed appears to be a looped recording, so the OKUMA sits idle for long stretches.

## How to run

1. `python proxy.py`
2. Open `http://localhost:8000/index.html?device=Mazak`

Screenshots: `mazak.png`, `okuma.png`.
