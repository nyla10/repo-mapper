
from app.analyzer import analyze_files


def test_creates_nodes_for_all_files():
    files = {
        "src/App.jsx": """
            import Header from "./components/Header";
            import { getData } from "./services/api";
        """,
        "src/components/Header.jsx": """
            export default function Header() {}
        """,
        "src/services/api.js": """
            export function getData() {}
        """
    }

    result = analyze_files(files)

    assert len(result["nodes"]) == 3


def test_detects_relative_imports():
    files = {
        "src/App.jsx": """
            import Header from "./components/Header";
            import { getData } from "./services/api";
        """,
        "src/components/Header.jsx": """
            export default function Header() {}
        """,
        "src/services/api.js": """
            export function getData() {}
        """
    }

    result = analyze_files(files)

    assert len(result["edges"]) == 2


def test_returns_nodes_and_edges():
    files = {
        "src/App.jsx": 'import Header from "./components/Header";',
        "src/components/Header.jsx": "export default function Header() {}"
    }

    result = analyze_files(files)

    assert "nodes" in result
    assert "edges" in result
