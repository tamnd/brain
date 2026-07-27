---
title: "CF 102777H - \u041f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0410\u0441\u043b\u0430\u043d\u0430"
description: "We need find the value of a sequence at a very large position. The first two elements are fixed, and every next element is created from the previous two elements plus a value that depends on the current index."
date: "2026-07-27T20:34:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "H"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 63
verified: true
draft: false
---

[CF 102777H - \u041f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0410\u0441\u043b\u0430\u043d\u0430](https://codeforces.com/problemset/problem/102777/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We need find the value of a sequence at a very large position. The first two elements are fixed, and every next element is created from the previous two elements plus a value that depends on the current index. The required answer is the element at position `n`, printed modulo `10^9 + 7`.

The difficulty comes from the size of `n`. Since `n` can reach `10^9`, an algorithm that computes every previous element one by one would require about one billion transitions, which is too slow in a one second limit. We need to reduce the number of operations from depending on `n` to depending on the number of bits in `n`, which suggests a logarithmic approach.

The boundary cases are the first two positions. For `n = 1`, the answer is `1`, and for `n = 2`, the answer is also `1`. A solution that immediately starts matrix exponentiation from `n - 2` without handling these values would create an invalid starting state. For example, input `1` must produce `1`, while a careless implementation may try to raise a transition matrix to a negative power.

Another easy mistake is forgetting that the recurrence contains the index itself. For input `3`, the calculation is `2 * 1 + 3 * 1 + 3`, giving `8`. Treating the recurrence like a normal Fibonacci-style linear recurrence and ignoring the added index value would produce an incorrect result.

## Approaches

A direct solution follows the definition literally. We store the last two values and repeatedly calculate the next one until reaching `n`. This is correct because each transition uses exactly the previous two values and the current index, so after `n - 2` transitions the stored value is the answer. The problem is the number of transitions. For `n = 10^9`, the algorithm performs roughly one billion iterations, which is far beyond what is practical.

The key observation is that the recurrence is almost a linear recurrence. The only extra part is the added `n`, and a value that changes linearly can itself be stored as part of the state. We can represent the current situation with four numbers: the current sequence value, the previous sequence value, the current index, and a constant `1`.

For a state `[F_k, F_{k-1}, k, 1]`, the next state is `[F_{k+1}, F_k, k+1, 1]`. This transformation is a fixed matrix multiplication. Once the recurrence becomes repeated multiplication by one constant matrix, binary exponentiation lets us jump from index `2` to index `n` in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Handle the two initial positions directly. If `n` is `1` or `2`, return `1` because the recurrence is only defined after these values.
2. Build the transition matrix. The state is `[F_k, F_{k-1}, k, 1]`, and the next state is produced by the matrix

```
[2 3 1 1]
[1 0 0 0]
[0 0 1 1]
[0 0 0 1]
```

The first row creates the next sequence value, the second row shifts the previous value forward, and the last two rows maintain the current index and constant term.

1. Start from the state at `k = 2`, which is `[1, 1, 2, 1]`.
2. Raise the transition matrix to the power `n - 2` using binary exponentiation. Each multiplication applies many transitions at once, and squaring the matrix reduces the required number of operations to logarithmic time.
3. Multiply the powered matrix by the starting state. The first component of the resulting vector is `F_n`, which is the required answer.

Why it works: the state always stores exactly the information needed to perform one more recurrence step. Applying the transition matrix once changes the state from index `k` to index `k + 1`. Applying it `n - 2` times therefore moves the known state at index `2` to the desired state at index `n`. Matrix exponentiation only changes how those repeated applications are grouped, not the transformation being applied, so the resulting first component is always the correct sequence value.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def multiply(a, b):
    n = len(a)
    m = len(b[0])
    k = len(b)
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0
            for x in range(k):
                s += a[i][x] * b[x][j]
            res[i][j] = s % MOD
    return res

def power_matrix(a, e):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while e:
        if e & 1:
            res = multiply(res, a)
        a = multiply(a, a)
        e >>= 1
    return res

def solve():
    n = int(input())
    if n <= 2:
        print(1)
        return

    transition = [
        [2, 3, 1, 1],
        [1, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1]
    ]

    state = [
        [1],
        [1],
        [2],
        [1]
    ]

    result = multiply(power_matrix(transition, n - 2), state)
    print(result[0][0])

if __name__ == "__main__":
    solve()
```

The `multiply` function handles multiplication of small matrices while reducing every value modulo `10^9 + 7`. Since the matrix size never changes from `4 x 4`, this operation is constant-sized.

The `power_matrix` function is standard binary exponentiation. Instead of applying the transition `n - 2` times, it repeatedly squares the transition matrix and uses the set bits of `n - 2` to select the needed powers.

The starting vector represents the second sequence element. Its third component is `2`, because the transition needs to know the current index in order to add the next index value. The special handling of `n <= 2` prevents invalid exponent values and avoids unnecessary matrix work.

## Worked Examples

For `n = 3`, the matrix is applied once.

| Step | Current index | State |
| --- | --- | --- |
| Start | 2 | `[1, 1, 2, 1]` |
| Apply transition | 3 | `[8, 1, 3, 1]` |

The first component becomes `8`, matching the recurrence calculation `2 * 1 + 3 * 1 + 3`.

For `n = 5`, the matrix is applied three times.

| Step | Current index | State |
| --- | --- | --- |
| Start | 2 | `[1, 1, 2, 1]` |
| Apply transition | 3 | `[8, 1, 3, 1]` |
| Apply transition | 4 | `[23, 8, 4, 1]` |
| Apply transition | 5 | `[75, 23, 5, 1]` |

The trace shows that the first two components always contain consecutive sequence values, while the index component increases exactly with each transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Binary exponentiation performs logarithmically many matrix squarings and multiplications. |
| Space | O(1) | Only a fixed number of 4 by 4 matrices and vectors are stored. |

The largest input only requires about 30 exponentiation steps because `log2(10^9)` is small. The constant matrix size keeps the solution well within the memory and time limits.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# The expected values are produced by the same recurrence definition.
assert run("1\n") == "1\n", "minimum position"
assert run("2\n") == "1\n", "second base position"
assert run("3\n") == "8\n", "first recurrence step"
assert run("5\n") == "75\n", "several recurrence steps"

# Maximum-size smoke test: checks that the logarithmic solution handles the limit.
assert len(run("1000000000\n").strip()) <= 10, "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Handles the smallest possible index. |
| `2` | `1` | Handles the second base value. |
| `3` | `8` | Checks the first use of the recurrence. |
| `5` | `75` | Checks several transitions in sequence. |
| `1000000000` | Ten or fewer digits modulo `10^9 + 7` | Confirms that the algorithm scales to the maximum index. |

## Edge Cases

For input `1`, the algorithm returns immediately before building a matrix. The answer is the predefined first sequence value, so no transition is needed.

For input `2`, the same direct return is used. Starting matrix exponentiation here would require raising the matrix to the power zero, which is mathematically possible, but the explicit handling keeps the boundary behavior clear and avoids unnecessary work.

For input `3`, the algorithm performs exactly one transition from `[1, 1, 2, 1]`. The resulting first component is `8`, proving that the additional index term is included correctly.

For input `1000000000`, the algorithm never creates all previous sequence values. It only performs around thirty matrix squaring steps, so the huge index affects the number of bits processed rather than the number of sequence elements generated.

I can also adapt this editorial to a shorter Codeforces-style format if you want something closer to what would be published in an official contest editorial.
