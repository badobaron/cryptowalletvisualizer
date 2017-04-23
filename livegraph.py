import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import requests 

#TODO: set figure size larger, axes bigger, better spacing, changing x intervals
#TODO: port to js (hopefully some easier more powerful graphing libraries)

#font size larger, window needs to be rescaled with cursor once started
font_prop = font_manager.FontProperties(size=20)

# get json from coin market cap for top 3 most capitalized currencies
# 1) xbt
# 2) eth
# 3) xrp
url = 'https://api.coinmarketcap.com/v1/ticker/?convert=USD&limit=3'

# (not very important for now) todo: pull these value directly from kraken wallet
amt_xbt = 0.00330
amt_xrp = 600

plt.axis([0, 1000, 21, 25], FontProperties=font_prop)
plt.title('Live Wallet USD Value', FontProperties=font_prop)
plt.xlabel('Time (5 sec intervals)', FontProperties=font_prop)
plt.ylabel('Total $USD Value of Crypto Wallet', FontProperties=font_prop)
plt.ion()

for i in range(1000):
	#pull response
	response = requests.get(url)
	data = response.json()

	#find dollar value of the bitcoins
	usd_xbt = float(data[0]['price_usd']) * amt_xbt;
	usd_xrp = float(data[2]['price_usd']) * amt_xrp;

	#total dollar value
	y = usd_xbt + usd_xrp;

	#set old for first time
	if i==0:
		usd_xbt_old = usd_xbt
		usd_xrp_old = usd_xrp
		y_old = y
		net = 0.0
		net_xbt = 0.0
		net_xrp = 0.0


	# check for increase or decrease
	if y != y_old:
		net = y-y_old
		y_old = y

	if usd_xbt != usd_xbt_old:
		net_xbt = usd_xbt-usd_xbt_old
		usd_xbt_old = usd_xbt

	if usd_xrp != usd_xrp_old:
		net_xrp = usd_xrp-usd_xrp_old
		usd_xrp_old = usd_xrp

	#display the live labels
	tvar1 = plt.text(1, 24.8, 'USD from XBT: $'+str(usd_xbt)+'   ('+('-' if (-1 if net_xbt < 0 else 1) < 0 else '+')+'$'+str(abs(net_xbt))+')', FontProperties=font_prop)
	tvar2 = plt.text(1, 24.6, 'USD from XRP: $'+str(usd_xrp)+'   ('+('-' if (-1 if net_xrp < 0 else 1) < 0 else '+')+'$'+str(abs(net_xrp))+')', FontProperties=font_prop)
	tvar3 = plt.text(1, 24.4, 'USD total: $'+str(y)+'   ('+('-' if (-1 if net < 0 else 1) < 0 else '+')+'$'+str(abs(net))+')', FontProperties=font_prop)

	#y = np.random.random()
	plt.plot(i, y, marker='o', linestyle='--', color='b')
	plt.pause(5) #pause 5 seconds until next fetch

	#clear live labels before setting them again
	tvar1.remove()
	tvar2.remove()
	tvar3.remove()

while True:
    plt.pause(0.05)

