
import csv
print "Dance Boogie Wonderland!"


TARGET_BOARD_SIZE = 10
TARGET_BOARD_TENURE = 8
TARGET_BOARD_OTHER_SEATS = 4

NAME                = "Company name"
TICKER              = "Ticker symbol"
CITY                = "City"
OP_REV              = "Operating revenue (Turnover) m USD Last avail. yr"
EMPLOYEES           = "Number of employees Last avail. yr"
MARKET_CAP          = "Current market capitalisation m USD"
EXCHANGE            = "Main exchange"
NUM_SHAREHOLDERS    = "No of recorded shareholders"
NUM_SUBSIDIARIES    = "No of recorded subsidiaries"
WOMAN_OWNED         = "Woman owned indicator (in US)"
MINORITY_OWNED      = "Ethnic minority owned indicator (in US)"
STATE               = "State or province (in US or Canada)"
COUNTRY             = "Country"
DIRECTOR_NAME       = "DMC Full name"
DIRECTOR_ID         = "DMC UCI (Unique Contact Identifier)"
DIRECTOR_START      = "DMC Appointment date"
DIRECTOR_GENDER     = "DMC Gender"
DIRECTOR_AGE        = "DMC Age"
DIRECTOR_NATION     = "DMC Country/ies of nationality"
DIRECTOR_COMP       = "DMC Compensation total USD"
DIRECTOR_NUM_BOARD  = "DMC No of cos in which a current position is held"
STOCK_PRICE_0       = "Market price - year end USD Last avail. yr"
STOCK_PRICE_1       = "Market price - year end USD Year - 1"
STOCK_PRICE_5       = "Market price - year end USD Year - 5"
ASSETS_0            = "Total assets m USD Last avail. yr"
ASSETS_1            = "Total assets m USD Year - 1"
ASSETS_5            = "Total assets m USD Year - 5"
PROFIT_MARGIN_0     = "Profit margin % Last avail. yr"
PROFIT_MARGIN_1     = "Profit margin % Year - 1"
PROFIT_MARGIN_5     = "Profit margin % Year - 5"
TOTAL_CASH_0        = "Total Cash from Operating Activities m USD Last avail. yr"
TOTAL_CASH_1        = "Total Cash from Operating Activities m USD Year - 1"
TOTAL_CASH_5        = "Total Cash from Operating Activities m USD Year - 5"
SECTOR              = 'BvD major sector'

HEADER_LIST = [
  NAME,
  TICKER,
  CITY,
  OP_REV,
  EMPLOYEES,
  MARKET_CAP,
  EXCHANGE,
  NUM_SHAREHOLDERS,
  NUM_SUBSIDIARIES,
  WOMAN_OWNED,
  MINORITY_OWNED,
  STATE,
  COUNTRY,
  DIRECTOR_NAME,
  DIRECTOR_ID,
  DIRECTOR_START,
  DIRECTOR_GENDER,
  DIRECTOR_AGE,
  DIRECTOR_NATION,
  DIRECTOR_COMP,
  DIRECTOR_NUM_BOARD,
  STOCK_PRICE_0,
  STOCK_PRICE_1,
  STOCK_PRICE_5,
  ASSETS_0,
  ASSETS_1,
  ASSETS_5,
  PROFIT_MARGIN_0,
  PROFIT_MARGIN_1,
  PROFIT_MARGIN_5,
  TOTAL_CASH_0,
  TOTAL_CASH_1,
  TOTAL_CASH_5,
  SECTOR
]


def parseNumber(s):
    if s != 'n.a.':
        return float(s.replace(',', ''))

    return -1

def mapHeaders(headers):
    head_map = {}
    index = 0
    for h in headers:
        h = h.replace('\n',' ')
        if h in HEADER_LIST:
            head_map[h] = index
        else:
            print "Unhandeld Header: " + h
        index += 1

    return head_map


class Director(object):
    def __init__(self, row, map):
        self.name = row[map[DIRECTOR_NAME]]
        self.id = row[map[DIRECTOR_ID]]
        self.gender = row[map[DIRECTOR_GENDER]]
        self.age = row[map[DIRECTOR_AGE]]
        self.nation = row[map[DIRECTOR_NATION]]
        self.comp = row[map[DIRECTOR_COMP]]
        self.num_boards = row[map[DIRECTOR_NUM_BOARD]]
        if self.num_boards != '':
            self.num_boards = int(self.num_boards)
        else:
            self.num_boards = 0

        self.start_date = row[map[DIRECTOR_START]]
        self.tenure = self.calcTenure(self.start_date)


        self.companies = []

    def addCompany(self, comp):
        self.companies.append(comp)

    def calcTenure(self, start):
        tokens = start.split('/')
        year = tokens[-1]
        if year == '':
            year = 2017
        return 2017 - int(year)

    def isMultiTechDirector(self):
        return len(companies) > 1

    def __str__(self):
        return self.name

class Company(object):
    def __init__(self, row, map):
        self.name = row[map[NAME]]
        self.ticker = row[map[TICKER]]
        self.state = row[map[STATE]]
        self.exchange = row[map[EXCHANGE]]
        self.sector = row[map[SECTOR]]
        self.num_shareholders = row[map[NUM_SHAREHOLDERS]]
        self.num_subsidiaries = row[map[NUM_SUBSIDIARIES]]
        self.woman_owned = row[map[WOMAN_OWNED]] == "Yes"
        self.minority_owned = row[map[MINORITY_OWNED]] == "Yes"

        # Stock Calculations
        self.stock0 = parseNumber(row[map[STOCK_PRICE_0]])
        self.stock1 = parseNumber(row[map[STOCK_PRICE_1]])
        self.stock5 = parseNumber(row[map[STOCK_PRICE_5]])
        ratio = self.stock0/self.stock5
        self.CARG5 = (pow(abs(ratio), 1.0/5.0)-1.0)*(ratio/abs(ratio))


        # Grab numbers and convert from strings
        self.op_rev = parseNumber(row[map[OP_REV]])
        self.market_cap = parseNumber(row[map[MARKET_CAP]])
        self.employees = parseNumber(row[map[EMPLOYEES]])

        # Values to be Calculated Later
        self.average_tenure = 0
        self.average_seats = 0
        self.board_size = 0
        self.multi_500 = 0

        self.directors = []
        self.cp_score = 0

    def addDirector(self, director):
        self.directors.append(director)

    def analyze(self):
        tenure_sum = 0
        seats_sum = 0
        salary_sum = 0


        self.board_size = len(self.directors)
        for d in self.directors:
            tenure_sum += d.tenure
            seats_sum += d.num_boards
            if len(d.companies) > 1:
                # A director at this company is on multiple boards is this sample
                self.multi_500 += len(d.companies)-1
                # print d.name + ' : ' + str(self.multi_500) + ' : ' + str (len(d.companies))


        self.average_tenure =  tenure_sum / self.board_size
        self.average_seats =  seats_sum / self.board_size

        multi500 = 0

        self.calcCPScore()

    def calcCPScore(self):
        # Weight Asspects of Boards
        seats_delta = abs(self.average_seats - TARGET_BOARD_OTHER_SEATS)
        tenure_delta = abs(self.average_tenure - TARGET_BOARD_TENURE)
        size_delta = abs(self.board_size - TARGET_BOARD_SIZE)
        self.cp_score = 0.5*seats_delta + 0.5*tenure_delta + 0.3*size_delta - 0.5*self.multi_500

    def getCSVRow(self):
        dirs = ""
        for d in self.directors:
            dirs += str(d) + ", "
        dirs = dirs[:-2]
        return [
            self.name,
            self.cp_score,
            self.ticker,
            self.op_rev,
            self.state,
            self.employees,
            self.market_cap,
            self.average_tenure,
            self.average_seats,
            self.sector,
            self.multi_500,
            self.CARG5,
            dirs

            # self.exchange,
            # self.num_shareholders,
            # self.num_subsidiaries,
            # self.woman_owned,
            # self.minority_owned,
        ]


def main():
    companies = []
    directors = {}

    # with open('317-tech-raw.csv', 'rU') as bd_csv:
    with open('317-SP.csv', 'rU') as bd_csv:
        bd_reader = csv.reader(bd_csv)
        headers = bd_reader.next()
        h_map = mapHeaders(headers)

        company = None
        for row in bd_reader:
            if row[1] != "":
                company = Company(row, h_map)
                companies.append(company)

            d_id = row[h_map[DIRECTOR_ID]]
            director = None
            if d_id in directors:
                director = directors[d_id]
            else:
                director = Director(row, h_map)
                directors[d_id] = director

            director.addCompany(company)
            company.addDirector(director)



    print "Total Directors:" + str(len(directors))

    with open('317-tech-comps.csv', 'w') as bd_csv:

        fieldnames = [
            'Company', 'Score', 'Ticker', 'Op_Rev', 'State',
            'Num_Employees', 'Market_Cap', 'AVG_Tenure', 'AVG_Seats',
            'Sector', 'Other_500', 'CARG5', 'Directors']
        writer = csv.writer(bd_csv)
        writer.writerow(fieldnames)

        for c in companies:
            c.analyze()
            c_csv = c.getCSVRow()
            writer.writerow(c_csv)




if __name__ == '__main__':
    main()
