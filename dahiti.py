def get_timeseries_data(dahiti_id,location_id):
    import requests
    import json
    import pandas
    from pandas.io.json import json_normalize
    url = 'http://dahiti.dgfi.tum.de/api/v1/'
    args = {}
    """ required options """
    args['username'] = 'ShravaniVadlamudi'
    args['password'] = '123456'
    args['action'] = 'download'
    args['dahiti_id'] = dahiti_id
    """ send request as method POST """
    response = requests.post(url, data=args)
    """ send request as method GET """
    response = requests.get(url, params=args)
    if response.status_code == 200:
        """convert json string in python list """
        data = json.loads(response.text)
        data = json_normalize(data)
        data['cl_id']= dahiti_id
        data['location_id'] = location_id
        return(data)
    else:
        return(response.status_code)
print (get_timeseries_data('85','2'))
print (get_timeseries_data('970','2'))
