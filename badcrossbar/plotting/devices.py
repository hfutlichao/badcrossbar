import badcrossbar.plotting.shapes as shapes
import numpy as np


def memristor(ctx, length=100, angle=0):
    """Draws a memristor.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    length : float, optional
        Total length of the memristor.
    angle : float, optional
        Angle in radians of the rotation of plane from the positive `x` axis
        towards positive `y` axis.
    """
    unit = length/14
    ctx.rotate(angle)
    shapes.line(ctx, 4 * unit)
    shapes.line(ctx, 1.5 * unit, -np.pi / 2)
    shapes.line(ctx, 2 * unit)
    shapes.line(ctx, 3 * unit, np.pi / 2)
    shapes.line(ctx, 2 * unit)
    shapes.line(ctx, 3 * unit, -np.pi / 2)
    shapes.line(ctx, 2 * unit)
    shapes.line(ctx, 1.5 * unit, np.pi / 2)
    shapes.line(ctx, 4 * unit)
    ctx.rotate(-angle)


def resistor_usa(ctx, length=100, angle=0):
    """Draws a resistor (USA version).

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    length : float, optional
        Total length of the resistor.
    angle : float, optional
        Angle in radians of the rotation of plane from the positive `x` axis
        towards positive `y` axis.
    """
    unit = length/14
    ctx.rotate(angle)
    zigzag_angle = 3*np.pi/8
    zigzag_length = unit/np.cos(zigzag_angle)
    shapes.line(ctx, 4 * unit)
    shapes.line(ctx, 0.5*zigzag_length, zigzag_angle)
    shapes.line(ctx, zigzag_length, -zigzag_angle)
    shapes.line(ctx, zigzag_length, zigzag_angle)
    shapes.line(ctx, zigzag_length, -zigzag_angle)
    shapes.line(ctx, zigzag_length, zigzag_angle)
    shapes.line(ctx, zigzag_length, -zigzag_angle)
    shapes.line(ctx, 0.5*zigzag_length, zigzag_angle)
    shapes.line(ctx, 4 * unit)
    ctx.rotate(-angle)


def resistor_europe(ctx, length=100, angle=0):
    """Draws a resistor (European version).

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    length : float, optional
        Total length of the resistor.
    angle : float, optional
        Angle in radians of the rotation of plane from the positive `x` axis
        towards positive `y` axis.
    """
    unit = length/14
    ctx.rotate(angle)
    shapes.line(ctx, 4*unit)
    ctx.rel_move_to(0, -unit)
    shapes.rectangle(ctx, 6*unit, 2*unit)
    ctx.rel_move_to(6*unit, unit)
    shapes.line(ctx, 4*unit)
    ctx.rotate(-angle)
