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

        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.

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
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: If the packet is correct, deliver to layer 5 and take the 
        # necessary actions as descriped in the FSM.
        


        # If receiver does not bugger out of order packets, 
        # then it will wait for all packets to be retransmitted
        # then only send one cumulative ACK?  


        return

b = R_receiver()