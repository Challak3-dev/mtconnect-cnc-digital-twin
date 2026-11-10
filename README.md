# MTConnect CNC Digital Twin

A browser-based digital twin that reads live data from an MTConnect agent and animates a 3D machine to match. It discovers the machine from the agent's probe (axes, position data items, units, coordinate systems, kinematic chain), so the same code runs any device the agent serves. Tested on the Mazak and OKUMA devices of the Metalogi demo agent.

Built for ASU Lab 2.8: A Reusable Three-Axis CNC Digital Twin.

## Run it
1. Install Python 3 (no extra packages).
2. In this folder: `python proxy.py`
   (uses https://demo.metalogi.io; for another agent: `python proxy.py --agent <url>`)
3. Open http://localhost:8000/index.html?device=Mazak
4. Pick another device from the dropdown.

The proxy forwards `/agent/*` to the MTConnect agent so the browser is not blocked by CORS. Full instructions with troubleshooting: `CNC_Digital_Twin_How_To_Run.docx`.

## Files
| File | What it is |
|---|---|
| `index.html` | Full twin: SketchUp parts, true-scale motion, collision check, tool path |
| `twin_simple.html` | Simple twin (~280 lines): plain boxes, same discovery and live motion |
| `proxy.py` | Local server and agent proxy |
| `kit.json` | Machine parts read back from the SketchUp model (also embedded in `index.html`) |
| `WRITEUP.md` | How the twin meets each lab requirement |
| `CNC_Digital_Twin_How_To_Run.docx` | Step-by-step guide for running it |
| `mazak.png`, `okuma.png` | The twin running on the live Metalogi agent |
