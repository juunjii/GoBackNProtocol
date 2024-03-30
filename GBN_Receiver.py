# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the receiver in a Go-Back-N data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_five
from packet import send_ack

class R_receiver:
    ''' Represents the Receiver in the Go-Back-N protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Receiver. '''

        # The sequence number of next packet that is expected to be received
        # from the Sender.
        self.seqnum = 0
        # This should be used as the first argument to to_layer_five() and 
        # send_ack().
        self.entity = 'R'
        # Counter for packet received 
        self.count = 0
        # NAK
        self.nak = 0
        # Max window size 
        self.max_window_size = 8
        return

    def R_input(self, received_packet):
        ''' 
        The Receiver received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Sender.
        ''' 
        # If the packet is received correctly (no corruption, expected sequence number), 
        # pass it to layer 5 
        if ((received_packet.checksum == received_packet.get_checksum()) and (received_packet.seqnum == self.seqnum)):
            self.count+=1
            to_layer_five(self.entity, received_packet.payload.data)
            send_ack(self.entity, self.seqnum) # Send an ACK packet to the Sender 
            sim.totalMsgSent+=1 
            # Update sequence number to the next expected 
            self.seqnum = (self.seqnum + 1) % (self.max_window_size + 1)

        # When receive out of order/corrupted packets
        else:
            sim.totalMsgSent+=1
            sim.retransmittedAck+=1
            sim.retransmittedTotal+=1
            sim.droppedData+=1
            sim.droppedTotal+=1

            # Update relevant simulation counters when packet is corrupt 
            if ((received_packet.checksum != received_packet.get_checksum())):
                sim.corruptedData+=1
                sim.corruptedTotal+=1


            # Send cumulative ACK of last received packet 
            
            # Case 1: Check when it is first packet that's corrupted, just return
            if self.count == 0:
                return
            
            # Case 2: When not first packet and when seqnum is 0, previous ACK would be 8
            # Next expected ack is 0, so previous ACK is 8 
            elif ((self.count > 0) and (self.seqnum == 0)):
                self.nak = self.max_window_size
                send_ack(self.entity, self.nak) 
            
            # Send previous ACK
            else: 
                send_ack(self.entity, self.seqnum -1) 
            
        return

b = R_receiver()