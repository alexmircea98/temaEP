from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

class LoadBalancingSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    global EX_IP
    EX_IP = "10.10.11.1"

    global SLAVES
    servers = ["10.10.10.11", "10.10.10.12", "10.10.10.13"]

    def __init__(self, *args, **kwargs):
        super(LoadBalancingSwitch, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser


        #check ip
        pack = packet.Packet(msg.data)
        self.logger.info("pkt %s", pkt)  # DEBUG
        ip = pack.get_protocol(ipv4.ipv4)
        self.logger.info("ipv4 %s", ip)  # DEBUG

        if ip.dst == EX_IP:
            #Load balance
            server_ip = random.choice(servers)  # Random choice

            actions = [
                parser.OFPActionSetNwDst(self.ipv4_to_int(server_ip)),
                parser.OFPActionOutput(ofproto.OFPP_LOCAL)
            ]

            out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id,
                                      data=message.data, in_port=message.in_port, actions=actions)

            datapath.send_msg(out)

        else:
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]

            data = None
            if msg.buffer_id == ofp.OFP_NO_BUFFER:
                data = msg.data

            out = ofp_parser.OFPPacketOut(
                datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,
                actions=actions, data = data)
            dp.send_msg(out)