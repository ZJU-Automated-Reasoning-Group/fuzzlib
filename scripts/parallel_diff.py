# coding: utf-8
"""
Parallel differential testing framework
- comparing the stdout +stderr

NOTE:
- Use Python3.7+

python3.7 parallel_diff.py --oytput /tmp/res --workers 8


TODO: this should work as a common library
"""

import os
import subprocess
import argparse
import shutil
import sys
from multiprocessing.pool import Pool
import signal
from threading import Timer
import logging
from os.path import dirname, abspath

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', type=str)
parser.add_argument('--output', dest='output', default='/tmp/res-fuzz', type=str)
parser.add_argument('--timeout', dest='timeout', default=10, type=int, help="timeout for each solving")
parser.add_argument('--count', dest='count', default=1000, type=int, help="counts for each combination")
parser.add_argument('--workers', dest='workers', default=1, type=int, help="num threads")
parser.add_argument('--config', dest='config', default='no', type=str)

args = parser.parse_args()
m_num_process = args.workers  # thread


# Examples:
m_tools = [
    'toola',
    'toolb --xx',
]

# Input generator
parent_dir = dirname(dirname(abspath(__file__)))
generator = parent_dir + ''

in_dir = args.input
out_dir = args.output
timeout = args.timeout
count = args.count

shutil.rmtree(out_dir)
os.mkdir(out_dir)

crashes = out_dir + '/crash'
inputs = out_dir + '/input'
os.mkdir(crashes)
os.mkdir(inputs)


def terminate(process, is_timeout):
    if process.poll() is None:
        try:
            process.terminate()
            is_timeout[0] = True
        except Exception as e:
            print("error for interrupting")
            print(e)


def work(idt):
    counter = 0
    while True:
        try:
            if counter % count == 0:
                logger.debug("enter parameter generations")
                counter = 0
            name = '/diff_input-' + str(idt) + "_" + str(counter) + '.smt2'
            tmp_file = inputs + name

            counter += 1
            # TODO: the generator can be binary files
            cmd = ['python3', generator]

            logger.debug("Enter constraint generation")
            logger.debug("{}".format(cmd))
            p_gene = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            is_timeout_gene = [False]
            timer_gene = Timer(15, terminate, args=[p_gene, is_timeout_gene])
            timer_gene.start()
            out_gene = p_gene.stdout.readlines()
            out_gene = ' '.join([str(element.decode('UTF-8')) for element in out_gene])
            f = open(tmp_file, 'w')
            f.write(out_gene)
            f.close()
            p_gene.stdout.close()  # close?
            timer_gene.cancel()

            if os.stat(tmp_file).st_size == 0: print("tmp file empty")
            logger.debug("{}".format(tmp_file))

            m_res = []
            for _ in m_tools:
                m_res.append('unknown')

            m_res_out = []

            for tool in m_tools:
                cmd_tool = []
                for cc in tool.split(' '):
                    cmd_tool.append(cc)

                cmd_tool.append(tmp_file)
                logger.debug(cmd_tool)
                logger.debug(tool)
                logger.debug(" start to solve")
                ptool = subprocess.Popen(cmd_tool, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                is_timeout = [False]
                timertool = Timer(45, terminate, args=[ptool, is_timeout])
                timertool.start()
                out_tool = ptool.stdout.readlines()
                out_tool = ' '.join([str(element.decode('UTF-8')) for element in out_tool])
                logger.debug(out_tool)

                if not is_timeout[0]:  # do not add timeout case
                    # TODO: keep unknown for finding performance issues
                    bl_msg = ['suppress', 'unknown', 'ASSERTION', 'Assertion', 'error', 'Fatal', 'inv']
                    toadd = True
                    for bl in bl_msg:
                        if bl in out_tool:
                            toadd = False
                            break
                    if toadd: m_res_out.append(out_tool)
                # close?
                ptool.stdout.close()
                timertool.cancel()

            logger.debug("Results: ")
            # decide if the elements of the list are equal (solving results are identical)
            if 2 <= len(m_res_out) != m_res_out.count(m_res_out[0]):
                print("find inconsistency!")
                # TODO: print the info. of the solvers
                shutil.copyfile(tmp_file, crashes + name)
            else:
                os.remove(tmp_file)
        except Exception as e:
            # remove file?
            print(e)
    print("We are finish here, have a good day!")


tp = Pool(m_num_process)


def signal_handler(sig, frame):
    tp.terminate()
    print("We are finish here, have a good day!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

for i in range(m_num_process):
    tp.apply_async(work, (i,))
tp.close()
tp.join()
