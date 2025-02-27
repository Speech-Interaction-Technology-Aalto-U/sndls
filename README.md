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
    - [Install through uv](#install-through-uv)
- [Tutorial](#tutorial)
    - [Quickstart](#quickstart)
    - [Help](#help)
    - [Recursive search](#recursive-search)
    - [Fast metadata search](#fast-metadata-search)
    - [Filtering by extension](#filtering-by-extension)
    - [Filtering by python expressions](#filtering-by-python-expressions)
    - [Filtering by using preloaded files](#filtering-by-using-preloaded-files)
    - [Generating SHA-256 hash](#generating-sha-256-hash)
    - [Saving output to csv file](#saving-output-to-csv-file)
    - [Post-actions](#post-actions)
    - [Random data sampling and splitting](#random-data-sampling-and-splitting)
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
This quick tutorial is structured into multiple sections, each focusing on a
fundamental aspect of `sndls` and its core functionalities.

## Quickstart
To inspect the audio data in a certain folder, run:
```bash
sndls /path/to/folder
```
If no path is provided, the current directory will be used as the default input.
If your folder contains audio files, you should see output similar to the
following in your terminal (the information will vary based on your folder's contents):

## Help
For a detailed description of all available options, run:
```bash
sndls --help
```
This will display all parameters along with their descriptions.

## Recursive search
By default, `sndls` searches for audio files only within the specified input folder.
To include audio files from nested directories, enable recursive search using `--recursive` or `-r`:

```bash
sndls /path/to/root/dir --recursive
```

## Generating SHA-256 hash
In addition to retrieving audio metadata and data for each file, you can generate the corresponding SHA-256 hash. To visualize the full SHA-256, use the `--sha256` option. If you'd prefer to see only the last 8 characters of the SHA-256, use the `--sha256-short` option instead:
```bash
sndls /path/to/audio/dir --sha256
```
This will make your output appear as follows:
```bash
/path/to/audio/dir/000_audio.wav    d4f72a9b8cfd7e33ab32e4f24cfdb7f8a28f85a4b7f29de96b0b2b74369b48e5  106.3K WAV  PCM_16        52782x1@16000hz     -18.3dBrms:0    -2.5dBpeak:0
/path/to/audio/dir/001_audio.wav    a6d1a0c02a5e55d531b29c6cf97c09cb68fe9b0f758bdf45c1ec8f7d915e9b63  111.7K WAV  PCM_16        61425x1@16000hz     -21.0dBrms:0    -4.2dBpeak:0
/path/to/audio/dir/002_audio.wav    0f2a4d6b19b6f9cf5d8f7d47d088dc9be7b964f017028d7389f1acb46a18c8b9   90.6K WAV  PCM_16        49200x1@16000hz     -16.8dBrms:0    -3.2dBpeak:0
/path/to/audio/dir/004_audio.wav    6a55cfef36e1a8937d66b9082f74c19bc82cdbf4db7a1c98a3f1b0883c1a7456  127.9K WAV  PCM_16        68042x1@16000hz     -19.1dBrms:0    -1.9dBpeak:0

...
```

## Fast metadata search
Inspecting large folders or those containing long audio files can take considerable time.
In some cases, it's preferable to extract only metadata without reading the actual audio samples.
For such cases, the `--meta`  or `-m` option is available. In this case, only metadata
based information will be printed to the terminal. Information such as `peak_db`, `rms_db` will
not be calculated.
```bash
sndls /path/to/audio/dir --meta
```
For small folders, the difference in runtime may be negligible, but for larger datasets, it can be
substantial.

## Filtering by extension
Listed files can be filtered by many ways, including their extension. Only certain audio file extensions
that can be parsed by `soundfile` are currently supported. Use the `--extension` or `-e` option if you want
to restrict your results to a certain extension or extensions:
```bash
sndls /path/to/audio/dir --extension .wav .flac
```
In this case, the search will include only `.wav` and `.flac` files, ignoring all other extensions.

## Filtering by `python` expressions
In addition to filtering by extension using the `--extension` or `-e` option, you can create custom
filters to find files with specific traits. This can be useful for tasks like:

- Finding clipped, silent, or anomalous files
- Finding files within a specific duration range
- Finding files with a particular sample rate

For these cases, the `--select` or `-`) option allows you to select files that meet certain criteria, while
the `--filter` or `-f` option lets you select all files except those that match the filter. Both options
accept `python` expressions for greater flexibility in your search. 

Note that these options are mutually exclusive, meaning only one can be used at a time.

For example, to search for only clipped mono files, run:
```bash
sndls /path/to/audio/dir --select "is_clipped and num_channels == 1"
```

To filter out files shorter than 3.0 seconds, run:
```bash
sndls /path/to/audio/dir --filter "duration_seconds < 3.0"
```

Please note that some fields contain lists of values, where the length depends on the
number of channels in the file, such as `peak_db` or `rms_db`. In such cases, methods
like `any()` or `all()` can be useful.

For example, to find all files where all channels have peak values in decibels (`peak_db`)
greater than -3.0 dB, you can do the following:
```bash
sndls /path/to/audio/dir --select "all(db > -3.0 for db in peak_db)"
```

Here is a list of all fields that can be used to refine your search:
| Field                      | Description                                                                  | Data type     |
|----------------------------|------------------------------------------------------------------------------|---------------|
| `file`                     | Audio file path                                                              | `str`         |
| `filename`                 | Audio filename                                                               | `str`         |
| `fs`                       | Audio sample rate in hertz (e.g. 16000, 48000)                               | `int`         |
| `num_channels`             | Number of channels in the file                                               | `int`         |
| `num_samples_per_channels` | Number of samples per channels                                               | `int`         |
| `duration_seconds`         | Duration of the file in seconds                                              | `float`       |
| `size_bytes`               | Size of the file in bytes                                                    | `int`         |
| `fmt`                      | File format (`WAV`, `RF64`, etc)                                             | `str`         |
| `subtype`                  | File subtype (`PCM_16`, `PCM_24`, `FLOAT`, etc)                              | `str`         |
| `peak_db`                  | Per-channel peak value in decibels                                           | `List[float]` |
| `rms_db`                   | Per-channel root mean square value in decibels                               | `List[float]` |
| `is_silent`                | `True` if all channels have less than `--silent-thresh` dB RMS               | `bool`        |
| `is_clipped`               | `True` if any channel contains values outside the `-1.0` to `1.0` range      | `bool`        |
| `is_anomalous`             | `True` if any sample is `NaN`, `inf` or `-inf`                               | `bool`        |
| `is_invalid`               | `True` if the file could not be read. Only valid with `--skip-invalid-files` | `bool`        |
| `sha256`                   | SHA-256 hash (only available if `--sha256` or `--sha256-short` is enabled    | `str`         |
| `preload`                  | Preloaded `DataFrame` (only available with `--preload`)                      | `DataFrame`   |

## Filtering by using preloaded files
...

## Saving output to `.csv` file
...

## Post-actions
...

## Random data sampling and splitting
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
For further details about the license of this tool, please see [LICENSE](LICENSE).