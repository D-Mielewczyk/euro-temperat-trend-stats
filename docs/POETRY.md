# Poetry Usage Tutorial

This tutorial will guide you through the essential steps to use a repository with Poetry. We'll cover installing dependencies, activating the shell, and adding/searching for packages.

## Prerequisites

Make sure you have Poetry installed. Use the appropriate command for your operating system:

### Windows (powershell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### macOS (with Homebrew)

```bash
brew install poetry
```

### Linux

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Step 1: Installing Dependencies

To install the dependencies for your project, navigate to the project directory and run:

```bash
poetry install
```

This command reads the `pyproject.toml` file in your project directory and installs the specified dependencies.

## Step 2: Activating the Virtual Environment

Poetry creates a virtual environment for your project. To activate this environment, you can use the `poetry shell` command:

```bash
poetry shell
```

This command activates the virtual environment, allowing you to run commands in an isolated environment specific to your project.

## Step 3: Adding Packages

To add a package to your project, use the `poetry add` command followed by the package name. For example, to add `requests` to your project:

```bash
poetry add requests
```

Poetry will automatically update your `pyproject.toml` file and install the package.

## Step 4: Searching for Packages

To search for packages, you can use the `poetry search` command followed by the search query. For example, to search for packages related to "flask":

```bash
poetry search flask
```

This command will list all packages related to "flask" available on PyPI.

## Summary

- **Install dependencies:** `poetry install`
- **Activate virtual environment:** `poetry shell`
- **Add a package:** `poetry add <package-name>`
- **Search for packages:** `poetry search <query>`

By following these steps, you can efficiently manage your project's dependencies and environment using Poetry. For more detailed information, you can refer to the [official Poetry documentation](https://python-poetry.org/docs/).

