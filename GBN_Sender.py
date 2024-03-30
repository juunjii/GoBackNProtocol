# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the sender in a Go-Back-N data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_three
from event_list import evl
from packet import *
from circular_buffer import circular_buffer

class S_sender:
    ''' Represents the Sender in the Go-Back-N protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Sender. '''
        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.
        
        # The sequence number of the next packet that will be sent.
        self.seq = 0
        # This should be used as the second argument to evl.start_timer().
        self.estimated_rtt = 30
        # This should be used as the first argument to to_layer_three() and 
        # evl.start_timer().
        self.entity = 'S'
        # The circular buffer that will store any outstanding and 
        # unacknowledged packets.
        self.c_b = circular_buffer(8)
        
        # First sent but unACKed pkt, move forward when ACK'ed
        # Expected ACK 
        self.base = 0
        # List representing current state of window (expected ACK to receive)
        self.window= []
        # Store package seq num in list 
        self.seqnum_list = []

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
      
        # Only send new packets when there is space in window  
        if ((not self.c_b.isfull())):
            # Make packet with message and sequence number 
            new_packet = packet(seqnum = self.seq, payload = message)
            # Send the packet to the Receiver.
            to_layer_three(self.entity, new_packet)
            sim.totalMsgSent +=1
            # Add packet to circular buffer
            self.c_b.push(new_packet) 
            
            # Sending new packet 
            if (self.base == self.seq):
                # Timer for oldest transmitted but not yet ACKed packet 
                evl.start_timer(self.entity, self.estimated_rtt)

            # Sequence number of next packet to be sent 
            self.seq = (self.seq + 1) % 9

        # Drop message when sender is waiting for an ACK or the buffer is full 
        else:
            print("buffer is full, new message is dropped: " + message.data)
            sim.droppedData+=1
            sim.droppedTotal+=1     
        return    
        
            
    def S_input(self, received_packet):
        '''
        The Sender received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Receiver.
        '''       
        
        window = self.c_b.read_all() # Window is list of packets 
        # List of packet's sequence numbers in window
        self.seqnum_list = [package.seqnum for package in window] 
      
        if (received_packet.checksum == received_packet.get_checksum()) and (received_packet.acknum in self.seqnum_list):

            if (self.base == received_packet.acknum):      
                self.c_b.pop()
                
            # Received ACK > expected ACK 
            elif (self.base < received_packet.acknum):
                # Update the circular buffer based on the received acknowledgment number
                # Go-Back-N uses cumulative ACKs meaning that more than 
                # one packet may need to be removed from the circular buffer.
                for i in range(self.base, received_packet.acknum + 1):
                    self.c_b.pop()
                    
            # Received ACK that is smaller than base but in sliding window
            elif (self.base > received_packet.acknum) and (received_packet.acknum in self.seqnum_list):
                for i in range(self.base, ((self.c_b.max + 1) - self.base + 2)):
                    self.c_b.pop()
            
            # Base increased to next expected sequence number when ACK received
            self.base = (received_packet.acknum + 1) % 9
            

            # There may be outstanding unACK packets in network 
            # To handle: 
            # If no outstanding unACKed packets, then timer is removed
            if (self.base == self.seq):
                evl.remove_timer() 
            # If ACK received but there still packets unACKed, 
            # then, the timer should be removed and restarted 
            else: 
                evl.remove_timer()
                evl.start_timer(self.entity, self.estimated_rtt)
        
        else:  
            # When receive wrong ACK num or corruption from packet 
            sim.droppedAck+=1
            sim.droppedTotal+=1  

            # Packet is corrupt 
            if (received_packet.checksum != received_packet.get_checksum()):
                sim.corruptedAck+=1
                sim.corruptedTotal+=1
        return


    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that an ACK for any of the most 
            recently sent packets wasn't received by the Sender in time, so 
            all currently outstanding and unacknowledged packet needs to be 
            retransmitted. '''  
        # Do not need a timer for each packet in window 
        evl.start_timer(self.entity, self.estimated_rtt)
        # Send all the unACKed packets in the circular buffer.
        for i in range(self.c_b.count):
            to_layer_three(self.entity, self.c_b.read_all()[i])
            sim.totalMsgSent+=1 
            sim.retransmittedData+=1
            sim.retransmittedTotal+=1

        return
    

a = S_sender()