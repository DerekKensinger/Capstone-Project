import requests

url = "https://api-formula-1.p.rapidapi.com/circuits"

querystring = {"id":"4"}

headers = {
	"X-RapidAPI-Key": "a89c14d218mshd88354c7de6b700p10ba46jsn17491764c2da",
	"X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())