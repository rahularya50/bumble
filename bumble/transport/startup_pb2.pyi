from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Chip(_message.Message):
    __slots__ = ["fd_in", "fd_out", "id", "kind", "loopback", "manufacturer", "model"]
    class ChipKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BLUETOOTH: Chip.ChipKind
    FD_IN_FIELD_NUMBER: _ClassVar[int]
    FD_OUT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    LOOPBACK_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    UNSPECIFIED: Chip.ChipKind
    UWB: Chip.ChipKind
    WIFI: Chip.ChipKind
    fd_in: int
    fd_out: int
    id: str
    kind: Chip.ChipKind
    loopback: bool
    manufacturer: str
    model: str
    def __init__(self, kind: _Optional[_Union[Chip.ChipKind, str]] = ..., id: _Optional[str] = ..., manufacturer: _Optional[str] = ..., model: _Optional[str] = ..., fd_in: _Optional[int] = ..., fd_out: _Optional[int] = ..., loopback: bool = ...) -> None: ...

class ChipInfo(_message.Message):
    __slots__ = ["chip", "serial"]
    CHIP_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    chip: Chip
    serial: str
    def __init__(self, serial: _Optional[str] = ..., chip: _Optional[_Union[Chip, _Mapping]] = ...) -> None: ...

class StartupInfo(_message.Message):
    __slots__ = ["devices"]
    class Device(_message.Message):
        __slots__ = ["chips", "serial"]
        CHIPS_FIELD_NUMBER: _ClassVar[int]
        SERIAL_FIELD_NUMBER: _ClassVar[int]
        chips: _containers.RepeatedCompositeFieldContainer[Chip]
        serial: str
        def __init__(self, serial: _Optional[str] = ..., chips: _Optional[_Iterable[_Union[Chip, _Mapping]]] = ...) -> None: ...
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[StartupInfo.Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[StartupInfo.Device, _Mapping]]] = ...) -> None: ...
