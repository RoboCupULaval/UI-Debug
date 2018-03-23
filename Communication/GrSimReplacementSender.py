
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
        # GrSim use meter not millimeters
        packet.replacement.ball.x = position[0] / 1000
        packet.replacement.ball.y = position[1] / 1000
        packet.replacement.ball.vx = speed[0]
        packet.replacement.ball.vy = speed[1]

        self.send_packet(packet)

    def set_robots_position(self, teams_formation):
        packet = grSim_Packet()
        for x, y, direction, robot_id, yellow_team in teams_formation:
            # GrSim use meter not millimeters
            packet.replacement.robots.add(x=x/1000, y=y/1000, dir=direction, id=robot_id, yellowteam=yellow_team)

            self.send_packet(packet)

    def set_robot_position(self, x, y, direction, robot_id, yellow_team):
        packet = grSim_Packet()
        # GrSim use meter not millimeters
        packet.replacement.robots.add(x=x / 1000, y=y / 1000, dir=direction, id=robot_id, yellowteam=yellow_team)

        self.send_packet(packet)
            
    def send_packet(self, packet):
        try:
            self.client.send(packet.SerializeToString())
        except ConnectionRefusedError:
            print("Trying to send message to grsim, connection refused")



