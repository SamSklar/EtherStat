import numpy as np
import requests
import json
import argparse
from matplotlib import pyplot as plt


#This is my unique API token from etherscan.io
apiToken = "VR6U6BCJQJEQKZ1NQ6UCCY3MWDX9T6Q3EP"


"""This class represents a single ethereum account. It is initialized with an ethereum address 
and stores the balance, number of blocks mined, number of normal transactions, and number of internal transactions"""

class Account:


	"""Rather than instantiating all of the variables when the account is first instantiated, I set each value to 
	the sentinel value of -1. API calls are slow even at the relatively small magnitude I am working with so I rely 
	on lazy evaluation (only get the info when necessary) but make sure to store that data so it doesn't need to be
	queried again.
	"""
	def __init__(self, address):
		self.address = address
		self.numBlocksMined = -1
		self.numNormalTransactions = -1
		self.numInternalTransactions = -1
		self.balance = -1

	def getNumBlocksMined(self):
		if self.numBlocksMined == -1:
			blocksMinedRequest = "https://api.etherscan.io/api?module=account&action=getminedblocks&address="
			request = blocksMinedRequest + self.address + "&tag=latest&apikey=VR6U6BCJQJEQKZ1NQ6UCCY3MWDX9T6Q3EP"
			r = requests.get(request)
			result = json.loads(r.text)
			self.numBlocksMined = len(result["result"])
			return self.numBlocksMined
		else:
			return self.numBlocksMined

	def getNumNormalTransactions(self):
		if self.numNormalTransactions == -1:
			normalTransactionsRequest = "http://api.etherscan.io/api?module=account&action=txlist&address=" + self.address + "a&startblock=0&endblock=99999999&sort=asc&apikey=VR6U6BCJQJEQKZ1NQ6UCCY3MWDX9T6Q3EP"
			r = requests.get(normalTransactionsRequest)
			result = json.loads(r.text)
			self.numNormalTransactions = len(result["result"])
			return self.numNormalTransactions
		else:
			return self.numNormalTransactions


	def getNumInternalTransactions(self):
		if self.numInternalTransactions == -1:
			normalTransactionsRequest = "http://api.etherscan.io/api?module=account&action=txlistinternal&address=" + self.address + "&startblock=0&endblock=2702578&sort=asc&apikey=" + apiToken
			r = requests.get(normalTransactionsRequest)
			result = json.loads(r.text)
			self.numInternalTransactions = len(result["result"])
			print(result)
			return self.numInternalTransactions
		else:
			return self.numInternalTransactions

	def getBalance(self):
		if self.balance == -1:
			request = "https://api.etherscan.io/api?module=account&action=balance&address=" + self.address + "&tag=latest&apikey=" + apiToken
			r = requests.get(request)
			result = json.loads(r.text)
			self.balance = float(result["result"]) / 1000000000000000000
			return self.balance
		else:
			return self.balance


	def getTransactions(self):
		normalTransactionsRequest = "http://api.etherscan.io/api?module=account&action=txlist&address=" + self.address + "&startblock=0&endblock=99999999&sort=asc&apikey=VR6U6BCJQJEQKZ1NQ6UCCY3MWDX9T6Q3EP"
		r = requests.get(normalTransactionsRequest)
		query = json.loads(r.text)
		return query["result"]

	def getNTransactions(self, n):
		transactions = self.getTransactions()
		if (n > len(transactions)):
			n = len(transactions)
		all_data = transactions[1:n+1]
		result = []
		print(all_data)
		for x in range(n):
			result.append(all_data[x]["blockHash"])
		return result



