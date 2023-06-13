#!/usr/bin/python3
import subprocess
import os

from fuzzlib.mutators.emi import EMI_generator, generator, replacer, checker, Config

file_count = 0
EMI_count = 0
total_real_time = 0
total_user_time = 0
total_sys_time = 0


def get_config(config_file):
    global file_count, EMI_count, total_real_time, total_user_time, total_sys_time
    isExists = os.path.exists(config_file)
    if not isExists:
        return
    f = open(config_file)
    if f:
        conf_txt = f.read()
    else:
        return
    f.close()
    pos = conf_txt.find('file_count: ')
    if pos != -1:
        count_txt = conf_txt[pos:]
        count_txt = count_txt[:count_txt.find('\n')]
        count_txt = count_txt.replace('file_count: ', '').strip(' \n')
        file_count = int(count_txt)

    if conf_txt.find('EMI_count: ') != -1:
        emi_count_txt = conf_txt[conf_txt.find('EMI_count: ') + 11:].split('\n')[0].strip(' \n')
        EMI_count = int(emi_count_txt)
    if conf_txt.find('total_real_time: ') != -1:
        real_txt = conf_txt[conf_txt.find('total_real_time: ') + 17:].split('\n')[0].strip(' \n')
        total_real_time = float(real_txt)
    if conf_txt.find('total_user_time: ') != -1:
        user_txt = conf_txt[conf_txt.find('total_user_time: ') + 17:].split('\n')[0].strip(' \n')
        total_user_time = float(user_txt)
    if conf_txt.find('total_sys_time: ') != -1:
        sys_txt = conf_txt[conf_txt.find('total_sys_time: ') + 16:].split('\n')[0].strip(' \n')
        total_sys_time = float(sys_txt)


def set_config(config_file):
    global file_count, EMI_count, total_real_time, total_user_time, total_sys_time
    f = open(config_file, 'w')
    f.write('file_count: ' + str(file_count) + '\n')
    f.write('EMI_count: ' + str(EMI_count) + '\n')
    f.write('total_real_time: ' + str(total_real_time) + '\n')
    f.write('total_user_time: ' + str(total_user_time) + '\n')
    f.write('total_sys_time: ' + str(total_sys_time) + '\n')
    f.close()


def copy_file(src, dst):
    sta, out = subprocess.getstatusoutput('cp ' + src + ' ' + dst)
    return sta, out


# This function is a little dangerous
# WASTED
def remove_all_file(directory):
    """remove all files except .txt files in this directory"""
    rm_cmd = "rm `ls | grep -v .txt`"
    cmd = "cd " + directory + "; " + rm_cmd
    sta, out = subprocess.getstatusoutput(cmd)
    return sta, out


def remove_file(file):
    sta, out = subprocess.getstatusoutput('rm ' + file)
    return sta, out


def remove_files(file_path, modified_file):
    # remove source files in this turn
    remove_file(file_path)
    # remove_file(modified_file)  # keep modified source code for debug
    remove_file(modified_file[:-2] + '_JEB3.c')
    remove_file(modified_file[:-2] + '_new.c')
    remove_file(modified_file[:-2] + '_new_nou.c')  # maybe
    # remove compiled files in this turn
    remove_file(file_path[:-2])
    remove_file(modified_file[:-2])
    remove_file(modified_file[:-2] + '_new')
    remove_file(modified_file[:-2] + '_new_nou')  # maybe


# -----------------------------------------------------------------------------------
# core functions: <test_single_file>, <recompile_single_file>, <generate_emi_variants>
# -----------------------------------------------------------------------------------

def append_to_file(file_path, append_str):
    f = open(file_path, 'a')
    f.write(append_str)
    f.close()


def generate_emi_variants(number_of_var, file_path, emi_dir):
    global EMI_count
    if number_of_var > 0:
        emi = EMI_generator.EMIWrapper(file_path)

        print('about %d variants will be generated, they are:' % int(number_of_var))
        variant_log_file_path = os.path.join(emi_dir, 'variant_log.txt')
        append_to_file(variant_log_file_path,
                       'about %d variants will be generated, they are:' % int(number_of_var) + '\n')
        for i in range(int(number_of_var)):
            status, variant_txt = emi.gen_a_new_variant()
            if status == -1:
                break
            if status != 0:
                continue

            variant_name = str(EMI_count) + '.c'
            EMI_count += 1
            variant_path = os.path.join(emi_dir, variant_name)
            f = open(variant_path, 'w')
            if f:
                f.write(variant_txt)
                f.close()
            print(variant_path, ' is generated')
            variant_log_file_path = os.path.join(emi_dir, 'variant_log.txt')
            append_to_file(variant_log_file_path, variant_path + ' is generated\n')

            # try to avoid redundant variants, too
            if emi.AP.dis_new == emi.AP.dis_old:
                print('variant has the same distance as old one, break')
                print('dis_new', str(emi.AP.dis_new), 'dis_old', str(emi.AP.dis_old))
                break
            if emi.AP.dis_new <= emi.AP.dis_old - 3:
                print(str(emi.AP.dis_new), '<=', str(emi.AP.dis_old), '- 3, break')
                break


def create_directory(directory):
    if os.path.exists(directory):
        return
    os.mkdir(directory)


def prepare_dirs(files_dir, emi=False):
    create_directory(files_dir)
    error_dir = os.path.join(files_dir, 'error/')
    create_directory(error_dir)
    result_dir = os.path.join(files_dir, 'result/')
    create_directory(result_dir)
    if emi:
        emi_dir = os.path.join(files_dir, 'emi/')
        create_directory(emi_dir)
