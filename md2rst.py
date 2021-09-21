# coding:utf-8
import os
# import commands
import subprocess
import platform

from git import Repo


osName = platform.system()
repo_path ='.'
if (osName == 'Windows'):
    repo_path = 'E:\\MING-Git\\GolangCodingTime'
    blog_path = 'E:\\MING-Git\GolangCodingTime\\source'
    index_path = 'E:\\MING-Git\\GolangCodingTime\\README.md'
elif (osName == 'Darwin'):
    repo_path = '/Users/MING/Github/golang-interview/'
    blog_path = '/Users/MING/Github/golang-interview/source'
    index_path = '/Users/MING/Github/golang-interview/README.md'


#repo = Repo.init(path=repo_path)
#if not repo.is_dirty():
#    # 没有文件变更
#    os._exit(0)

base_link = "http://go-interview.iswbm.com/en/latest/"

def get_file_info(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        first_line = file.readline().replace("#", "").strip()
    return first_line.split(' ', 1)

def make_line(chapter, file):
    page_name, _ = os.path.splitext(file)
    (index, title) = get_file_info(file)
    url = base_link  + chapter + "/" + page_name + ".html"
    item_list = ["-", index, "[{}]({})\n".format(title, url)]
    return " ".join(item_list)


def convert_md5_to_rst(file):
    '''
    转换格式：md5转换成rst
    '''
    (filename, extension) = os.path.splitext(file)
    convert_cmd = 'pandoc -V mainfont="SimSun" -f markdown -t rst {md_file} -o {rst_file}'.format(
        md_file=filename+'.md', rst_file=filename+'.rst'
    )
    # status, output = commands.getstatusoutput(convert_cmd)
    status = subprocess.call(convert_cmd.split(" "))
    if status != 0:
        print("命令执行失败: " + convert_cmd)
        os._exit(1)
    if status == 0:
        print(file + ' 处理完成')
    else:
        print(file + '处理失败')

def get_all_dir():
    '''
    获取所有的目录
    '''
    dir_list = []
    file_list = os.listdir(blog_path)
    for item in file_list:
        abs_path = os.path.join(blog_path, item)
        if os.path.isdir(abs_path):
            dir_list.append(abs_path)
    return dir_list


def init_index_info():
    '''
    初始化索引
    '''
    index_info = {}
    chapter_dir = os.path.join(blog_path, "chapters")
    os.chdir(chapter_dir)
    for file in os.listdir(chapter_dir):
        name, _ = os.path.splitext(file)
        with open(file, 'r', encoding="utf-8") as f:
            chapter_name = f.readlines()[1].strip()
        index_info[name.replace("p", "")] = {"name": chapter_name, "contents": []}
    return index_info

def main(index_info):
    for folder in get_all_dir():
        os.chdir(folder)
        chapter = os.path.split(folder)[1]
        all_file = os.listdir(folder)
        all_md_file = sorted([file for file in all_file if file.endswith('md')])

        for file in all_md_file:
            line = make_line(chapter, file)
            index_info[chapter.replace("c", "")]["contents"].append(line)
            convert_md5_to_rst(file)


if __name__ == '__main__':
    index_info = init_index_info()
    main(index_info)
    print("OK")
