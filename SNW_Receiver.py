# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the receiver in a Stop-and-Wait data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_five
from packet import send_ack

class R_receiver:
    ''' Represents the Receiver in the Stop-and-Wait protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Receiver. '''

        # The sequence number of next packet that is expected to be received
        # from the Sender.
        self.seqnum = 0

        # This should be used as the first argument to to_layer_five() and 
        # send_ack().
        self.entity = 'R'

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
       
        # If the packet is received correctly (no corruption, correct sequence number), 
        # pass it to layer 5 
        if ((received_packet.checksum == received_packet.get_checksum()) and (received_packet.seqnum == self.seqnum)):
            to_layer_five(self.entity, received_packet.payload.data)

            send_ack(self.entity, self.seqnum) # Send an ACK packet to the Sender 
            sim.totalMsgSent+=1 

            # Update sequence number to the next expected 
            self.seqnum = (self.seqnum ^ 1)
           
        else:
            # Send implicit nak when packet corrupt/wrong seq num 
            send_ack(self.entity, self.seqnum ^ 1)
            sim.totalMsgSent+=1
            sim.retransmittedAck+=1
            sim.retransmittedTotal+=1
            sim.droppedData+=1
            sim.droppedTotal+=1

            # Update relevant simulation counters when packet is corrupt 
            if ((received_packet.checksum != received_packet.get_checksum())):
                sim.corruptedData+=1
                sim.corruptedTotal+=1
       
        return

b = R_receiver()