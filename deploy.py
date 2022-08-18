from brownie import Contract
from solcx import compile_standard,  install_solc
# solc is compiler.
import json, os
from web3 import Web3
from dotenv import load_dotenv

# looks for .env and loads it automatically
load_dotenv()  

# to deploy on blockchain, we first compile the code in python
# we get metadata; bytecode and abi
# use ganache to simulate a blockchain
# to connect to ganache we use http/rpc provider
# just like metamask connects directly to blockchain, we will use http in ganache to connect
# we use chainId, http, wallet addresses
# create contract
# w3.eth.contract(abi = abi, bytecode = bytecode)
# GET nonce 
# build a transaction
# sign a transaction
# send transaction 


with open("./simplestorage.sol") as file:
    simple_storage_file = file.read()
    #print (simple_storage_file)
install_solc("0.6.0")

# COMPILED OUR SOLIDITY.

# we compiled solidity code from simplestorage.sol, and we saved metadata 
compiled_sol = compile_standard (
    {
        "language": "Solidity",
        "sources":{"simplestorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*":{"*":["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }

            }
        },
    },
    solc_version="0.6.0",
)

# print (compiled_sol)

# will open compiled_code and dump compiled_sol in it 
with open ("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["simplestorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get ABI
abi = compiled_sol["contracts"]["simplestorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache, first we need http of the node
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/d73477856a614d759d97fd036400f101"))

# next we need chainID, networkID
chain_id = 4
my_address = "0xfEF88f0b6D464534060B3C5EE57810741805ac18"
#use environment varialble to hide private key
private_key = os.getenv("PRIVATE_KEY")


# NOW DEPLOY, create contract IN python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)


# get nonce, nonce is also usually the number of transaction 
# it took for a specific transaction to go through
nonce = w3.eth.get_transaction_count(my_address)
 
# build a transaction
# sign a transaction
# send transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id,"from": my_address, "nonce":nonce })

signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
print ("deploying contract...")
# print (transaction)
# sending signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
ContractAddress = tx_receipt.contractAddress
print ("contract deployed!!!")
#block = w3.eth.get_block('latest')
print ("tx_hash of contract: ",ContractAddress, "is: ", tx_hash.hex())


# working with contract requirements
# contract address
# contract ABI

# contract deployed above, so now we work with it by creating a contract object
# Call -> simulate a call and only get return value
# Transact -> make a state chain on the blockchain

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# print(simple_storage.functions.retrieve().call()) 
# print (simple_storage.functions.store(14).call())

print ("\nUpdating Contract...")
# making a transaction on contract
# get a new nonce as it can ONLY BE USED ONCE per contract
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id,"from": my_address, "nonce":nonce +1}
)

#signing 
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
    )
send_stored_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
print ("the tx_hash of this transaction is: ", send_stored_tx_hash.hex(), " on contract:", ContractAddress )
tx_receipt = w3.eth.wait_for_transaction_receipt(send_stored_tx_hash)
print ("Contract Updated!!!")



