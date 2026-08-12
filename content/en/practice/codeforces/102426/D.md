---
title: "CF 102426D - \u5143\u7d20\u5468\u671f\u8868"
description: "We need to evaluate several chemical formulas and compute their relative molecular masses. A formula is a sequence of element symbols, where an element symbol consists of one uppercase letter and possibly one lowercase letter."
date: "2026-08-12T19:22:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "D"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 110
verified: true
draft: false
---

[CF 102426D - \u5143\u7d20\u5468\u671f\u8868](https://codeforces.com/problemset/problem/102426/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to evaluate several chemical formulas and compute their relative molecular masses. A formula is a sequence of element symbols, where an element symbol consists of one uppercase letter and possibly one lowercase letter. A number immediately following the symbol gives the number of atoms of that element. If the number is omitted, the element occurs exactly once.

For example, `H2O` means two hydrogen atoms and one oxygen atom, so its molecular mass is `2 × 1.008 + 1 × 16 = 18.016`. Similarly, `CO2` is `1 × 12.01 + 2 × 16 = 44.01`.

The input contains at most 200 formulas, and every formula has length at most 1000. An element count is at most 1000. These bounds are small enough that we should simply process every character once. The total amount of input is at most 200,000 characters, so an O(total length) solution performs only a few hundred thousand parsing operations. There is no reason to use dynamic programming, hashing tricks, or any more complicated technique.

The difficulty is not the arithmetic. The parser has to distinguish between uppercase letters, lowercase letters belonging to the same symbol, and digits belonging to the atom count. A formula such as `NaCl` contains two elements even though there is no number between them, while `C12H22O11` contains three elements with multi-digit counts.

Several boundary cases can silently break an implementation. For `H`, the answer is `1.008`, because an omitted count means one atom. A parser that only adds an element after seeing a number would incorrectly ignore it.

For `He`, the answer is `4.003`. The `e` is part of the element symbol, not a separate token. An implementation that assumes every element is one character would look up `H` and then mishandle `e`.

For `O1000`, the answer is `16000.000`. The count can contain three digits, so reading only one digit would turn 1000 into 1.

For `NaCl`, the answer is `58.440`. There are no explicit counts, so both elements have implicit count one. A parser must finish the current element before moving to the next uppercase letter.

The atomic masses are fixed constants. The conventional table used for this problem gives values such as H = 1.008, He = 4.003, C = 12.01, O = 16, and continues through all 118 elements. A published solution for this exact problem uses the same 118-entry table.

## Approaches

A literal brute-force parser could repeatedly inspect the remaining part of the formula whenever it needs to determine where an element token or its number ends. For a formula of length L, such rescanning can examine a suffix of length roughly L, then L - 1, and so on, giving about `1 + 2 + ... + L = L(L + 1) / 2` character inspections. With L = 1000, that is about 500,500 inspections for one formula. At the maximum T = 200, this reaches roughly 100 million character inspections, which is unnecessarily expensive under a 1 second limit.

The brute-force approach works because every piece of information is local. The problem is that it keeps rediscovering information that has already been consumed.

The key observation is that the formula has a very strict grammar. Whenever we encounter an uppercase letter, a new element starts. There can be at most one lowercase letter immediately after it. After the symbol, there can be zero or more digits. Once those digits end, the next uppercase letter begins the next element. We never need to look backward or rescan anything.

That lets us parse the formula with one left-to-right pointer. At each element, we read its symbol, read all following digits as its count, add `atomic_mass × count` to the answer, and continue exactly where the next element begins. Every character is consumed once, so the complexity drops from quadratic to linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L²) per formula | O(1) | Too slow in the worst case |
| Optimal | O(L) per formula | O(1) apart from the fixed mass table | Accepted |

Here L is the length of one molecular formula. The fixed periodic-table dictionary has only 118 entries, so its size is effectively constant.

## Algorithm Walkthrough

1. Store the atomic mass of every chemical element in a dictionary keyed by its symbol. The formula gives symbols such as `H`, `O`, `Na`, and `Cl`, so direct dictionary lookup lets us obtain each mass immediately.
2. Set a pointer `i` to the beginning of the formula and initialize the molecular mass `total` to zero. The pointer always marks the first character of the next element that has not yet been processed.
3. Read the uppercase character at `i` as the first part of the element symbol. If the next character exists and is lowercase, append it to the symbol and advance `i`. This handles both one-letter symbols such as `C` and two-letter symbols such as `Fe`.
4. Starting from the current position, consume every consecutive digit and build the atom count. If no digit appears, use count one. The absence of a number has a precise meaning in chemical notation, so treating it as one avoids a special case later.
5. Look up the atomic mass of the parsed symbol and add `mass × count` to `total`. At this point, every character belonging to this element has been consumed.
6. Repeat until `i` reaches the end of the formula. Since every iteration consumes at least one character, the pointer always moves forward and the loop terminates.
7. Print `total` with three digits after the decimal point. Three decimal places give an error far below the required `10^-3` tolerance.

Why it works

The invariant is that immediately before each iteration, every character before `i` has already been assigned to exactly one element occurrence and its contribution has been added to `total`. The current position `i` is therefore exactly the start of the next unprocessed element. Reading one uppercase letter, its optional lowercase letter, and its following digits consumes precisely the complete representation of that element occurrence. Its contribution is then added exactly once. The invariant remains true after the iteration, and when `i` reaches the end, every element occurrence has been processed exactly once, so `total` is the molecular mass.

## Python Solution

```python
import sys
input = sys.stdin.readline

symbols = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
]

masses = [
    1.008, 4.003, 6.941, 9.012, 10.81, 12.01, 14.01, 16.0, 19.0, 20.18,
    22.99, 24.31, 26.98, 28.09, 30.97, 32.07, 35.45, 39.95, 39.10, 40.08,
    44.96, 47.88, 50.94, 52.0, 54.94, 55.85, 58.93, 58.69, 63.55, 65.39,
    69.72, 72.59, 74.92, 78.96, 79.90, 83.80, 85.47, 87.62, 88.91, 91.22,
    92.91, 95.94, 97.91, 101.1, 102.9, 106.4, 107.9, 112.4, 114.8, 118.7,
    121.8, 127.6, 126.9, 131.3, 132.9, 137.3, 138.9, 140.1, 140.9, 144.2,
    144.9, 150.4, 152.0, 157.3, 158.9, 162.5, 164.9, 167.3, 168.9, 173.0,
    175.0, 178.5, 180.9, 183.9, 186.2, 190.2, 192.2, 195.1, 197.0, 200.6,
    204.4, 207.2, 209.0, 209.0, 210.0, 222.0, 223.0, 226.0, 227.0, 232.0,
    231.0, 238.0, 237.1, 244.1, 243.1, 247.1, 247.1, 252.1, 252.1, 257.1,
    258.1, 259.1, 262.1, 265.1, 268.1, 271.1, 270.1, 277.2, 276.2, 281.2,
    280.2, 285.2, 284.2, 289.2, 288.2, 293.2, 294.2, 294.2
]

MASS = dict(zip(symbols, masses))

def molecular_mass(formula):
    n = len(formula)
    i = 0
    total = 0.0

    while i < n:
        # Every element starts with an uppercase letter.
        symbol = formula[i]
        i += 1

        # A second lowercase letter belongs to the same symbol.
        if i < n and formula[i].islower():
            symbol += formula[i]
            i += 1

        # Read the complete decimal count.
        count = 0
        while i < n and formula[i].isdigit():
            count = count * 10 + (ord(formula[i]) - ord('0'))
            i += 1

        # No explicit count means exactly one atom.
        if count == 0:
            count = 1

        total += MASS[symbol] * count

    return total

def solve():
    t = int(input())
    for _ in range(t):
        formula = input().strip()
        print(f"{molecular_mass(formula):.3f}")

if __name__ == "__main__":
    solve()
```

The `symbols` and `masses` arrays describe the same periodic table in atomic-number order. `dict(zip(...))` turns them into direct symbol-to-mass lookup, so parsing does not require searching through all 118 elements. The values above follow the fixed table used in accepted solutions for this problem.

Inside `molecular_mass`, `i` is the only parsing pointer. The first character of every element is uppercase, so it can immediately start a symbol. The lowercase check uses `i < n` before indexing, which prevents an out-of-range access when a two-letter check occurs at the end of the formula.

The digit loop is deliberately separate from symbol parsing. A formula such as `C123` first produces the symbol `C`, then reads `1`, `2`, and `3` as one count of 123. The expression `count = count * 10 + digit` is the standard way to construct a decimal integer from its characters.

Using `count == 0` as the indicator for an omitted number is safe because the statement guarantees valid formulas and every explicit element count is positive. An omitted count leaves `count` at zero, after which it is changed to one.

Python integers do not overflow, and the largest possible molecular mass is comfortably within the range of a floating-point value. Printing with `.3f` gives the required precision while also producing a consistent output format.

## Worked Examples

### Sample 1: H2O

The formula is processed from left to right.

| `i` before | Symbol | Count | Contribution | `total` |
| --- | --- | --- | --- | --- |
| 0 | H | 2 | 2 × 1.008 = 2.016 | 2.016 |
| 2 | O | 1 | 1 × 16 = 16.000 | 18.016 |

After reading `H`, the parser sees the digit `2`, so the count is 2. The next uppercase letter starts `O`, which has no following number, so its count becomes 1. The final answer is `18.016`.

### Sample 2: CO2

| `i` before | Symbol | Count | Contribution | `total` |
| --- | --- | --- | --- | --- |
| 0 | C | 1 | 1 × 12.01 = 12.010 | 12.010 |
| 1 | O | 2 | 2 × 16 = 32.000 | 44.010 |

The first element has no explicit number, so the parser assigns it count one. The `O` is followed by `2`, which becomes its complete count. The printed result is `44.010`, which is equivalent to the sample's `44.01` and satisfies the required error tolerance.

### Additional trace: C12H22O11

| `i` before | Symbol | Count | Contribution | `total` |
| --- | --- | --- | --- | --- |
| 0 | C | 12 | 12 × 12.01 = 144.120 | 144.120 |
| 3 | H | 22 | 22 × 1.008 = 22.176 | 166.296 |
| 6 | O | 11 | 11 × 16 = 176.000 | 342.296 |

This trace demonstrates why the digit loop must continue until the entire number has been consumed. Reading only the first digit would produce completely different counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) per formula, O(total input length) overall | Every character is examined once, and each element lookup is O(1) |
| Space | O(1) auxiliary space | Only a constant number of parsing variables are used; the 118-entry mass table is fixed |

Across all test cases, the total formula length is at most 200,000 characters. A linear scan therefore performs only O(200,000) parsing work, which is easily within the stated time limit. The memory usage is also tiny, since the formula itself and the fixed 118-element table are the only relevant storage.

## Test Cases

```python
import sys
import io

symbols = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
]

masses = [
    1.008, 4.003, 6.941, 9.012, 10.81, 12.01, 14.01, 16.0, 19.0, 20.18,
    22.99, 24.31, 26.98, 28.09, 30.97, 32.07, 35.45, 39.95, 39.10, 40.08,
    44.96, 47.88, 50.94, 52.0, 54.94, 55.85, 58.93, 58.69, 63.55, 65.39,
    69.72, 72.59, 74.92, 78.96, 79.90, 83.80, 85.47, 87.62, 88.91, 91.22,
    92.91, 95.94, 97.91, 101.1, 102.9, 106.4, 107.9, 112.4, 114.8, 118.7,
    121.8, 127.6, 126.9, 131.3, 132.9, 137.3, 138.9, 140.1, 140.9, 144.2,
    144.9, 150.4, 152.0, 157.3, 158.9, 162.5, 164.9, 167.3, 168.9, 173.0,
    175.0, 178.5, 180.9, 183.9, 186.2, 190.2, 192.2, 195.1, 197.0, 200.6,
    204.4, 207.2, 209.0, 209.0, 210.0, 222.0, 223.0, 226.0, 227.0, 232.0,
    231.0, 238.0, 237.1, 244.1, 243.1, 247.1, 247.1, 252.1, 252.1, 257.1,
    258.1, 259.1, 262.1, 265.1, 268.1, 271.1, 270.1, 277.2, 276.2, 281.2,
    280.2, 285.2, 284.2, 289.2, 288.2, 293.2, 294.2, 294.2
]

MASS = dict(zip(symbols, masses))

def molecular_mass(formula):
    i = 0
    total = 0.0
    n = len(formula)

    while i < n:
        symbol = formula[i]
        i += 1

        if i < n and formula[i].islower():
            symbol += formula[i]
            i += 1

        count = 0
        while i < n and formula[i].isdigit():
            count = count * 10 + int(formula[i])
            i += 1

        if count == 0:
            count = 1

        total += MASS[symbol] * count

    return total

def run(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    output = []

    for _ in range(t):
        formula = data.readline().strip()
        output.append(f"{molecular_mass(formula):.3f}")

    return "\n".join(output) + "\n"

# Provided samples
assert run("""2
H2O
CO2
""") == """18.016
44.010
""", "provided samples"

# Minimum-size input and implicit count
assert run("""1
H
""") == """1.008
""", "single-letter element with omitted count"

# Two-letter element at the end, with omitted count
assert run("""1
He
""") == """4.003
""", "two-letter element at formula boundary"

# Maximum allowed count
assert run("""1
O1000
""") == """16000.000
""", "three-digit count equal to 1000"

# Multiple elements and multiple digits
assert run("""1
C6H12O6
""") == """180.156
""", "multi-element formula with multi-digit counts"

# Maximum formula length: 200 copies of H1000 gives exactly 1000 characters
max_formula = "H1000" * 200
assert len(max_formula) == 1000
assert run("1\n" + max_formula + "\n") == "201600.000\n", \
    "maximum formula length"

# Consecutive two-letter and one-letter symbols without counts
assert run("""1
NaCl
""") == """58.440
""", "adjacent elements without explicit counts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `H` | `1.008` | Minimum-size formula and implicit count one |
| `He` | `4.003` | Two-letter symbol and end-of-string boundary |
| `O1000` | `16000.000` | Maximum allowed element count and multi-digit parsing |
| `C6H12O6` | `180.156` | Several elements and multi-digit counts |
| `H1000` repeated 200 times | `201600.000` | Maximum formula length and repeated identical elements |
| `NaCl` | `58.440` | Consecutive elements with no explicit counts |

## Edge Cases

For an omitted count such as `H`, the parser reads `H`, finds that the next character does not exist, and leaves `count` at zero. It then converts that zero to one and adds `1 × 1.008`, producing `1.008`. This prevents the common mistake of requiring every element to be followed by a digit.

For a two-letter symbol such as `He`, the parser first consumes `H`, checks the next character, sees lowercase `e`, and extends the symbol to `He`. The pointer then reaches the end, so the count is one. The lookup returns 4.003 and the answer is `4.003`. The explicit boundary check before reading the lowercase character is what makes the end of the string safe.

For `O1000`, the parser reads `O` and then executes the digit loop four times. The intermediate counts are 1, 10, 100, and finally 1000. The contribution is `1000 × 16 = 16000`, so the output is `16000.000`. A parser that reads only one digit would fail this case immediately.

For `NaCl`, the parser first reads `Na` and assigns count one because no digit follows. The pointer is now positioned at `C`, which starts a new element. It then reads `Cl`, again with implicit count one. The result is `22.99 + 35.45 = 58.44`, printed as `58.440`. This exercises the transition directly from one element to the next without any numeric separator.

For `C6H12O11`, the parser must distinguish the digit sequence `12` from two separate quantities. After reading `H`, it consumes both digits before continuing to `O`. The contribution of the hydrogen part is `12 × 1.008 = 12.096`. The same mechanism handles `O11`. The pointer-based invariant guarantees that no digit is accidentally interpreted as part of the following element.

For the maximum-length formula consisting of 200 copies of `H1000`, each five-character block contributes `1000 × 1.008 = 1008`. There are 200 such blocks, so the final mass is `200 × 1008 = 201600`. Every iteration consumes exactly one complete element occurrence, demonstrating that the linear parser remains correct even when the input reaches its maximum length.
