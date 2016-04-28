from steemapi.steemclient import SteemClient
import time
import os

class Config():
 # Port and host of the RPC-HTTP-Endpoint of the wallet
 wallet_host           = "127.0.0.1"
 wallet_port           = 8091
 # Websocket URL to the full node
 witness_url           = "ws://localhost:8090"

client = SteemClient(Config)

account = "riverhead"
miners = ["riverhead","riverhead2","riverhead3","riverhead4","riverhead5","mecon"]
#os.system('clear')
print("<HTML><BODY style='backgroup-color:lightgrey;'><table border='1' cellpadding='10'>")
print("<td valign='top' ><b>Active Witnesses:</b><BR><BR>")


active_witnesses = client.rpc.get_active_witnesses()
for witness in active_witnesses:
  if witness == account or witness[:-1] == account or witness == "mecon":
    print("<b>%s</b><BR>"% witness)
  else:
    print("%s<BR>" % witness)

print("</td><td valign='top'><b>Miners and Witnesses:</b><BR><BR>")

miner_queue = client.rpc.get_miner_queue()
position = 1
all_steem = 0

for miner in miners:
  miner_info = client.rpc.get_account(miner)
  chain_info = client.rpc.info()
  witness_info = client.rpc.get_witness(miner)
  total_vesting_fund_steem = float(chain_info["total_vesting_fund_steem"][:-5])
  total_vesting_shares     = float(chain_info["total_vesting_shares"][:-5])
  balance                  = float(miner_info["vesting_shares"][:-5])
  total_balance            = round(((total_vesting_fund_steem / total_vesting_shares) * balance), 3)
  all_steem                = all_steem + total_balance
  print("%s votes: %s<BR>" % (miner, witness_info["votes"]))
  print("Last block signed: %s<BR>" % witness_info["last_confirmed_block_num"])
  print("%s | %s | %s<br><BR>" % (total_balance , miner_info["balance"], miner_info["sbd_balance"]))

print("Head Block: %s <BR>"%chain_info["head_block_number"])
print("Total STEEM: %s\n" % all_steem)

print("</td><td valign='top' width=200><b>Mining Queue:</b><BR><BR>")
for miner in miner_queue:
  if miner == account or miner == 'mecon' or miner[:-1] == account:
    print("%d : %s<BR>\n" % (position, miner ))
  else:
    position = position + 1
print("</td>")

outvotes = {}
invotes = {}

stopsearch = False
startfrom = -1
limit = 1000
i = 1
#os.system('clear')
while stopsearch == False:
 transactions = client.rpc.get_account_history(account,startfrom,limit)
 for transaction in transactions:
   if transaction[1]['op'][0] == 'account_witness_vote':
     vote = transaction[1]['op'][1]
     set = False
     if vote['account'] == account:
       try:
         if outvotes[vote['witness']][1] == i:
           set = True
       except KeyError:
         set = True

       if set == True:
         outvotes[vote['witness']] = [vote['approve'],i]

     else:
       try:
         if invotes[vote['account']][1] == i:
           set = True
       except KeyError:
         set = True

       if set == True:
         invotes[vote['account']] = [vote['approve'],i]


 if transactions[0][0] == 0:
   stopsearch = True
 else:
   startfrom = transaction[0][0]
   if limit > startfrom:
     limit = startfrom
 i = i + 1

i=1
print("<td valign='top'><b>You Vote For:</b><BR><BR>")
for k,v in outvotes.items():
  print("%s. %s %s<BR>" % (i, k))
  i = i + 1

i=1
print("</td><td valign='top'><b>Votes For You:</b><BR><BR>")
for k,v in invotes.items():
  if v[0] == True:
    print("%s. %s<BR>" % (i,k))
    i = i + 1

i=1
print("</td><td valign='top'><b>No Longer Support You:</b><BR><BR>")
for k,v in invotes.items():
  if v[0] == False:
    print("%s. %s<BR>" % (i,k))
    i = i + 1
print("<meta http-equiv='Refresh' content='10'>")
