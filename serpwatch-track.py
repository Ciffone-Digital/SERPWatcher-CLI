import argparse
import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout, SSLError
import json
from prettytable import PrettyTable

# call SerpWatch API
def callSerpAPI(api_key, tracking_id):
    MANGOOLS_API_URL=f"https://api.mangools.com/v2/serpwatcher/trackings/{tracking_id}"
    headers = {
        'accept': 'application/json',
        'x-access-token': api_key
        }

    response = ''

    try:
        response = requests.get(url=MANGOOLS_API_URL, headers=headers, timeout=(5, 5))
    except HTTPError as http_err:
        print("ERROR: There was an HTTP_ERROR on the server side.")
        exit()
    except SSLError as ssl_err:
        print("ERROR: There was an SSL_ERROR on the server side.")
        exit()
    except ConnectTimeout as ct:
        print("ERROR: The server was unable to make an HTTP connection.")
        exit()
    except ReadTimeout as rt:
        print("ERROR: The server took too long to respond.")
        exit()
    except Exception as err:
        print("ERROR: An unknown error occured on the server side.")
        exit()
    else:
        if response.status_code == 200:
            message = response.json()
        elif response.status_code == 401:
            print("ERROR: Bad API key")
            exit()

    return message

# Parse response from SerpWatch API
def parseJsonResponse(message):
    data = {}
    data['keywords'] = []
    for i in message['keywords']:
        newrow = {}
        newrow['keyword'] = i['kw']
        newrow['search_volume'] = i['search_volume'] if i['search_volume'] != None else "-"
        newrow['estimated_visits'] = i['estimated_visits'] if i['estimated_visits'] != None else "-"
        newrow['rank_last'] = i['rank']['last'] if i['rank']['last'] != None else "-"
        newrow['rank_avg'] = i['rank']['avg'] if i['rank']['avg'] != None else "-"
        newrow['rank_best'] = i['rank']['best'] if i['rank']['best'] != None else "-"

        data['keywords'].append(newrow)

    return data

# Output parsed response
def outputData(data):
    t = PrettyTable(["keyword", "search_volume", "estimated_visits", "rank_last", "rank_avg", "rank_best"])
    for i in data['keywords']:
        t.add_row([i['keyword'],i['search_volume'],i['estimated_visits'],i['rank_last'],i['rank_avg'],i['rank_best']])

    print(t)
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get keyword data from Mangools SerpWatch API.')
    parser.add_argument('-a', '--api-key', dest='api_key', action='store', required=True, help='This is the API key that Mangools has assigned to you.')
    parser.add_argument('-t', '--tracking-id', dest='tracking_id', action='store', required=True, help='This is the tracking ID for the list of keywords.')

    args = parser.parse_args()

    outputData(parseJsonResponse(callSerpAPI(args.api_key, args.tracking_id)))
