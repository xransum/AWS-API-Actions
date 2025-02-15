"""Nox sessions."""

import os
import shlex
import sys
from pathlib import Path
from textwrap import dedent

import nox
from nox_poetry import Session, session


package = "aws_api_actions"
python_version = "3.11"
locations = ("src", "tests", "noxfile.py")
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("pre-commit", "safety", "mypy", "tests")


def activate_virtualenv_in_precommit_hooks(session: Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.
    """
    assert session.bin is not None  # noqa: S101

    # Only patch hooks containing a reference to this session's bindir. Support
    # quoting rules for Python and bash, but strip the outermost quotes so we
    # can detect paths within the bindir, like <bindir>/python.
    bindirs = [
        bindir[1:-1] if bindir[0] in "'\"" else bindir
        for bindir in (repr(session.bin), shlex.quote(session.bin))
    ]

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    headers = {
        # pre-commit < 2.16.0
        "python": f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """,
        # pre-commit >= 2.16.0
        "bash": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
        # pre-commit >= 2.17.0 on Windows forces sh shebang
        "/bin/sh": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
    }

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        if not hook.read_bytes().startswith(b"#!"):
            continue

        text = hook.read_text()

        if not any(
            Path("A") == Path("a")
            and bindir.lower() in text.lower()
            or bindir in text
            for bindir in bindirs
        ):
            continue

        lines = text.splitlines()

        for executable, header in headers.items():
            if executable in lines[0].lower():
                lines.insert(1, dedent(header))
                hook.write_text("\n".join(lines))
                break


@session(name="pre-commit", python=python_version)
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--hook-stage=manual"]
    session.install(
        "black",
        "darglint",
        "flake8",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-rst-docstrings",
        "isort",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "pyupgrade",
    )

    try:
        session.run("poetry", "--version")
    except Exception:
        print("Installing poetry!")
        session.install("poetry")

    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@session(python=python_version)
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()

    session.install("safety")

    args = ["safety", "check", "--full-report", f"--file={requirements}"]

    if os.path.exists(".safety") is True:
        with open(".safety", encoding="utf-8") as f:
            lines = [
                line.strip() for line in f.readlines() if line.strip() != ""
            ]

            if len(lines) > 0:
                vulns = ",".join(lines)
                args.append(f"--ignore={vulns}")

    session.run(*args)


@session(python=python_version)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations

    session.install(".", "mypy", "pytest", "importlib-metadata")
    session.run("mypy", *args)

    if not session.posargs and session.python == python_version:
        session.run(
            "mypy", f"--python-executable={sys.executable}", "noxfile.py"
        )


@session(python=python_version)
def pytype(session: Session) -> None:
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@session(python=python_version)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(
        "coverage[toml]",
        "poetry",
        "pytest",
        "pytest-datadir",
        "pygments",
        "typing_extensions",
    )

    try:
        session.run(
            "coverage", "run", "--parallel", "-m", "pytest", *session.posargs
        )
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(python=python_version)
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=python_version)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".")
    session.install("pytest", "typeguard", "pygments")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)
