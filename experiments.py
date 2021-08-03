import time


class Payment:

    def mock_request_payment(self, sum):
        print('connecting to bank.....')
        time.sleep(3)
        print('request for payment of ' + str(sum)  + ' euros successful')

    def mock_do_payment(self, sum):
        print('connecting to bank.....')
        time.sleep(3)
        print('payment of ' + str(sum)  + ' euros successful')

    def __init__(self, bank, curr):
        self.bank_name = bank
        self.currency = curr

    def __str__(self):
        return('Bank:' + self.bank_name + ', currency: ' + self.currency)

if __name__ == '__main__':
    print('Hallo payment')
