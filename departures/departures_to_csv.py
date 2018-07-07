from datetime import datetime as dt
import requests

INITIAL_URL = "http://localhost:8000/departures/?format=json"
DATEFORMAT = "%Y-%m-%d"
DEADLINE = dt.strptime("2018-06-01",DATEFORMAT)

def load_departures(url,departure_list):
    """
    Load all the departure list from the API
    
    Parameters:
    url - the URL of this API
    departure_list - a list where the departures will be loaded 

    Returns: A list with departures added
    """
    resp = requests.get(url).json()
    departure_list.extend(resp["results"])
    
    #recursivelly loads the list
    if resp["next"] is None:
        return departure_list
    else:
        return load_departures(resp["next"], departure_list)

def save_into_csv_files(departure_list):
    """
    Save the Departure list on a departures.csv file
    """
    try:
        with open("departures.csv", "w") as f:
            f.write("Name;Start Date;Finish Date;Category;\n")

            for dep in departure_list:
                print(f"{dep['name']};{dep['start_date']};{dep['finish_date']};{dep['category']};\n")
                f.write(f"{dep['name']};{dep['start_date']};{dep['finish_date']};{dep['category']};\n")
    
    except Exception as ex:
        raise ex
    
        


def main():
    #filter to get only needed departures
    search = lambda x: x["category"] == "Adventurous" and dt.strptime(x["start_date"], DATEFORMAT) > DEADLINE
    departures = filter(search,load_departures(INITIAL_URL,[]))
    save_into_csv_files(departures)


if __name__ == '__main__':
    main()