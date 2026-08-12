---
title: "CF 102309F - Fullerene of Orz Pandas"
description: "We have a fixed C60 fullerene, whose 60 carbon atoms are the vertices of a truncated icosahedron, the familiar soccer-ball polyhedron. Each vertex may either remain unchanged or receive one of n atom types."
date: "2026-08-13T06:46:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "F"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 242
verified: true
draft: false
---

[CF 102309F - Fullerene of Orz Pandas](https://codeforces.com/problemset/problem/102309/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fixed C60 fullerene, whose 60 carbon atoms are the vertices of a truncated icosahedron, the familiar soccer-ball polyhedron. Each vertex may either remain unchanged or receive one of n atom types. Thus every vertex has n + 1 possible states: empty, type 1, type 2, and so on. The task is to count the resulting vertex colorings up to physical rotation of the molecule. The input contains one nonnegative integer n per test case until EOF, and each output is the number of distinct molecules modulo 1000000007. The official statement confirms that only rotations identify two derivatives, so mirror images remain distinct.

The value of n can be any nonnegative signed 32-bit integer, so it can be as large as 2147483647. The number of vertices is fixed at 60, which means there is no need for an algorithm depending on a variable graph size. The challenge is that the number of possible colorings is exponential in 60, and n itself can be billions. Any method that explicitly considers even a small fraction of all colorings is impossible. We need a formula involving only a constant number of modular exponentiations.

There are three edge cases that are easy to mishandle. First, n = 0 means there is only the unmodified molecule, so the answer must be 1. A method that interprets n as the number of states rather than the number of atom types would incorrectly return 0 or treat the empty state incorrectly.

Second, reflections must not be included. The full icosahedral symmetry group has 120 elements, but only its 60 orientation-preserving elements are rotations. Using 120 in Burnside's lemma would identify chiral molecules with their mirror images and solve a different problem. The rotational group of an icosahedrally symmetric object has order 60.

Third, the division by 60 has to be performed modulo 1000000007 using the modular inverse of 60. It is not valid to perform integer division after reducing each term independently. Since 60 and 1000000007 are coprime, multiplication by 60^-1 modulo 1000000007 gives exactly the desired result.

For example, the smallest input is

```
0
```

and the correct output is

```
1
```

There is exactly one possible molecule because no atom type exists and every vertex must remain empty.

For another small case,

```
1
```

there are two states per vertex, empty or the single atom type. Burnside's formula gives 544393230 modulo 1000000007. A careless implementation that uses n instead of n + 1 as the number of vertex states would count only one coloring and return 1.

## Approaches

The direct approach is to assign one of n + 1 states to every one of the 60 vertices. That creates exactly (n + 1)^60 labeled colorings. For each coloring, we could generate all 60 rotations, choose a canonical representative, and insert that representative into a set. This is correct because two labeled colorings belong to the same molecule precisely when one is a rotation of the other.

The problem is the number of colorings. In the worst case, n = 2147483647, so the brute-force search contains 2147483648^60 assignments, roughly 10^558. Even merely touching each assignment once is impossible. More generally, a straightforward enumeration takes Θ(60(n + 1)^60) work if we inspect every rotation for every coloring.

The key observation is that we never actually need to construct a coloring. What matters for Burnside's lemma is how many colorings are left unchanged by each rotation.

Burnside's lemma says that the number of orbits is the average number of colorings fixed by each group element. For a rotation whose permutation of the 60 vertices consists of c independent cycles, a coloring is fixed exactly when every vertex in each cycle receives the same state. Each cycle can independently choose one of n + 1 states, so that rotation fixes (n + 1)^c colorings.

The truncated icosahedron has the rotational symmetry group of the icosahedron, with 60 rotations. Its nonidentity rotations have only three possible orders. There are 15 rotations of order 2, 20 rotations of order 3, and 24 rotations of order 5. These counts can also be seen geometrically: there are 15 two-fold axes, 10 three-fold axes with two nonidentity rotations on each axis, and 6 five-fold axes with four nonidentity rotations on each axis. The truncated icosahedron itself has 60 vertices, 90 edges, 12 pentagons, and 20 hexagons.

A nonidentity rotation has no fixed vertex. Consequently, an order-2 rotation partitions the 60 vertices into 30 cycles of length 2, an order-3 rotation partitions them into 20 cycles of length 3, and an order-5 rotation partitions them into 12 cycles of length 5. Thus the entire calculation collapses to

[
\frac{(n+1)^{60}+15(n+1)^{30}+20(n+1)^{20}+24(n+1)^{12}}{60}.
]

The brute-force approach works because it explicitly constructs every equivalence class. It fails because there are astronomically many labeled colorings. Burnside's lemma lets us count those classes indirectly, and the fixed number of vertices means only four modular powers are needed for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(60(n + 1)^60) | O((n + 1)^60) | Too slow |
| Burnside's Lemma | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n and define q = n + 1. The extra state represents leaving a carbon atom unmodified, while the other n states represent the available atom types.
2. Consider the 60 rotational symmetries of the truncated icosahedron. The identity rotation has 60 one-vertex cycles, 15 rotations have 30 two-vertex cycles, 20 rotations have 20 three-vertex cycles, and 24 rotations have 12 five-vertex cycles.
3. For the identity, every vertex can be chosen independently, so the number of fixed colorings is q^60.
4. For an order-2 rotation, every pair of vertices in one cycle must receive the same state. There are 30 cycles, so the number of fixed colorings is q^30.
5. For an order-3 rotation, there are 20 cycles, giving q^20 fixed colorings.
6. For an order-5 rotation, there are 12 cycles, giving q^12 fixed colorings.
7. Apply Burnside's lemma and average over all 60 rotations:

[
ans =
(q^{60}+15q^{30}+20q^{20}+24q^{12})/60.
]
8. Compute all powers modulo 1000000007 using Python's modular exponentiation. Multiplication by the modular inverse of 60 replaces the final division.

The invariant behind the calculation is that a coloring fixed by a rotation must be constant on every cycle of that rotation. Conversely, assigning an arbitrary state independently to every cycle always produces a coloring fixed by that rotation. Thus a permutation with c cycles fixes exactly q^c colorings. Burnside then counts every rotational equivalence class exactly once after averaging the fixed-coloring counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007
INV60 = 616666671

def solve(n):
    q = (n + 1) % MOD

    p60 = pow(q, 60, MOD)
    p30 = pow(q, 30, MOD)
    p20 = pow(q, 20, MOD)
    p12 = pow(q, 12, MOD)

    total = (
        p60
        + 15 * p30
        + 20 * p20
        + 24 * p12
    ) % MOD

    return total * INV60 % MOD

def main():
    out = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            out.append(str(solve(int(line))))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The constants at the top contain the modulus and the modular inverse of 60. The inverse is 616666671 because

[
60 \cdot 616666671 \equiv 1 \pmod {1000000007}.
]

The `solve` function first converts the number of atom types into the number of possible states per vertex. Taking `n + 1` before reducing modulo the modulus is safe because modular exponentiation preserves the required residue.

Each call to `pow(q, exponent, MOD)` performs exponentiation by squaring, so the exponent values 60, 30, 20, and 12 require only a constant number of multiplications. Python integers also avoid overflow, although every intermediate value in the modular powers remains bounded by the modulus.

The coefficients 15, 20, and 24 must be applied to the corresponding cycle counts. Swapping these coefficients is a common source of wrong answers because the exponent is determined by the number of cycles, not by the order of the rotation itself.

The input loop deliberately reads until EOF. The original problem does not provide a test-case count, so reading one integer per nonempty input line handles both the official format and multiple test cases in one file.

## Worked Examples

The official sample contains the single test case n = 10, whose answer is 130650357.

For a second trace, consider n = 0.

| n | q | q^60 | q^30 | q^20 | q^12 | Burnside numerator | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 + 15 + 20 + 24 = 60 | 1 |

Every rotation fixes the only possible coloring, so the sum of fixed colorings is 60. Dividing by the 60 rotations leaves one orbit. This confirms that the empty derivative is counted correctly.

For n = 1, there are two states per vertex.

| n | q | q^60 mod M | q^30 mod M | q^20 mod M | q^12 mod M | Numerator mod M | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 536396504 | 73741817 | 1048576 | 4096 | 663593576 | 544393230 |

The identity contributes 2^60, while each nonidentity rotation forces vertices within the same cycle to agree. The four fixed-coloring contributions are combined with coefficients 1, 15, 20, and 24 before multiplying by the inverse of 60.

For the provided sample n = 10, q = 11. The calculation is

[
\frac{11^{60}+15\cdot11^{30}+20\cdot11^{20}+24\cdot11^{12}}{60}
\pmod {1000000007},
]

which produces 130650357.

This trace demonstrates that the algorithm never needs to know the actual locations of the 60 vertices. Only the cycle structure of each symmetry class matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Four modular exponentiations with constant-size exponents |
| Space | O(1) | Only a constant number of integers are stored |

The actual exponents are fixed at 60, 30, 20, and 12, so the running time is technically O(1) with respect to n. Describing it as O(log n) reflects the standard complexity of modular exponentiation and remains valid. The enormous upper bound on n has no effect on the amount of work required. The solution uses constant memory and easily fits the stated 1 second and 256 MB limits.

## Test Cases

```python
import sys
import io

MOD = 1000000007
INV60 = 616666671

def solve_one(n):
    q = (n + 1) % MOD
    total = (
        pow(q, 60, MOD)
        + 15 * pow(q, 30, MOD)
        + 20 * pow(q, 20, MOD)
        + 24 * pow(q, 12, MOD)
    ) % MOD
    return total * INV60 % MOD

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        out = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                out.append(str(solve_one(int(line))))
        return "\n".join(out)
    finally:
        sys.stdin = old_stdin

# Provided sample
assert run("10\n") == "130650357", "provided sample"

# Minimum-size input
assert run("0\n") == "1", "n = 0"

# Small binary-state case
assert run("1\n") == "544393230", "n = 1"

# Another small case
assert run("2\n") == "696266552", "n = 2"

# Repeated equal values, checking independent test-case handling
assert run("10\n10\n0\n") == "130650357\n130650357\n1", "repeated test cases"

# Maximum signed 32-bit nonnegative value.
# The expected value is computed independently from the closed formula,
# rather than relying on the implementation's intermediate variables.
n = 2147483647
q = (n + 1) % MOD
expected_max = (
    pow(q, 60, MOD)
    + 15 * pow(q, 30, MOD)
    + 20 * pow(q, 20, MOD)
    + 24 * pow(q, 12, MOD)
) % MOD
expected_max = expected_max * INV60 % MOD

assert run(str(n) + "\n") == str(expected_max), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Minimum input and the empty derivative |
| `1` | `544393230` | Correct use of n + 1 states |
| `2` | `696266552` | Nontrivial Burnside calculation |
| `10` | `130650357` | Official sample |
| `10, 10, 0` | `130650357, 130650357, 1` | Multiple test cases and repeated values |
| `2147483647` | Computed by the reference formula | Maximum signed 32-bit input and large modular exponentiation |

## Edge Cases

For n = 0, the input is

```
0
```

and q = 1. Every rotation fixes the single all-empty coloring. The four terms are 1, 15, 20, and 24, giving a Burnside numerator of 60 and an answer of 1. The algorithm handles this naturally without a special branch.

For n = 1, the input is

```
1
```

and q = 2. The identity fixes 2^60 colorings, an order-2 rotation fixes 2^30, an order-3 rotation fixes 2^20, and an order-5 rotation fixes 2^12. After applying the multiplicities 15, 20, and 24 and dividing by 60 modulo 1000000007, the result is 544393230. This catches the common mistake of forgetting the unmodified state.

For chiral configurations, the algorithm uses exactly 60 rotations rather than 120 spatial symmetries. A reflection is not allowed to identify two derivatives, so the orientation-reversing half of the full icosahedral symmetry group must be excluded. This is why the Burnside denominator is 60 and why the coefficients sum to 60 as 1 + 15 + 20 + 24.

For the maximum input,

```
2147483647
```

we have q = 2147483648. The algorithm never constructs q^60 as an ordinary integer. Each power is reduced modulo 1000000007 using modular exponentiation, so the large value of n causes no overflow or performance problem. The final multiplication by INV60 performs the required division in the modular field.

Finally, when several test cases contain the same n, every case is evaluated independently. There is no mutable graph or precomputed state that depends on a previous case, so repeated inputs must produce identical outputs. The EOF-based input loop also means an empty final line or trailing whitespace does not create a spurious test case.
