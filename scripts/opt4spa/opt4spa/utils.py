# coding: utf-8
import os
import os.path
import resource
import subprocess
import time
# import logging
import uuid
from threading import Timer
from typing import List


def get_unique_id():
    """Get a unique ID"""
    return uuid.uuid4().int


def is_bc_or_ll_file(name):
    """Decide whether name is LLVM IR"""
    ext = os.path.splitext(name)[1]
    return ext == '.bc' or ext == '.ll'


def limit_memory(maxsize, hardmax=resource.RLIM_INFINITY):
    # soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hardmax))


def terminate(process, is_timeout):
    """
    Callback for timeout:
       terminate the process and set is_timeout[0] to True
    """
    if process.poll() is None:
        try:
            process.terminate()
            is_timeout[0] = True
        except Exception as e:
            print("error for interrupting")
            print(e)


def isexec(fpath):
    """Decide whether fpath is exec or not"""
    if fpath is None:
        return False
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def run_cmd(cmd_tool: List, timeout=300):
    """Run a command within a time limit"""
    out_tool = None
    try:
        time_start = time.time()
        ptool = subprocess.Popen(cmd_tool, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # start_time = time.time()
        is_timeout = [False]
        timer = Timer(timeout, terminate, args=[ptool, is_timeout])
        timer.start()
        out_tool = ptool.stdout.readlines()
        out_tool = ' '.join([str(element.decode('UTF-8')) for element in out_tool])
        ptool.stdout.close()
        timer.cancel()
        return time.time() - time_start
    except Exception as ex:
        print(ex)
        print(out_tool)
        # return out_tool?
        return -1


def which(program):
    if isinstance(program, str):
        choices = [program]
    else:
        choices = program

    for p in choices:
        fpath, _ = os.path.split(p)
        if fpath:
            if isexec(p):
                return p
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, p)
                if isexec(exe_file):
                    return exe_file
    return None
