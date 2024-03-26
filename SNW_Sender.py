# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the sender in a Stop-and-Wait data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_three
from event_list import evl
from packet import *

class S_sender:
    ''' Represents the Sender in the Stop-and-Wait protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Sender. '''
        
        # For Stop-and-Wait, the state can be "WAIT_LAYER5" or "WAIT_ACK".
            # "WAIT_LAYER5" is the state where the Sender waits for messages 
            # from the application layer (layer 5).
            # "WAIT_ACK" is the state where the Sender waits to receive an 
            # ACK from the Receiver.
        
        self.state = "WAIT_LAYER5"
        # The sequence number of the next packet that will be sent.
        self.seq = 0
        # This should be used as the second argument to evl.start_timer().
        self.estimated_rtt = 30
        # This should be used as the first argument to to_layer_three() and 
        # evl.start_timer().
        self.entity = 'S'
        # For retransmitting lost packet
        self.lost_packet = None
        
        return

    def S_output(self, message):
        '''
        The Sender received a message from layer 5, so it should try to create
        a packet containing the message and send it to layer 3.
        
        Parameters
        ----------
        - message : msg
            - The message the Sender received from layer 5.
        '''
     
        # Verify the current state of the Sender to make sure it should
        # actually send the message to the Receiver.
        if (self.state == "WAIT_LAYER5"): 
            # Make packet with message and sequence number 
            new_packet = packet(seqnum = self.seq, payload = message)
            self.lost_packet = new_packet # for retransmission when timeout 
            # Send the packet to the Receiver.
            to_layer_three(self.entity, new_packet)
            sim.totalMsgSent +=1
            # Update state to WAIT_ACK when packet is sent 
            self.state = 'WAIT_ACK'
            # Start the timer 
            evl.start_timer(self.entity, self.estimated_rtt)
             
        # When sender in WAIT_ACK state, packets would be dropped 
        else:
            print("waiting for ack, new message is dropped:" + message.data)
            sim.droppedData+=1
            sim.droppedTotal+=1     

        return

    '''
    Routine will be called whenever a (possibly corrupted) packet sent by the
    Receiver (i.e., as a result of the to_layer_three() function being called by
    the Receiver) arrives at the Sender.

    '''
    def S_input(self, received_packet):
        '''
        The Sender received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Receiver.
        '''
     
        # State to receive ACK from receiver 
        if (self.state == "WAIT_ACK"):
        
            # Checks if packet is corrupted & ACK num is correct
            if ((received_packet.checksum == received_packet.get_checksum()) and (received_packet.acknum == self.seq)):
                evl.remove_timer() 
                self.state = "WAIT_LAYER5"
                # Update sequence number to the next expected ACK number 
                self.seq = (self.seq ^ 1) 
    
            else:  
                # When receive wrong ACK num or corruption from packet 
                sim.droppedAck+=1
                sim.droppedTotal+=1  

                # Packet is corrupt 
                if (received_packet.checksum != received_packet.get_checksum()):
                    sim.corruptedAck+=1
                    sim.corruptedTotal+=1
            
        return


    '''
        Routine will be called when the Sender’s timer
        expires (thus generating a timer interrupt). 

        controls the retransmission of packets 
    '''
    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that the ACK for the most recently 
            sent packet wasn't received by the Sender in time, so the packet 
            needs to be retransmitted. '''
    
        # State to handle timeout 
        if (self.state == "WAIT_ACK"):    
            to_layer_three(self.entity, self.lost_packet) # Retransmit 
         
            sim.totalMsgSent+=1 
            sim.retransmittedData+=1
            sim.retransmittedTotal+=1
            evl.start_timer(self.entity, self.estimated_rtt)

        return

a = S_sender()