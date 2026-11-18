"""Exercise all ten instrumented methods using temporary fixtures."""

from io import StringIO
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import graphtaint
import parser


def main():
    output = StringIO()
    logging.basicConfig(
        stream=output, level=logging.INFO, format="%(levelname)s %(name)s %(message)s"
    )
    with TemporaryDirectory() as directory:
        valid = Path(directory, "valid.yaml")
        invalid = Path(directory, "invalid.yaml")
        shell = Path(directory, "example.sh")
        content = "# sample\napiVersion: v1\nkind: ConfigMap\n"
        valid.write_text(content, encoding="utf-8")
        invalid.write_text("name: [unclosed\n", encoding="utf-8")
        shell.touch()

        assert parser.checkIfWeirdYAML(".github/workflows/example.yaml")
        assert parser.checkIfValidK8SYaml(valid)
        parser.checkIfValidHelm("charts/values.yaml")
        assert parser.readYAMLAsStr(valid) == content
        assert not parser.checkParseError(invalid)
        assert parser.count_initial_comment_line(valid) == 1
        assert set(map(Path, graphtaint.getYAMLFiles(directory))) == {valid, invalid}
        assert list(map(Path, graphtaint.getSHFiles(directory))) == [shell]

    evidence = output.getvalue().replace(f"{directory}/", "").replace(directory, "<fixture directory>")
    print(evidence, end="")
    expected = {
        "yaml_path_filtered", "kubernetes_yaml_checked", "helm_path_checked",
        "yaml_text_read", "yaml_parse_failed", "yaml_load_finished",
        "yaml_header_counted", "yaml_documents_combined",
        "yaml_files_discovered", "shell_files_discovered",
    }
    observed = {line.split("event=", 1)[1].split()[0] for line in evidence.splitlines()}
    if observed != expected:
        raise SystemExit(f"Unexpected event set (missing={expected - observed}, extra={observed - expected})")
    print(f"Verified {len(expected)} forensic events.")


if __name__ == "__main__":
    main()
