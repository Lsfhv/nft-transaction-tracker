# NFT Transaction Tracker

A service to collect nft trades on Blur, Opensea and Magic Eden. 

# How To Use 

Set your infura key as a path variable with name `INFURAAPIKEY`

Set up mongodb. In `src/constants` change the ip and port to those which mongodb is listening on. 

Run `python3 main.py` in the root

Run `python3 -m unittest discover test` in the root to run all the tests. 