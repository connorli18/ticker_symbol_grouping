import json
import requests

def get_ticker_information(exchange, num):
    url = "https://www.sec.gov/files/company_tickers_exchange.json"
    headers = {
        "User-Agent": "John Doe (test@example.com)"
    }
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        if response.text:
            data = response.json()['data']


            #filter by exchange and num
            data = filter(exchange, num, data)
            

            #get more info via gropuing by stateOfIncorporation
            grouper(data, "stateOfIncorporation")
        else:
            print("Empty response received")

    else:
        print("Error: ", response.status_code)


#filter by exchange and num
def filter(exchange, num, data):
    
    result = []

    for ticker in data:
        if len(result) == num:
            break
        if ticker[-1].lower() == exchange.lower():
            result.append(ticker)

    return result


#group by what attribute?
def grouper(data, attribute):

    state_tracker = {}

    for ticker in data:
        cik_num = str(ticker[0]).zfill(10)

        url = f"https://data.sec.gov/submissions/CIK{cik_num}.json"
        headers = {
            "User-Agent": "John Doe (test@example.com)"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            state_of_incorp = response.json()[attribute]
            if state_of_incorp == "":
                state_of_incorp = "No state present"

            if state_of_incorp in state_tracker:
                state_tracker[state_of_incorp].append(ticker)
            else:
                state_tracker[state_of_incorp] = [ticker]

        else:
            print("Error: ", response.status_code)
            return None


    #print out the desired result
    for state in sorted(state_tracker, key=lambda s: len(state_tracker[s]), reverse=True):
        print(state + ": " + str(len(state_tracker[state])))




if __name__ == "__main__":
    get_ticker_information("NASDAQ", 10)