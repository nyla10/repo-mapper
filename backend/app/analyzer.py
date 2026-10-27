import re
from pathlib import PurePosixPath


def analyze_files(files):
    """Build a dependency graph from JavaScript and TypeScript source files."""
    nodes = []
    edges = []
    file_paths = set(files.keys())

    for file_path, content in files.items():
        nodes.append({
            "id": file_path,
            "label": PurePosixPath(file_path).name,
        })

        imports = re.findall(
            r"""(?:import\s+(?:[\w*\s{},]+\s+from\s+)?|"""
            r"""export\s+[\w*\s{},]+\s+from\s+)"""
            r"""['"]([^'"]+)['"]|"""
            r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""",
            content,
        )

        for match in imports:
            imported_path = match[0] or match[1]

            if not imported_path.startswith("."):
                continue

            current_dir = PurePosixPath(file_path).parent
            target = str(PurePosixPath(current_dir / imported_path))

            candidates = [
                target,
                target + ".js",
                target + ".jsx",
                target + ".ts",
                target + ".tsx",
                target + ".mjs",
                target + ".cjs",
                target + "/index.js",
                target + "/index.jsx",
                target + "/index.ts",
                target + "/index.tsx",
            ]

            for candidate in candidates:
                if candidate in file_paths:
                    edges.append({
                        "source": file_path,
                        "target": candidate,
                    })
                    break

    return {"nodes": nodes, "edges": edges}

