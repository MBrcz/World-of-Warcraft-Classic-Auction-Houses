-------------------------------------
Date: 02.01.2024
-------------------------------------

World of Warcraft Classic Auction Houses
!PROJECT IS STILL IN DEVELOPMENT!

	The idea of this project is to utilise the open sourced Blizzard Entertainment World of Warcraft (WoW) related game API (Application Programming Interface) to get the data about the state of auctions.

	Auction is a ingame mechanism that allows players to trade some items (non "souldbound") for ingame currency. In the project there is downloaded data about servers from 4 different worlds (United States, Europe, Korea, Taiwan). Chinease servers are removed from analyssis due to the "Netase drama" see more: https://investor.activision.com/news-releases/news-release-details/blizzard-entertainment-and-netease-suspending-game-services. In blizzard API there are 2 types of data user can get, dynamic and static.

Dynamic data is the one that is changing with time are:
	a) list of realms / servers,
	b) list of items on noted on auctions,
Static data is the one which tends to be constant in expansion like:
	a) list of all items,
	b) icons of items,
	c) items classes and subclasses.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
HOW TO GET A DATA?
	The procedure of pulling data is a python Command Line Application. In order to get it run, user needs to get unique client ID and secret password (see more: https://develop.battle.net/documentation/guides/getting-started). Those parameters shall be passed to ~/dataClasses/Scrapper/py - object Scrapper.py class attributes: _CLIENT_ID and _CLIENT_SECRET. Next one has to reinstanciate venv via cmd (Python 3.11) required via commands:
	cd {RootProjectDir} && /{FirstLetterOfDiscName} && rmdir "venv" /S /Q && python.exe -m venv venv && venv\scripts\activate && pip install -r requirements.txt
	After while one can start typing commands using "call.py" prefix.
	List of available commands:
		servers             Gets the name of all valid realms and servers and creates the table out of them.
   		items               Downloads the basic information about items that are in the auction house.
    		auctions            Downloads the items from the auction houses.
    		items_classes       Downloads the data about the classes of the items from the Item.csv file.
    		items_media         Downloads the data about the url to the items icons. Use after check_auction command!
    		check_auction_items Tests whether the items stored in auction are in the file containing list of items.
    		mk_dead_servers     Marks dead servers from the auction file and realms.csv files.Dead servers are considered the one that have less that 1000 transactions in total on Auction.
    		rm_sus_trans        Removes the suspiscius transactions (outliners) from Auction.csv.
    		all  Uses all methods that are above. This will last like dozens of minutes.

	For instance, typing: "call.py servers" will result in a table that gets name of all servers and realms.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
DATA SET.
	Data for the project is mostly taken from above Command Line Application. One can find it in directory: ~/Scrapper/Data/DownloadsFromAPI/* . Some of the files are made by hand, like AuctionNames.csv.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Report.
	Report is currently durning construction. In a directory ~/Report one can find .pbix and .pdf which presents the current state of report (for day 02.01.2024).
	To be continued...
	
	Used technologies:
		a) Power Query,
		b) DAX,
		c) Python (bs4 and pandas).