from solana.account import Account
from solana.publickey import PublicKey
from spl.token.client import Token
from solana.rpc.types import TxOpts
from solana.rpc import api
from spl.token.constants import TOKEN_PROGRAM_ID
from pyserum.market import Market
from pyserum.market import State
from pyserum.enums import OrderType, Side
from pyserum.open_orders_account import OpenOrdersAccount
from pyserum.connection import conn, get_live_markets, get_token_mints
from time import sleep
import binascii, hashlib
import base58
import json
import sys



class SolSerumClient:
    
    def __init__(self,secret_b58=None, market_address=None, owner_wallet=None, token_mint_wallet_bas=None, token_mint_wallet_quo=None) -> None:
        base_url = 'https://api.mainnet-beta.solana.com/'
        self._cc = conn(base_url)
        self._market = Market.load(conn(base_url), PublicKey(market_address))
        self._payer = Account(base58.b58decode(secret_b58)[:32])
        self._owner_wallet = owner_wallet
        self._token_mint_wallet_bas = token_mint_wallet_bas
        self._token_mint_wallet_quo = token_mint_wallet_quo
    
    def check_pub_key(self):
        pub_k = self._payer.public_key()
        if str(pub_k) == str(self._owner_wallet):
            print('exact pub_k')
            return 1
        else:
            print('false pub_k')
            return 0
    
    def ex_ordre_serum(self,sens,qte,pri):
        
        pri = int(float(pri)*10)    #pri en quote  (token_mint_wallet_quo)
        qte = int(float(qte)*10000) #qte de la base(token_mint_wallet_bas)
        
        if sens == 'buy':
            quote_wallet = self._token_mint_wallet_quo
            sens = Side.Buy
        elif sens == 'sell':
            quote_wallet = self._token_mint_wallet_bas
            sens = Side.Sell
        else:
            return
        
        print(quote_wallet,sens,pri,qte)
        try:
            tx_sig = self._market.place_order(payer = quote_wallet,
                                        owner = self._payer,
                                        side = sens,
                                        order_type = OrderType.Limit,
                                        limit_price = pri,              # price divided per 10 for BTC ex 193750 pour 19375,0
                                        max_quantity = qte,             # quantity divided per 10000 for BTC ex 1 pour 0.0001 (mini 1)
                                        opts = TxOpts()
                                        )
            print(tx_sig)
            return tx_sig['result']
        except:
            print('transaction argument error (probably amount non-conforme)')
    
    def cancel_serum(self):
        try:
            canc = self._market.cancel_order(owner=self._payer,
                                       order=self._market.load_orders_for_owner(self._owner_wallet)[0]
                                       )
            print(canc)
            return canc['result']
        except:
            print('no order to cancel')
    
    def settl_wal_serum(self):
        settl = None
        try:
            open_orders_account = self._market.find_open_orders_accounts_for_owner(owner_address=PublicKey(self._owner_wallet))
            settl = self._market.settle_funds(owner=self._payer,
                                        open_orders=open_orders_account[0],
                                        base_wallet=self._token_mint_wallet_bas,
                                        quote_wallet=self._token_mint_wallet_quo
                                        )
            print(settl)
            return 0, settl
        except:
            print('no amount to settle')
            return 1, settl
    
    def settl_withCheck_done(self,qte_ord,pri):
        val_av = val_ap = float(self.val_wallet(pri))
        val_ord = float(qte_ord)*float(pri)
        sett_noNeed = 0
        print(val_av,val_ap,val_ord,sett_noNeed)
        nb_set = 0
        
        settl = None
        while val_ap - val_av < (val_ord/2) and int(sett_noNeed) == 0 and nb_set < 4:
            nb_set += 1
            sett_noNeed, settl = self.settl_wal_serum()
            sleep(20)
            val_ap = float(self.val_wallet(pri))
            print(val_av,val_ap,val_ord)
        
        if settl == None:
            return settl
        return settl['result']
    
    def val_wallet(self,pri):
        qte_bas_av = float(self.requ_qte_tok(self._token_mint_wallet_bas,tok_wall=1))*float(pri)
        qte_quo_av = float(self.requ_qte_tok(self._token_mint_wallet_quo,tok_wall=1))
        return qte_bas_av + qte_quo_av
    
    def requ_qte_tok(self,tok,tok_wall=0):
        if tok_wall == 0:
            if tok == 'BTC':
                tok = self._token_mint_wallet_bas
            else:
                tok = self._token_mint_wallet_quo
        return self._cc.get_token_account_balance(tok)['result']['value']['uiAmount']

