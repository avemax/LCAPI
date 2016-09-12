# LCAPI  :tophat: - from this [blog](http://joeywhelan.blogspot.com/2015/11/lendingclub-rest-api-access-with-python.html) <sup>1</sup>



![diagram](http://3.bp.blogspot.com/-HSuZ3_G65FY/VlZUpbGhqcI/AAAAAAAABGQ/1C53dKLWaOM/s1600/figure1.jpg)

#https://github.com/joeywhelan/lcInvestor



1: http://joeywhelan.blogspot.com/2015/11/lendingclub-rest-api-access-with-python.html
2: https://github.com/joeywhelan/lcInvestor/blob/master/lcInvestor.py
3: [LCAPI reference](https://www.lendingclub.com/developers/add-funds.action)

# Summary
LendingClub is one of the peer-to-peer lenders out there.  They provide a REST API for simple account transactions such as querying account data, available loans, and submitting loan orders.  In this article, I'll be discussing the development of a simple auto-investment tool I wrote in Python with the Lending Club API.  The application reads a user-configurable file for options and then if funds are available and loans exist that meet the user's criteria, orders are placed with LendingClub for those loans.  The application was designed to be run out of a cron script to periodically check funds + loans and place orders accordingly.

I have an additional set of articles discussing integration of machine learning techniques with this API here.

# Preparation
Obviously, Step 1 is to establish an account at LendingClub.  After that, you can make a request for access to the REST API.  There are two critical pieces of info you'll need execute any API calls:  the Account ID and an Authorization Key.  LendingClub uses the auth key method for securing access to their API.  As will be discussed later, the auth key will be passed as a HTTP header item for any API call.

Application Organization
Figure 1 below depicts the overall organization of this application.  All user-configurable options are held in a configuration file.  The ConfigParser module is utilized for reading that file.  Configuration state is managed in a class I developed called ConfigData.  All the REST calls to the LendingClub API are bundled into a class I developed called LendingClub.  The requests module is leveraged for the HTTP operations.

Figure 1
Code Snippets
Configuration File

This represents a simplistic user-configuration file.
Line 1:  AccountData section of the configuration file.
Line 2:  Your LendingClub account ID.  You can find this on the main account summary page on Lending's Club's site.
Line 3:  The authorization key issued by LendingClub when you request access to their API.
Line 4:  The amount of cash you want to remain in 'reserve'.  That means it will not be invested.
Line 5:  The amount you want invested in each loan.
Line 6:  The textual name of the portfolio where you want any loan purchases to be placed.
Line 7:  LoanCriteria section of the configuration file.
Lines 8-10:  Any criteria you wish to employ to filter loans for investment.  The filtering logic in the main app (discussed later) is very simple - it looks at equality only, e.g.  does Grade = 'A'.  You can find a full listing of the various loan data points in the Lending Club API documentation for the LoanList resource.

Application Body

Line 2:  Constructor for this class.
Lines 3-5:  Instantiate a ConfigParser object.  Read the config file and make option names case-sensitive.
Lines 6-12:  Set instance variables to the various account-data options in the config file.
Lines 14-16: Create an instance dictionary variable to store the user-specified loan criteria.
Lines 18-27: Helper function for casting options to the correct numeric type.

Line 4:  Constructor for this class.  Accepts a ConfigData object as input.
Lines 5-18:  Set the state for this object based on the configuration data passed as input.
Lines 20-23:  Private method for obtaining the cash available in the LendingClub account.  Utilizes the 'response' module for the HTTP operation.
Lines 26-43:  Private method for fetching available loans from LendingClub.  After the loans are fetched, they checked against the user's criteria and then sorted by their current funding percentage.
Lines 45-61:  Private method for submitting a loan order to LendingClub.  The LendingClub API actually allows to bundle multiple orders into one REST call; however, I'm only doing one order at time in this app.  That made the post-order error-checking logic simpler.

Main Code Block

    try:
        lc = LendingClub(ConfigData(CONFIG_FILENAME))
        while lc.hasCash() and lc.hasLoans():
            lc.buy()
    except:
        logger.exception('')


Line 2:  Instantiate a LendingClub object with the configuration data object as the input parameter.
Lines 3-4:  Loop based on availability of cash and matching loans.  If both exist, place an order.
