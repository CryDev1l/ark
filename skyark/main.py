import os
import time
import json
import random
from config import *
from web3 import Web3
from loguru import logger

def load_abi(name):
    try:
        path = f"{os.path.dirname(os.path.abspath(__file__))}/abis/"
        with open(os.path.abspath(path + f"{name}.abi")) as f:
            abi: str = json.load(f)
        return abi
    except Exception as error:
        logger.error(error)

def task(private_key, task_number, task_name):
    if task_name == 'Dispatch_Squad':
        token_contract = Web3.toChecksumAddress("0x9465fe0e8cdf4e425e0c59b7caeccc1777dc6695")
        contract = web3.eth.contract(address=token_contract, abi=load_abi('Dispatch_Squad'))
    else:
        token_contract = Web3.toChecksumAddress("0xd42126d46813472f83104811533c03c807e65435")
        contract = web3.eth.contract(address=token_contract, abi=load_abi('exploration'))
    nonce = web3.eth.get_transaction_count(address_wallet)
    gasLimit = 200000
    contract_txn = contract.functions.signin(
        task_number
    ).buildTransaction({
        'from': address_wallet,
        'value': 0,
        'gas': gasLimit,
        'maxFeePerGas': web3.eth.gas_price,
        'maxPriorityFeePerGas': web3.eth.max_priority_fee,
        'nonce': nonce,
    })
    gasLimit = web3.eth.estimate_gas(contract_txn)
    contract_txn['gas'] = gasLimit
    signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.info(f"https://opbnbscan.com/tx/{web3.toHex(tx_hash)}'")


if __name__ == "__main__":
    try:
        with open("private_keys.txt", "r") as f:
            private_keys = [row.strip() for row in f]
        RPC = "https://opbnb.publicnode.com"
        web3 = Web3(Web3.HTTPProvider(RPC))
        while working_days > 0:
            for private_key in private_keys:
                account = web3.eth.account.privateKeyToAccount(private_key)
                address_wallet = account.address
                logger.info(f'Выполняю задание для {address_wallet}:')
                for i in range(0, iter_number):
                    task_name = 'Exploration'
                    task(private_key, 1, task_name)
                    time.sleep(random.randint(15, 30))
                    task_name = 'Dispatch_Squad'
                    task(private_key, 1, task_name)
                    time.sleep(random.randint(15, 30))
                    task(private_key, 2, task_name)
                    time.sleep(random.randint(15, 30))
                logger.info(f'Сегодняшние задания успешно выполнены!')
                working_days -= 1
                time.sleep(60*60*24)  # ждем сутки
        logger.info(f'Все задания успешно выполнены!')
    except Exception as e:
        logger.error(e)
