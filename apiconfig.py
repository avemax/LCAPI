class ConfigData(object):
    def __init__(self, filename):
        cfgParser = ConfigParser.ConfigParser()
        cfgParser.optionxform = str
        cfgParser.read(filename)
        self.investorId = self.castNum(cfgParser.get('AccountData', 'investorId'))
        self.authKey = cfgParser.get('AccountData', 'authKey')
        self.reserveCash = self.castNum(cfgParser.get('AccountData', 'reserveCash'))
        self.investAmount = self.castNum(cfgParser.get('AccountData', 'investAmount'))
        if self.investAmount < 25 or self.investAmount % 25 != 0:  
            raise RuntimeError('Invalid investment amount specified in configuration file')
        self.portfolioName = cfgParser.get('AccountData', 'portfolioName')
        criteriaOpts = cfgParser.options('LoanCriteria')  #Loan filtering criteria
        self.criteria = {}
        for opt in criteriaOpts:
            self.criteria[opt] = self.castNum(cfgParser.get('LoanCriteria', opt));
 
    def castNum(self, val):
        try:
            i = int(val)
            return i
        except ValueError:
            try:
                d = decimal.Decimal(val)
                return d
            except decimal.InvalidOperation:
                return val
