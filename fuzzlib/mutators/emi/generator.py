#!/usr/bin/python3
import subprocess
import os
import re

from fuzzlib.mutators.emi import replacer, Config

file_num = 0

csmith_cmd = Config.csmith_cmd


def gen_single_file(file_name):
    global csmith_cmd
    cmd_line = csmith_cmd + " --output " + file_name
    status, output = subprocess.getstatusoutput(cmd_line)
    if status != 0:
        print(output)
    else:
        print(file_name + ' generated')
    return status


# compile_cmd = 'gcc -fno-stack-protector -no-pie -O0 -Wall -m32 '
compile_cmd = Config.compile_cmd
runtime_dir = Config.runtime_dir


def compile_single_file(file_path):
    if os.path.isdir(file_path):
        pass
    elif os.path.splitext(file_path)[1] == '.c':
        status, output = \
            subprocess.getstatusoutput(compile_cmd +
                                       ' -I ' + runtime_dir +
                                       ' -o ' + os.path.splitext(file_path)[0] +
                                       ' ' + file_path)
        if status != 0:
            # print(output)
            print(file_path + ' compilation failed')
            return status, output
        else:
            print(file_path + ' compiled')
            return 0, ''


def batch_compile(src_dir):
    """compile all .c files in the directory"""
    files = os.listdir(src_dir)
    files.sort()
    for file in files:
        file_path = os.path.join(src_dir, file)
        if not file_path.endswith('.c'):
            continue
        if file_path.endswith('_JEB3.c') or file_path.endswith('_retdec.c') or file_path.endswith(
                '_ida.c') or file_path.endswith('_new.c'):
            continue
        if os.path.exists(file_path[:-2]):
            continue
        if compile_single_file(file_path)[0] == 0:
            print(file + ' compiled')


time_cmd = Config.time_cmd


def add_extra_declarations(code_txt, error_msg):
    var_list = []
    reg_exp = r"error: ‘([a-z0-9]+)’ undeclared"  # match global var name
    pattern = re.compile(reg_exp)
    matches = pattern.finditer(error_msg)
    # get all undeclared vars
    for m in matches:
        var_name = m.group(1)

        if __name__ == '__main__':
            print('var name: ', var_name)
        var_list.append(var_name)
    if len(var_list) == 0:
        return code_txt

    # new declaration stmt
    decl_txt = '    unsigned int '
    for name in var_list:
        decl_txt += name
        if name != var_list[-1]:
            decl_txt += ', '
        else:
            decl_txt += ';\n'
    # insert into code_txt
    reg_exp = r"func_1\(void\)\s*{"  # match func_1
    pattern = re.compile(reg_exp)
    matches = pattern.finditer(code_txt)
    for m in matches:
        pos = m.end()
        new_txt = code_txt[:pos] + decl_txt + code_txt[pos:]
        return new_txt


def remove_unclear_member(code_txt, error_msg):
    new_txt = code_txt
    member_list = []
    reg_exp = r"error: request for member ‘([a-z0-9_]+)’ in something not a structure or union"  # match member name
    pattern = re.compile(reg_exp)
    matches = pattern.finditer(error_msg)
    # get all undeclared vars
    for m in matches:
        var_name = m.group(1)

        if __name__ == '__main__':
            print('var name: ', var_name)
        member_list.append(var_name)
    # simply delete unclear members
    for name in member_list:
        member_name = '.' + name
        new_txt = code_txt.replace(member_name, '')
    return new_txt

