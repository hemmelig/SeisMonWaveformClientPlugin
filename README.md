QuakeMigrate SeisMonPy Waveform Client Plugin
=============================================

A waveform client plugin for QuakeMigrate that retrieves waveform data from a SeisMon archive using the NORSAR `seismonpy` client.

Installation
------------

This plugin depends on the internal `seismonpy` package, which is available from the NORSAR internal Python package index.

With `uv`:

```bash
uv sync
```

The project metadata configures `seismonpy` to resolve from the internal package index:

```toml
[tool.uv.sources]
seismonpy = { index = "norsar-seismon" }

[[tool.uv.index]]
name = "norsar-seismon"
url = "http://srv-wcomp2/seismon/python/"
explicit = true
```

For manual installation with `pip`, users may need to provide the internal index explicitly:

```bash
pip install \
  --extra-index-url http://srv-wcomp2/seismon/python/ \
  --trusted-host srv-wcomp2 \
  qm-seismon-waveform-plugin
```

Usage
-----

The plugin registers a QuakeMigrate waveform client through the `quakemigrate.waveform_clients` entry point:

```toml
[project.entry-points."quakemigrate.waveform_clients"]
seismon = "seismon_waveform_client:SeismonWaveformClient"
```

The client class is:

```python
from seismon_waveform_client import SeismonWaveformClient
```

Example:

```python
client = SeismonWaveformClient(
    db_path="/path/to/seismon/db",
    db_archive_path="/path/to/archive",
    inventories_path="/path/to/inventories",
)
```

The client fetches waveforms from SeisMonPy and returns an ObsPy `Stream` through the QuakeMigrate waveform client interface.

Requirements
------------

- Python >= 3.13
- QuakeMigrate >= 1.3.0
- SeisMonPy >= 2025.2.1

`seismonpy` is an internal dependency and requires access to the NORSAR package index.

License
-------

GNU General Public License, Version 3.
