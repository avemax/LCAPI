try:
    lc = LendingClub(ConfigData(CONFIG_FILENAME))
    while lc.hasCash() and lc.hasLoans():
        lc.buy()
except:
    logger.exception('')
