# simpleClient-for-pyserum
simple trading client for pyserum

This is a simple client to trade on the serum DEX.

It allow you to make some of the solana request easily through the pyserum librairy:

- send order
- cancel order
- settle wallet


And the test file is an example how to use it,

in the examples we try to send an order (place on purpose an order couldn't be fill)
after waiting a little to be sure the order is in the orderbook. We try to cancel it
and after the cancelling, it waits a little to be sure it was cancelled.
Then it try to settle the wallet 
'''cfApisol.settl_withCheck_done(amount,price)'''
(enter the approximate amount and the limite price of the precedent order), it'll check 
that was realised after multiple try, since the amount appear in the wallet.
