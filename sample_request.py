import urllib.request, urllib.parse

def get_user_input_list():
    user_input = []
    user_love = []
    user_like = []
    user_normal = []
    user_unlike = []
    user_hate = []

    for idx in range(10, 20):
        idx = str(idx)
# 3, 1, 2, 4, 0
        user_love.append('3' + idx)
        user_like.append('1' + idx)
        user_normal.append('2' + idx)
        user_unlike.append('4' + idx)
        user_hate.append(idx)

    user_input.append(user_love)
    user_input.append(user_like)
    user_input.append(user_normal)
    user_input.append(user_unlike)
    user_input.append(user_hate)

    ret = {
        'input': user_input
    }

    return ret

data = urllib.parse.urlencode(get_user_input_list()).encode("utf-8")
with urllib.request.urlopen("http://localhost:3000/result", data=data) as res:
   json = res.read().decode("utf-8")
   print(json)
