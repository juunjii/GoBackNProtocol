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
        if ((not self.c_b.isfull())):
            print("Buffer size when send to layer3: " + str(self.c_b.count))
            # Make packet with message and sequence number 
            new_packet = packet(seqnum = self.seq, payload = message)
            print("Sequence number of current packet: " + str(self.seq))
            # Send the packet to the Receiver.
            to_layer_three(self.entity, new_packet)
            sim.totalMsgSent +=1
            self.c_b.push(new_packet) 
            print("Buffer size after adding new packet: " + str(self.c_b.count))
           
        
            if (self.base == self.seq):
                # Timer for oldest transmitted but not yet ACKed packet 
                evl.start_timer(self.entity, self.estimated_rtt)

            # Sequence number of next packet to be sent 
            self.seq = (self.seq + 1) % 9
            print("Sequence number of next packet to send: " + str(self.seq))

          
            
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
        if (received_packet.checksum == received_packet.get_checksum()):
            print("ACK received: " + str(received_packet.acknum))
            print("Circular buffer size: " + str(self.c_b.count))
            
            # print("Entered S_input")
            window = self.c_b.read_all() # Window is list of packets 
            # Store package seq num in list 
            # print("window: ")
            # print(window)
            self.seqnum_list = [package.seqnum for package in window] 
            print("seqnum_list: " + str(self.seqnum_list))
            print("Length of seqnum_list: " + str(len(self.seqnum_list)))

            # Case when r
            if (self.base == received_packet.acknum):
                    print("base = acknum")
                    # print("When base = acknum buffer state:")
                    # print(self.c_b.read_all())
                    # Packet removed
                    self.c_b.pop()
                    # print("When base = acknum buffer after pop state:")
                    # print(self.c_b.read_all())
                    
            # Firt case: Received ACK > expected ACK 
            if (self.base < received_packet.acknum):
                print("base < acknum")
                # Update the circular buffer based on the 
                # received acknowledgment number using pop().
                # Go-Back-N uses cumulative ACKs meaning that more than 
                # one packet may need to be removed from the circular buffer.
                for i in range(self.base, received_packet.acknum + 1):
                    # Packet removed
                    # print("First case buffer state:")
                    self.c_b.pop()
                    # print("First case buffer after pop state:")
                    # print(self.c_b.read_all())

                    # print(self.c_b.read_all())
                
            # Second case: Received ACK that is smaller than base but
            # in sliding window (eg: base:3, ack: 0)
            elif (self.base > received_packet.acknum) and (received_packet.acknum in self.seqnum_list):
                print("base > acknum")
                for i in range(self.base, ((received_packet.acknum + 9) - self.base + 2)):
                    # Packet removed
                    # print("Second case buffer state:")
                    self.c_b.pop()
                    # print("Second case buffer after pop state:")
                    # print(self.c_b.read_all())
                    # print(self.c_b.read_all())


            # Base increased to next expected sequence number 
            # when ACK received
            # print("Base: " + str(self.base))
            self.base = (received_packet.acknum + 1) % 9

            print("Base after increment: " + str(self.base))

            
            # If no outstanding unACKed packets, then timer is removed
            if (self.base == self.seq):
                evl.remove_timer() 
            # If ACK received but there still packets unACKed, 
            # then, the timer should be removed and restarted 
            else: 
                evl.remove_timer()
                evl.start_timer(self.entity, self.estimated_rtt)
        
        # Covers dup ACK num case? 
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
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces and 2.5.4 Helpful Hints in the Project Instructions
        # for how to use each method and how to handle timers.

        
        # Do not need a timer for each packet in window 

        # But there may be outstanding unACK paackets in network 
        # (need think about how to use one timer)


        evl.start_timer(self.entity, self.estimated_rtt)
        # TODO: Send all the unACKed packets in the circular buffer.

        # What are unACKed packets in the cb?
        # between base and seq num 


        # index = self.seqnum_list.index(self.base - 1)
        # index2 = self.seqnum_list.index(self.seq)
        # for i in range(index, index2 + 1:
        for i in range(self.c_b.count):
            to_layer_three(self.entity, self.c_b.read_all()[i])
            sim.totalMsgSent+=1 
            sim.retransmittedData+=1
            sim.retransmittedTotal+=1

        return

a = S_sender()