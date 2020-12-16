# simpleClient-for-pyserum
simple trading client for pyserum

This is a simple client to trade on the serum DEX.

It allows you to make some of the solana request easily through the pyserum librairy:

- send order
- cancel order
- settle wallet

Insert in the info_market_wallet file the following informations:


market_serum =    ''              between the quote insert the address of the market

secret_b58 =    ''                  between the quote insert the secret key of your wallet you'll find in the sollet.io wallet

public_key_sol =  ''            between the quote insert the public key of your wallet

token_mint_wallet_bas =  ''     between the quote insert the base token recipient address of your wallet

token_mint_wallet_quo =  ''      between the quote insert the quote token recipient address of your wallet



And the test file is an example how to use the client,

in the example we make an order to send it (place on purpose an order couldn't be filled).
After waiting a little to be sure the order is in the orderbook, we try to cancel it
and after the cancelling, it waits a little to be sure it was cancelled.
Then it try to settle the wallet

"cfApisol.settl_withCheck_done(amount,price)"

(enter the approximate amount and the limite price of the precedent order), it'll check 
that was released after multiple tries, since the amount appears in the wallet.
