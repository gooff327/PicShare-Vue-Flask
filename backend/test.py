import os
current_path = os.path.abspath(__file__)
print('当前目录',current_path)
with open('./img/avatar/admin.jpg') as f:
    print(f)