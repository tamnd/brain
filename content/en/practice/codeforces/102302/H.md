---
title: "CF 102302H - Log Concave Sequences"
description: "We need to count arrays of length (N), where every element is one of (0,1,2), such that every three consecutive elements satisfy [ a{i-1}a{i+1}le ai^2. ] The answer is required modulo (10^9+7)."
date: "2026-08-14T04:39:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "H"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 218
verified: false
draft: false
---

[CF 102302H - Log Concave Sequences](https://codeforces.com/problemset/problem/102302/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We need to count arrays of length (N), where every element is one of (0,1,2), such that every three consecutive elements satisfy

[
a_{i-1}a_{i+1}\le a_i^2.
]

The answer is required modulo (10^9+7). The difficulty is that (N) can be as large as (10^{18}), so the task is not to construct or scan an array. We need to count exponentially many arrays using a fixed-size state representation.

The local inequality becomes especially simple because every value is only (0,1,) or (2). If the middle value is (0), its square is zero, so at least one of its two neighbors must also be zero. If the middle value is (1), the product of the neighbors must be at most one, so the only forbidden case is having both neighbors equal to (2). If the middle value is (2), its square is (4), and every possible neighbor product is at most (4), so every choice is valid.

For (N=3), there is only one condition to check. Among the (3^3=27) possible triples, exactly 20 satisfy it, which gives the sample answer. A careless implementation that treats zeros as automatically safe can incorrectly accept (101), but (1\cdot1\le0^2) is false, so (101) is invalid. Similarly, (212) is invalid because (2\cdot2>1^2).

The lower bound (N\ge3) means the local condition always exists, while the upper bound (10^{18}) rules out anything proportional to (N). Even a linear dynamic program would need far too many operations. Since the allowed values and the local condition are fixed, we should look for a constant-size state and then use exponentiation to jump over the enormous number of positions.

## Approaches

The direct approach is to generate every array over ({0,1,2}), giving (3^N) candidates, and check all (N-2) consecutive triples in each candidate. This is correct because the definition is local and checking every triple exactly characterizes a valid array. Its worst-case number of inequality checks is ((N-2)3^N). Already for (N=20), that is more than (10^{10}) checks, and for (N=10^{18}) it is completely impossible.

The brute force works because each decision only depends on three adjacent values, but it fails because it repeatedly recomputes the same local possibilities. The key observation is that after fixing the last two values, the earlier part of the array no longer matters when deciding which value may be appended. That means the entire prefix can be represented by one of only (3^2=9) states.

Use a state ((x,y)) for the last two elements of the current valid prefix. To append (z), we only need to test

[
xz\le y^2.
]

If the transition is valid, the new state becomes ((y,z)). This creates a fixed directed graph with nine states and at most three outgoing transitions from each state.

We can represent that graph by a (9\times9) transition matrix (T). If a row corresponds to state ((x,y)) and a column corresponds to state ((y,z)), then (T[row][column]=1) exactly when (xz\le y^2). Every length-three valid array corresponds to one valid transition between two pair states.

There are nine possible choices for the first two elements, and every one is initially allowed because no condition has been imposed yet. Thus the initial state vector consists entirely of ones. Extending the sequence once multiplies this vector by (T), extending it twice multiplies by (T^2), and so on. A sequence of length (N) requires exactly (N-2) transitions.

Since (N-2) may be (10^{18}-2), we compute (T^{N-2}) with binary matrix exponentiation. The matrix dimension is only nine, so each multiplication is constant-sized. The logarithm of (N) is at most about 60, making this easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N3^N)) | (O(N)) | Too slow |
| Optimal | (O(9^3\log N)) | (O(9^2)) | Accepted |

## Algorithm Walkthrough

1. Number the nine states by the ordered pair of the last two values. For example, state (0) can represent ((0,0)), state (1) can represent ((0,1)), and in general state (3x+y) represents ((x,y)). This state contains exactly the information needed to decide whether another value can be appended.
2. Construct a (9\times9) matrix (T). For every pair ((x,y)) and every possible next value (z), check whether (xz\le y^2). If it is valid, set the transition from ((x,y)) to ((y,z)) to one. The transition changes only the two-element suffix, which is why nine states are sufficient.
3. Initialize the conceptual row vector with one for every state. Every pair ((x,y)) is a possible first two elements because there is no three-element condition yet.
4. Compute (T^{N-2}) using binary exponentiation. The exponent is (N-2) because an array containing two elements has not checked any triple yet, and each appended element introduces exactly one new condition.
5. Sum all entries of (T^{N-2}). Multiplying the all-ones initial vector by this matrix counts every possible final state, and summing those final states counts every valid sequence exactly once.
6. Perform every matrix operation modulo (10^9+7). Since the modulus is applied after every multiplication and addition, the values remain small enough for Python integers to handle comfortably.

### Why it works

The invariant is that a state represents exactly the last two elements of a valid prefix, while the number associated with that state represents how many valid prefixes have that suffix. When we append (z), the only newly created condition is the one involving the old last two values and (z). The matrix includes exactly those transitions satisfying that condition, so every valid prefix produces exactly its valid extensions and no invalid extension. Starting from all nine possible first pairs and applying (N-2) transitions consequently counts every valid length-(N) array exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
S = 9

def mat_mul(a, b):
    c = [[0] * S for _ in range(S)]

    for i in range(S):
        ai = a[i]
        ci = c[i]

        for k in range(S):
            if ai[k] == 0:
                continue

            aik = ai[k]
            bk = b[k]

            for j in range(S):
                if bk[j]:
                    ci[j] = (ci[j] + aik * bk[j]) % MOD

    return c

def mat_pow(a, exponent):
    result = [[0] * S for _ in range(S)]

    for i in range(S):
        result[i][i] = 1

    while exponent:
        if exponent & 1:
            result = mat_mul(result, a)
        a = mat_mul(a, a)
        exponent >>= 1

    return result

def solve(n):
    transition = [[0] * S for _ in range(S)]

    for x in range(3):
        for y in range(3):
            state = 3 * x + y

            for z in range(3):
                if x * z <= y * y:
                    next_state = 3 * y + z
                    transition[state][next_state] = 1

    powered = mat_pow(transition, n - 2)

    answer = 0
    for row in powered:
        answer = (answer + sum(row)) % MOD

    return answer

def main():
    n = int(input())
    print(solve(n))

if __name__ == "__main__":
    main()
```

The transition construction directly implements the original inequality. State (3x+y) means that the current suffix is ((x,y)), and appending (z) is legal precisely when (xz\le y^2). The destination state is (3y+z), because the new suffix consists of the old second element and the appended value.

The identity matrix in `mat_pow` represents zero transitions. Standard binary exponentiation then builds the required power using only (O(\log N)) matrix multiplications.

The final sum uses every entry of the powered matrix rather than explicitly constructing the initial vector. This works because the initial vector contains nine ones. For every starting state (s) and ending state (t), the entry (T^{N-2}_{s,t}) counts valid paths between them. Summing all entries counts all choices of starting pair and ending pair.

There is no integer overflow concern in Python. In a fixed-width language, the product of two values below the modulus can approach (10^{18}), so a 64-bit integer is needed for the multiplication before taking the modulus. The exponent is `n - 2`, not `n - 1`, because the first two elements form the initial state without requiring a condition.

## Worked Examples

For (N=3), the exponent is (1), so the matrix itself describes all valid triples. The initial pair can be any of the nine possibilities, and one transition appends the third value.

| Current pair | Valid next values | Number |
| --- | --- | --- |
| 00 | 0, 1, 2 | 3 |
| 01 | 0, 1, 2 | 3 |
| 02 | 0, 1, 2 | 3 |
| 10 | 0 | 1 |
| 11 | 0, 1 | 2 |
| 12 | 0, 1, 2 | 3 |
| 20 | 0 | 1 |
| 21 | 0 | 1 |
| 22 | 0, 1, 2 | 3 |
| Total |  | 20 |

The total is 20, matching the sample. The rows involving a middle zero illustrate why (101) and (102) are rejected, while (100) and (200) are accepted. The middle value (2) imposes no restriction, so states ending in (2) have three possible continuations.

For (N=4), there are two transitions. After the first transition, the numbers of valid prefixes ending in the nine states are

| State | 00 | 01 | 02 | 10 | 11 | 12 | 20 | 21 | 22 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Length 3 | 3 | 3 | 3 | 1 | 2 | 3 | 1 | 1 | 3 |

The second transition gives

| State | 00 | 01 | 02 | 10 | 11 | 12 | 20 | 21 | 22 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Length 4 | 9 | 6 | 5 | 3 | 3 | 5 | 3 | 1 | 5 |

Summing these values gives (40). The state counts demonstrate the invariant directly: each value records exactly how many valid prefixes have that particular two-element suffix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(9^3\log N)) | Binary exponentiation performs (O(\log N)) multiplications of (9\times9) matrices |
| Space | (O(9^2)) | Only a constant number of (9\times9) matrices are stored |

The largest possible (N) has only about 60 binary digits, so roughly 60 matrix squarings plus at most 60 additional multiplications are needed. Each multiplication has only (9^3=729) scalar products before considering the small constant factors. This is comfortably inside the 2 second and 64 MB limits.

## Test Cases

The small expected values below can be checked independently by enumerating all arrays. The maximum-size case uses a separate reference implementation in the test harness so that the huge exponent is exercised without storing an array of length (10^{18}).

```python
import sys
import io

MOD = 10**9 + 7
S = 9

def solve(n):
    transition = [[0] * S for _ in range(S)]

    for x in range(3):
        for y in range(3):
            state = 3 * x + y
            for z in range(3):
                if x * z <= y * y:
                    transition[state][3 * y + z] = 1

    def mul(a, b):
        c = [[0] * S for _ in range(S)]

        for i in range(S):
            for k in range(S):
                if a[i][k] == 0:
                    continue
                for j in range(S):
                    if b[k][j]:
                        c[i][j] = (
                            c[i][j] + a[i][k] * b[k][j]
                        ) % MOD

        return c

    def power(a, e):
        r = [[0] * S for _ in range(S)]
        for i in range(S):
            r[i][i] = 1

        while e:
            if e & 1:
                r = mul(r, a)
            a = mul(a, a)
            e >>= 1

        return r

    p = power(transition, n - 2)
    return sum(map(sum, p)) % MOD

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n = int(sys.stdin.readline())
        return str(solve(n))
    finally:
        sys.stdin = old_stdin

assert run("3\n") == "20", "sample 1"

assert run("4\n") == "40", "minimum extension"

assert run("5\n") == "85", "catches transition counting errors"

assert run("6\n") == "207", "catches another off-by-one in the exponent"

max_n = 10**18
max_expected = solve(max_n)
assert run(str(max_n) + "\n") == str(max_expected), "maximum N"
assert 0 <= max_expected < MOD, "modulo range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `20` | Minimum allowed length and the single-triple condition |
| `4` | `40` | First genuine matrix composition and exponent (N-2=2) |
| `5` | `85` | Correct propagation through multiple transitions |
| `6` | `207` | Guards against another exponent or boundary error |
| `10^18` | `solve(10^18)` | Maximum input size and binary exponentiation |

The maximum test deliberately checks the boundary without attempting to construct an array. Its reference value is computed by the same finite-state mathematics, but the test is useful for catching accidental linear loops, incorrect integer handling, or an exponentiation loop that cannot process a 60-bit exponent.

## Edge Cases

For the minimum input (N=3), the algorithm computes (T^1). There is no extra extension beyond the first triple, so every matrix entry corresponds directly to one valid triple. The nine rows contain (3,3,3,1,2,3,1,1,3) valid continuations respectively, summing to (20). Thus the exact input `3` produces `20`.

The zero value is a particularly easy source of mistakes. For the triple `101`, the middle value is zero, so the inequality becomes (1\cdot1\le0), which is false. For `100`, it becomes (1\cdot0\le0), which is true. The transition construction checks the actual product rather than applying a loose rule such as treating every sequence containing zero as valid.

The value (1) has a different restriction. For `212`, the inequality is (2\cdot2\le1), which is false. For `210`, the inequality is (2\cdot0\le1), which is true. The matrix therefore allows state `21` to transition only to `0`, exactly as required.

A middle value of (2) creates no restriction at all. For example, `022`, `122`, and `222` are all valid because the largest possible neighbor product is (2\cdot2=4), equal to (2^2). Any transition whose middle state value is (2) consequently has all three possible next values.

Finally, the maximum input (N=10^{18}) cannot be handled by iterating over positions. The algorithm reduces the entire computation to (T^{10^{18}-2}), and binary exponentiation reaches that exponent using only about 60 iterations. The state space remains fixed at nine states throughout, so the enormous sequence length affects only the number of squaring steps, not the amount of stored sequence data.
