import cfApi_sol
import csv
from time import sleep

def fich_input(fich_ier):
    fil = open(fich_ier, "r")
    lu = csv.reader(fil)
    n = 0
    fila = {}
    for row in lu:
        fila[n] = row
        n += 1
    fil.close()
    return fila

def extract_keys(fil_in_put,info):
    
    if info == 'market_serum':
        li = 0
    if info == 'secret_b58':
        li = 0
    if info == 'public_key_sol':
        li = 2
    if info == 'token_mint_wallet_bas':
        li = 3
    if info == 'token_mint_wallet_quo':
        li = 4
    line = fil_in_put[li][0]
    lon =len(line)
    ch = 0
    key = ''
    for i in range(lon):
        if ch == 1 and int(ord(line[i])) != 39:
            key = key + line[i]
        if int(ord(line[i])) == 39:
            if ch == 0:
                ch = 1
            else:
                ch = 0
    return key



market_serum = extract_keys(fich_input('info_market_wallet'),'market_serum')                      #address of market BTC-USDT
secret_b58 = extract_keys(fich_input('info_market_wallet'),'secret_b58')                        #secret key from sollet.io
public_key_sol = extract_keys(fich_input('info_market_wallet'),'public_key_sol')                  #wallet SOL
token_mint_wallet_bas = extract_keys(fich_input('info_market_wallet'),'token_mint_wallet_bas')    #wallet mint BTC
token_mint_wallet_quo = extract_keys(fich_input('info_market_wallet'),'token_mint_wallet_quo')    #wallet mint USDT

cfApisol = cfApi_sol.SolSerumClient(secret_b58=secret_b58,market_address=market_serum, owner_wallet=public_key_sol,\
                                token_mint_wallet_bas=token_mint_wallet_bas, token_mint_wallet_quo=token_mint_wallet_quo)


print(cfApisol.check_pub_key())


#try to send an order (place on purpose an order couldn't be fill)

cfApisol.ex_ordre_serum('buy',0.0005,12000)
input('order sent')
sleep(20)

#after waiting a little to be sure the order is in the orderbook,
#try to cancel it

cfApisol.cancel_serum()
input('order cancelled')
sleep(20)

#after the cancelling, it waits a little to be sure it was cancelled
#then it try to settle the wallet (enter here the approximate amount
#and the limite price of the precedent order), it'll check that was 
#realised after multiple try, since the amount appear in the wallet.

cfApisol.settl_withCheck_done(0.0005,12000)
print('wallet settled')

