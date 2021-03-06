from badcrossbar import check, computing, utils


def compute(
        applied_voltages, resistances, r_i=None,
        r_i_word_line=None, r_i_bit_line=None, **kwargs):
    """Computes branch currents and node voltages of a crossbar.

    Parameters
    ----------
    applied_voltages : array_like
        Applied voltages. Voltages must be supplied in an array of shape `m x
        p`, where `m` is the number of word lines and `p` is the number of
        examples (sets of voltages applied one by one).
    resistances : array_like
        Resistances of crossbar devices. Resistances must be supplied in an
        array of shape `m x n`, where `n` is the number of bit lines.
    r_i : int or float, optional
        Interconnect resistance of the word and bit line segments. If None,
        `r_i_word_line` and `r_i_bit_line` are used instead.
    r_i_word_line : int or float, optional
        Interconnect resistance of the word line segments.
    r_i_bit_line : int or float, optional
        Interconnect resistance of the bit line segments.
    **kwargs
        node_voltages : bool, optional
            If False, None is returned instead of node voltages.
        all_currents : bool, optional
            If False, only output currents are returned, while all the other
            ones are set to None.
        verbose : {1, 2, 0}, optional
            If 1, all messages are shown. If 2, only warnings are shown. If
            0, no messages are shown.
        show_time : bool, optional
            If True, includes current time when the messages are printed.
        gap_size : int, optional
            Number of whitespace characters to be printed between current
            time and the message.

    Returns
    -------
    named tuple
        Branch currents and node voltages of the crossbar. Field `currents`
        is a named tuple itself with fields `output`, `device`, `word_line`
        and `bit_line` and contains output currents, as well as currents
        flowing through the devices and interconnect segments of the word and
        bit lines. Field `voltages` is a named tuple itself with fields
        `word_line` and `bit_line` and contains the voltages at the nodes on
        the word and bit lines. `currents.output` is an array of shape `p x n`,
        while all the others are arrays of shape `m x n` if `p == 1`,
        or arrays of shape `m x n x p` if `p > 1`.
    """
    kwargs.setdefault('node_voltages', True)
    kwargs.setdefault('all_currents', True)
    kwargs.setdefault('verbose', 1)
    kwargs.setdefault('show_time', True)
    kwargs.setdefault('gap_size', 5)

    if r_i is not None:
        r_i_word_line = r_i_bit_line = r_i

    resistances, applied_voltages = check.crossbar_requirements(
        resistances, applied_voltages, r_i_word_line, r_i_bit_line)

    utils.message('Initialising simulation.', **kwargs)

    solution = computing.extract.solution(
            resistances, r_i_word_line, r_i_bit_line,
            applied_voltages, **kwargs)

    return solution
