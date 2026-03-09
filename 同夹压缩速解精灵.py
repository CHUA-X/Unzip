#!/usr/bin/python3
# unzip.py ——自动解压缩指定文件夹窗口内所有压缩包

import os
import sys
import platform
from pathlib import Path


def main_ctrl():
    """选择要操作的文件夹窗口路径"""
    while 1:
        flag_ = pymsgbox.prompt('按1从固定路径解压缩\n按2改变固定路径\n按3输入指定路径解压缩\n按取消退出\n请输入选项：',
                                '一键解压小程序')
        if flag_ == '1':
            if not Path('.unzip').is_file():
                folder_path = pymsgbox.prompt('请输入固定路径（按取消返回）：', '一键解压小程序')
                if folder_path is None:
                    continue
                Path('.unzip').write_text(folder_path)
            folder_path = Path('.unzip').read_text()
            os.chdir(folder_path)
            break
        elif flag_ == '2':
            folder_path = pymsgbox.prompt('请输入新的固定路径（按取消返回）：', '一键解压小程序')
            if folder_path is None:
                continue
            Path('.unzip').write_text(folder_path)
            continue
        elif flag_ == '3':
            folder_path = pymsgbox.prompt('请输入欲解压压缩包绝对路径（按取消返回）：', '一键解压小程序')
            if folder_path is None:
                continue
            os.chdir(folder_path)
            break
        elif flag_ is None:
            sys.exit()


def extract_by_zip(file):
    """使用zipfile解压缩文件"""
    import zipfile
    with zipfile.ZipFile(file, 'r') as zipObj:
        # 将解压后的文件存放到已解压文件文件夹中
        print(f'正在解压{os.path.basename(file)}中······')
        zipObj.extractall(Path('已解压文件') / Path(file).stem)


def extract_by_tar(file):
    """使用tarfile解压缩文件"""
    import tarfile
    with tarfile.open(file, 'r') as tarObj:
        # 将解压后的文件存放到已解压文件文件夹中
        print(f'正在解压{os.path.basename(file)}中······')
        tarObj.extractall(Path('已解压文件') / Path(file).stem)


def extract_by_rar(file):
    """使用rarfile解压缩文件"""
    import rarfile
    with rarfile.RarFile(file, 'r') as rarObj:
        # 将解压后的文件存放到已解压文件文件夹中
        print(f'正在解压{os.path.basename(file)}中······')
        rarObj.extractall(Path('已解压文件') / Path(file).stem)


def extract_by_7z(file):
    """使用py7zr解压缩文件"""
    import py7zr
    with py7zr.SevenZipFile(file, mode='r') as seven_zObj:
        # 将解压后的文件存放到已解压文件文件夹中
        print(f'正在解压{os.path.basename(file)}中······')
        seven_zObj.extractall(Path('已解压文件') / Path(file).stem, overwrite=True)


def extract_by_cab(file):
    """使用cabfile解压缩文件"""
    import cabfile
    with cabfile.CabFile(file, 'r') as cabObj:
        # 将解压后的文件存放到已解压文件文件夹中
        print(f'正在解压{os.path.basename(file)}中······')
        cabObj.extractall(Path('已解压文件') / Path(file).stem)


try:
    import py7zr
    import cabfile
    import rarfile
    import pymsgbox

except (ModuleNotFoundError, ImportError):
    # 若未安装相关库，则自动安装
    print('缺少依赖，正在安装中……')
    info = os.popen('py -m pip install pymsgbox rarfile py7zr cabfile')
    text = info.read()

    if "Requirement" in text:
        # 第三方库安装成功
        print('安装成功！')

    else:
        # 记录失败情况
        print('安装失败！')
        print("state:" + str(text in "Requirement"))
        print("log:\n" + text)

# 执行选择文件夹路径
main_ctrl()
# 在文件夹下创建一个名为已解压文件的新文件夹
os.makedirs('已解压文件', exist_ok=True)

# 遍历文件夹中的文件
for filename in os.listdir('.'):
    # 检查文件
    if filename.lower().endswith('.zip'):
        # 调用extract_by_zip()函数解压
        extract_by_zip(filename)  # 解压zip文件
    elif filename.lower().endswith('.tar'):
        # 调用extract_by_tar()函数解压
        extract_by_tar(filename)  # 解压tar文件
    elif filename.lower().endswith('.rar'):
        # 调用extract_by_tar()函数解压
        extract_by_rar(filename)  # 解压rar文件
    elif filename.lower().endswith('.7z'):
        # 调用extract_by_7z()函数解压
        extract_by_7z(filename)  # 解压7z文件
    elif filename.lower().endswith('.cab'):
        # 调用extract_by_cab()函数解压
        extract_by_cab(filename)  # 解压cab文件

# 是否打开文件夹
way = Path.cwd() / '已解压文件'
flag = pymsgbox.confirm(f'所有压缩文件解压完成，解压后的文件已放入{way}。\n是否立即打开此文件夹窗口？',
                        '一键解压小程序', buttons=['是的，谢谢。', '不用了，谢谢。'])
if flag == '是的，谢谢。':
    if platform.system() == 'Windows':  # Windows系统下打开文件夹窗口
        os.system(f'explorer {way}')
    elif platform.system() == 'Darwin':  # MacOS系统下打开文件夹窗口
        os.system(f'open {way}')
    elif platform.system() == 'Linux':  # Linux系统下打开文件夹窗口
        os.system(f'nautilus {way}')
