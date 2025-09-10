
# Hydraulic Network & HGL Visualiser

Small, clean tool to compute head losses and plot HGL/EGL — perfect companion to fluids labs.
This starter implements:
- Darcy–Weisbach friction (Colebrook–White and Swamee–Jain).
- Single-pipe profile plotting (HGL/EGL), minor losses `K`, and elevation line.
- A minimal Hardy–Cross loop solver (experimental) scaffold.
- CLI to run a YAML/JSON config and save a plot.

## Install (local dev)
```bash
pip install -e .
```

## Example (single pipe)
```bash
hglviz run examples/single_pipe.yaml --save hgl.png
```

This writes `examples/single_pipe_results.json` and saves `hgl.png`.

## Config (YAML)
```yaml
fluid: {rho: 1000, mu: 1.0e-3}
g: 9.81
nodes:
  A: {head: 10.0, z: 0.0}
  B: {z: 0.0}
pipes:
  - {name: P1, from: A, to: B, L: 10.0, D: 0.008, eps: 1.5e-6, K: 0.2, Q: 2.0e-4}
friction_method: auto   # auto | colebrook | swamee
```

## Equations
- Reynolds: `Re = ρVD/μ`
- Darcy–Weisbach: `h_f = f (L/D) (V^2/2g)`
- Minor losses: `h_m = K (V^2/2g)`
- Colebrook–White: `1/√f = -2log10( ε/(3.7D) + 2.51/(Re√f) )`
- Swamee–Jain: `f = 0.25 / [log10( ε/(3.7D) + 5.74/Re^0.9 )]^2`

## Tests
```bash
pytest -q
```

## Roadmap
- Node-head solver and robust Hardy–Cross for multi-loop networks
- Monte Carlo sensitivity (ε, D, Q)
- Streamlit GUI
- PDF report export
