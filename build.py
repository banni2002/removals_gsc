import os
from PyInstaller.utils.hooks import collect_data_files


# datas = collect_data_files('grpc')
add_datas = []

import PyInstaller.__main__

# for data in datas:
#     add_datas.append(f"--add-data='{data[0]};{data[1]}'")
# add_datas.append(f"--add-data 'resources;resources'")
PyInstaller.__main__.run([
                                'submit_index_with_sqlite.py',
                                '--name=submit_index_with_sqlite',
                                # '--icon=./resources/images/icon.ico',
                                '--onefile',
                                # '--windowed',
                                # '--add-data=UTILS:UTILS',
                                '--workpath=build/work',
                                '--distpath=build/dist',
                                '--clean',
                                # '--upx-dir=D:\\upx',
                            ] + add_datas)
print('BUILD DONE!')
