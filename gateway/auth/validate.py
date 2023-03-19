import os, requests

def token(request):
    print("IN auth.validate.token")
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)
    
    token = request.headers["Authorization"]
    
    if not token:
        return None, ("missing credentials", 401)
    print("Authorization present in token")
    print("Making request to AUTH SVC")
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate", headers={"Authorization": token},
    )
    
    if response.status_code == 200:
        print("GOT 200 BACK")
        return response.text, None
    else:
        print("GOT ERROR BACK")
        return None, (response.text, response.status_code)