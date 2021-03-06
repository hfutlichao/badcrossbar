import numpy as np
from badcrossbar import utils


def crossbar_requirements(resistances, applied_voltages,
                          r_i_word_line, r_i_bit_line, **kwargs):
    """Checks if crossbar variables satisfy all requirements.

    Parameters
    ----------
    resistances : array_like
        Resistances of crossbar devices.
    applied_voltages : array_like
        Applied voltages.
    r_i_word_line : any
        Interconnect resistance of the word line segments.
    r_i_bit_line : any
        Interconnect resistance of the bit line segments.

    Returns
    -------
    ndarray
        Potentially modified (converted to `ndarray`) resistances and applied
        voltages.
    """
    resistances, applied_voltages = (np.array(i) for i in
                                     (resistances, applied_voltages))
    for value, name in ((resistances, 'resistances'),
                        (applied_voltages, 'applied_voltages')):
        n_dimensional(value, [2], name)
        numeric_array(value, name)
        non_empty(value, name)

    non_negative_array(resistances, 'resistances')
    match_shape(resistances=(resistances, 0),
                applied_voltages=(applied_voltages, 0))

    for value, name in ((r_i_word_line, 'r_i_word_line'),
                        (r_i_bit_line, 'r_i_bit_line')):
        if r_i_word_line == r_i_bit_line:
            name = 'r_i'
        number(value, name)
        non_negative_number(value, name)

    short_circuit(resistances, r_i_word_line, r_i_bit_line)

    return resistances, applied_voltages


def plotting_requirements(device_branch_vals=None, word_line_branch_vals=None,
                          bit_line_branch_vals=None, word_line_node_vals=None,
                          bit_line_node_vals=None, branches=True):
    """Checks if arrays containing branch or node values satisfy all
    requirements.

    Parameters
    ----------
    device_branch_vals : ndarray or None, optional
        Values associated with crossbar devices.
    word_line_branch_vals : ndarray or None, optional
        Values associated with the interconnect segments along the word lines.
    bit_line_branch_vals : ndarray or None, optional
        Values associated with the interconnect segments along the bit lines.
    word_line_node_vals : ndarray or None, optional
        Values associated with the nodes on the word lines.
    bit_line_node_vals : ndarray or None, optional
        Values associated with the nodes on the bit lines.
    branches : bool, optional
        If True, it is assumed that branch values are passed. Otherwise,
        node values are expected.

    Returns
    -------
    ndarray
        Potentially modified (converted to `ndarray`) branch or nodes values.
    """
    if branches:
        valid_arrays = not_none(device_branch_vals=device_branch_vals,
                                word_line_branch_vals=word_line_branch_vals,
                                bit_line_branch_vals=bit_line_branch_vals)
    else:
        valid_arrays = not_none(word_line_node_vals=word_line_node_vals,
                                bit_line_node_vals=bit_line_node_vals)
    valid_arrays = {key: np.array(value) for key, value in
                    valid_arrays.items()}

    for key, value in valid_arrays.items():
        numeric_array(valid_arrays[key], key)
        non_empty(valid_arrays[key], key)
        n_dimensional(valid_arrays[key], [2, 3], key)
        valid_arrays[key] = utils.average_if_3D(valid_arrays[key])
        non_infinite_array(valid_arrays[key], key)

    if len(valid_arrays) != 1:
        for dim in [0, 1]:
            dim_arrays = {key: (value, dim)
                          for key, value in valid_arrays.items()}
            match_shape(**dim_arrays)

    if branches:
        return valid_arrays.get('device_branch_vals'), \
            valid_arrays.get('word_line_branch_vals'),\
            valid_arrays.get('bit_line_branch_vals')
    else:
        return valid_arrays.get('word_line_node_vals'), \
            valid_arrays.get('bit_line_node_vals')


def not_none(**kwargs):
    """Confirms that at least one of the items is not None.

    Parameters
    ----------
    **kwargs : dict of any, optional
        Items of arbitrary type.

    Returns
    -------
    dict of any
        Items that are not None.

    Raises
    -------
    ValueError
        If all of the items are None.
    """
    valid_items = {}
    all_none = True
    for key, value in kwargs.items():
        if value is not None:
            all_none = False
            valid_items[key] = value
    if all_none:
        raise ValueError('At least one of {{{}}} should be not None!'.format(
            ', '.join(kwargs)))

    return valid_items


def n_dimensional(array, n_list=[2], name='array'):
    """Checks that array is `n`-dimensional.

    Parameters
    ----------
    array : ndarray
        Array.
    n_list : list of int, optional
        Possible number of dimensions.
    name : str, optional
        Name of the variable.

    Raises
    -------
    TypeError
        If array is not `n`-dimensional.
    """
    dim = array.ndim
    if dim not in n_list:
        err_msg = '\'{}\' should be {}-dimensional array! Instead received ' \
                  '{}-dimensional array.'
        if len(n_list) == 1:
            n_list_str = str(n_list[0])
        else:
            n_list_str = '- or '.join([str(i) for i in n_list])

        raise TypeError(err_msg.format(name, n_list_str, dim))


def numeric_array(array, name='array'):
    """Checks that array only contains numbers.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str, optional
        Name of the array.

    Raises
    -------
    TypeError
        If array contains non-number elements.
    """
    if np.issubdtype(array.dtype, np.number) is False:
        raise TypeError('\'{}\' should only contain numbers!'.format(name))


def non_empty(array, name='array'):
    """Checks that array is not empty.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str, optional
        Name of the array.

    Raises
    -------
    ValueError
        If the array is empty.
    """
    if array.size == 0:
        raise ValueError('\'{}\' array is empty!'. format(name))


def match_shape(**kwargs):
    """Checks if arrays have matching dimensions.

    Parameters
    ----------
    **kwargs : dict of tuple of (ndarray and int)
        Arrays and the dimension along which they should be matched.

    Raises
    -------
    ValueError
        If any of the arrays do not match specified dimensions.
    """
    first_key = list(kwargs.keys())[0]
    first_value = list(kwargs.values())[0]
    dim = first_value[0].shape[first_value[1]]
    for key, value in kwargs.items():
        if value[0].shape[value[1]] != dim:
            raise ValueError(
                'Dimension {} of array \'{}\' should match dimension {} of '
                'array \'{}\'!'.format(value[1], key, first_value[1], first_key)
            )


def non_negative_array(array, name='array'):
    """Checks if all the elements of the array are non-negative.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str, optional
        Name of the array.

    Raises
    -------
    ValueError
        If the array contains negative values.
    """
    if (array < 0).any():
        raise ValueError(
            '\'{}\' array contains at least one negative value!'.format(name))


def non_infinite_array(array, name='array'):
    """Checks if all the elements of the array are non-infinite.

    Parameters
    ----------
    array : ndarray
        Array.
    name : str, optional
        Name of the array.

    Raises
    -------
    ValueError
        If the array contains positive or negative infinities.
    """
    if (array == np.inf).any() or (array == -np.inf).any():
        raise ValueError(
            '\'{}\' array contains at least one value with infinite '
            'magnitude!'.format(name))


def number(value, name='variable'):
    """Checks if the variable is a number.

    Parameters
    ----------
    value : any
        Variable of arbitrary type.
    name : str, optional
        Name of the variable.

    Raises
    -------
    TypeError
        If the variable is not int or float.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            'Type {} of \'{}\' is not supported. Use int or '
            'float instead.'.format(type(value).__name__, name))


def non_negative_number(value, name='number'):
    """Checks if the number is negative.

    Parameters
    ----------
    value : int or float
        Number.
    name : str, optional
        Name of the number.

    Raises
    -------
    ValueError
        If the number is negative.
    """
    if value < 0:
        raise ValueError('\'{}\' is negative!'. format(name))


def short_circuit(resistances, r_i_word_line, r_i_bit_line):
    """Checks if crossbar will be short-circuited.

    This refers to a theoretical scenario when there exists a path of zero
    resistance in a crossbar.

    Parameters
    ----------
    resistances : ndarray
        Resistances of crossbar devices.
    r_i_word_line : int or float
        Interconnect resistance of the word line segments.
    r_i_bit_line : int or float
        Interconnect resistance of the bit line segments.

    Raises
    -------
    ValueError
        If any of the devices have zero resistance.
    """

    if 0 in resistances:
        if r_i_word_line == r_i_bit_line == 0:
            err_txt = 'At least some crossbar devices have zero resistance ' \
                      'causing short circuit!'
        else:
            err_txt = 'At least some crossbar devices have zero resistance! ' \
                      'This is not currently supported even if it does not ' \
                      'cause short circuit.'
        raise ValueError(err_txt)
