
"""
Simple CLI:
  - Run a single-pipe config and produce a results JSON + optional plot.
Usage:
  python -m hglviz.run examples/single_pipe.yaml
"""
import argparse, os, json
from hglviz.io import load_config, export_results_json
from hglviz.pipes import Pipe
from hglviz.plotting import plot_hgl_egl

def run_single_pipe(cfg_path: str, save_plot: str | None):
    cfg = load_config(cfg_path)
    fluid = cfg["fluid"]
    g = cfg.get("g", 9.81)
    nodes = cfg["nodes"]
    pipe_cfg = cfg["pipes"][0]  # single pipe demo
    Q = pipe_cfg["Q"]

    A = nodes[pipe_cfg["from"]]
    B = nodes[pipe_cfg["to"]]

    H_in = A.get("head", 0.0)
    z_in = A.get("z", 0.0)
    z_out = B.get("z", 0.0)

    pipe = Pipe(
        name=pipe_cfg.get("name", "P1"),
        L=pipe_cfg["L"],
        D=pipe_cfg["D"],
        eps=pipe_cfg.get("eps", 0.0),
        K=pipe_cfg.get("K", 0.0),
        z_in=z_in, z_out=z_out
    )

    x, HGL, EGL, zline, hf, hm, V = pipe.profile(
        rho=fluid["rho"], mu=fluid["mu"], Q=Q, H_in=H_in, g=g, npts=50, method=cfg.get("friction_method","auto")
    )

    results = {
        "pipe": pipe_cfg.get("name", "P1"),
        "Q_m3s": Q,
        "V_ms": V,
        "hf_major_m": hf,
        "hm_minor_m": hm,
        "H_in_m": H_in,
        "H_out_m": HGL[-1],
        "g": g,
        "fluid": fluid,
    }

    out_json = os.path.splitext(cfg_path)[0] + "_results.json"
    export_results_json(out_json, results)

    if save_plot:
        plot_hgl_egl(x, HGL, EGL, zline, title=f"HGL/EGL: {pipe.name}", savepath=save_plot)
    return out_json, save_plot

def main():
    parser = argparse.ArgumentParser(description="HGL Visualiser (single-pipe demo)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run a single-pipe YAML/JSON config")
    run_p.add_argument("config", help="Path to config file (.yaml/.json)")
    run_p.add_argument("--save", help="Save plot to path", default=None)

    args = parser.parse_args()
    if args.cmd == "run":
        out_json, out_plot = run_single_pipe(args.config, args.save)
        print(f"Wrote results to {out_json}")
        if out_plot:
            print(f"Saved plot to {out_plot}")

if __name__ == "__main__":
    main()
