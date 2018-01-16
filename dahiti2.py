def create_location_table():
    ## lists targets
    import requests
    import json
    import pandas
    from pandas.io.json import json_normalize
    
    url = 'http://dahiti.dgfi.tum.de/api/v1/'

    args = {}
    """ required options """
    args['username'] = 'ShravaniVadlamudi'
    args['password'] = '123456'
    args['action'] = 'list-targets'

    """ optional options """
    #args['basin'] = 'Amazon'
    #args['continent'] = 'Asia'
    #args['country'] = 'de'
    #args['min_lon'] = 0
    #args['max_lon'] = 10
    #args['min_lat'] = 0
    #args['max_lat'] = 10
    #args['software'] = '3.1'

    """ send request as method POST """
    response = requests.post(url, data=args)
    """ send request as method GET """
    response = requests.get(url, params=args)

    if response.status_code == 200:
        """ convert json string in python list """
        data = json.loads(response.text)
        data = json_normalize(data)
        data.drop('location', axis=1, inplace=True)
        data.columns=['cl_id','latitude','longitude','target_name']
        return(data)
    else:
        return(response.status_code)        

x=create_location_table()
print (x)
#x["latitude"]+","+x["longitude"]
