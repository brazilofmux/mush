# Math and Logic Functions

## Overview

Math and logic functions perform arithmetic, trigonometric, and bitwise
operations on numeric values. MUSH arithmetic operates on both integers and
floating-point numbers. Integer operations that would produce fractional
results are truncated unless a floating-point variant is used.

All numeric functions return `#-1` or an error string on invalid input (such
as non-numeric arguments or division by zero) unless otherwise specified.

## Basic Arithmetic

### add()

```
add(<number>, <number>, ...)
```

Returns the sum of all arguments. Accepts two or more arguments.

### sub()

```
sub(<number1>, <number2>)
```

Returns \<number1\> minus \<number2\>.

### mul()

```
mul(<number>, <number>, ...)
```

Returns the product of all arguments. Accepts two or more arguments.

### div()

```
div(<number1>, <number2>)
```

Returns the integer quotient of \<number1\> divided by \<number2\>. The result
is truncated toward zero. Division by zero returns an error.

### fdiv()

```
fdiv(<number1>, <number2>)
```

Returns the floating-point quotient of \<number1\> divided by \<number2\>.
Division by zero returns an error.

### mod()

```
mod(<number1>, <number2>)
```

Returns the remainder of \<number1\> divided by \<number2\>. The sign of the
result follows the sign of the dividend. Division by zero returns an error.

### remainder()

```
remainder(<number1>, <number2>)
```

Returns the remainder of integer division. Differs from `mod()` in handling
of negative numbers: the result has the same sign as the dividend. Level 2.

## Rounding

### round()

```
round(<number>, <places>)
```

Rounds \<number\> to \<places\> decimal places. Uses "round half away from
zero" semantics. If \<places\> is 0, rounds to the nearest integer.

### trunc()

```
trunc(<number>)
```

Truncates \<number\> toward zero, removing the fractional part.

### ceil()

```
ceil(<number>)
```

Returns the smallest integer greater than or equal to \<number\>.

### floor()

```
floor(<number>)
```

Returns the largest integer less than or equal to \<number\>.

## Unary and Sign

### abs()

```
abs(<number>)
```

Returns the absolute value of \<number\>.

### sign()

```
sign(<number>)
```

Returns -1 if \<number\> is negative, 0 if zero, or 1 if positive. Level 2.

### inc()

```
inc(<number>)
```

Returns \<number\> plus 1.

### dec()

```
dec(<number>)
```

Returns \<number\> minus 1.

## Minimum and Maximum

### min()

```
min(<number>, <number>, ...)
```

Returns the smallest of all arguments. Accepts two or more arguments.

### max()

```
max(<number>, <number>, ...)
```

Returns the largest of all arguments. Accepts two or more arguments.

### bound()

```
bound(<value>, <lower>, <upper>)
```

Returns \<value\> constrained to the range [\<lower\>, \<upper\>]. If \<value\>
is less than \<lower\>, returns \<lower\>. If greater than \<upper\>, returns
\<upper\>. Level 2.

## Exponential and Logarithmic

### power()

```
power(<base>, <exponent>)
```

Returns \<base\> raised to \<exponent\>. Supports fractional exponents.

### sqrt()

```
sqrt(<number>)
```

Returns the square root of \<number\>. Returns an error for negative numbers.

### exp()

```
exp(<number>)
```

Returns _e_ raised to the power of \<number\>.

### ln()

```
ln(<number>)
```

Returns the natural logarithm (base _e_) of \<number\>. Returns an error for
non-positive numbers.

### log()

```
log(<number>)
```

Returns the base-10 logarithm of \<number\>. Returns an error for non-positive
numbers.

## Trigonometric Functions

All trigonometric functions operate in radians by default. Implementations may
support an optional unit parameter (`r` for radians, `d` for degrees, `g` for
gradians).

### sin()

```
sin(<number> [, <units>])
```

Returns the sine of \<number\>.

### cos()

```
cos(<number> [, <units>])
```

Returns the cosine of \<number\>.

### tan()

```
tan(<number> [, <units>])
```

Returns the tangent of \<number\>.

### asin()

```
asin(<number> [, <units>])
```

Returns the arcsine of \<number\>. The argument shall be in the range [-1, 1].

### acos()

```
acos(<number> [, <units>])
```

Returns the arccosine of \<number\>. The argument shall be in the range
[-1, 1].

### atan()

```
atan(<number> [, <units>])
```

Returns the arctangent of \<number\>.

### atan2()

```
atan2(<y>, <x> [, <units>])
```

Returns the arctangent of \<y\>/\<x\>, using the signs of both arguments to
determine the quadrant of the result.

### pi()

```
pi()
```

Returns the value of pi.

## Distance

### dist2d()

```
dist2d(<x1>, <y1>, <x2>, <y2>)
```

Returns the 2D Euclidean distance between points (\<x1\>, \<y1\>) and
(\<x2\>, \<y2\>).

### dist3d()

```
dist3d(<x1>, <y1>, <z1>, <x2>, <y2>, <z2>)
```

Returns the 3D Euclidean distance between two points.

## Random Numbers

### rand()

```
rand(<upper> [, <lower>])
```

Returns a random integer. With one argument, returns a value from 0 to
\<upper\>-1. With two arguments, returns a value from \<lower\> to \<upper\>-1.

### die()

```
die(<count>, <sides>)
```

Simulates rolling \<count\> dice each with \<sides\> faces. Returns the sum
of the rolls.

### lrand()

```
lrand(<lower>, <upper>, <count> [, <delimiter>])
```

Returns a \<delimiter\>-separated list of \<count\> random integers between
\<lower\> and \<upper\>. Level 2.

## Base Conversion

### baseconv()

```
baseconv(<number>, <from-base>, <to-base>)
```

Converts \<number\> from \<from-base\> to \<to-base\>. Bases from 2 through 36
are supported.

## Bitwise Operations

### band()

```
band(<number1>, <number2>)
```

Returns the bitwise AND of \<number1\> and \<number2\>.

### bor()

```
bor(<number1>, <number2>)
```

Returns the bitwise OR of \<number1\> and \<number2\>.

### bxor()

```
bxor(<number1>, <number2>)
```

Returns the bitwise XOR of \<number1\> and \<number2\>.

### bnand()

```
bnand(<number1>, <number2>)
```

Returns the bitwise NAND of \<number1\> and \<number2\>. Level 2.

## Implementation Notes

Floating-point precision is implementation-defined but shall be at least IEEE
754 double precision (approximately 15 significant digits). Integer range
shall support at least 32-bit signed integers.

Trigonometric functions should be accurate to the precision of the underlying
C library. Implementations may differ in their handling of edge cases such as
`tan(pi/2)`.

The `die()` function uses a uniform random distribution. The quality of the
random number generator is implementation-defined.
