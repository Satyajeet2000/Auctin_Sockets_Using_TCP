# Names - Parshav Gandhi(pjgandh3), Satyajeet Patil(smpatil2)

import socket
import threading
import sys

# Global variables
seller_data = {}
bids = []
seller_info = []
buyers_list = []
seller_ip = []
buyer_ip = []
status = 0
SERVER = socket.gethostbyname(socket.gethostname())
UDP_IP =socket.gethostbyname(socket.gethostname())
UDP_PORT = 4001
PORT = int(sys.argv[1])


def seller_handler(client_socket):
    global seller_data
    
    while True:
        # seller_info = client_socket
        status = 1
        client_socket.send("seller".encode())
        seller_string = client_socket.recv(1024).decode()
        print(f"Received auction request from Seller: {seller_string}")

        components = seller_string.split()
        # Assign the components to four different variables
        arg1, arg2, arg3, arg4 = components
        seller_data["type_of_auction"] = int(arg1)
        seller_data["lowest_price"] = int(arg2)
        seller_data["number_of_bids"] = int(arg3)
        
        # validate the auction request
        if validate_auction_request(client_socket, seller_data):
            # This goes to variable called response in the start seller function
            client_socket.send(f"Auction request received: {seller_string}".encode())
            # print(seller_ip[0])
            client_socket.send(seller_ip[0].encode())
            
            while True:
                if(status == 4):
                    client_socket.send("Item sold".encode())
            break
        
        # If could not be validated, ask for a new auction request
        else:
            client_socket.send("Invalid auction request!".encode())


# Bidding doesnt start until we have enough buyers

def buyer_handler(client_socket):
    # Here you have to check the number of buyers connected to the server
    # If they are equal to the number in the input, then you can start the bidding and call bid_handler
    # Also don't send start bidding just yet
    client_socket.send("buyer".encode())
    buyers_list.append(client_socket)
    
    if len(buyers_list) > seller_data["number_of_bids"]:
        client_socket.send("Auction is already going on".encode())
        client_socket.close()
    while True:
        if len(buyers_list) == seller_data["number_of_bids"]:
            bid_handler(client_socket)
            break

def bid_handler(client_socket):
    client_socket.send("start bidding".encode())
    if len(bids) < seller_data["number_of_bids"]:
        bid = client_socket.recv(1024).decode()
        print(f"Received bid from Buyer: {bid}")
        if validate_bid(client_socket, bid):
            bids.append(int(bid))
            client_socket.send("start".encode())
            if len(bids) == seller_data["number_of_bids"]:
                process_auction(client_socket)
        else:
            client_socket.send("Invalid bid. Please submit a positive integer!".encode())
    else:
        client_socket.send("Bidding on-going!".encode())
        # client_socket.close()

def validate_auction_request(client_socket, request):
    # Implement validation logic for the auction request
    b = seller_data["lowest_price"] 
    c = seller_data["number_of_bids"]
    if b>0 and c>0:
        return True
    return False


def validate_bid(client_socket, bid):
    try:
        bid = int(bid)
        return bid > 0
    except ValueError:
        return False


def process_auction(client_socket):
    # Implement the auction logic here
    highest_bid = max(bids)
    if highest_bid >= seller_data["lowest_price"]:
        if seller_data["type_of_auction"] == 1:
            # First-price auction
            status = 4  
            message = f"Item sold for ${highest_bid}"
            #Send message to the buyer
            # This goes to a variable called response in the start buyer function
            client_socket.send("You have won this bid".encode())
            highest_bid = str(highest_bid)
            client_socket.send(highest_bid.encode())
            client_socket.send(seller_ip[0].encode())
            #Send message to the seller
            # This goes to variable called response in the start seller function
            seller_info[0].send(message.encode())
            seller_info[0].send(buyer_ip[0].encode())
            # client_socket.close()
        elif seller_data["type_of_auction"] == 2:
            # Second-price auction
            status = 4
            second_highest_bid = max([b for b in bids if b != highest_bid])
            # This goes to variable called response in the start seller function
            message = f"Item sold for ${second_highest_bid}"
            #Send message to the buyer
            # This goes to a variable called response in the start buyer function
            client_socket.send("You have won this bid".encode())
            second_highest_bid = str(second_highest_bid)
            client_socket.send(second_highest_bid.encode())
            temp_ip = client_socket.getsockname()
            # Extract the IP address and port from the socket address
            ip_address, port = temp_ip
            buyer_ip.append(ip_address)
            client_socket.send(seller_ip[0].encode())
            #Send message to the seller
            # This goes to variable called response in the start seller function
            seller_info[0].send(message.encode())
            # The winning buyers address is supposed to be sent here
            seller_info[0].send(buyer_ip[0].encode())
        # Notify Seller and Buyers
        print(message)
    else:
        message = "Item not sold in the auction"
        print(message)

    reset_auction()


def reset_auction():
    global seller_data, bids
    seller_data = {}
    bids = []


def start_auctioneer():
    # This function starts the auctioneer server
    auctioneer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    auctioneer.bind((SERVER, PORT))
    auctioneer.listen(5)
    print("Auctioneer server is listening for connections on PORT.", PORT)

    while True:
        # This is the main loop that accepts connections from the seller and buyers
        client, addr = auctioneer.accept()

        if seller_data == {}:
            # The first client to connect is the seller
            seller_info.append(client)
            print("Waiting for Seller...")
            print(f"Connected to Seller at{addr}")
            seller_ip.append(addr[0])
            seller_thread = threading.Thread(target=seller_handler, args=(client,))
            seller_thread.start()

        else:
            # All other clients are buyers
            if buyers_list == []:
                print("Waiting for Buyer...")
            print(f"Connected to Buyer {len(buyers_list)+1} at {addr}")
            buyer_thread = threading.Thread(target=buyer_handler, args=(client,))
            buyer_thread.start()
            
        



if __name__ == "__main__":
    #This is the main function and starts the auctioneer server
    start_auctioneer()




