import requests

class Genre():

    def __init__(self, inp):
        self.url = "https://streaming-availability.p.rapidapi.com/genres"

        self.headers = {
            "X-RapidAPI-Key": "81f9b30c24mshad02b4dfe62ebd6p1f3890jsn1123d21c4f86",
            "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
        }

        self.inp = inp

    def genreConvert(self):
        genres = requests.request("GET", self.url, headers=self.headers)

        genres_json = genres.json()
        #print(genres_json)

        for key , value in genres_json.items(): 
            if value == self.inp: 
                genre = key
                return genre


#example genre = "Comedy"

#test = Genre("Comedy")
#res = test.genreValue()
#print(res)