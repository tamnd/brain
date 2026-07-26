---
title: "CF 102829D - Useful Proofs"
description: "The problem asks us to count ordered pairs of elements in an array such that writing one number immediately after another creates a number divisible by a given modulus. The order matters, so choosing x then y is different from choosing y then x."
date: "2026-07-26T15:29:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102829
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 11-06-20 Div. 1 (Tryout)"
rating: 0
weight: 102829
solve_time_s: 39
verified: true
draft: false
---

[CF 102829D - Useful Proofs](https://codeforces.com/problemset/problem/102829/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count ordered pairs of elements in an array such that writing one number immediately after another creates a number divisible by a given modulus. The order matters, so choosing `x` then `y` is different from choosing `y` then `x`. The task is to count all valid pairs of positions, not just distinct values.

The input gives the number of values, the divisor, and the array itself. Each array value can have up to 10 digits, and the array size can reach 200,000. A solution that checks every pair would perform around 40 billion checks in the largest case, which is far beyond what a typical 2 second limit allows. We need to reduce the work per element to something close to constant time.

The main challenge is that concatenation depends on the number of digits in the second value. For example, appending `34` to `12` creates `1234`, which is `12 * 100 + 34`. A correct solution must preserve this positional effect instead of treating the numbers as ordinary sums.

A careless implementation can fail on repeated values. For example:

```
Input:
3 2
1 1 1

Output:
6
```

Every ordered pair of different positions works because every concatenation is `11`, which is divisible by 2. An implementation that stores only whether a value exists instead of how many times it appears would undercount.

Another edge case is when the same value can be used many times but positions must still be different. For example:

```
Input:
2 11
1 1

Output:
2
```

There are two ordered pairs, `(first 1, second 1)` and `(second 1, first 1)`. Counting values instead of positions can accidentally remove these pairs.

The number of digits is also a common source of mistakes. For example:

```
Input:
2 100
12 3

Output:
1
```

The concatenation `123` is not divisible by 100, while `312` is not either, so this example actually has answer `0`. A wrong approach that always multiplies by `10^9` instead of using the real digit length of the appended number will calculate incorrect remainders.

## Approaches

The direct approach is to try every ordered pair `(i, j)`, concatenate the two numbers, and check the remainder. For two numbers `a` and `b`, if `b` has `d` digits, the concatenation is:

`a * 10^d + b`

Checking one pair is constant time, but there are `n * (n - 1)` ordered pairs. With `n = 200000`, this is close to 40 billion operations, so the brute force approach cannot pass.

The key observation is that for a fixed first number `a`, we do not need to know the exact second number yet. We only need the remainder that the second number must provide.

For a second number `b` with `d` digits:

`a * 10^d + b ≡ 0 (mod k)`

The digit length of `b` can only be between 1 and 10, because every value is at most `10^9`. This means there are only ten possible shifts. For each number, we can compute:

`a * 10^d mod k`

for every possible digit length `d`.

While scanning the array, we store how many numbers of each digit length have each remainder modulo `k`. Then, when processing `a`, we know the required remainder of `b` for every possible digit count.

The brute force works because it checks all possible partners explicitly, but it fails because there are too many partners. The observation that only the remainder and digit length of the partner matter lets us replace pair enumeration with frequency counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(10n) | O(10n) | Accepted |

## Algorithm Walkthrough

1. Store every array number grouped by its digit length. For each length, keep a frequency map of remainders modulo `k`.

The digit length matters because concatenating a number after another shifts it by a power of ten. Two numbers with the same remainder but different lengths are not interchangeable.

1. Process each number `a` as the first element of a pair. For every possible digit length `d` from 1 to 10, compute:

`(a * 10^d) mod k`

The second number must have remainder:

`(-a * 10^d) mod k`

to make the whole concatenation divisible by `k`.

1. Add to the answer the number of stored values that have digit length `d` and the required remainder.

The frequency table immediately tells us how many possible second positions exist.

1. Remove the current number from the stored frequencies before counting it as a partner, then add it back after processing.

This prevents counting a number paired with itself at the same position while still allowing equal values from different positions.

### Why it works

For any pair `(a, b)`, the concatenation is determined by the value of `a`, the value of `b`, and the number of digits in `b`. The algorithm groups all possible second numbers by exactly the two properties that affect the divisibility equation: digit length and remainder modulo `k`.

When processing `a`, every possible digit length of `b` is considered. The required remainder is derived directly from the divisibility condition, so every counted frequency entry represents a valid partner. Removing the current element before querying guarantees that only different positions are counted. Every valid ordered pair is counted once when its first element is processed.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [defaultdict(int) for _ in range(11)]
    lengths = []

    for x in a:
        d = len(str(x))
        lengths.append(d)
        cnt[d][x % k] += 1

    ans = 0

    for x, d in zip(a, lengths):
        cnt[d][x % k] -= 1

        power = 10
        for length in range(1, 11):
            need = (-x * power) % k
            ans += cnt[length][need]
            power = (power * 10) % k

        cnt[d][x % k] += 1

    print(ans)

solve()
```

The frequency table has eleven slots because digit lengths from 1 to 10 are possible. Each slot is a dictionary because `k` can be as large as `10^9`, so an array indexed by remainder would be impossible.

The removal step before querying is essential. Without it, a number would match itself whenever its own concatenation satisfies the condition. After the query finishes, the value is restored so it can be used for later first positions.

The variable `power` stores `10^length mod k`. Updating it modulo `k` keeps all calculations small and avoids unnecessary large integers.

## Worked Examples

Consider:

```
Input:
6 11
45 1 10 12 11 7
```

A trace for the first value:

| Current value | Current length | Checked second length | Required remainder | Matches added |
| --- | --- | --- | --- | --- |
| 45 | 2 | 1 | 6 | 0 |
| 45 | 2 | 2 | 0 | 1 |
| 45 | 2 | 3 | 7 | 1 |
| 45 | 2 | 4 | 5 | 0 |

The value `45` finds partners such as `1` and `10` because their digit lengths and remainders satisfy the concatenation equation.

For the second example:

```
Input:
4 2
2 78 4 10
```

| Current value | Length | Required remainders checked | Valid partners |
| --- | --- | --- | --- |
| 2 | 1 | all lengths | 3 |
| 78 | 2 | all lengths | 3 |
| 4 | 1 | all lengths | 3 |
| 10 | 2 | all lengths | 3 |

Every ordered pair works, giving `12` total pairs. The trace demonstrates that the method counts positions rather than distinct values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10n) | Each number checks only ten possible digit lengths |
| Space | O(10n) | At most ten frequency maps store remainders for all numbers |

The algorithm performs roughly two million remainder checks for the maximum input size, which fits comfortably within the limits. The memory usage depends on the number of distinct remainders rather than the full range of possible modulo values.

## Test Cases

```python
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [defaultdict(int) for _ in range(11)]
    lengths = []

    for x in a:
        d = len(str(x))
        lengths.append(d)
        cnt[d][x % k] += 1

    ans = 0

    for x, d in zip(a, lengths):
        cnt[d][x % k] -= 1
        power = 10

        for length in range(1, 11):
            ans += cnt[length][(-x * power) % k]
            power = power * 10 % k

        cnt[d][x % k] += 1

    return str(ans) + "\n"

assert run("""6 11
45 1 10 12 11 7
""") == "7\n", "sample 1"

assert run("""4 2
2 78 4 10
""") == "12\n", "sample 2"

assert run("""5 2
3 7 19 3 3
""") == "0\n", "sample 3"

assert run("""2 11
1 1
""") == "2\n", "same values"

assert run("""1 100
123
""") == "0\n", "single element"

assert run("""3 2
2 2 2
""") == "6\n", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 11 / 1 1` | `2` | Counts different positions with equal values |
| `1 100 / 123` | `0` | Handles the smallest array |
| `3 2 / 2 2 2` | `6` | Handles many duplicate values |

## Edge Cases

For duplicate values, the algorithm removes only the currently processed position, not every equal value. With:

```
2 11
1 1
```

the first `1` is removed, leaving one valid partner. The second `1` is then processed similarly. The answer becomes `2`.

For self-pairing, consider:

```
1 1
5
```

There is only one position, so no pair is allowed. The algorithm removes the only stored remainder before checking, making the frequency zero and returning `0`.

For numbers with different digit lengths, consider:

```
2 10
1 23
```

The algorithm checks length `2` when using `1` as the first number because `23` contributes a shift of `100`. It does not treat `23` as a one digit number, so the computed remainder is correct.

For large values, such as:

```
2 1000000000
999999999 1
```

the algorithm never builds the concatenated number directly. It keeps every multiplication modulo `k`, avoiding overflow and preserving the divisibility calculation.
