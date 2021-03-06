from pathlib import Path

import semver
from invoke import run as invoke_run
from invoke import task
from termcolor import cprint

VERSION_TEMPLATE = """__version__ = "{version_string}"
"""

TEST_VERSION_TEMPLATE = """from dash_bootstrap_components import __version__


def test_version():
    assert __version__ == "{version_string}"
"""

HERE = Path(__file__).parent

DASH_BOOTSTRAP_DIR = HERE / "dash_bootstrap_components"


@task(help={"version": "Version number to release"})
def prerelease(ctx, version):
    """
    Release a pre-release version
    Running this task will:
     - Bump the version number
     - Push a release to pypi
    """
    info(f"Creating prerelease branch for {version}")
    set_source_version(version)
    run(f"git checkout -b prerelease/{version}")
    run(
        "git add package.json package-lock.json "
        "dash_bootstrap_components/__init__.py "
        "tests/test_version.py"
    )
    run(f'git commit -m "Set version to {version}"')
    run(f"git push origin prerelease/{version}")


@task(help={"version": "Version number to release"})
def release(ctx, version):
    """
    Release a new version
    Running this task will:
     - Create a release branch
     - Bump the version number
    Release notes should be written in the body of the pull request. When
    changes are merged GitHub actions will
     - Build the package
     - Push a release to PyPI
     - Create a release
     - Revert to a dev version change.
    """
    info(f"Creating release branch for {version}")
    set_source_version(version)

    run(f"git checkout -b release/{version}")
    run(
        "git add package.json package-lock.json "
        "dash_bootstrap_components/__init__.py "
        "tests/test_version.py"
    )
    run(f'git commit -m "Bump version to {version}"')
    run(f"git push origin release/{version}")


@task
def copy_examples(ctx):
    """
    Copy examples used in documentation to the docs directory.
    """
    info("copying examples into docs directory")
    # TODO: have this determined by some configuration rather than hardcoded
    run("cp examples/gallery/iris-kmeans/app.py docs/examples/vendor/iris.py")
    run(
        "cp examples/advanced-component-usage/graphs_in_tabs.py "
        "docs/examples/vendor/graphs_in_tabs.py"
    )
    run(
        "cp examples/multi-page-apps/simple_sidebar.py "
        "docs/examples/vendor/simple_sidebar.py"
    )


@task(
    help={
        "version": "Version number to finalize. Must be "
        "the same version number that was used in the release."
    },
)
def postrelease(ctx, version):
    """
    Finalise the release
    Running this task will:
     - bump the version to the next dev version
     - push changes to master
    """
    clean_version = semver.finalize_version(version)
    if clean_version == version:
        # last release was full release, bump patch
        new_version = semver.bump_patch(version) + "-dev"
    else:
        # last release was prerelease, revert to dev version
        new_version = clean_version + "-dev"

    info(f"Bumping version numbers to {new_version} and committing")
    set_source_version(new_version)


def set_source_version(version):
    set_js_version(version)
    set_py_version(version)


def set_py_version(version):
    version = normalize_version(version)
    init_path = DASH_BOOTSTRAP_DIR / "__init__.py"
    with init_path.open("r") as f:
        lines = f.readlines()

    index = [line.startswith("__version__ = ") for line in lines].index(True)
    lines[index] = VERSION_TEMPLATE.format(version_string=version)

    with init_path.open("w") as f:
        f.writelines(lines)

    test_version_path = HERE / "tests" / "test_version.py"
    with test_version_path.open("w") as f:
        f.write(TEST_VERSION_TEMPLATE.format(version_string=version))


def set_js_version(version):
    version = normalize_version(version)
    package_json_path = HERE / "package.json"
    with package_json_path.open() as f:
        package_json = f.readlines()
    for iline, line in enumerate(package_json):
        if '"version"' in line:
            package_json[iline] = f'  "version": "{version}",\n'
    with open(package_json_path, "w") as f:
        f.writelines(package_json)


@task
def set_documentation_version(ctx, version):
    version = normalize_version(version)
    docs_requirements_path = HERE / "docs" / "requirements.txt"
    with docs_requirements_path.open() as f:
        docs_requirements = f.readlines()
    for iline, line in enumerate(docs_requirements):
        if "dash_bootstrap_components" in line:
            updated_line = f"dash_bootstrap_components=={version}\n"
            docs_requirements[iline] = updated_line
    with open(docs_requirements_path, "w") as f:
        f.writelines(docs_requirements)


def normalize_version(version):
    version_info = semver.parse_version_info(version)
    version_string = str(version_info)
    return version_string


def run(command, **kwargs):
    result = invoke_run(command, hide=True, warn=True, **kwargs)
    if result.exited != 0:
        error(f"Error running {command}")
        print(result.stdout)
        print()
        print(result.stderr)
        exit(result.exited)


def error(text):
    cprint(text, "red")


def info(text):
    print(text)
