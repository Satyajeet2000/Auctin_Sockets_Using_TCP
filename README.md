
# Project Title

A brief description of what this project does and who it's for

## Part 1

### Sealed-Bid Auction Simulation
This project implements a sealed-bid auction simulation with two types of processes: an "Auctioneer" server and a "Seller/Buyer" client. The simulation involves the following components:

#### Auctioneer Server
Hosts auctions and accepts auction requests from Sellers.
Manages the auction process, including specifying auction type (first-price or second-price), the lowest acceptable price, the intended number of bids, and the item to be sold.
Opens the auction, accepts bids from Buyers, and processes the bids at the end of the auction.

#### Seller/Buyer Client
Submits auction requests to the Auctioneer server.
Bids for items in the auction after connecting to the Auctioneer server.
A client can act as either a Seller or a Buyer but not both.
Project Highlights
Supports both first-price and second-price auction types.
Enables Sellers to specify the lowest acceptable price and intended number of bids.
Facilitates bidding from connected Buyers.
Processes all bids at the end of the auction, finds the highest bid, and notifies the Seller and Buyers about the auction's status.

---

## Part 2
### Sealed-Bid Auction Simulation with UDP-Based File Transfer

This extended version of the sealed-bid auction simulation project includes a UDP-based, application-layer reliable data transfer (RDT) protocol. The key components and features remain the same, with an additional scenario:

#### Our Scenario: UDP-Based File Transfer

- **Objective**: Transmit the auctioned item (file) directly from the Seller to the winning Buyer.
- **Implementation**: A custom UDP-based RDT protocol is introduced for reliable data transfer.
- **Process**:
  1. After the auction concludes, the Auctioneer server acts as an index server in a peer-to-peer transfer scenario.
  2. The Seller, the winning Buyer, and the Auctioneer collaborate to carry out the file transfer.
  3. The UDP-based RDT protocol ensures reliable and efficient transfer from the Seller to the winning Buyer.

#### Existing Components

- **Auctioneer Server**: Hosts auctions, manages auction details, and oversees the file transfer process.
- **Seller/Buyer Client**: Submits auction requests, places bids, and participates in the file transfer.

#### Project Highlights

- Supports both first-price and second-price auction types.
- Enables Sellers to specify the lowest acceptable price and intended number of bids.
- Facilitates bidding from connected Buyers.
- Processes all bids at the end of the auction, finds the highest bid, and notifies the Seller and Buyers about the auction's status.
- Implements a custom UDP-based RDT protocol for reliable file transfer post-auction, so that the Seller buyer and auction winner can communicate and share files amongst themselves.
