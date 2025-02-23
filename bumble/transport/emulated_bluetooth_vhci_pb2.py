# Copyright 2021-2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: emulated_bluetooth_vhci.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import emulated_bluetooth_packets_pb2 as emulated__bluetooth__packets__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1d\x65mulated_bluetooth_vhci.proto\x12\x1b\x61ndroid.emulation.bluetooth\x1a emulated_bluetooth_packets.proto2y\n\x15VhciForwardingService\x12`\n\nattachVhci\x12&.android.emulation.bluetooth.HCIPacket\x1a&.android.emulation.bluetooth.HCIPacket(\x01\x30\x01\x42J\n\x1f\x63om.android.emulation.bluetoothP\x01\xf8\x01\x01\xa2\x02\x03\x41\x45\x42\xaa\x02\x1b\x41ndroid.Emulation.Bluetoothb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'emulated_bluetooth_vhci_pb2', globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\037com.android.emulation.bluetoothP\001\370\001\001\242\002\003AEB\252\002\033Android.Emulation.Bluetooth'
    _VHCIFORWARDINGSERVICE._serialized_start = 96
    _VHCIFORWARDINGSERVICE._serialized_end = 217
# @@protoc_insertion_point(module_scope)
