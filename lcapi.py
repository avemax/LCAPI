class LendingClub(object):
    apiVersion = 'v1'
    
    def __init__(self, config):
        self.config = config
        self.header = {'Authorization' : self.config.authKey, 'Content-Type': 'application/json'}
        self.loans = None
        self.cash = None
        self.portfolioId = None
        
        self.acctSummaryURL = 'https://api.lendingclub.com/api/investor/' + LendingClub.apiVersion + \
        '/accounts/' + str(self.config.investorId) + '/summary'
        self.loanListURL = 'https://api.lendingclub.com/api/investor/' + LendingClub.apiVersion + \
        '/loans/listing'
        self.portfoliosURL = 'https://api.lendingclub.com/api/investor/' + LendingClub.apiVersion + \
        '/accounts/' + str(self.config.investorId) + '/portfolios'
        self.ordersURL = 'https://api.lendingclub.com/api/investor/' + LendingClub.apiVersion + \
        '/accounts/' + str(self.config.investorId) + '/orders'
        
    def __getCash(self):
        resp = requests.get(self.acctSummaryURL, headers=self.header)
        resp.raise_for_status()
        return decimal.Decimal(str(resp.json()['availableCash']))
        
    
    def __getLoans(self):
        payload = {'showAll' : 'true'}
        resp = requests.get(self.loanListURL, headers=self.header, params=payload)
        resp.raise_for_status()
     
        loanDict = {}
        for loan in resp.json()['loans']:
            numChecked = 0
            for criterion in self.config.criteria:
                if loan[criterion] == self.config.criteria[criterion]:
                    numChecked += 1              
                else:
                    break
            if numChecked == len(self.config.criteria):
                loanDict[loan['id']] = loan['fundedAmount'] / loan['loanAmount']
                logger.info('Loan id:' + str(loan['id']) + \
                             ' was a match, funded percentage = ' + str(loanDict[loan['id']]))
        return sorted(loanDict.items(), key=operator.itemgetter(1), reverse=True)            
 
    def __postOrder(self, aid, loanId, requestedAmount, portfolioId):
        payload = json.dumps({'aid': aid, \
                   'orders':[{'loanId' : loanId, \
                                'requestedAmount' : float(requestedAmount), \
                                'portfolioId' : portfolioId}]})
        resp = requests.post(self.ordersURL, headers=self.header, data=payload)
        retVal = resp.json();
        
        if 'errors' in retVal:
            for error in retVal['errors']:
                logger.error('Order error: ' + error['message'])
        resp.raise_for_status()
        
        confirmation = retVal['orderConfirmations'][0]
        logger.info('OrderId:' + str(retVal['orderInstructId']) + ', $' + \
                    str(confirmation['investedAmount']) + ' was invested in loanId:' + str(confirmation['loanId']))
        return decimal.Decimal(str(confirmation['investedAmount']))
