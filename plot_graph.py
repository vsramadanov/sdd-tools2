import argparse
import importlib


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Render a LangGraph app's mermaid diagram to a PNG file."
    )
    parser.add_argument(
        "module",
        help="Python module path containing the compiled `app` (e.g. my_pkg.graph).",
    )
    parser.add_argument(
        "-o", "--output",
        default="compilation_graph.png",
        help="Output PNG path (default: compilation_graph.png).",
    )
    return parser.parse_args(argv)


def load_app(module_name: str):
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise SystemExit(f"ERROR: cannot import module {module_name!r}: {e}")

    app = getattr(module, "app", None)
    if app is None:
        raise SystemExit(
            f"ERROR: module {module_name!r} has no attribute 'app'")

    return app


if __name__ == "__main__":
    args = parse_args()
    app = load_app(args.module)

    with open(args.output, "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())

    print(f"OK: wrote {args.output}")
