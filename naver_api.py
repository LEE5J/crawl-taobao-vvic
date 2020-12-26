def kor2cn(word):
    import os
    import sys
    import urllib.request
    client_id = ""
    client_secret = ""
    cnText = urllib.parse.quote(word)
    data = "source=ko&target=zh-CN&text=" + cnText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        return response_body.decode('utf-8').split("\"")[27]
    else:
        print("Error Code:" + rescode)


def cn2kor(word):
    import os
    import sys
    import urllib.request
    client_id = "7ZbdU2FMTiKfTtseJ4Fx"
    client_secret = "J_vZIGCmys"
    korText = urllib.parse.quote(word)
    data = "source=zh-CN&target=ko&text=" + korText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        return response_body.decode('utf-8').split("\"")[27]
    else:
        print("Error Code:" + rescode)
