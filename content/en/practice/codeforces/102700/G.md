---
title: "CF 102700G - Great dinner"
description: "We have (N) distinct students who must be arranged in a line. Among them, there are (M) disjoint bully-victim pairs. For every input pair ((A,B)), student (A) must appear before student (B). The statement describes this as (B) not being ahead of (A)."
date: "2026-08-08T08:21:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "G"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 350
verified: true
draft: false
---

[CF 102700G - Great dinner](https://codeforces.com/problemset/problem/102700/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have \(N\) distinct students who must be arranged in a line. Among them, there are \(M\) disjoint bully-victim pairs. For every input pair \((A,B)\), student \(A\) must appear before student \(B\). The statement describes this as \(B\) not being ahead of \(A\).

The crucial structural property is that every student appears in at most one pair. Thus the \(M\) restrictions involve \(2M\) different students. The remaining \(N-2M\) students are completely unrestricted.

The task is to count every permutation of the \(N\) students that satisfies all \(M\) ordering restrictions, and output that count modulo \(10^9+7\).

The value of \(N\) can reach \(10^5\), so anything involving all permutations is immediately impossible. There are \(N!\) permutations, and even for \(N=20\), that is already far beyond what a typical contest program can enumerate. With \(N=10^5\) and a two-second limit, the intended solution must be essentially linear in \(N\), with perhaps a small additional factor depending on \(M\). The second constraint is especially useful: \(2M\le 2000\), so there are at most \(1000\) independent restrictions.

There are a few edge cases that can make a careless implementation fail. With no restrictions, for example,

```text
1 0
```

has exactly \(1\) valid arrangement. A formula that divides by \(2^M\) but mishandles \(M=0\) could incorrectly produce zero or fail to compute the inverse.

A boundary case with one restriction is

```text
4 1
1 4
```

There are \(4!=24\) total arrangements, and exactly half put student \(1\) before student \(4\), so the answer is \(12\). A careless solution might try to use the actual student numbers in the formula, even though only the number of independent restrictions matters.

Finally, multiple restrictions must involve different students. For example,

```text
6 3
1 2
3 4
5 6
```

has three independent restrictions. The answer is \(6!/2^3=90\). Treating the restrictions as dependent would give the wrong count. The input guarantee that every endpoint occurs at most once is exactly what makes the simple division by \(2^M\) valid.

The phrase "all-equal values" does not describe a valid input case here, because every student appearing in a pair must be different from every other paired student. The closest meaningful equivalent is \(M=0\), where all students are unrestricted and every permutation is valid.

## Approaches

A direct brute-force solution would generate every permutation of the \(N\) students. For each permutation, it could locate the positions of the students in every bully-victim pair and check whether all required orientations are correct. This is correct because every possible line is considered exactly once, and a line is counted precisely when every restriction holds.

The problem is the number of permutations. There are \(N!\) of them, and checking \(M\) restrictions for each one gives \(O(N!\,M)\) time. Even if we optimized the checking so that each permutation could be validated in constant time, enumerating \(N!\) permutations would still be hopeless for \(N=10^5\). The factorial growth is the real obstacle.

The structure of the restrictions gives us a much stronger observation. Consider just one pair \((A,B)\). In a uniformly chosen permutation, exactly half of all permutations place \(A\) before \(B\), while the other half place \(B\) before \(A\). So one restriction reduces the number of valid permutations by a factor of exactly two.

Because all \(M\) pairs are disjoint, these restrictions can be treated independently. More formally, imagine choosing an orientation for every pair. There are \(2^M\) possible orientation patterns. Every one of these patterns is realized by exactly the same number of permutations. We can prove this with a bijection: if we want to change the orientation of one pair, swap the identities of its two students in every permutation. Since no student belongs to another pair, this swap changes only that pair's orientation.

There are \(N!\) permutations distributed equally among \(2^M\) orientation patterns. Exactly one pattern is the desired one, namely the pattern where every bully precedes the corresponding victim. Hence the answer is

\[
\frac{N!}{2^M}.
\]

Since the answer is required modulo \(10^9+7\), we cannot perform ordinary integer division. The modulus is prime, so \(2^M\) has a modular inverse. We compute

\[
N!\cdot (2^M)^{-1}\pmod{10^9+7}.
\]

The brute-force method works because it explicitly examines the objects we want to count, but fails because there are factorially many of them. The observation that every disjoint pair has two equally sized possible orientations lets us count all permutations at once and replace enumeration by a factorial and a modular inverse.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---:|---:|---|
| Brute Force | \(O(N!\,M)\) | \(O(N+M)\) | Too slow |
| Optimal | \(O(N+M)\) | \(O(1)\) auxiliary | Accepted |

## Algorithm Walkthrough

1. Read \(N\) and \(M\). The actual identities of the paired students do not affect the final formula, because the only relevant property is that the \(M\) pairs are disjoint.

2. Read all \(M\) pairs. We do not need to store them or inspect their student numbers after reading them. Their role is only to tell us that there are \(M\) independent ordering restrictions.

3. Compute \(N!\) modulo \(10^9+7\). Start with `fact = 1` and multiply by every integer from \(1\) through \(N\), taking the remainder after each multiplication.

4. Compute \(2^M\) modulo \(10^9+7\). This represents the \(2^M\) equally sized orientation classes into which all permutations are divided.

5. Compute the modular inverse of \(2^M\). By Fermat's little theorem, for a nonzero value \(x\) modulo the prime \(P=10^9+7\),

\[
x^{-1}\equiv x^{P-2}\pmod P.
\]

Thus the inverse of \(2^M\) is obtained with `pow(2, M, P)` followed by another modular exponentiation, or equivalently with `pow(2, M * (P - 2), P)`. Computing the denominator first is clearer.

6. Multiply the factorial by that inverse and take the result modulo \(P\). This gives

\[
N!\cdot (2^M)^{-1}\pmod P,
\]

which is exactly the required number of valid arrangements.

### Why it works

Every permutation has one definite orientation for each of the \(M\) disjoint pairs. Therefore every permutation belongs to exactly one of \(2^M\) orientation patterns.

For any two orientation patterns, we can transform every permutation belonging to the first pattern into a permutation belonging to the second by swapping the two students in each pair whose orientation needs to change. Because the pairs are disjoint, these swaps do not interfere with one another. The transformation is reversible, so all \(2^M\) patterns contain exactly the same number of permutations.

Since all \(N!\) permutations are partitioned among \(2^M\) equally sized classes, each class contains \(N!/2^M\) permutations. The required arrangements are exactly one of these classes, so the algorithm returns the correct count.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m = map(int, input().split())

    for _ in range(m):
        input()

    fact = 1
    for x in range(1, n + 1):
        fact = fact * x % MOD

    denominator = pow(2, m, MOD)
    inverse_denominator = pow(denominator, MOD - 2, MOD)

    answer = fact * inverse_denominator % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The input loop consumes all \(M\) restrictions, but deliberately does not store them. The guarantee that all endpoints are distinct means their exact values are irrelevant after we know that the input contains \(M\) restrictions.

The factorial loop runs through every student exactly once. Taking the modulus after every multiplication keeps all intermediate values bounded by roughly \(MOD^2\), which Python handles comfortably.

The denominator is computed as \(2^M\bmod MOD\). Since \(M\le1000\), this exponentiation is tiny, although Python's built-in `pow` also performs modular exponentiation efficiently for much larger exponents.

The expression `pow(denominator, MOD - 2, MOD)` computes the modular inverse. This is valid because \(MOD=10^9+7\) is prime and `denominator` is not divisible by \(MOD\).

There is no integer overflow issue in Python. In languages with fixed-width integers, the multiplication must use a sufficiently wide type or modular multiplication strategy.

The restrictions are read before computing the answer, so the program also handles \(M=0\) correctly. In that case the denominator is \(2^0=1\), its inverse is also \(1\), and the answer is simply \(N!\).

## Worked Examples

### Sample 1

The input is

```text
4 2
2 1
4 3
```

There are four students and two independent restrictions. The first requires student \(2\) to appear before student \(1\), while the second requires student \(4\) to appear before student \(3\).

The factorial and denominator calculation proceeds as follows.

| Step | Variable | Value |
|---|---|---:|
| Start | `fact` | 1 |
| \(1!\) | `fact` | 1 |
| \(2!\) | `fact` | 2 |
| \(3!\) | `fact` | 6 |
| \(4!\) | `fact` | 24 |
| Restrictions | `m` | 2 |
| Orientation classes | \(2^M\) | 4 |
| Final count | \(24/4\) | 6 |

The two pairs give four possible orientation patterns. Each pattern contains \(24/4=6\) permutations, and exactly one pattern has \(2\) before \(1\) and \(4\) before \(3\). The answer is therefore `6`.

### Sample 2

The input is

```text
4 1
1 3
```

There is only one restriction, requiring student \(1\) to precede student \(3\).

| Step | Variable | Value |
|---|---|---:|
| Start | `fact` | 1 |
| \(1!\) | `fact` | 1 |
| \(2!\) | `fact` | 2 |
| \(3!\) | `fact` | 6 |
| \(4!\) | `fact` | 24 |
| Restrictions | `m` | 1 |
| Orientation classes | \(2^M\) | 2 |
| Final count | \(24/2\) | 12 |

Exactly half of the \(24\) permutations put \(1\) before \(3\), so the answer is `12`. The actual identities of the two students do not matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(N+M+\log MOD)\) | The factorial takes \(O(N)\), reading restrictions takes \(O(M)\), and modular exponentiation takes \(O(\log MOD)\) multiplications. |
| Space | \(O(1)\) auxiliary | The restrictions are consumed without being stored. |

With \(N\le10^5\), the factorial loop performs only \(10^5\) iterations. The restriction count is at most \(1000\), so the total work is easily within the two-second limit. The program also uses constant auxiliary memory apart from the input machinery.

## Test Cases

The following harness mirrors the submitted solution while allowing several independent calls.

```python
import sys
import io

MOD = 10**9 + 7

def solution():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    for _ in range(m):
        input()

    fact = 1
    for x in range(1, n + 1):
        fact = fact * x % MOD

    denominator = pow(2, m, MOD)
    inverse_denominator = pow(denominator, MOD - 2, MOD)

    print(fact * inverse_denominator % MOD)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """4 2
2 1
4 3
"""
).strip() == "6", "sample 1"

# Provided sample 2
assert run(
    """4 1
1 3
"""
).strip() == "12", "sample 2"

# Minimum size: one student, no restrictions
assert run(
    """1 0
"""
).strip() == "1", "minimum size"

# No restrictions: every permutation is valid
assert run(
    """5 0
"""
).strip() == "120", "M = 0"

# Three disjoint restrictions
assert run(
    """6 3
1 2
3 4
5 6
"""
).strip() == "90", "three independent pairs"

# Boundary student numbers: the identities do not affect the count
assert run(
    """4 1
1 4
"""
).strip() == "12", "boundary endpoints"

# Maximum-size configuration allowed by the constraints
n = 100000
m = 1000
pairs = "\n".join(f"{2 * i - 1} {2 * i}" for i in range(1, m + 1))
max_input = f"{n} {m}\n{pairs}\n"

expected = 1
for x in range(1, n + 1):
    expected = expected * x % MOD
expected = expected * pow(pow(2, m, MOD), MOD - 2, MOD) % MOD

assert run(max_input).strip() == str(expected), "maximum-size case"
```

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 0` | `1` | Minimum \(N\), zero restrictions, and the \(0!\)-style boundary |
| `5 0` | `120` | No restrictions, so every permutation is valid |
| `6 3` with pairs `(1,2)`, `(3,4)`, `(5,6)` | `90` | Several independent restrictions |
| `4 1` with pair `(1,4)` | `12` | Boundary student numbers and a single restriction |
| \(N=100000,\ M=1000\) with \(1000\) disjoint pairs | Computed modulo \(10^9+7\) | Maximum constraints and performance |

The constraints forbid repeated endpoints, so a test with several identical pair values would not be a valid test case. Testing \(M=0\) is the appropriate way to cover the unrestricted, all-students-equally-free situation.

## Edge Cases

The first edge case is \(M=0\). For

```text
1 0
```

the algorithm skips the restriction-reading loop, computes \(1!=1\), obtains \(2^0=1\), and multiplies by its inverse \(1\). The result is `1`. More generally, for `5 0`, the result is \(5!=120\), because there is no ordering restriction at all.

The second edge case is a single restriction. Consider

```text
4 1
1 4
```

The algorithm computes \(4!=24\). There are \(2^1=2\) possible orientations of the pair \((1,4)\), and both orientations contain the same number of permutations. Dividing by two gives `12`. This also shows why the student numbers themselves do not enter the formula.

The third edge case is several independent restrictions:

```text
6 3
1 2
3 4
5 6
```

The algorithm computes \(6!=720\) and divides by \(2^3=8\), giving `90`. Each pair independently contributes a factor of one half, so the three restrictions together contribute \(1/8\).

The final edge case is the maximum input size. With \(N=100000\) and \(M=1000\), there are still only \(100000\) factorial multiplications and \(1000\) restrictions to consume. The algorithm never constructs a permutation and never stores the pairs, so its running time remains linear in the number of students and its auxiliary memory remains constant. This is precisely the scale that makes the factorial counting formula suitable for the given limits.
:::
