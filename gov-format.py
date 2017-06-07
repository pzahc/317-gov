
import csv
print "Dance Boogie Wonderland!"


TARGET_BOARD_SIZE = 7
TARGET_BOARD_TENURE = 6
TARGET_BOARD_OTHER_SEATS = 3

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
    if s != 'n.a.' and s != 'n.s.' :
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
            self.num_boards = int(parseNumber(self.num_boards))
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
        self.woman_owned = row[map[WOMAN_OWNED]] == "Yes"
        self.minority_owned = row[map[MINORITY_OWNED]] == "Yes"


        self.num_shareholders = int(parseNumber(row[map[NUM_SHAREHOLDERS]]))
        self.num_subsidiaries = int(parseNumber(row[map[NUM_SUBSIDIARIES]]))

        # Finacials
        self.assets = parseNumber(row[map[ASSETS_0]])
        self.total_cash = parseNumber(row[map[TOTAL_CASH_0]])
        self.profit_margin = parseNumber(row[map[PROFIT_MARGIN_0]])

        # Stock Calculations
        self.stock0 = parseNumber(row[map[STOCK_PRICE_0]])
        self.stock1 = parseNumber(row[map[STOCK_PRICE_1]])
        self.stock5 = parseNumber(row[map[STOCK_PRICE_5]])
        if self.stock5 != 0 and self.stock0 != 0:
            ratio = self.stock0/self.stock5
            self.CAGR5 = (pow(abs(ratio), 1.0/5.0)-1.0)*(ratio/abs(ratio))
        else:
            self.CAGR5 = 0.0


        # Grab numbers and convert from strings
        self.op_rev = parseNumber(row[map[OP_REV]])
        self.market_cap = parseNumber(row[map[MARKET_CAP]])
        self.employees = parseNumber(row[map[EMPLOYEES]])

        # Values to be Calculated Later
        self.average_tenure = 0.0
        self.average_seats = 0.0
        self.board_size = 0
        self.average_prime_seats = 0.0

        self.directors = []
        self.cp_score = 0

    def addDirector(self, director):
        self.directors.append(director)

    def analyze(self):
        tenure_sum = 0.0
        seats_sum = 0.0
        salary_sum = 0.0
        prime_seat_sum = 0.0

        self.board_size = float(len(self.directors))
        for d in self.directors:
            tenure_sum += d.tenure
            seats_sum += d.num_boards

            prime_seat_sum += len(d.companies)
            # if len(d.companies) > 5:
            #     print len(d.companies)
            #     print d.name

            

        self.average_tenure =  tenure_sum / self.board_size
        self.average_seats =  seats_sum / self.board_size
        self.average_prime_seats =  prime_seat_sum / self.board_size

        self.calcCPScore()

    def calcCPScore(self):
        # Weight Asspects of Boards
        seats_delta = abs(self.average_seats - TARGET_BOARD_OTHER_SEATS)
        tenure_delta = abs(self.average_tenure - TARGET_BOARD_TENURE)
        size_delta = abs(self.board_size - TARGET_BOARD_SIZE)


        self.cp_score = 0.5*seats_delta + 0.5*tenure_delta + 0.3*size_delta - min(4, self.average_prime_seats)
        # if self.cp_score < -100:
        #     print str(self.cp_score) +': '+ str((seats_delta, tenure_delta, size_delta, self.average_prime_seats))


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
            self.average_prime_seats,
            self.CAGR5,
            self.minority_owned,
            self.woman_owned,
            self.assets,
            self.total_cash,
            self.profit_margin,
            self.num_shareholders,
            self.num_subsidiaries,
            self.board_size,
            dirs
        ]


def convertCSV(filename):

    companies = []
    directors = {}

    fileCSV = filename + '.csv'
    with open(fileCSV, 'rU') as bd_csv:
        bd_reader = csv.reader(bd_csv)
        headers = bd_reader.next()
        h_map = mapHeaders(headers)

        company = None
        for row in bd_reader:
            if row[1] != "":
                if company != None and len(company.directors) < 2:
                    companies.remove(company)

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

    outCSV = filename + '-comps.csv'
    with open(outCSV, 'w') as bd_csv:

        fieldnames = [
            'Company', 'Score', 'Ticker', 'Op_Rev', 'State',
            'Num_Employees', 'Market_Cap', 'AVG_Tenure', 'AVG_Seats',
            'Sector', 'AVG_Prime', 'CAGR5', 'M_OWNED', 'W_OWNED',
            'Assets', 'Total_Cash', 'Profit_Margin', 'Num_Share', 'Num_Subs',
            'Board_Size', 'Directors']
        writer = csv.writer(bd_csv)
        writer.writerow(fieldnames)

        for c in companies:
            c.analyze()
            c_csv = c.getCSVRow()
            writer.writerow(c_csv)

def main():
    convertCSV('317-MCapUS')
    convertCSV('317-SP')



if __name__ == '__main__':
    main()
