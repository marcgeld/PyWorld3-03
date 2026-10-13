"""Command-line interface for the World3-03 model."""
import argparse
from pathlib import Path

from .world3 import World3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year-min", type=float, default=1900)
    parser.add_argument("--year-max", type=float, default=2100)
    parser.add_argument("--dt", type=float, default=0.5)
    parser.add_argument("--output", type=Path, help="Save the plot instead of opening a window")
    args = parser.parse_args()
    try:
        world = World3(year_min=args.year_min, year_max=args.year_max, dt=args.dt)
    except ValueError as exc:
        parser.error(str(exc))
    if args.output:
        import matplotlib
        matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    from .utils import plot_world_variables

    world.init_world3_constants()
    world.init_world3_variables()
    world.set_world3_table_functions()
    world.set_world3_delay_functions()
    world.run_world3()
    plot_world_variables(
        world.time, [world.nrfr, world.iopc, world.fpc, world.pop, world.ppolx],
        ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
        [[0, 1], [0, 1000], [0, 1000], [0, 16e9], [0, 32]],
        figsize=(14, 9), grid=True, title="World3-03 reference run",
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.output, dpi=150)
        plt.close()
        print(f"Saved plot to {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
