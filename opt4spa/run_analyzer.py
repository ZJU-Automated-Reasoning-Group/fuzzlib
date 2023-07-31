# coding: utf-8
"""
This is a script for testing (showing the use of our APIs to run a set of bitcode files)
"""
import logging

from opt4spa.config import m_tool
from opt4spa.utils import run_cmd, is_bc_or_ll_file

g_analyzer_timeout = 43200  # 12 hours

middle_bc_files = [
    "~/data/BC/Open/imagemagick.bc",
    "~/data/BC/Open/swoole.bc",
]


def run_analyzer(bc: str) -> float:
    # m_tool is the program analyzer
    try:
        cmd_tool = [i for i in m_tool]
        cmd_tool.append(bc)
        logging.info(cmd_tool)
        duration = run_cmd(cmd_tool, g_analyzer_timeout)
        if duration >= g_analyzer_timeout:
            return 4294967295.0
        return duration
    except Exception as ex:
        print(ex)
        return 4294967295.0


def run_tests(bc_files):
    for bc in bc_files:
        if is_bc_or_ll_file(bc):
            print("Starting to analyze", bc)
            time = run_analyzer(bc)
            output_filename = "regression.txt"
            with open(output_filename, mode="a") as file:
                file.write("{}: {}\n".format(bc, time))
                file.close()
        else:
            print(bc, "is not a bitcode file!!!")
    print("Good bye!")
