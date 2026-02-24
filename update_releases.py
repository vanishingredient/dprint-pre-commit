import json
import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(x) for x in version.split("."))


def get_all_versions() -> list[str]:
    request = urllib.request.Request("https://pypi.org/pypi/dprint-py/json")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read())
    except OSError as exc:
        msg = "Failed to fetch versions from PyPI"
        raise RuntimeError(msg) from exc

    versions = [
        version
        for version in data["releases"]
        if re.fullmatch(r"\d+\.\d+\.\d+(?:\.\d+)?", version)
    ]

    return sorted(versions, key=version_tuple)


def git_tag_exists(tag: str) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def main():
    root_dir = Path(__file__).parent
    pyproject_path = root_dir / "pyproject.toml"
    readme_path = root_dir / "README.md"

    pyproject_content = pyproject_path.read_text(encoding="utf-8")

    match = re.search(r'"dprint-py==([^"]+)"', pyproject_content)
    if not match:
        msg = "dprint-py dependency not found in pyproject.toml"
        raise ValueError(msg)
    current_version = match.group(1)

    all_versions = get_all_versions()

    current_tuple = version_tuple(current_version)
    target_versions = [
        version for version in all_versions if version_tuple(version) >= current_tuple
    ]

    if not target_versions:
        print("No new versions to mirror.")
        return

    tags_created: list[str] = []

    for version in target_versions:
        if git_tag_exists(version):
            print(f"Tag {version} already exists. Skipping.")
            continue

        print(f"Mirroring version: {version}")

        pyproject_content = re.sub(
            r'"dprint-py==[^"]+"', f'"dprint-py=={version}"', pyproject_content
        )
        _ = pyproject_path.write_text(pyproject_content, encoding="utf-8", newline="\n")

        readme_content = readme_path.read_text(encoding="utf-8")
        readme_content = re.sub(
            r'^(\s*rev\s*[:=]\s*"?)[0-9.]+',
            rf"\g<1>{version}",
            readme_content,
            flags=re.MULTILINE,
        )
        _ = readme_path.write_text(readme_content, encoding="utf-8", newline="\n")

        _ = subprocess.run(
            ["git", "add", str(pyproject_path), str(readme_path)], check=True
        )
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            check=False,
        )
        if result.returncode != 0:
            time.sleep(1)  # Ensure that mirror commits have distinct timestamps
            _ = subprocess.run(
                ["git", "commit", "-m", f"Mirror dprint-py {version}"], check=True
            )
            print(f"Created commit for {version}")
        else:
            print(f"Using current commit for {version}")

        _ = subprocess.run(["git", "tag", f"{version}"], check=True)
        print(f"Created tag for {version}")
        tags_created.append(version)

    if "GITHUB_OUTPUT" in os.environ and tags_created:
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as file:
            _ = file.write(f"tags={' '.join(tags_created)}\n")


if __name__ == "__main__":
    main()
