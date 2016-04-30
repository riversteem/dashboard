# dashboard

**Based on the "show who's voting for me" script written by "pharesim". Please vote for his witness!**

http://steemd.com/@pharesim


Run:
-----------

Adjust monitor.sh to suit your environment.

Requires Xeroc's STEEM libraries: https://github.com/xeroc/python-steemlib

Todo list:
- Move parameters to a .json file
- Implement each category as a function that can be turned on and off
- ~~Sort votes so the list order remains constant~~
- Sort Witness lists so the order is ranked by votes
- Include standby witnesses in list and make list numbered
- Add email notifications for missed blocks by tracked witness
- Telegram integration

Known Bugs:
- Crash reported on account with greater than 1000 transactions (dele-puppy)
