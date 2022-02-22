# -*- coding:utf-8 -*-

import tomli
import tomli_w
import glob
import os

def initial(app,tomls_folder='kipro_tomls'):
    '''
        环境变量或{app}_CONC 是否并行
        
        返回 当前app的confs[conf1,conf2]，以及 if_conc是否并行
    '''
    if os.listdir(tomls_folder):
        tomls_data = get_data(tomls_folder=tomls_folder)  # 合并tomls_folder下所有文件 读取为 {'app':[conf1,conf2]}
        confs = tomls_data.get(app) # 获取当前app的confs [conf1,conf2]  conf格式{'cookie':'xxx','xxx':'xxxx'}
        if_conc = env_if_conc if (env_if_conc:=os.environ.get(f'{app}_CONC')) else tomls_data.get(f'{app}_CONC')
        return confs,if_conc
    else:
        print(f"'{tomls_folder}'不存在")

def get_data(tomls_folder='kipro_tomls'):
    path_lst = glob.glob(f"{tomls_folder}/*.toml")
    f_lst = [open(path,'r',encoding='utf-8') for path in path_lst]
    lines_lst = [f.read() for f in f_lst]
    [f.close() for f in f_lst]
    res = '\n'.join(lines_lst)
    return tomli.loads(res)

def disable_account(user,app,tomls_folder='kipro_tomls'):
    path = f'{tomls_folder}/{user}.toml'
    with open(path,'rb+') as f:
        r = tomli.load(f)
        r[app][0]['status'] = 0
        f.seek(0)
        tomli_w.dump(r,f)
