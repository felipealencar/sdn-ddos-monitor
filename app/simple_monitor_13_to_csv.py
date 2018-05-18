# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from operator import attrgetter

from ryu.app import simple_switch_stp_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

import csv
import os.path


class SimpleMonitor13(simple_switch_stp_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.file1_exists = os.path.isfile('../dataset/monitor-ddos-flow-stats.csv')
        self.file2_exists = os.path.isfile('../dataset/monitor-ddos-port-stats.csv')

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPMeterStatsRequest

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        
        body = ev.msg.body

        self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')

        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info('%016x %8x %17s %8x %8d %8d %d %d %d 0x%04x',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count, stat.duration_sec,
                             stat.duration_nsec, ev.timestamp, stat.flags)
            with open('../dataset/monitor-ddos-flow-stats.csv', 'ab') as csvfile:
                fieldnames = ['datapath', 'in-port', 'eth-dst', 'out-port',
                              'packets', 'bytes', 'duration-sec', 'duration-nsec', 'timestamp', 'flags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not self.file1_exists:
                    writer.writeheader()
                datapath_id = "%016x" % ev.msg.datapath.id
                inport = "%8x" % stat.match['in_port']
                eth_dst = "%17s" % stat.match['eth_dst']
                outport = "%8x" % stat.instructions[0].actions[0].port
                packets = "%8d" % stat.packet_count
                bytes = "%8d" % stat.byte_count
                duration_sec = "%d" % stat.duration_sec
                duration_nsec = "%d" % stat.duration_nsec
                timestamp = "%d" % ev.timestamp
                flags = "0x%04x" % stat.flags

                writer.writerow({'datapath': datapath_id, 'in-port': inport, 'eth-dst': eth_dst,
                                 'out-port': outport, 'packets': packets, 'bytes': bytes,
                                 'duration-sec': duration_sec, 'duration-nsec': duration_nsec, 'timestamp': timestamp,
                                 'flags': flags})

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d %d %d %d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors,
                             stat.duration_sec, stat.duration_nsec, ev.timestamp)
            with open('../dataset/monitor-ddos-port-stats.csv', 'ab') as csvfile:
                fieldnames = ['datapath', 'port', 'rx-pkts', 'rx-bytes', 'rx-error', 'tx-pkts', 'tx-bytes', 'tx-error',
                              'duration-sec', 'duration-nsec', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not self.file2_exists:
                    writer.writeheader()
                datapath_id = "%016x" % ev.msg.datapath.id
                port = "%8x" % stat.port_no
                rx_pkts = "%8d" % stat.rx_packets
                rx_bytes = "%8d" % stat.rx_bytes
                rx_error = "%8d" % stat.rx_errors
                tx_pkts = "%8d" % stat.tx_packets
                tx_bytes = "%8d" % stat.tx_bytes
                tx_error = "%8d" % stat.tx_errors
                duration_sec = "%d" % stat.duration_sec
                duration_nsec = "%d" % stat.duration_nsec
                writer.writerow({'datapath': datapath_id, 'port': port, 'rx-pkts': rx_pkts,
                                 'rx-bytes': rx_bytes, 'rx-error': rx_error, 'tx-pkts': tx_pkts,
                                 'tx-bytes': tx_bytes, 'tx-error': tx_error,
                                 'duration-sec': duration_sec, 'duration-nsec': duration_nsec})