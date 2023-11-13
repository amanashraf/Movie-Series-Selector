import pandas as pd
import requests
from Genres import Genre
import statistics

#Documentation: https://developers.themoviedb.org/3/getting-started/introduction


class Data():
    
    def __init__(self, time, service, SorM, genre):

        self.time = time.lower()
        self.service = service.lower()
        self.SorM = SorM.lower()
        if genre == "Any":
            self.genre = "Any"
        else:
            self.genre = str(Genre(genre).genreConvert())
        #self.new = new


    def avgSRuntime(self, dataframe, column):
        lst = []
        for row_val in dataframe[column]:
            #print(row_val)
            avg_val = statistics.mean(row_val)
            #print(avg_val)
            lst.append(avg_val)
            #print(lst, "\n")
        return(lst)


    def getData(self):
        
        url = "https://streaming-availability.p.rapidapi.com/search/basic"
        
        if self.genre == "Any":
            querystring = {"country":"gb", "service":self.service, "type":self.SorM, "output_language":"en", "language":"en"}
        else:
            querystring = {"country":"gb", "service":self.service, "type":self.SorM, "genre":self.genre, "output_language":"en", "language":"en"}

        headers = {
            "X-RapidAPI-Key": "81f9b30c24mshad02b4dfe62ebd6p1f3890jsn1123d21c4f86",
            "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
        }

        try:
            response = requests.request("GET", url, headers=headers, params=querystring)

            #print(response.status_code)

            response_json = response.json()
            #print(response_json)


            response_df = pd.DataFrame(response_json["results"])
            #print(response_df)
            
            if self.SorM == "movie":
                var = ['title','genres', 'year', 'runtime', 'overview', 'cast', 'posterURLs']
            else:
                var = ['title','genres', 'year', 'episodeRuntimes', 'overview', 'cast', 'posterURLs']

            #dataframe filtered by column
            refined_df = response_df[var]  
        
            
            if self.SorM != "movie":
                for series in range(len(refined_df['episodeRuntimes'])):
                    if len(refined_df['episodeRuntimes'][series]) <= 0:
                        refined_df = refined_df.drop([series])    
                
                avg_runtime = self.avgSRuntime(refined_df, "episodeRuntimes")
                #print(runtime)
                runtime = pd.DataFrame({"runtime":avg_runtime})
                #print(refined_df)
                refined_df = pd.concat([refined_df, runtime], axis=1)
                #print(refined_df)
                refined_df = refined_df.drop("episodeRuntimes", axis=1)
                #print(refined_df)
            
            
            for row in range(len(refined_df['runtime'])):
                if self.time == "<30mins":
                    if not ((refined_df['runtime'][row]<=30) and (refined_df['runtime'][row]>0)):
                        refined_df = refined_df.drop([row])
                        
                elif self.time == "30mins - 1hr":
                    if not ((refined_df['runtime'][row]<=60) and (refined_df['runtime'][row]>30)):
                        refined_df = refined_df.drop([row])
                
                elif self.time == "1hr - 2hrs 30mins":
                    if not ((refined_df['runtime'][row]<=150) and (refined_df['runtime'][row]>60)):
                        refined_df = refined_df.drop([row])
                
                elif self.time == "+2hrs 30mins":
                    if not ((refined_df['runtime'][row]>=150)):
                        refined_df = refined_df.drop([row])

            
            df = refined_df.sample()

            title = df['title']
            title = (title.to_numpy()).item(0)
            
            year = df['year']
            year = "Release Date: " + str(int((year.to_numpy()).item(0)))
            
            image = (df['posterURLs'].item())['original']
            
            cast = df['cast'].item()
            cast = 'Starring: ' + (', '.join(cast))
            
            overview = 'Overview: ' + df['overview'].item()

            runtime = df['runtime']
            runtime = str(int((runtime.to_numpy()).item(0))) + " mins"

            results = [title, year, image, cast, overview, runtime]
            #print(results)
            return(results)
            
        #except KeyError: 
        except:
            results = "Well this is awkward...we can't find any results. \nPlease try different inputs"
            return(results)
        
