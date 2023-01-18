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

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import logging
import grpc
import os
import pathlib
import sys

from .common import PumpedTransport, PumpedPacketSource, PumpedPacketSink
from .packet_streamer_pb2_grpc import PacketStreamerStub
from .packet_streamer_pb2 import PacketRequest
from .hci_packet_pb2 import HCIPacket
from .startup_pb2 import Chip, ChipInfo
from .emulated_bluetooth_vhci_pb2_grpc import VhciForwardingServiceStub

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
DEFAULT_SERIAL = 'bumble0'
DEFAULT_MANUFACTURER = 'Bumble'


# -----------------------------------------------------------------------------
def find_grpc_port():
    ini_dir = None
    if sys.platform == 'darwin':
        if home := os.getenv('HOME', None):
            ini_dir = pathlib.Path(home) / 'Library/Caches/TemporaryItems'
    elif sys.platform == 'linux':
        if xdg_runtime_dir := os.environ.get('XDG_RUNTIME_DIR', None):
            ini_dir = pathlib.Path(xdg_runtime_dir)
    elif sys.platform == 'win32':
        if local_app_data_dir := os.environ.get('LOCALAPPDATA', None):
            ini_dir = pathlib.Path(local_app_data_dir) / 'Temp'
    
    if not ini_dir:
        logger.debug('no known directory for ini file')
        return 0
    
    ini_file = ini_dir / 'netsim.ini'
    if ini_file.is_file():
        logger.debug(f'Found .ini file at {ini_file}')
        with open(ini_file, 'r') as ini_file_data:
            for line in ini_file_data.readlines():
                if '=' in line:
                    key, value = line.split('=')
                    if key == 'grpc.backend.port':
                        logger.debug('gRPC port = {value}')
                        return int(value)

    # Not found
    return 0


# -----------------------------------------------------------------------------
async def open_android_netsim_transport(spec):
    '''
    Open a transport connection to Android's `netsim` simulator via its gRPC interface.
    The parameter string has this syntax:
    [<remote-host>:<remote-port>][,serial=<serial>]
    The <remote-host>:<remote-port> part is optional. When not specified, the transport
    looks for a netim .ini file, from which is will read the grpc.backend.port property.

    Examples:
    (empty string) --> connect to netsim on the port specified in the .ini file
    localhost:8555 --> connect to netsim on localhost:8555
    serial=bumble1 --> connect to netsim, using `bumble1` as the "chip" serial.
    '''

    # Wrapper for I/O operations
    class HciDevice:
        def __init__(self, serial, manufacturer, hci_device):
            self.serial = serial
            self.manufacturer = manufacturer
            self.hci_device = hci_device

        async def start(self):  # Send the startup info
            chip_info = ChipInfo(
                serial=self.serial,
                chip=Chip(kind=Chip.ChipKind.BLUETOOTH, manufacturer=self.manufacturer),
            )
            await self.hci_device.write(PacketRequest(initial_info=chip_info))

        async def read(self):
            response = await self.hci_device.read()
            response_type = response.WhichOneof('response_type')
            if response_type == 'error':
                logger.warning(f'received error: {response.error}')
                raise RuntimeError(response.error)
            elif response_type == 'hci_packet':
                return (
                    bytes([response.hci_packet.packet_type])
                    + response.hci_packet.packet
                )

            raise ValueError('unsupported response type')

        async def write(self, packet):
            await self.hci_device.write(
                PacketRequest(
                    hci_packet=HCIPacket(packet_type=packet[0], packet=packet[1:])
                )
            )

    # Parse the parameters
    serial = DEFAULT_SERIAL
    manufacturer = DEFAULT_MANUFACTURER
    params = spec.split(',') if spec else []

    if params and ':' in params[0]:
        # Explicit <host>:<port>
        server_host, server_port = params[0].split(':')
        params_offset = 1
    else:
        # Look for the gRPC config in a .ini file
        server_host = 'localhost'
        server_port = find_grpc_port()
        if not server_port:
            raise RuntimeError('gRPC server port not found')
        params_offset = 0

    for param in params[params_offset:]:
        if '=' not in param:
            raise ValueError('invalid parameter, expected <name>=<value>')
        param_name, param_value = param.split('=')
        if param_name == 'serial':
            serial = param_value

    # Connect to the gRPC server
    server_address = f'{server_host}:{server_port}'
    logger.debug(f'connecting to gRPC server at {server_address}')
    channel = grpc.aio.insecure_channel(server_address)

    # Connect as a host
    service = PacketStreamerStub(channel)
    hci_device = HciDevice(
        serial=serial,
        manufacturer=manufacturer,
        hci_device=service.StreamPackets(),
    )
    await hci_device.start()

    # Create the transport object
    transport = PumpedTransport(
        PumpedPacketSource(hci_device.read),
        PumpedPacketSink(hci_device.write),
        channel.close,
    )
    transport.start()

    return transport
