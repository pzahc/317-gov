
import csv
print "Dance Boogie Wonderland!"


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
]


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
        self.start_date = row[map[DIRECTOR_START]]
        self.gender = row[map[DIRECTOR_GENDER]]
        self.age = row[map[DIRECTOR_AGE]]
        self.nation = row[map[DIRECTOR_NATION]]
        self.comp = row[map[DIRECTOR_COMP]]
        self.num_boards = row[map[DIRECTOR_NUM_BOARD]]

        self.companies = []

    def addCompany(self, comp):
        self.companies.append(comp)

    def isMultiTechDirector(self):
        return len(companies) > 1

    def __str__(self):
        return self.name

class Company(object):
    def __init__(self, row, map):
        self.name = row[map[NAME]]
        self.ticker = row[map[TICKER]]
        self.op_rev = row[map[OP_REV]]
        self.state = row[map[STATE]]
        self.employees = row[map[EMPLOYEES]]
        self.market_cap = row[map[MARKET_CAP]]
        self.exchange = row[map[EXCHANGE]]
        self.num_shareholders = row[map[NUM_SHAREHOLDERS]]
        self.num_subsidiaries = row[map[NUM_SUBSIDIARIES]]
        self.woman_owned = row[map[WOMAN_OWNED]] != "Yes"
        self.minority_owned = row[map[MINORITY_OWNED]] != "Yes"
        self.directors = []
        self.cp_score = 0

    def addDirector(self, director):
        self.directors.append(director)

    def calcCPScore(self):
        pass

    def getCSVRow(self):
        dirs = ""
        for d in self.directors:
            dirs += str(d) + ", "
        dirs = dirs[:-2]
        return [
            self.name,
            self.cp_score,
            self.ticker,
            # self.op_rev,
            # self.state,
            # self.employees,
            # self.market_cap,
            # self.exchange,
            # self.num_shareholders,
            # self.num_subsidiaries,
            # self.woman_owned,
            # self.minority_owned,
            dirs
        ]


def main():
    companies = []
    directors = {}

    with open('317-tech-raw.csv', 'rU') as bd_csv:
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

    with open('317-tech-ready.csv', 'w') as bd_csv:

        fieldnames = ['Company', 'Score', 'Ticker', 'Directors']
        writer = csv.writer(bd_csv)
        writer.writerow(fieldnames)

        for c in companies:
            c.calcCPScore()
            c_csv = c.getCSVRow()
            writer.writerow(c_csv)




if __name__ == '__main__':
    main()
