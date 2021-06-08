from divesoft_parser.decoders.records.configuration import ConfigurationRecordParser
from divesoft_parser.models.enums import DiveRecordType, ConfigurationType
from divesoft_parser.utilities import BitArray


def test_configuration_decoder_1():
    cfg = ConfigurationRecordParser(
        DiveRecordType.Configuration,
        BitArray(bytes.fromhex('f6ffbf00')),
        bytes.fromhex('000300011102000008160000'),
    ).decode()

    assert cfg.record_type == DiveRecordType.Configuration
    assert cfg.configuration_type == ConfigurationType.Version

    # { "device": 0,
    #   "hwMajor": 3, "hwMinor": 0,
    #   "swMajor": 1, "swMinor": 17,
    #   "swPatchLevel": 2, "swFlags": 0, "swBuild": 5640 }
    assert cfg.device == 0
    assert cfg.hardware_major == 3
    assert cfg.hardware_minor == 0
    assert cfg.software_major == 1
    assert cfg.software_minor == 17
    assert cfg.software_patch == 2
    assert cfg.software_flags == 0
    assert cfg.software_build == 5640


def test_configuration_decoder_2():
    cfg = ConfigurationRecordParser(
        DiveRecordType.Configuration,
        BitArray(bytes.fromhex('f6ffbf00')),
        bytes.fromhex('000300010f030000ab120000'),
    ).decode()

    assert cfg.record_type == DiveRecordType.Configuration
    assert cfg.configuration_type == ConfigurationType.Version

    # { "device": 0,
    #   "hwMajor": 3, "hwMinor": 0,
    #   "swMajor": 1, "swMinor": 15,
    #   "swPatchLevel": 3, "swFlags": 0, "swBuild": 4779 }
    assert cfg.device == 0
    assert cfg.hardware_major == 3
    assert cfg.hardware_minor == 0
    assert cfg.software_major == 1
    assert cfg.software_minor == 15
    assert cfg.software_patch == 3
    assert cfg.software_flags == 0
    assert cfg.software_build == 4779


def test_configuration_decoder_3():
    cfg = ConfigurationRecordParser(
        DiveRecordType.Configuration,
        BitArray(bytes.fromhex('f6ffbf00')),
        bytes.fromhex('000300010f02000033120000'),
    ).decode()

    assert cfg.record_type == DiveRecordType.Configuration
    assert cfg.configuration_type == ConfigurationType.Version

    # { "device": 0,
    #   "hwMajor": 3, "hwMinor": 0,
    #   "swMajor": 1, "swMinor": 15,
    #   "swPatchLevel": 2, "swFlags": 0, "swBuild": 4659 }
    assert cfg.device == 0
    assert cfg.hardware_major == 3
    assert cfg.hardware_minor == 0
    assert cfg.software_major == 1
    assert cfg.software_minor == 15
    assert cfg.software_patch == 2
    assert cfg.software_flags == 0
    assert cfg.software_build == 4659
