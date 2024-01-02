# Names - Parshav Gandhi(pjgandh3), Satyajeet Patil(smpatil2)

import socket
import numpy as np
import time
import sys


SERVER = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[2]) #5050
# UDP_PORT = 5005
buyer_ip = []
UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 4001
packet_loss_rate = float(sys.argv[3])  # Adjust the packet loss rate as needed


def check_status(seller_client, msg):
        # This function checks the status of the auction request from the seller
        if msg == "Invalid auction request!":
            #This is when the auction request is invalid
            auction_request = input("Enter auction request (e.g., '2 10 3 WolfPackSword'): ")       
            seller_client.send(auction_request.encode())
            response = seller_client.recv(1024).decode()
            check_status(seller_client, response)
        elif msg == "Auction request received: ":
            #This is when the auction request is valid
            print(msg)
            return

def start_seller(seller_client):

    print("Connected to the Auctioneer server as a Seller.")
    auction_request = input("Enter auction request (e.g., '2 10 3 WolfPackSword'): ")
    # The auction request is sent to the server
    seller_client.send(auction_request.encode())    
    response = seller_client.recv(1024).decode()
    # This response says "Auction request received: 2 10 3 WolfPackSword"
    print(response)
    response2 = seller_client.recv(1024).decode()
    # This response says the IP address of the seller
    check_status(seller_client, response)
    while True:
        print("Server: Auction Start")
        response = seller_client.recv(1024).decode()
        # This response says that the auction has ended and the item has been sold for whatever amount
        print('Auction finished!')
        response2 = seller_client.recv(1024).decode()
        print('Success! ' + response+". Buyer IP: "+response2)
        print('Disconnecting from the Auctioneer server. Auction is over!')
        break
        if "Server: Auction Start" in auctioneer_response:
            break
    
    seller_client.close()
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP socket opened for RDT.\nStart sending file.")

    # Set the server address
    server_address = (socket.gethostbyname(socket.gethostname()), UDP_PORT)
    seq_num = 0
    message_type = 0  # Assuming this message is a control message with TYPE 0
    chunk_size = 2000  # in bytes
    with open('tosend.file', 'rb') as file:
            byte_string = file.read()
    chunks = [byte_string[i:i+chunk_size]
              for i in range(0, len(byte_string), chunk_size)]
    temp = 0
    # length = len(chunks)
    for i in chunks:
        decoded_string = i.decode('utf-8')  # Assuming utf-8 encoding, adjust if needed
        temp+=len(decoded_string)
    # payload = read_input_file("tosend.file")[0].decode()
    # total_size = len(payload)
    x = str(temp)
    client_socket.sendto(x.encode(), server_address)
    total_size = temp
    print(f"Total size of the file: {total_size} bytes")
    start_time = time.time()
    temp=0
    for i in chunks:     
        flag = False
        while not flag:
            # Some random condition
            if np.random.binomial(1, packet_loss_rate) == 0:
                flag = True
                print(f"Packet Successfully sent")
                temp+=len(decoded_string)
            else:
                print(f"Packet loss encounterd, \nRetrying...")  

            decoded_string = i.decode('utf-8')  # Assuming utf-8 encoding, adjust if needed
            payload = decoded_string
            # for i in range(2):
            message = f"{seq_num}:{message_type}:{payload}"

            # Send the message to the server
            client_socket.sendto(message.encode(), server_address)
            # Wait for the acknowledgment
            try:
                client_socket.settimeout(2)  # Timeout for acknowledgment
                ack, server_address = client_socket.recvfrom(1024)
                print(f"Sending control seq: {temp} / {total_size}")
                y = ack.decode().split(":")
                print(f"Acknowledgment received: {y[1]}")
                print("\n")
                
            except socket.timeout:
                print("Timeout: No acknowledgment received.")
    end_time = time.time()
    
    tct = end_time - start_time
    at = total_size / tct

    print(f"TCT: {tct} seconds")
    print(f"AT: {at}")
    client_socket.close()
        
        

def check_bid_status(buyer_client, msg):
        # This function checks the status of the bid from the buyer
        if msg == "Invalid bid. Please submit a positive integer!":
            bid = input("Enter your bid (a positive integer): ")
            buyer_client.send(bid.encode())
            response = buyer_client.recv(1024).decode()
            check_bid_status(buyer_client, response)
        else:
            # This is if the bid is valid
            return

def start_buyer(buyer_client):
    # This function starts the buyer client
    print("Connected to the Auctioneer server as a Buyer.")
    print("Waiting for more buyers to join")
    role = buyer_client.recv(1024).decode()
    print(role)
    
    if "start bidding" in role:
        #This message from the server is indicative of when the bidding starts
        bid = input("Enter your bid (a positive integer): ")
        # The bid is sent to the server
        buyer_client.send(bid.encode())
        response = buyer_client.recv(1024).decode()
        check_bid_status(buyer_client, response)
        if "Bidding on-going" in response:
            print("Bidding is on going")
        else:
            print("Your bid has been submitted")
            response = buyer_client.recv(1024).decode()
            # This response says that you have won this bid
            print('Auction finished!')
            response2 = buyer_client.recv(1024).decode()
            response3 = buyer_client.recv(1024).decode()
            # This response gives the IP address of the seller
            print(f'You have won this item WolfPackSword! Your payment due is ${response2}. ' + 'Seller IP: ' + response3)
            print('Disconnecting from the Auctioneer server. Auction is over!')
            print('UDP socket opened for RDT.\nStart receiving file.')
                    
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Bind the socket to a specific IP address and port
            server_address = (socket.gethostbyname(socket.gethostname()), UDP_PORT)
            server_socket.bind(server_address)

            # print(f"UDP Server is listening on {server_address}...")
            total_length = server_socket.recvfrom(4000)[0].decode()	
            expected_seq_num = 0
            temp = 0
            tp = 0
            tp2 = 1
            file_text=''
            a= time.time()
            while True:
                # Receive a packet from the client
                data, client_address = server_socket.recvfrom(4000)
                # Extract sequence number and payload
                seq_num, message_type, payload = data.decode().split(":")
                seq_num = int(seq_num)
                file_text+=payload
                # print(file_text)
                temp+=len(payload)
                # Check if the received packet has the expected sequence number
                if seq_num == expected_seq_num:
                    # Acknowledge the received packet
                    
                    server_socket.sendto(f"ACK:{tp}".encode(), client_address)

                    # Process the received payload
                    print(f"Received data seq {tp2}: {temp} / {total_length}")
                    print(f"Msg recieved: {tp}")
                    print(f"Ack sent: {tp}")
                    if(temp==int(total_length)):
                        print("\n")
                        print(f"Received data seq {tp2}: {temp} / {total_length}")
                        print(f"Msg recieved: {tp}")
                        print(f"Ack sent: {tp}")
                        with open('output.txt', 'w') as file:
                            file.write(file_text)
                    if tp==0:
                        tp=1
                    else:
                        tp=0
                    if tp2==0:
                        tp2=1
                    else:
                        tp2=0

                    # Move to the next expected sequence number
                    # expected_seq_num = (expected_seq_num + 1) % 2
                else:
                    
                    # Resend the acknowledgment for the previous packet
                    server_socket.sendto(f"ACK:{(expected_seq_num - 1) % 2}".encode(), client_address)
                buyer_client.close()
                
                b = time.time()
                print("TCT: ", b-a)
                print("AT: ", temp/(b-a))
            
    elif "Bid submitted" in role:
        print("Bid submitted")
    else:
        print("Closing Buyer connection")
        buyer_client.close()
    # print("Closing Buyer connection")

def create_file_chunks(file_byte_string, chunk_size):
    # divide a file into chunks of size chunk_size
    chunks = [file_byte_string[i:i+chunk_size]
              for i in range(0, len(file_byte_string), chunk_size)]
    # print(chunks)
    return chunks


def read_input_file(file_path):
    try:
        # open the file as a binary byte string
        with open(file_path, 'rb') as file:
            byte_string = file.read()
        # if the file is successfully opened then create chunks of the file
        if byte_string is not None:
            return create_file_chunks(byte_string, 200)
    except FileNotFoundError:
        # if the file is not found then print an error message
        print(f'Error: File {file_path} not found.')
        return


if __name__ == "__main__":
    # client_type = input("Enter 'Seller' or 'Buyer': ")
    server_ip = SERVER  # Replace with the Auctioneer server IP
    server_port = PORT  # Replace with the Auctioneer server port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    server_response = client_socket.recv(1024).decode()
    if server_response == 'seller':
        print("Your role is: [Seller]")
        start_seller(client_socket)
    elif server_response == 'buyer':
        print("Your role is: [Buyer]")
        start_buyer(client_socket)
    else:
        print("Invalid client type. Use 'Seller' or 'Buyer'.")

