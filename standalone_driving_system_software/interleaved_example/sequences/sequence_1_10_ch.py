# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:22:51 2024

Author: ir. Margely Cornelissen, FUS Initiative, Radboud University

"""

##############################################################################
# import the 'fus_driving_systems - sequence' into your code
##############################################################################

import sys


from fus_driving_systems.config.config import config_info as config
from fus_driving_systems import driving_system, transducer
from fus_driving_systems import sequence


def create_sequence_collection(logger):
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

    # NOTE: Due to compensation equations, the focus has to be set first when using amplitude or
    # voltage as power input.
    seq1.focus_wrt_exit_plane = 40  # [mm], focal depth w.r.t. the exit plane and FWHM middle

    # Degree used to dephase every nth elemen based on chosen degree. None = no dephasing
    # One value (>0) is the degree of dephasing, for example [90] with 4 elements: 1 elem: 0 dephasing,
    # 2 elem: 90 dephasing, 3 elem: 180 dephasing, 4 elem: 270 dephasing.
    # When the amount of values match the amount of elements, it will override the calculated phases
    # based on the set focus.
    seq1.dephasing_degree = None  # [degrees]: None, [120] or [0, 135, 239, 90]

    # THE FEATURE IS NOT ENABLED YET! Use amplitude only for now
    # either set maximum pressure in free water [MPa], voltage [V] or amplitude [%]
    seq1.press = 0.5  # [MPa], maximum pressure in free water
    # seq1.volt = 0  # [V], voltage per channel
    # seq1.ampl = 10  # [%], amplitude. NOTE: DIFFERENT THAN SC

    seq2 = None  # seq2 is None of a second transducer isn't used
    if use_two_transducers:
        seq2 = sequence.Sequence()

        seq2.driving_sys = seq1.driving_sys.serial

        # to check available transducers: print(transducer.get_tran_serials())
        # choose one transducer from that list as input
        seq2.transducer = 'IS_PCD15287_01002'

        # Check if available channels is equal to the number of elements of the transducers combined
        n_comb_elem = seq1.transducer.elements + seq2.transducer.elements
        if seq1.driving_sys.available_ch != n_comb_elem:
            logger.error(f'Number of available channels ({seq1.driving_sys.available_ch}) is not ' +
                         'equal to the number of elements of the transducers combined (' +
                         f'{n_comb_elem}). Equipment configuration {seq1.driving_sys.name} - ' +
                         f'{seq1.transducer.name} & {seq2.transducer.name} does ' +
                         'not seem to be compatible or use_two_transducers is incorrectly True.')
            sys.exit()

        # set general parameters
        seq2.oper_freq = 300  # [kHz], operating frequency

        # NOTE: Due to compensation equations, the focus has to be set first when using amplitude or
        # voltage as power input.
        seq2.focus_wrt_exit_plane = 80  # [mm], focal depth w.r.t. the exit plane and FWHM middle

        # Degree used to dephase every nth elemen based on chosen degree. None = no dephasing
        # One value (>0) is the degree of dephasing, for example [90] with 4 elements: 1 elem: 0
        # dephasing. 2 elem: 90 dephasing, 3 elem: 180 dephasing, 4 elem: 270 dephasing.
        # When the amount of values match the amount of elements, it will override the calculated phases
        # based on the set focus.
        seq2.dephasing_degree = None  # [degrees]: None, [120] or [0, 135, 239, 90]

        # THE FEATURE IS NOT ENABLED YET! Use amplitude only for now
        # either set maximum pressure in free water [MPa], voltage [V] or amplitude [%]
        seq2.press = 0  # [MPa], maximum pressure in free water
        # seq2.volt = 0  # [V], voltage per channel
        # seq2.ampl = 0  # [%], amplitude. NOTE: DIFFERENT THAN SC

    # Check if available channels is equal to the number of elements of the transducer
    elif seq1.driving_sys.available_ch != seq1.transducer.elements:
        logger.error(f'Number of available channels ({seq1.driving_sys.available_ch}) is not ' +
                     'equal to the number of elements of the transducer (' +
                     '{seq1.transducer.elements}). Equipment configuration ' +
                     f'{seq1.driving_sys.name} - {seq1.transducer.name} does not seem to be ' +
                     'compatible or use_two_transducers is incorrectly False.')
        sys.exit()

    # # timing parameters # #
    # you can use the TUS Calculator to visualize the timing parameters:
    # https://www.socsci.ru.nl/fusinitiative/tuscalculator/

    # Compensate for delay measured with PicoScope
    interleave_diff = 13.9  # [ms]

    # ## pulse ## #
    seq1.pulse_dur = 45  # [ms], pulse duration
    seq1.pulse_rep_int = 100 - interleave_diff  # [ms], pulse repetition interval

    # pulse ramping
    # to check available ramp shapes: print(seq1.get_ramp_shapes())
    # choose one ramp shape from that list as input
    seq1.pulse_ramp_shape = 'Tukey'

    # ramping up and ramping down duration are equal and are equal to ramp duration
    seq1.pulse_ramp_dur = 5  # [ms], ramp duration, with at least 70 us between ramping up and down

    # ## pulse train ## #
    # if you only want one pulse train, keep the values equal to the pulse repetition interval
    seq1.pulse_train_dur = 100 - interleave_diff  # [ms], pulse train duration

    # set wait_for_trigger to true if you want to use trigger
    seq1.wait_for_trigger = False

    # When you only want to trigger a pulse train repetition once: 'TriggerOnePulseTrainRepetition'
    # Multiple times triggering a pulse train repetition isn't supported.
    # to check available trigger options: print(seq1.get_trigger_options())
    seq1.trigger_option = 'TriggerSequence'
    if seq1.wait_for_trigger and seq1.trigger_option == config['General']['Trigger option.seq']:
        seq1.n_triggers = 4  # number of timings above defined sequence will be triggered

    else:
        seq1.pulse_train_rep_int = 100 - interleave_diff  # [ms], pulse train repetition interval, NOTE: DIFFERENT THAN SC

        # ## pulse train repetition ## #
        # if you only want one pulse train, keep the value equal to the pulse repetition interval
        # if you only want one pulse train repetition block, keep the value equal to the pulse train
        # repetition interval
        seq1.pulse_train_rep_dur = (100 - interleave_diff) / 1000  # [s], pulse train repetition duration, NOTE: DIFFERENT THAN SC

    # to get a summary of your entered sequence: print(seq1)

    return seq1, seq2