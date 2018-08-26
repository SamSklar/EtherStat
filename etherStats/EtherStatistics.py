import numpy as np
import requests
import json
import argparse
import csv
import random
from matplotlib import pyplot as plt
from Account import Account

#Query for current ether supply (requires my api token) 
#result returned in Wei so divide by 1000000000000000000
etherSupply = "https://api.etherscan.io/api?module=stats&action=ethsupply&apikey="

#Query for last update ether price (requires my api token)
etherPrice = "https://api.etherscan.io/api?module=stats&action=ethprice&apikey="

#My api token generated on etherscan.
apiToken = "VR6U6BCJQJEQKZ1NQ6UCCY3MWDX9T6Q3EP"

#Query for ether balance at a specific address (requires address and api key)
accountBalance = "https://api.etherscan.io/api?module=account&action=balance&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a&tag=latest&apikey=VR6U6BCJQJEQKZ1NQ6UCCY3MWDX9T6Q3EP"

#list of selected random addresses
ethDataSubset = []

#list of ethereum account objects
ethAccounts = []

#combined addresses and account values
ethData = []

#Users Ethereum Address, set to sentinel initially
userAddress = "SENTINEL"

#list of all valid commands
commandList = ["Commands", "Ether Supply", "Ether Price", "Current Market Cap", "My Address", "Address Balance Stats"]

def main():

	parser = argparse.ArgumentParser(description='Takes in specified number of IID Ethereum addresses and returns associated statistics.')
	parser.add_argument('numAddresses', metavar='N', type=int, help='specify the number of IID Ethereum addresses, must be between 1 and 500')

	#list of all addresses
	ethAddresses = []
	#Populate the ethAddresses with the subset of 820 random addresses taken from ethernet
	with open("/Users/samsklar/Desktop/etherStats/ether_address.csv") as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		for row in csvReader:
			ethAddresses.append(row[0])
	ethAddresses.pop(0)


	#list of all balances
	accountBalances = []
	with open("/Users/samsklar/Desktop/etherStats/balanceAmounts.csv") as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		for row in csvReader:
			accountBalances.append(float(row[0]))
	global ethData
	ethData = zip(ethAddresses, accountBalances)

	#Get the numAddresses argument that was passed in and generate a random subset of that size
	args = parser.parse_args()
	numAddresses = max(min(args.numAddresses, 500), 1)
	generateSubset(numAddresses)
	generateAccountList()


	print("Welcome to ether stats! This interface will allow you to do data analysis on ethereum addresses. At any time, hit ENTER to break or type \"Commands\" for a list of commands.")

	while(True):
		command = raw_input("Please input a command: ")
		if(command == ""): break
		interperateCommand(command)

	print("Thanks for using ether stats!")
	

def test():
	curr = Account("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae")
	print("testing balance")
	print(curr.getBalance())
	print("testing n addresses...")
	print(curr.getNTransactions(3))

def printCurrPrice():
	r = requests.get(etherPrice + apiToken)
	result = json.loads(r.text)
	print("The current price of a single coin in USD is: " + result["result"]["ethusd"])


def printCurrTotalSupply():
	r = requests.get(etherSupply + apiToken)
	result = json.loads(r.text)
	print("The current total number of ether coins is: " + str(float(result["result"]) / 1000000000000000000))

def printCurrMarketCap():
	r = requests.get(etherSupply + apiToken)
	result = json.loads(r.text)
	currSupply = float(result["result"]) / 1000000000000000000

	r = requests.get(etherPrice + apiToken)
	result = json.loads(r.text)
	currPrice = float(result["result"]["ethusd"])

	print("The total current market cap in USD is: " + str(currSupply * currPrice))


def printBalanceAddressStats():
	balances = [x[1] for x in ethDataSubset]
	print("The sample mean is: " + str(np.mean(balances)))
	print("The sample variance is: " + str(np.var(balances)))

	fig, (ax1, ax2) = plt.subplots(nrows=2)

	ax1.hist(balances)
	ax1.set_title('Histogram')

	ax2.plot(balances)
	ax2.set_title('Raw Plot')

	plt.show(block=True)


def generateSubset(size):
	indices = random.sample(xrange(len(ethData)), size)
	for x in indices:
		ethDataSubset.append(ethData[x])

def getBalanceList():
	balances = []
	for account in ethAccounts:
		balances.append(float(account.getBalance()))
	return balances

def getNumNormalTransactionsList():
	transactions = []
	for account in ethAccounts:
		transactions.append(account.getNumNormalTransactions())
	print(transactions)
	return transactions

def generateAccountList():
	for address in ethDataSubset:
		curr = Account(address[0])
		ethAccounts.append(curr)

def printUserAddressStats():
	global userAddress
	if userAddress == "SENTINEL":
		command = raw_input("Please enter your ethereum address: ")
		userAddress = command
	
	userAccount = Account(userAddress)

	print("Your current balance is: " + str(userAccount.getBalance()))

	print("Your total number of blocks mined is: " + str(userAccount.getNumBlocksMined()))

	print("Your total number of transactions is: " + str(userAccount.getNumNormalTransactions()))



def printIntructionList():
	print("The command Ether Supply will yield the current total number of tokens available.\n")
	print("The command Ether Price will yield the current price of one ether token in USD.\n")
	print("The command Current Market Cap will yield the total USD value of all outstanding coins.\n")
	print("The command My Address will give you stats on your ethereum wallet!\n")
	print("The command Address Balance Stats will do a statistical analysis of your random subset of addresses.\n")

def get20Balances(adds):
	request = "https://api.etherscan.io/api?module=account&action=balancemulti&address="
	for add in adds:
		request = request + add + ","
	request = request[:-1]
	request = request + "&tag=latest&apikey=" + apiToken
	r = requests.get(request)
	result = json.loads(r.text)
	output = []
	for x in result["result"]:
		output.append(float(x["balance"]) / 1000000000000000000)
	return output

def interperateCommand(command):
	if command not in commandList: 
		print("invalid command")

	if command == "Ether Price":
		printCurrPrice()
	elif command == "Ether Supply":
		printCurrTotalSupply()
	elif command == "Commands":
		printIntructionList()
	elif command == "Address Balance Stats":
		printBalanceAddressStats()
	elif command == "Current Market Cap":
		printCurrMarketCap()
	elif command == "My Address":
		printUserAddressStats()
	elif command == "test":
		test()





if __name__ == "__main__":
	main()
