from steemapi.steemclient import SteemClient
import time
import os
import json


class Config():
 # Port and host of the RPC-HTTP-Endpoint of the wallet
 wallet_host           = "127.0.0.1"
 wallet_port           = 8092
 # Websocket URL to the full node
 witness_url           = "ws://localhost:8090"

client = SteemClient(Config)

account = " "  # Account to track votes for
miners = [accont, " "] # Comma seperated list of miners and witnesses you want to track

print("<HTML><BODY style='background-color:lightgrey;'><table border='1' cellpadding='10'>")
print("<td valign='top' width = 225><b>Active Witnesses:</b><BR><BR>")

active_witnesses = client.rpc.get_active_witnesses()

witness_list = []

for witness in active_witnesses:

    w = client.rpc.get_witness(witness)
    w_vote_count = round((float(w["votes"])/1000000000000),1)

    witness_list.append(list([witness, w_vote_count]))

i=0

witness_list.sort(key=lambda tup: tup[1])
witness_list.reverse()

for w in witness_list:
 if witness_list[i][0] in miners:
   print("<table border='0'><td>{0:n}</td><td halign='left' width=125>{1:s}</td><td>{2:12,.0f}</td></table>".format(i+1, witness_list[i][0], witness_list[i][1]))
 else:
   print("<table border='0'><td halign='right' width=24>{0:n}</td><td halign='left' width=125>{1:s}</td><td>{2:12,.0f}</td></table>".format(i+1, witness_list[i][0], witness_list[i][1]))
 i = i + 1

print("</td><td valign='top' width=275><b>Miners and Witnesses:</b><BR><BR>")

miner_queue = client.rpc.get_miner_queue()
position = 1
all_steem = 0

for miner in miners:
  try:
    miner_info = client.rpc.get_account(miner)
    chain_info = client.rpc.info()
    witness_info = client.rpc.get_witness(miner)
    total_vesting_fund_steem = float(chain_info["total_vesting_fund_steem"][:-5])
    total_vesting_shares     = float(chain_info["total_vesting_shares"][:-5])
    balance                  = float(miner_info["vesting_shares"][:-5])
    total_balance            = round(((total_vesting_fund_steem / total_vesting_shares) * balance), 3)
    all_steem                = all_steem + total_balance
    print("<b>{0:s}</b> votes: {1:12,.0f} M<BR>".format(miner, round((float(witness_info["votes"])/1000000000000),1)))
    print("Last block signed: %s<BR>" % witness_info["last_confirmed_block_num"])
    print("Vests %s Missed: %s<BR><BR>" % (total_balance , witness_info["total_missed"]))
  except :
    print("<b>%s</b> has not been mined yet.<BR><BR>" % miner)

print("Total STEEM: %s" % round(all_steem, 3))

print("</td><td valign='top' width=150><b>Mining Queue:</b><BR><BR>")
position = 1
for m in miner_queue:
  if m in miners:
    print("<b>%d : %s</b><BR>" % ( position, m ))
    position = position + 1
  else:
    position = position + 1
print("</td>")

outvotes = {}
invotes = {}

stopsearch = False
startfrom = -1
limit = 1000
i = 1

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


 try:
   if transactions[0][0] == 0:
     stopsearch = True
   else:
     try:
       startfrom = transaction[0][0]
       if limit > startfrom:
         limit = startfrom
     except:
       stopsearch = True
 except:
   stopsearch = True
 i = i + 1

i=1
print("<td valign='top' width=150><b>You Support:</b><BR><BR>")
for k,v in sorted(outvotes.items()):
  if v[0] == True:
    print("%s. %s<BR>" % (i, k))
    i = i + 1

i=1
print("</td><td valign='top' width=150><b>Supports You:</b><BR><BR>")
for k,v in sorted(invotes.items()):
  if v[0] == True:
    print("%s. %s<BR>" % (i,k))
    i = i + 1

i=1
print("</td><td valign='top'><b>No Longer Supports You:</b><BR><BR>")
for k,v in sorted(invotes.items()):
  if v[0] == False:
    print("%s. %s<BR>" % (i,k))
    i = i + 1
print("</td></table></body></html>")
print("<BR>Head Block: %s <BR>"%chain_info["head_block_number"])
print("<meta http-equiv='Refresh' content='10'>")
