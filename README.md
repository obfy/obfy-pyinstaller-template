# obfy + PyInstaller template

A minimal, ready-to-build project that ships a Python app as a **single native
executable** with its source **obfuscated and AES-256-GCM encrypted** by
[obfy](https://github.com/obfy/obfy).

The flow is two steps: `obfy build` turns `./src` into a protected drop-in mirror
(`./protected`), then PyInstaller bundles that mirror — never your real source —
into one binary.

```
src/run.py ──► obfy build ──► protected/  ──► pyinstaller ──► dist/app
src/app/                      (encrypted)                     (one binary)
```

## Layout

| Path | What it is |
|------|------------|
| `src/run.py` | App entry point. Edit or replace. |
| `src/app/` | Your code package — **this is what gets protected**. |
| `app.spec` | PyInstaller spec, already pointed at the protected `./protected` tree. |
| `build.sh` | One-shot: `obfy build` + `pyinstaller`. |
| `Pipfile` | Build-time tools (`obfy`, `pyinstaller`), managed with pipenv. |
| `protected/`, `build/`, `dist/` | Generated output (git-ignored). |

## Prerequisites

- **CPython 3.10–3.13.** Build with the **same Python version** you ship for —
  obfy's marshalled bytecode is interpreter-version specific.
- macOS (Apple Silicon / Intel), Linux (x86_64 / aarch64), or Windows (x64).
- PyInstaller produces a binary for the **OS and architecture you build on**.
  Build on each target platform you want to ship (e.g. in CI).

## Setup

This template uses [pipenv](https://pipenv.pypa.io/) (the `Pipfile` pins
`python_version = "3.12"`). Install the build tooling into a managed virtualenv:

```bash
pip install --user pipenv          # if you don't have it
pipenv install                     # creates the venv from Pipfile
```

> Add your app's own runtime dependencies to the `Pipfile` too (`pipenv install
> <pkg>`), so PyInstaller can discover and bundle them.

Prefer a plain venv + pip? That works as well:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install obfy pyinstaller
```

## Build

```bash
pipenv run build                   # == pipenv run bash build.sh
```

That runs the two steps for you. To run them by hand (inside `pipenv shell` or an
activated venv):

```bash
# 1. Protect ./src into ./protected (a drop-in mirror)
obfy build --src ./src --out ./protected --python python --level 5

# 2. Bundle the protected mirror into one executable
pyinstaller --noconfirm app.spec
```

Run the result:

```bash
./dist/app            # Windows: dist\app.exe
./dist/app Ada        # pass args through as usual
```

## How it fits together

- **`obfy build --src ./src --out ./protected`** discovers every `.py` under
  `src/`, obfuscates it (`--level 5` also natively compiles eligible functions so
  their CPython bytecode never ships), then compiles → marshals → AES-256-GCM
  encrypts each module. `./protected` is a 1:1 mirror of `./src`: each `.py`
  becomes a tiny self-activating stub, the real code lives encrypted in
  `protected/__obfy__/*.obfy`, and obfy's native loader is bundled in.

- **`app.spec`** points PyInstaller at `protected/run.py` (not `src/run.py`) and
  ships the whole `./protected/` tree as data, plus `obfy_runtime` as a hidden
  import because the loader is imported dynamically at runtime. The decryption
  happens in memory at import time; plaintext source is never written to disk.

## Customizing

- **Your code:** put it under `src/app/` (or add packages alongside it) and import
  it from `src/run.py`. Keep `src/` to code only — `obfy build` copies every
  non-`.py` file under `--src` into the output, so don't point it at a tree that
  contains `.env` files or keys.
- **Executable name / icon / windowed mode:** edit `app.spec` (`name=`, add
  `icon=`, set `console=False` for a GUI app).
- **Obfuscation level:** change `--level` in `build.sh` (`0`–`5`; higher does
  strictly more). See
  [obfuscation levels](https://docs.camouflage.network/obfy/guides/obfuscation-levels).
- **Excluding files from protection** (e.g. framework files read as text): use
  `--exclude` (`fnmatch` patterns, repeatable). See
  [packaging](https://docs.camouflage.network/obfy/guides/packaging).

## Honest posture

Python obfuscation is **deterrence, not encryption-grade security** — CPython must
eventually execute real bytecode. obfy stops casual copying and raises the cost for
everyone else; it does not replace legal protection for sensitive IP. See the
[honest posture](https://docs.camouflage.network/obfy/guides/obfuscation-levels#honest-posture).

## Docs

Full obfy documentation: **[docs.camouflage.network/obfy](https://docs.camouflage.network/obfy/introduction)**.

## License

MIT — see [LICENSE](./LICENSE). The code you build with this template is yours.
