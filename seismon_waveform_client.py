"""
SeisMon waveform client.

Provides a QuakeMigrate waveform client backed by the SeisMonPy NORSAR database client
for retrieving waveform data from a SeisMon archive.

:author: Conor A. Bacon

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from quakemigrate.clients.base import BaseWaveformClient
from seismonpy.norsardb import Client


if TYPE_CHECKING:
    from obspy import Stream, UTCDateTime
    from quakemigrate.io.station import Station


@dataclass(kw_only=True)
class SeismonWaveformClient(BaseWaveformClient):
    """
    Waveform client backed by SeisMonPy.

    This client implements the QuakeMigrate waveform client interface using the
    SeisMonPy NORSAR database client. It is responsible only for fetching waveform
    data from the SeisMon backend; common waveform post-processing is handled by
    :class:`~quakemigrate.io.clients.base.BaseWaveformClient`.

    Parameters
    ----------
    db_path:
        Path to the SeisMon database.
    db_archive_path:
        Path to the waveform archive.
    inventories_path:
        Path to station inventory files.
    cache_waveforms:
        Whether waveform caching should be enabled.
    load_response:
        Whether response information should be loaded.
    inventory_index_path:
        Path to the inventory index.
    noresponse_inventory_path:
        Path to inventory data without response information.
    response_inventory_path:
        Path to inventory data with response information.
    static_xml_inventory_path:
        Path to static StationXML inventory files.
    index_path:
        Path to the SeisMon index.

    """

    db_path: str | None = None
    db_archive_path: str | None = None
    inventories_path: str | None = None
    cache_waveforms: bool | None = None
    load_response: bool | None = None
    inventory_index_path: str | None = None
    noresponse_inventory_path: str | None = None
    response_inventory_path: str | None = None
    static_xml_inventory_path: str | None = None
    index_path: str | None = None

    _client: Client = field(init=False)

    def __post_init__(self) -> None:
        """
        Initialise the underlying SeisMonPy client.

        """

        super().__post_init__()

        kwargs = {
            "db_path": self.db_path,
            "db_archive_path": self.db_archive_path,
            "inventories_path": self.inventories_path,
            "cache_waveforms": self.cache_waveforms,
            "load_response": self.load_response,
            "inventory_index_path": self.inventory_index_path,
            "noresponse_inventory_path": self.noresponse_inventory_path,
            "response_inventory_path": self.response_inventory_path,
            "static_xml_inventory_path": self.static_xml_inventory_path,
            "index_path": self.index_path,
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self._client = Client(**kwargs)

    def _fetch_stream(
        self, stations: list[Station], starttime: UTCDateTime, endtime: UTCDateTime
    ) -> Stream:
        """
        Fetch waveform data from the configured SeisMon backend.

        Parameters
        ----------
        stations:
            List of Station objects for which to request waveform data.
        starttime:
            First timestamp of data to be loaded from the SeisMon client.
        endtime:
            Final timestamp of data to be loaded from the SeisMon client.

        Returns
        -------
        st:
            Stream containing waveform data returned by the SeisMon backend.

        """

        st = self._client.get_waveforms(
            ",".join(station.station for station in stations),
            "*",
            starttime,
            endtime,
        ).split()

        for station in stations:
            for tr in st.select(station=station.station):
                tr.stats.network = station.network

        return st

    def _client_description(self) -> list[str]:
        lines = ["\tSeisMon client"]
        if self.db_path:
            lines.append(f"\tDB path:\t{self.db_path}")
        if self.db_archive_path:
            lines.append(f"\tArchive path:\t{self.db_archive_path}")
        return lines
