from random import randint
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account import Account
import secrets

'''
made by gensx-x1
git: https://github.com/gensx-x1
tg: @gensx1
'''


def generatePair():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return acct.address, acct.key.hex()


def generateWallets(n):
    wal = list()
    for x in range(0, n):
        addr, pKey = generatePair()
        wal.append((addr, pKey))
    return wal


def dist(walletsList, amount_):
    for x in walletsList:
        wal = w3.to_checksum_address(x[0])
        pKey = x[1]
        _amount = w3.to_wei(amount_, 'ether')
        transaction = {'to': wal,
                       'value': _amount,
                       'gas': 21000,
                       'gasPrice': 0,
                       'nonce': w3.eth.get_transaction_count(vault),
                       'chainId': 56}
        txnHash = w3.eth.account.sign_transaction(transaction, vaultKey)
        sendTxn = w3.eth.send_raw_transaction(txnHash.rawTransaction)
        check = w3.eth.wait_for_transaction_receipt(sendTxn.hex())
        print(f'dist done {walletsList.index(x)}', end='\r')
        balance = w3.eth.get_balance(wal)
        print(f'{x[0]} balance: {w3.from_wei(balance, "ether")}')
    print('dist done\n')


def placeBets(walletsList):
    for x in walletsList:
        print('------------------------------------')
        wal = w3.to_checksum_address(x[0])
        pKey = x[1]
        betAmount = randint(0, w3.eth.get_balance(wal)*0.8)
        betSide = randint(1, 2)
        print(f'from: {wal}\n'
              f'betting: {round(w3.from_wei(betAmount, "ether"), 6)}\n'
              f'side: {betSide} (1 = Musk , 2 = Zuckerberg)')
        transaction = {'value': betAmount,
                       'gas': 2100000,
                       'gasPrice': 0,
                       'nonce': w3.eth.get_transaction_count(wal),
                       'chainId': 56}
        betTxn = betContract.functions.placeBet(betSide).build_transaction(transaction)
        betTxn_signed = w3.eth.account.sign_transaction(betTxn, private_key=pKey)
        betTxn_transaction = w3.eth.send_raw_transaction(betTxn_signed.rawTransaction)
        print(f'txn sent')
    print('Done placing bets\n')

def withdrawBet(walletsList):
    for x in walletsList:
        wal = w3.to_checksum_address(x[0])
        pKey = x[1]
        transaction = {'gas': 2100000,
                       'gasPrice': 0,
                       'nonce': w3.eth.get_transaction_count(wal),
                       'chainId': 56}
        betTxn = betContract.functions.withdrawBet().build_transaction(transaction)
        betTxn_signed = w3.eth.account.sign_transaction(betTxn, private_key=pKey)
        betTxn_transaction = w3.eth.send_raw_transaction(betTxn_signed.rawTransaction)
        print(f'withdraw done {walletsList.index(x)}', end='\r')


def checkWin(walletsList):
    for x in walletsList:
        wal = w3.to_checksum_address(x[0])
        pKey = x[1]
        transaction = {'gas': 2100000,
                       'gasPrice': 0,
                       'nonce': w3.eth.get_transaction_count(wal),
                       'chainId': 56}
        checkTxn = betContract.functions.claim().build_transaction(transaction)
        checkTxn_signed = w3.eth.account.sign_transaction(checkTxn, private_key=pKey)
        checkTxn_transaction = w3.eth.send_raw_transaction(checkTxn_signed.rawTransaction)
        checkTxn_check = w3.eth.wait_for_transaction_receipt(checkTxn_transaction.hex())
        if checkTxn_check['status'] == 0:
            print('fail on claim')
        print(f'check done {walletsList.index(x)}', end='\r')


def loadSettings():
    settingsFile = open('settings', 'r').readlines()
    _rpcUrl = settingsFile[30].strip('\n').split('=')[1]
    _vault = settingsFile[31].strip('\n').split('=')[1]
    _vaultKey = settingsFile[32].strip('\n').split('=')[1]
    _contract = settingsFile[33].strip('\n').split('=')[1]
    for x in range(1, 21):
        print(settingsFile[x].strip('\n'))
    print(settingsFile[23].strip('\n'))
    return _rpcUrl, _vault, _vaultKey, _contract

print(f'loading settings file')
(rpcUrl, vault, vaultKey, betContract_address) = loadSettings()


w3 = Web3(HTTPProvider(rpcUrl))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

betContract_abi = open('abi', 'r').read()
betContract = w3.eth.contract(address=betContract_address, abi=betContract_abi)

while True:

    print(f'Vault balance:{w3.from_wei(w3.eth.get_balance(vault), "ether")}\n'
          'Choose option:\n'
          '[1] Make new wallets and distrubute funds\n'
          '[2] Place Bets only\n'
          '[3] Withdraw Bets only\n'
          '[4] Check wins only\n'
          '[5] New contract address\n'
          '[6] Quick tests scenarios\n')
    opt = input('>>')
    try:
        opt = int(opt)
    except:
        continue
    if opt == 1:
        wallets = generateWallets(int(input('How many wallets>> ')))
        amount = int(input('How much funds>> '))
        dist(wallets, amount)
    if opt == 2:
        placeBets(wallets)
    if opt == 3:
        withdrawBet(wallets)
    if opt == 4:
        checkWin(wallets)
    if opt == 5:
        betContract_address = input('contract address>> ')
    if opt == 6:
        print('Quick tests:\n'
              '[1] -Make new wallets (10)\n'
              '    -Distribution (10bnb)\n'
              '    -Place bets\n'
              '    -Withdraw bets\n\n'
              '[2] \n')
        opt = int(input('>>'))
        if opt == 1:
            wallets = generateWallets(10)
            dist(wallets, 10)
            placeBets(wallets)
            withdrawBet(wallets)



