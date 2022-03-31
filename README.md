# solominer
Solo Mining in python for BTC Block Reward, Pure luck

This is a solominer random nonences between 0-4294967295 are checked to see if you could accidently solve the mining problem in 1 thread using Python and Get BTC Block Reward, this miner requests job from solockpool and start hashing the block header using random noncences, while a new block is detected on network, the miner restarts automatically in order to request new job from ckpool. 

It is based on Luck giving so much hashrate all around the world, but still possible.

The Script will display those hash having more than 7 zeros in the beginning. Although the current difficulty for getting mining reward is 17 zeros. All events is stored in a file called miner.log. 
Good Luck !!

You should replace the existing bitcoin adress in solo_miner.py with your own bitcoin address.

```
python solo_miner.py
[*] Bitcoin Miner Started

```
You can run it local on your pc or in aws instance, if you run it on aws for example you can setup a cronjob to run every 2-3 minutes in any case that miner stops to restart the miner. Good luck.
