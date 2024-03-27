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


        # TODO: Initialize any other useful class variables you can think of.
        
        # First sent but unACKed pkt, move forward when ACK'ed
        # Expected ACK 
        self.base = 0
        # For retransmitting lost packet
        self.lost_packet = None
        # List representing current state of window (expected ACK to receive)
        # self.window= []


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
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: Implement the output function as mentioned in the FSM to send 
        # the message to the receiver if the circular buffer isn't full. If it 
        # is, then drop the message and update your variables and indicate 
        # that in your output and update the statistics counters accordingly.
        

        # Buffer is space of window 

        # Only send new packets when there is space in window 
        # Send messages up to window size
        # Circular buffer is not full, send message to receiver 
        if ((not self.c_b.isfull()) and (self.seq < (self.base + self.c_b.max))):
    
            # Make packet with message and sequence number 
            new_packet = packet(seqnum = self.seq, payload = message)
            self.lost_packet = new_packet # for retransmission when timeout 
            # Send the packet to the Receiver.
            to_layer_three(self.entity, new_packet)
            self.c_b.push(new_packet) 
            sim.totalMsgSent +=1
        
            if (self.base == self.seq):
                # Timer for oldest transmitted but not yet ACKed packet 
                evl.start_timer(self.entity, self.estimated_rtt)

            # Sequence number of next packet to be sent 
            self.seq = (self.seq + 1) % 9
          
            
        # Drop message when sender is waiting for an ACK or the buffer is full (pg 11)
        # Extra credit to buffer new messages when window is full 
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
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: Verify the received packet's checksum to make sure that it's
        # uncorrupted and it's acknowledgment number to see whether it is 
        # within the Sender's window. Update the circular buffer based on the 
        # received acknowledgment number using pop(). Go-Back-N uses cumulative 
        # ACKs meaning that more than one packet may need to be removed 
        # from the circular buffer.

        # Use read_all and form actual window 
        # and compare sequence number of packets 
        
        # Verify the received packet's checksum to make sure that it's
        # uncorrupted and it's acknowledgment number to see whether it is 
        # within the Sender's window.
        if ((received_packet.checksum == received_packet.get_checksum()) and (received_packet.acknum <= self.c_b.count)):
            window = [] 
            # Firt case: Received ACK > expected ACK 
            if (self.base < received_packet.acknum):
                window = self.c_b.read_all() # List containing all packets 


            # Update the circular buffer based on the 
            # received acknowledgment number using pop().
                # for i in range(self.base, received_packet.acknum + 1):
                #     if (self.c_b.pop())
                #     self.c_b.pop()

            # Solution: pop, move one up, so can add, rearrange buffer so empty space @ back 
                    
            # Go-Back-N uses cumulative ACKs meaning that more than 
            # one packet may need to be removed from the circular buffer.

                # Base increased to next expected sequence number 
                self.base = received_packet.acknum + 1


           # Move window up when received ACK
            # self.c_b.push(new_packet)

            # If no outstanding unACKed packets, then timer is removed
            if (self.base == self.seq):
                evl.remove_timer() 
            # If ACK received but there still packets unACKed, 
            # then, the timer should be removed and restarted 
            else: 
                evl.remove_timer()
                # evl.start_timer(received_packet)
         

            # Deal with out of order packets by your own implementation
        

        return


    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that an ACK for any of the most 
            recently sent packets wasn't received by the Sender in time, so 
            all currently outstanding and unacknowledged packet needs to be 
            retransmitted. '''
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces and 2.5.4 Helpful Hints in the Project Instructions
        # for how to use each method and how to handle timers.

        
        # Do not need a timer for each packet in window 

        # But there may be outstanding unACK paackets in network 
        # (need think about how to use one timer)


        evl.start_timer(self.entity, self.estimated_rtt)
        # TODO: Send all the unACKed packets in the circular buffer.
        for i in range(self.base, self.seq):
            to_layer_three(self.entity, self.c_b.read_all[i])


        return

a = S_sender()