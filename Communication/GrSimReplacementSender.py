
import socket

from Communication.grSim_Packet_pb2 import grSim_Packet
from Communication.grSim_Replacement_pb2 import grSim_RobotReplacement


def udp_socket(host, port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_info = (host, port)
    skt.connect(connection_info)
    return skt


class GrSimReplacementSender:
    def __init__(self, host="127.0.0.1", port=20011):
        self.client = udp_socket(host, port)

    def set_ball_position(self, position: tuple, speed=(0, 0)):

        packet = grSim_Packet()
        packet.replacement.ball.x = position[0]
        packet.replacement.ball.y = position[1]
        packet.replacement.ball.vx = speed[0]
        packet.replacement.ball.vy = speed[1]
        print(packet)
        self.client.send(packet.SerializeToString())

    def set_robot_positions(self, positions_wrapper: tuple):
        packet = grSim_Packet()
        for position in positions_wrapper:
            packet.replacement.robots.add(x=position[0], y=position[1], dir=position[2], id=position[3],
                                          yellowteam=position[4])
        print(packet)
        self.client.send(packet.SerializeToString())



