import requests
import json
import os

Item_Name_List: list
Item_Name_List_File_Name = 'dat/item.json'


def download_json():
    page_index = 1
    url = 'https://esi.evepc.163.com/latest/characters/462934341/assets/'
    parameters = {
        'datasource': 'serenity',
        'page': page_index,
        'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkpXVC1TaWduYXR1cmUtS2V5IiwidHlwIjoiSldUIn0.eyJzY3AiOiJlc2ktYXNzZXRzLnJlYWRfYXNzZXRzLnYxIiwianRpIjoiNjhlZTY0NGEtMGJhMy00Njg0LThhNDItZGZjYzk1Y2JjZDljIiwia2lkIjoiSldULVNpZ25hdHVyZS1LZXkiLCJzdWIiOiJDSEFSQUNURVI6RVZFOjQ2MjkzNDM0MSIsImF6cCI6ImJjOTBhYTQ5NmE0MDQ3MjRhOTNmNDFiNGY0ZTk3NzYxIiwibmFtZSI6IuasoOaIkTEw5Z2XIiwib3duZXIiOiJSMXdTM2RHbFZ6N21DVGIrZnlqamZuaThOR0U9IiwiZXhwIjoxNjA1MDgwMTQzLCJpc3MiOiJsb2dpbi5ldmVwYy4xNjMuY29tIn0.nFfa2PFaFXvz5S-yOKLGtKMtcmrTZ4K4Iu5W4c43N8LYR6WTX72uR9aXlWQEbaGmuNynyPegyDmXpdmMk5rxGdxWM2rL4qNF-M3GLGnClvYdp5w7lop2xaOnScaEr2mfg7DP0xmX_0vqDxli1jEvFn6XiJJ_REWYkaL0NvSnbhEaqm1bwaux1gbdrnlUY8M9XQj-UGY1TLAcXo02DGmR_IS6s-XQ5zI7S1FiE-lMw0JSRWKVHDsxzr3V5eGMcHdc2G-5ASL5xUVquuLQjJS8hX_WiIWQaJlpI81BDggfreFak5WxsxmPfImyPrlXUoP3PlaoZ8yJMvUlH6VVt5sjJA'
    }
    continue_flag = True
    while continue_flag:
        ret = requests.get(url, params=parameters)
        print(f'页面{page_index}: {ret.status_code}')
        if ret.status_code == 200:
            # print(len(ret.text))
            print()
            parameters['page'] = page_index
            jobj = json.loads(ret.text)
            if len(jobj) > 0:
                with open(f'dat/page{page_index}.json', 'w', encoding='utf8') as fs:
                    fs.write(ret.text)
                page_index += 1
            else:
                print('空内容')
                continue_flag = False
        else:
            # print(ret.status_code)
            continue_flag = False


def load_assets() -> list:
    index = 1
    file_name = f'dat/page{index}.json'
    alist = []
    while os.path.exists(file_name):
        # print(f'读取{file_name}')
        with open(file_name, 'r', encoding='utf8') as fs:
            for asset_item in json.load(fs):
                alist.append(asset_item)
        index += 1
        file_name = f'dat/page{index}.json'

    return alist


def init_item_list():
    global Item_Name_List
    global Item_Name_List_File_Name
    if os.path.exists(Item_Name_List_File_Name):
        with open(Item_Name_List_File_Name, 'r', encoding='utf8') as fs:
            Item_Name_List = json.load(fs)
    else:
        Item_Name_List = {}


def get_item_name(item_id: int) -> str:
    global Item_Name_List
    is_new_item_flag = False
    for item in Item_Name_List:
        if item['id'] == item_id:
            return item['name']

    if not is_new_item_flag:
        print(f'尝试从网络获取{item_id}')
        url = f'https://esi.evepc.163.com/latest/universe/types/{item_id}/?datasource=serenity&language=zh'
        ret = requests.get(url)
        if ret.status_code == 200:
            item_name = json.loads(ret.text)['name']
            Item_Name_List.append({
                'id': item_id,
                'name': item_name
            })
            with open('dat/item.json', 'w', encoding='utf8') as fs:
                json.dump(Item_Name_List, fs, ensure_ascii=False, indent=4)
            return item_name
        else:
            return '未知物品'


if __name__ == '__main__':
    init_item_list()
    assert_list = load_assets()

    for item in assert_list:
        if item['location_type'] == 'station':
            item_id = item['type_id']
            name = get_item_name(item_id)
            quantity = item['quantity']
            print(f'{name} × {quantity}')
