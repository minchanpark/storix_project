# Installing Storix

Storix is a macOS-first CLI and TUI application for local storage analysis and cleanup.

## Requirements

- macOS
- Python 3.11 or newer
- Terminal access
- `git` if you plan to install from GitHub or a local clone

## Recommended: Install with `pipx`

`pipx` installs Storix into its own isolated environment while still making the `storix` command available globally.

### 1. Install `pipx`

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

After `ensurepath`, restart your shell or open a new terminal window if `pipx` is not immediately available.

### 2. Install Storix

Choose one install source.

#### From GitHub

```bash
pipx install "git+https://github.com/minchanpark/storix_project.git"
```

#### From a local clone

```bash
git clone https://github.com/minchanpark/storix_project.git
cd storix_project
pipx install .
```

### 3. Verify the install

```bash
storix --help
```

Notes:

- The package distribution name is `storix-cli`.
- The installed command is `storix`.

## Alternative: Install in a virtual environment

Use this flow if you prefer a project-local environment instead of `pipx`.

```bash
git clone https://github.com/minchanpark/storix_project.git
cd storix_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
storix --help
```

If you are contributing to the project, use the development extras instead:

```bash
python -m pip install -e ".[dev]"
```

## Upgrade

Upgrade commands depend on how you installed Storix.

### If installed from GitHub with `pipx`

```bash
pipx reinstall "git+https://github.com/minchanpark/storix_project.git"
```

### If installed from a local clone with `pipx`

```bash
cd storix_project
git pull
pipx reinstall .
```

### If installed in a virtual environment

```bash
source .venv/bin/activate
python -m pip install --upgrade .
```

## Uninstall

### If installed with `pipx`

```bash
pipx uninstall storix-cli
```

### If installed in a virtual environment

Deactivate the environment and remove the `.venv` directory if you no longer need it.

## First commands to try

```bash
storix scan
storix doctor
storix top
storix clean all-safe --dry-run
storix tui
```
