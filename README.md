# `sndls`: An audio-friendly `ls`, with a little something extra

`sndls` is a command-line tool designed for quick and efficient inspection of audio data. It provides functionalities such as:

- Saving search results to a `.csv` file for later analysis.
- Detecting clipped, silent, or anomalous files that may impact machine learning pipelines.
- Computing and verifying SHA-256 hashes to detect file modifications or corruption.
- Filtering files using `python` expressions to identify those matching specific criteria.
- Performing fast, metadata-based file inspection.
- Executing post-processing actions, such as removing clipped files, copying files that meet certain conditions, and more.

# Table of contents
- [Installation](#installation)
    - [Install through pip](#install-through-pip)
    - [Install in developer mode](#install-in-developer-mode)
    - [Install through `uv`](#install-through-uv)
- [Tutorial](#tutorial)
- [Cite](#cite)
- [License](#license)

# Installation
## Install through pip
To install `sndls`, run:
```bash
pip install sndls
```
Verify the installation with:
```bash
sndls --version
```
This should output:
```
sndls version x.y.z yyyy-zzzz developed by Esteban Gómez
```
Where:
- `x.y.z` represents the major, minor, and patch version
- `yyyy-zzzz` indicates the development start year and the current 

## Install in developer mode
Developer mode installation is intended for those developing new features for the tool. To set it up:
1. Clone the repository to your desired folder using:
```bash
git clone <repository_url>
```
2. Navigate to the root directory (where `pyproject.toml` is located):
```bash
cd <repository_folder>
```
3. Install in developer mode with:
```bash
python -m flit install -s
```
This will allow immediate reflection of any code modifications when the tool is executed in the terminal.

Before proceeding, ensure that Flit is installed. If not, install it with:
```bash
python -m pip install flit
```
For more information on `flit`, refer to the [Flit Command Line Interface documentation](https://flit.pypa.io/en/stable/).

## Install through `uv`
Alternatively, you can install the tool using `uv`. This is adequate for when you can to keep it isolated from your `python`
environment setup and just run it to analyze a certain data collection.

1. Install `uv` and `uvx` following the instructions for your operating system in [`uv` website](https://docs.astral.sh/uv/getting-started/installation/).
2. Run:
```bash
uv tool install sndls
```
3. Verify the installation with
```bash
uv tool run sndls --version
```
or you can use the shortcut version `uvx`:
```bash
uvx sndls --version
```
This should output:
```
sndls version x.y.z yyyy-zzzz developed by Esteban Gómez
```
Where:
- `x.y.z` represents the major, minor, and patch version
- `yyyy-zzzz` indicates the development start year and the current

# Tutorial
...

# Cite
If this tool contributed to your work, please consider citing it:

```
@misc{sndls,
  author = {Esteban Gómez},
  title  = {sndls},
  year   = 2024,
  url    = {https://github.com/eagomez2/sndls}
}
```

# License
For further details about the license of this package, please see [LICENSE](LICENSE).