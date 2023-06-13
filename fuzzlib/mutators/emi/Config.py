####################################################################################
#
# Please update these absolute paths below before use
#
####################################################################################

# Absolute path to csmith runtime directory
runtime_dir = '/home/homework/DecFuzzer/runtime'
csmith_absolute_path = '/home/fuzz/Documents/csmith-2.3.0/src/csmith'  #

####################################################################################
#
# Please do not modify anything below unless you are clear about what is it used for
#
####################################################################################
probability_live_code_mutate = 0.3

timeout_sec = 2

replaced_func_name = 'func_1'

time_cmd = "time -p "

# this csmith command is not used in the Artifact Evaluation Package
csmith_cmd = (csmith_absolute_path + " "
                                     " --no-arrays"
                                     " --no-structs"
                                     " --no-unions"
                                     " --no-safe-math"
                                     " --no-pointers"
                                     " --no-longlong"
                                     " --max-funcs 1"
                                     " --max-expr-complexity 5"
              # " --max-expr-complexity 10" # too complicated to analyse?
              )

compile_cmd = 'gcc -fno-stack-protector -no-pie -O0 -w -m32 '

# CFG_measurer
gcc_cfg_option = ' -fdump-tree-cfg '
cfg_suffix = '.011t.cfg'


def get_live_code_mutate():
    global probability_live_code_mutate
    return probability_live_code_mutate


def set_live_code_mutate(value):
    global probability_live_code_mutate
    probability_live_code_mutate = value
