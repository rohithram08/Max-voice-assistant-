import requests
api_address="https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=c422f8e7e19b45c99e9522021c11f62f"
json_data = requests.get(api_address).json()

ar=[]

def news():
    for i in range(3):
        ar.append("Number "+ str(i+1) +"-"+ json_data["articles"][i]["title"]+".")
        
    return ar