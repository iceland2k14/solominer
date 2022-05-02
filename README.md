# solominer
Solo Mining in python for BTC Block Reward, Pure luck

This is a solominer random noncences between 0-4294967295 or regular noncences starting from 0 are checked to see if you could accidently solve the mining problem using Python and Get BTC Block Reward, this miner requests job from solockpool and start hashing the block header using random noncences, or regular noncences, while a new block is detected on network, the miner restarts automatically in order to request new job from ckpool, if a nonce is found the blockheader data is submited to ckpool  automatically. 

It is based on Luck giving so much hashrate all around the world, but still possible.

The Script will store in miner.log file those hashes having more than 7 zeros in the beginning. Although the current difficulty for getting mining reward is 19 zeros. All events is stored in a file called miner.log. 

### You should replace the existing bitcoin adress in solo_miner.py with your own bitcoin address.



For local run in your pc 
``` python
# This will start the miner, with random nonceses 
python3 solo_miner.py
[*] Bitcoin Miner Started
# This will start the miner, with regular nonceses
python3 solo_miner.py 1
[*] Bitcoin Miner Started

```
If you want to run it aws instance or vps server 
``` pyton
# for random nonceses
nohup python3 solo_miner.py & 
# for regular nonceses
nohup python3 solo_miner.py 1 & 


```


## Tip
You can run it local on your pc or in aws instance, if you run it on aws for example you can setup a cronjob to run every 2-3 minutes in any case that miner stops to restart the miner. Good luck.
