import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import pathlib
import os
import shutil


def deeppath(tdir):
    """
    递归获取目录下的所有文件

    参数
        tdir 目录
    """
    paths = []
    for p in tdir.iterdir():
        if p.is_dir():
            paths.extend(deeppath(p))
        else:
            paths.append(str(p))
    return paths


def build_package(package_path):
    """
    将自编写的扩展包编译成由pyd文件组成的扩展包

    参数
        package_path 扩展包文件夹的路径
    """
    package_path = pathlib.Path(package_path)
    package_name = package_path.name

    # 清理编译中间件.c文件
    logger.info(f'清理编译过程中生成的.c文件')
    file_paths = deeppath(package_path)
    cfile_paths = [p for p in file_paths if p.endswith('.c')]
    for cp in cfile_paths:
        if os.path.exists(cp):
            os.remove(cp)

    # # 扫描需要编译的.py文件
    logger.info(f'扫描扩展包中的.py文件')
    file_paths = deeppath(package_path)
    sourcefiles = [p for p in file_paths if p.endswith('.py') and p.find('__init__') == -1]
    # # print(sourcefiles)

    # 将包中的py文件编译成pyd文件
    logger.info(f'编译扩展包中的.py文件，除__init__.py')
    setup(
        name="Build material recognition extension",
        ext_modules=cythonize(sourcefiles)
    )
    
    # 清理编译中间件.c文件
    logger.info(f'清理编译过程中生成的.c文件')
    file_paths = deeppath(package_path)
    cfile_paths = [p for p in file_paths if p.endswith('.c')]
    for cp in cfile_paths:
        if os.path.exists(cp):
            os.remove(cp)

    # 将原目录中的__init__文件复制到编译后的目录中
    logger.info(f'将源扩展包目录中的__init__文件复制到编译后的目录中')
    build_path = pathlib.Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build'))
    libfolder_path = list(build_path.glob("lib.*"))

    if len(libfolder_path) == 1:
        buildpackage_path = libfolder_path[0].joinpath(package_name)
        initfiles = [p for p in file_paths if p.endswith('.py') and p.find('__init__') != -1]
        
        for p in initfiles:
            shutil.copy(p, buildpackage_path.joinpath(p.split(package_name)[-1].strip(os.sep)))


def build_file(file_path):
    """
    将自编写的py文件编译成pyd文件

    参数
        file_path py文件路径
    """

    setup(
        name="Build material recognition extension",
        ext_modules=cythonize(file_path)
    )

    middlefile_path = os.path.splitext(file_path)[0] + '.c'
    if os.path.exists(middlefile_path):
        os.remove(middlefile_path)



if __name__ == '__main__':
    package_path = r'D:\Code\CRRC_build\material_reognition'
    build_package(package_path)
    build_file(r'D:\Code\CRRC_build\material_recognition_module.py')