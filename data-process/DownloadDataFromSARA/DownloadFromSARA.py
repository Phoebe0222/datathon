import webbrowser
import urllib.request, json 
from datetime import date, timedelta
from math import sin, cos, sqrt, atan2, radians
from shapely.wkt import loads as load_wkt
import subprocess
import sys

class sara():
    '''
    parameter:
        geometry is the user-defined polygon, a string e.g. 'POLYGON((point1,point2,point3,point4))'
        dateRange is the range of time searched for, default is 10 days
        completionDate is the end of date searched for, default is today 
    
    
    output:
        get_url gives search results from the parameters from SARA API, in the format of json file url link
        get_json gives the selected download links from the json file 
        download_from_link starts the download process in the current directory 
    
    '''
    
    def __init__ (self, geometry, unique_id, dateRange = 10, completionDate = date.today()):
        # default is search for the past 10 days data
        self.email = 'mlsa.unimelb.au@gmail.com'
        self.password = 'mlsa12345'
        self.startDate = completionDate - timedelta(days=dateRange)
        self.completionDate = completionDate
        self.geometry = geometry
        self.centroid = load_wkt(geometry).centroid
        self.unique_id = unique_id
    
    def get_url(self):
        self.link = "https://copernicus.nci.org.au/sara.server/1.0/api/collections/S2/search.json?_pretty=1&startDate={}&completionDate={}&geometry={}&processingLevel=L2A".format(self.startDate,self.completionDate,self.geometry)
        self.link = self.link.replace(" ","")
        return self.link
    
    def get_distance(self,lon2,lat2):
        # approximate radius of earth in km
        R = 6373.0
        lon1 = self.centroid.x
        lat1= self.centroid.y

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c # in km
        
        return distance

    def get_json(self):
        with urllib.request.urlopen(self.link) as url:
            self.data = json.loads(url.read().decode())
            count = self.data['properties']['totalResults']
            download_links = []
            # select from the searched results, with cloud cover no larger than 20 and centroid distance no larger than 10
            for i in range(count):
                if self.data['features'][i]['properties']['cloudCover'] <= 20:
                    feature_centroid = self.data['features'][i]['properties']['centroid']['coordinates']
                    if self.get_distance(feature_centroid[0], feature_centroid[1]) <= 70:
                        download_links.append(self.data['features'][i]['properties']['services']['download']['url'])

        self.download_links = download_links
        return self.download_links
    
     
    def download_from_link(self, quicklook = False):

        if quicklook == True: webbrowser.open(self.data['features'][0]['properties']['quicklook'])
        download_link = self.download_links[0]
        subprocess.run("pwd",shell=True) 
        # print(self.email, self.password, download_link)
        # subprocess.call(['curl', '-n', '-L', '-O', '-J', '-k', '-u', self.email , ':', self.password, download_link], shell=True)

        command = 'curl -n -L -k -u ' + self.email  + ':' + self.password + ' ' + download_link + ' -o ' + self.unique_id + '.zip' 
        print(command)
        subprocess.Popen(command, shell=True)
        # out, err = p.communicate()
        

#  mlsa.unimelb.au@gmail.com:mlsa12345 https://copernicus.nci.org.au/sara.server/1.0/collections/S2/149f8167-d9f6-5ef3-8941-e44fb7d5526f/download
  


if __name__ == "__main__":
    unique_id = 'default'
    geometry = 'POLYGON((149.03 -35.18,149.23 -35.18,149.23 -35.38,149.03 -35.38,149.03 -35.18))'

    if sys.argv[1]: 
        geometry = sys.argv[1]
        print(geometry)
    
    if sys.argv[2]:
        unique_id = sys.argv[2] 
        print(unique_id)

    test = sara(geometry = geometry, unique_id = unique_id)
    test.get_url()
    test.get_json()
    print("Downloading the files...")
    test.download_from_link()

                

