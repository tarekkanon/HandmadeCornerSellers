import urllib.request as ureq, json
import urllib.error

def CallAPI(call_method, request_url,request_token='', require_authorization=True, request_data={}):

    try:
        if require_authorization:
                requestExt = ureq.Request(request_url, 
                                    data= json.dumps(request_data).encode('utf-8'), 
                                    method=call_method, 
                                    headers={
                                            "Content-Type" : "application/json"
                                            ,"Authorization": "Bearer {token}".format(token=request_token)
                                    })
        else: 
                requestExt = ureq.Request(request_url, 
                                    data= json.dumps(request_data).encode('utf-8'), 
                                    method=call_method, 
                                    headers={
                                            "Content-Type" : "application/json"
                                    })
                
        response = ureq.urlopen(requestExt)
        
        data = response.read()
        result = json.loads(data)

        return result
    except urllib.error.HTTPError as e:
        print(e.reason)