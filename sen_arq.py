import logging
import socket
import sys
import time

import coloredlogs
import verboselogs

import packet

# Configure logging
verboselogs.install()
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", fmt="%(asctime)s - %(message)s", datefmt="%H:%M:%S")

# Just packet every character in message as there are no windows needed
def sender():

    next_seq_no = 0

    for char in message:

        # Create packet
        pkt = packet.Packet(next_seq_no, ptype=packet.Packet.TYPE_DATA, data=char)
        logger.info("[SEND]: Sending %s." % pkt)

        # Send packet
        packet.send_packet(client, pkt)
        next_seq_no = (next_seq_no + 1) % 2
        ack = packet.recv_packet(client, timeout=packet.ACK_WAIT_TIME / 1000)

        # Check if packet is corrupt or not the expected one
        while (
            ack is None
            or ack.is_corrupt()
            or ack.ptype != packet.Packet.TYPE_ACK
            or ack.seq_no != next_seq_no
        ):
            if ack is None:
                logger.error("[TIMEOUT]: Sending %s again" % pkt)
            elif ack.is_corrupt():
                logger.error("[ERR]: ACK not received.")
                logger.info("Sending %s again." % pkt)

            packet.send_packet(client, pkt)
            ack = packet.recv_packet(client, timeout=packet.ACK_WAIT_TIME / 1000)
        logger.debug("[ACK]: Received %s" % ack)
        time.sleep(1)

    # EOF
    pkt = packet.Packet(-1, data=None)
    packet.send_packet(client, pkt)
    logger.success("[SEND]: Transfer complete. Sending EOF")


if __name__ == "__main__":
    # Create socket instance
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    sock.bind((socket.gethostname(), 3300 if len(sys.argv) <= 1 else int(sys.argv[1])))
    sock.listen(1)

    client, _addr = sock.accept()
    logger.debug("Connected.")

    # Set vars if given (Default set in packet module)
    if len(sys.argv) >= 3:
        packet.LOSS_PROB = float(sys.argv[2])
        packet.ACK_WAIT_TIME = int(sys.argv[3])
        message = sys.argv[4]

    logger.verbose(
        "LOSS_PROB: {0}, ACK_WAIT_TIME: {1}, MESSAGE: {2}".format(
            packet.LOSS_PROB,
            packet.ACK_WAIT_TIME,
            message,
        )
    )

    sender()
    client.close()
    sock.close()
    sys.exit(0)