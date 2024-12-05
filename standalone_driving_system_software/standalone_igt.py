# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:13:58 2024

Author: ir. Margely Cornelissen, FUS Initiative, Radboud University

"""

# IGT example
# Note: you can click on each parameter to get more information


##############################################################################
# initialize logging.
##############################################################################

from fus_driving_systems.config.config import config_info as config

from fus_driving_systems.config.logging_config import initialize_logger

log_dir = "C://Temp"
filename = "standalone_igt"
logger = initialize_logger(log_dir, filename)

# When this code is embedded in other code with logging, ignore above commands and sync the logger
# in the following way:

# from fus_driving_systems.config.logging_config import sync_logger
# sync_logger(logger)  # logger needs to be created with logging.getLogger()

##############################################################################
# import the 'fus_driving_systems - sequence' into your code
##############################################################################

from fus_driving_systems import driving_system, transducer
from fus_driving_systems import sequence

##############################################################################
# create a sequence for an IGT driving system
# a sequence can be created in advance and a new sequence can be defined
# later on in the code
##############################################################################

seq1 = sequence.Sequence()

# Number of sequence starting at zero. Currently only used to differentiate and send multiple
# sequences to the IGT system. Only 0 and 1 are possible. Don't change this value if you only
# using one sequence definition.
seq1.seq_num = 0

# equipment
# to check available driving systems: print(driving_system.get_ds_serials())
# choose one driving system from that list as input
seq1.driving_sys = 'IGT-32-ch_comb_2x10-ch'
use_two_transducers = True  # is true if you are using two transducers simulateneously or interleaved

# to check available transducers: print(transducer.get_tran_serials())
# choose one transducer from that list as input
seq1.transducer = 'IS_PCD15287_01001'

# set general parameters
seq1.oper_freq = 300  # [kHz], operating frequency
seq1.focus = 40  # [mm], focal depth w.r.t. middle of the transducer bowl and FWHM

# Degree used to dephase every nth elemen based on chosen degree. None = no dephasing
# One value (>0) is the degree of dephasing, for example [90] with 4 elements: 1 elem: 0 dephasing,
# 2 elem: 90 dephasing, 3 elem: 180 dephasing, 4 elem: 270 dephasing.
# When the amount of values match the amount of elements, it will override the calculated phases
# based on the set focus.
seq1.dephasing_degree = None  # [degrees]: None, [120] or [0, 135, 239, 90]

# THE FEATURE IS NOT ENABLED YET! Use amplitude only for now
# either set maximum pressure in free water [MPa], voltage [V] or amplitude [%]
# seq1.press = 1  # [MPa], maximum pressure in free water
# seq1.volt = 0  # [V], voltage per channel
seq1.ampl = 10  # [%], amplitude. NOTE: DIFFERENT THAN SC

seq2 = None  # seq2 is None of a second transducer isn't used
if use_two_transducers:
    seq2 = sequence.Sequence()

    seq2.driving_sys = seq1.driving_sys.serial

    # to check available transducers: print(transducer.get_tran_serials())
    # choose one transducer from that list as input
    seq2.transducer = 'IS_PCD15287_01002'

    # set general parameters
    seq2.oper_freq = 300  # [kHz], operating frequency
    seq2.focus = 80  # [mm], focal depth w.r.t. middle of the transducer bowl and FWHM

    # Degree used to dephase every nth elemen based on chosen degree. None = no dephasing
    # One value (>0) is the degree of dephasing, for example [90] with 4 elements: 1 elem: 0
    # dephasing. 2 elem: 90 dephasing, 3 elem: 180 dephasing, 4 elem: 270 dephasing.
    # When the amount of values match the amount of elements, it will override the calculated phases
    # based on the set focus.
    seq2.dephasing_degree = None  # [degrees]: None, [120] or [0, 135, 239, 90]

    # THE FEATURE IS NOT ENABLED YET! Use amplitude only for now
    # either set maximum pressure in free water [MPa], voltage [V] or amplitude [%]
    # seq2.press = 1  # [MPa], maximum pressure in free water
    # seq2.volt = 0  # [V], voltage per channel
    seq2.ampl = 10  # [%], amplitude. NOTE: DIFFERENT THAN SC

# # timing parameters # #
# you can use the TUS Calculator to visualize the timing parameters:
# https://www.socsci.ru.nl/fusinitiative/tuscalculator/

# ## pulse ## #
seq1.pulse_dur = 10  # [ms], pulse duration
seq1.pulse_rep_int = 200  # [ms], pulse repetition interval

# pulse ramping
# to check available ramp shapes: print(seq.get_ramp_shapes())
# choose one ramp shape from that list as input
seq1.pulse_ramp_shape = 'Rectangular - no ramping'

# ramping up and ramping down duration are equal and are equal to ramp duration
seq1.pulse_ramp_dur = 0  # [ms], ramp duration, with at least 70 us between ramping up and down

# ## pulse train ## #
# if you only want one pulse train, keep the values equal to the pulse repetition interval
seq1.pulse_train_dur = 200  # [ms], pulse train duration

# set wait_for_trigger to true if you want to use trigger
seq1.wait_for_trigger = True

# When you only want to trigger a pulse train repetition once: 'TriggerOnePulseTrainRepetition'
# Multiple times triggering a pulse train repetition isn't supported.
# to check available trigger options: print(seq1.get_trigger_options())
seq1.trigger_option = 'TriggerSequence'

if seq1.wait_for_trigger and seq1.trigger_option == config['General']['Trigger option.seq']:
    seq1.n_triggers = 4  # number of timings above defined sequence will be triggered

else:
    seq1.pulse_train_rep_int = 200  # [ms], pulse train repetition interval, NOTE: DIFFERENT THAN SC

    # ## pulse train repetition ## #
    # if you only want one pulse train, keep the value equal to the pulse repetition interval
    # if you only want one pulse train repetition block, keep the value equal to the pulse train
    # repetition interval
    seq1.pulse_train_rep_dur = 2  # [s], pulse train repetition duration, NOTE: DIFFERENT THAN SC

# to get a summary of your entered sequence: print(seq1)

##############################################################################
# connect with driving system and execute sequence
##############################################################################

# creating an IGT driving system instance, connecting to it and sending your first sequence can be
# done when initializing your experiment. When appropriate, execute your sequence by implementing
# 'execute_sequence()' into your code or by using the external trigger.

# when you want to change your sequence in the middle of your experimental code, create a new
# sequence as above and send the new sequence: 'send_sequence()'. When appropriate, execute your
# sequence by implementing 'execute_sequence()' into your code or by using the external trigger.

##############################################################################
# import the 'fus_driving_systems - ds' into your code
##############################################################################

from fus_driving_systems.igt import igt_ds

igt_driving_sys = igt_ds.IGT(log_dir)

try:
    igt_driving_sys.connect(seq1.driving_sys.connect_info, log_dir, filename)

    # you can check if the system is still connected by using the following:
    # print(igt_ds.is_connected())

    igt_driving_sys.send_sequence(seq1, seq2)

    # If wait_for_trigger is true, only the sequence is sent and will be executed by the external
    # trigger
    if seq1.wait_for_trigger:
        igt_driving_sys.wait_for_trigger(seq1, seq2)

    # If wait_for_trigger is false, the sequence is sent and can be executed directly using the
    # execute_sequence() function
    else:
        igt_driving_sys.execute_sequence(seq1, seq2)

finally:
    # When the sequence is executed using execute_sequence(), the system will be disconnected
    # automatically. In the case your code is stopped abruptly, the driving system will be
    # disconnected. Otherwise, there is a change that it keeps on firing ultrasound sequences.
    # When using the external trigger, disconnect the driving system yourself.
    if not seq1.wait_for_trigger:
        igt_driving_sys.disconnect()
