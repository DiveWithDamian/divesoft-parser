"""
divesoft_parser - Divesoft DLF parser

MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
from typing import Union

from divesoft_parser.models.enums import ConfigurationType, DiveRecordType
from divesoft_parser.models.records.configuration import ConfigurationVersionRecord
from divesoft_parser.utilities import BitArray, ByteConverter

logger: logging.Logger = logging.getLogger(__name__)


class ConfigurationRecordParser:
    def __init__(self, record_type: DiveRecordType,
                 bit_array: BitArray,
                 raw_bytes: bytes) -> None:
        self.record_type = record_type
        self.bit_array = bit_array
        self.record_data = raw_bytes
        if len(self.record_data) < 12:
            raise AssertionError(f"Truncated configuration record ({self.record_data.hex()})")

    def decode(self) -> Union[None,
                              ConfigurationVersionRecord]:
        try:
            configuration_type = ConfigurationType(self.bit_array.get_int(21, 31))
        except ValueError:
            logger.warning(f'Skipping decoding of configuration record ({self.record_data.hex()})')
            return None

        if configuration_type == ConfigurationType.Version:
            return self._decode_version()

        else:
            logger.error(f'Unknown configuration type: {configuration_type}')
            return None

    def _decode_version(self) -> ConfigurationVersionRecord:
        return ConfigurationVersionRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            configuration_type=ConfigurationType.Version,
            device=ByteConverter.to_uint8(self.record_data[0:1]),
            hardware_major=ByteConverter.to_uint8(self.record_data[1:2]),
            hardware_minor=ByteConverter.to_uint8(self.record_data[2:3]),
            software_major=ByteConverter.to_uint8(self.record_data[3:4]),
            software_minor=ByteConverter.to_uint8(self.record_data[4:5]),
            software_patch=ByteConverter.to_uint8(self.record_data[5:6]),
            software_flags=ByteConverter.to_uint16(self.record_data[6:8]),
            software_build=ByteConverter.to_int16(self.record_data[8:10]),
        )
