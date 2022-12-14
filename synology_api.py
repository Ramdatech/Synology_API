import requests

class Synology:

    def __init__(self, user, pw, url):
        self.url = url
        self.id, self.pw = user, pw
        self.ds_sid, self.fs_sid = '', ''

    def auth(self):
        # download station auth
        url = self.url + '/webapi/auth.cgi?api=SYNO.API.Auth&version=7&method=login'
        param = {}
        param['account'] = self.id
        param['passwd'] = self.pw
        param['session'] = 'DownloadStation'
        param['format'] = 'sid'
        response = requests.get(url=url, params=param)
        self.ds_sid = response.json()['data']['sid']

        # file station auth
        param['session'] = 'FileStation'
        response = requests.get(url=url, params=param)
        self.fs_sid = response.json()['data']['sid']

    def create_download_task(self, target_url):
        url = self.url + '/webapi/DownloadStation/task.cgi'
        data = {}
        data['sid'] = ''
        data['api'] = 'SYNO.DownloadStation.Task'
        data['version'] = '1'
        data['method'] = 'create'
        data['uri'] = target_url
        data['_sid'] = self.ds_sid
        response = requests.post(url, data=data, verify=False)
        bs = response.json()
        if 'success' in bs.keys() and bs['success'] :
            print(">> Done : create download task")
        else :
            print(">> Fail : create download task")


    def get_list_share_folder(self):
        url = self.url + '/webapi/entry.cgi?'
        param = {}
        param['api'] = 'SYNO.FileStation.List'
        param['version'] = '2'
        param['method'] = 'list_share'
        param['_sid'] = self.fs_sid
        response = requests.get(url=url, params=param)
        result = response.json()
        if result['success'] :
            print(">> Done : get list folder(share)")
            filelist = [x['path'] for x in result['data']['shares']]
            return filelist
        else :
            print(">> Fail : get list folder(share)")
            return []

    def get_list_folder(self, path):
        url = self.url + '/webapi/entry.cgi?'
        param = {}
        param['api'] = 'SYNO.FileStation.List'
        param['version'] = '2'
        param['method'] = 'list'
        param['folder_path'] = path
        param['_sid'] = self.fs_sid
        response = requests.get(url=url, params=param)
        result = response.json()
        if result['success'] :
            print(">> Done : get list folder")
            filelist = [x['path'] for x in result['data']['files']]
            return filelist
        else :
            print(">> Fail : get list folder")
            return []

    def update_file_name(self, src, new_name):
        url = self.url + '/webapi/entry.cgi?'
        param = {}
        param['api'] = 'SYNO.FileStation.Rename'
        param['version'] = '2'
        param['method'] = 'rename'
        param['path'] = src
        param['name'] = new_name
        param['_sid'] = self.fs_sid
        response = requests.get(url=url, params=param)
        result = response.json()
        if result['success'] :
            path, name = result['data']['files'][0]['path'], result['data']['files'][0]['name']
            print(f">> Done : Rename, '{path}' => '{name}'")
        else :
            print(">> Fail : Rename")


    def move_file(self, src, dst):
        url = self.url + '/webapi/entry.cgi?'
        param = {}
        param['api'] = 'SYNO.FileStation.CopyMove'
        param['version'] = '3'
        param['method'] = 'start'
        param['path'] = src
        param['dest_folder_path'] = dst
        param['remove_src'] = 'true'
        param['_sid'] = self.fs_sid
        response = requests.get(url=url, params=param)
        result = response.json()
        if result['success'] :
            print(f">> Done : Move")
        else :
            print(">> Fail : Move")


    def create_folder(self, path, name):
        url = self.url + '/webapi/entry.cgi?'
        param = {}
        param['api'] = 'SYNO.FileStation.CreateFolder'
        param['version'] = '2'
        param['method'] = 'create'
        param['folder_path'] = path
        param['name'] = name
        param['_sid'] = self.fs_sid
        response = requests.get(url=url, params=param)
        result = response.json()
        print(result)
        if result['success'] :
            print(f">> Done : Create Folder")
        else :
            print(">> Fail : Create Folder")


