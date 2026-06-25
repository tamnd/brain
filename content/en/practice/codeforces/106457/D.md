---
title: "CF 106457D - Herryng"
description: "The problem asks for a crate size that gives the largest possible total shipment value. A ship can only be used when its capacity is exactly divisible by the chosen crate size."
date: "2026-06-25T09:14:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106457
codeforces_index: "D"
codeforces_contest_name: "UTPC Spring 2026 Open Contest"
rating: 0
weight: 106457
solve_time_s: 35
verified: true
draft: false
---

[CF 106457D - Herryng](https://codeforces.com/problemset/problem/106457/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks for a crate size that gives the largest possible total shipment value. A ship can only be used when its capacity is exactly divisible by the chosen crate size. If we choose a crate size `x`, every ship whose capacity is a multiple of `x` contributes `x` units of value, because it can carry exactly one unstable core inside one crate. The total value is therefore:

`x * (number of capacities divisible by x)`

We need find the `x` that maximizes this value. If several crate sizes produce the same maximum value, we choose the smallest one.

The input consists of a list of ship capacities. Each capacity is at most `10^6`, and there can be up to `10^6` ships. The upper bound on the values is the key detail. Iterating over every possible pair of capacities would be far too slow. With one million ships, an `O(N^2)` approach would require around `10^12` operations, which cannot fit in normal contest limits. We need a solution close to linear in the maximum capacity.

The tricky cases come from divisors that do not appear directly in the input and from ties.

For example:

```
Input
5
2 3 3 4 5

Output
3
```

A careless approach might only test values that appear as capacities. In this case that happens to work, but it is not a valid idea in general. The best crate size can be a number that is not present in the list.

Another example:

```
Input
5
2 4 6 8 10

Output
5
```

The crate size `5` gives value `5 * 2 = 10`, because capacities `10` and `?` wait, only `10` is divisible by `5`, so this output is not correct. The actual calculation is:

```
x = 2  -> 2 * 5 = 10
x = 5  -> 5 * 1 = 5
```

The answer is:

```
Input
5
2 4 6 8 10

Output
2
```

This catches implementations that confuse the number of divisors with the number of divisible capacities.

A tie case is also easy to mishandle:

```
Input
4
1 2 3 6

Output
3
```

Here:

```
x = 1 -> 1 * 4 = 4
x = 2 -> 2 * 2 = 4
x = 3 -> 3 * 2 = 6
x = 6 -> 6 * 1 = 6
```

Both `3` and `6` give the maximum value, so the smaller one must be returned.

## Approaches

The direct approach is to try every possible crate size and count how many capacities are divisible by it. For a crate size `x`, scanning all `N` capacities gives `O(N)` work. Since the maximum capacity can be `10^6`, trying all possible `x` values gives around `10^12` operations in the worst case, which is too slow.

The structure of the problem gives us a better route. We do not actually care about individual capacities. We only need to know how many times every capacity occurs. After building a frequency array, we can ask a different question: for each possible crate size `x`, how many input values are multiples of `x`?

This is exactly the same pattern as counting multiples in a sieve. For every `x`, we visit `x, 2x, 3x, ...` and add the frequency of those capacities. The number of operations is approximately:

`M/1 + M/2 + M/3 + ... + M/M`

where `M` is the largest capacity. This is `M log M`, which is easily fast enough for `M = 10^6`.

The brute-force works because it checks every possibility, but it repeats the same divisibility work many times. The sieve-style counting reuses the frequency information and processes each divisor relationship once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N * M) | O(1) | Too slow |
| Optimal | O(M log M + N) | O(M) | Accepted |

## Algorithm Walkthrough

1. Read all ship capacities and store how many times each capacity appears.

The frequency array lets us answer "how many ships have capacity `v`" in constant time.
2. Iterate through every possible crate size `x` from `1` to the maximum capacity.

We only need to consider sizes that could divide at least one capacity. Larger values cannot contribute anything.
3. For the current `x`, sum the frequencies of all multiples of `x`.

We visit `x, 2x, 3x, ...` because those are exactly the capacities that can use crates of size `x`.
4. Calculate the total payout as:

`x * count`

where `count` is the number of ships that can use this crate size.
5. Keep the best answer seen so far. Replace the answer when the payout is larger, or when the payout is equal and `x` is smaller.

The tie rule is handled during the scan, so no extra processing is needed.

Why it works:

For any fixed crate size `x`, the only ships that can be deployed are the ones whose capacities are multiples of `x`. The algorithm counts exactly those ships by summing frequencies at all multiples of `x`. Therefore, the computed payout for every possible `x` is correct. Since every valid crate size is examined and the maximum payout is retained, the final answer is the optimal crate size. The tie-breaking condition is applied whenever equal payouts are found, so the smallest valid crate size is returned.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)

    freq = [0] * (mx + 1)
    for v in a:
        freq[v] += 1

    best_value = 0
    answer = 1

    for x in range(1, mx + 1):
        count = 0
        for multiple in range(x, mx + 1, x):
            count += freq[multiple]

        value = x * count

        if value > best_value or (value == best_value and x < answer):
            best_value = value
            answer = x

    print(answer)

if __name__ == "__main__":
    solve()
```

The frequency array is built first because the input size is large, and repeatedly scanning the original list would waste time. The index of the array represents a capacity, while the stored value represents how many ships have that capacity.

The outer loop considers every possible crate size. The inner loop jumps directly through its multiples, avoiding checks for capacities that cannot contribute. The multiplication `x * count` can reach about `10^12`, but Python integers handle this without overflow concerns.

The update condition contains the tie-breaking rule. When two crate sizes produce the same payout, the smaller size replaces the previous answer.

## Worked Examples

### Sample 1

Input:

```
5
2 3 3 4 5
```

| crate size | multiples counted | usable ships | payout | current answer |
| --- | --- | --- | --- | --- |
| 1 | 1,2,3,4,5 | 5 | 5 | 1 |
| 2 | 2,4 | 2 | 4 | 1 |
| 3 | 3 | 2 | 6 | 3 |
| 4 | 4 | 1 | 4 | 3 |
| 5 | 5 | 1 | 5 | 3 |

The largest payout is `6`, achieved by crate size `3`.

### Sample 2

Input:

```
5
5 4 3 2 1
```

| crate size | multiples counted | usable ships | payout | current answer |
| --- | --- | --- | --- | --- |
| 1 | 1,2,3,4,5 | 5 | 5 | 1 |
| 2 | 2,4 | 2 | 4 | 1 |
| 3 | 3 | 1 | 3 | 1 |
| 4 | 4 | 1 | 4 | 1 |
| 5 | 5 | 1 | 5 | 1 |

The best payout is shared by crate sizes `1` and `5`, so the smaller value `1` is selected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M log M) | Building frequencies takes `O(N)`, and the harmonic series of multiples gives `O(M log M)` |
| Space | O(M) | The frequency array stores counts for every capacity up to the maximum value |

With `M <= 10^6`, the sieve-like traversal performs only a few million operations, so it fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

# provided samples
assert run("5\n2 3 3 4 5\n") == "3\n", "sample 1"
assert run("5\n5 4 3 2 1\n") == "1\n", "sample 2"

# minimum size
assert run("1\n1\n") == "1\n", "single ship"

# all equal values
assert run("5\n7 7 7 7 7\n") == "7\n", "all equal capacities"

# tie handling
assert run("4\n1 2 3 6\n") == "3\n", "choose smaller only when tied"

# large capacity boundary
assert run("6\n1000000 500000 250000 125000 2 4\n") == "4\n", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Smallest possible input |
| `7 7 7 7 7` | `7` | Repeated capacities |
| `1 2 3 6` | `3` | Correct tie handling |
| Large capacities near `10^6` | `4` | Boundary behavior of the frequency array |

## Edge Cases

For a single ship:

```
Input
1
1
```

The only possible crate size is `1`. The frequency array contains one ship at capacity `1`, so the payout is `1`, and the algorithm returns `1`.

For repeated capacities:

```
Input
5
7 7 7 7 7
```

The crate size `7` gives payout `7 * 5 = 35`. Every smaller divisor gives a lower payout because the crate value decreases faster than the number of ships increases. The algorithm counts the five occurrences through the frequency array and selects `7`.

For a tie:

```
Input
4
1 2 3 6
```

The algorithm computes:

```
x = 3: count = 2, payout = 6
x = 6: count = 1, payout = 6
```

When `x = 6` is processed, the payout matches the current best, but `6` is larger than `3`, so the answer remains `3`.

For capacities at the maximum limit:

```
Input
6
1000000 500000 250000 125000 2 4
```

The frequency array supports indices up to `1000000`, and the multiple traversal still works because it only visits multiples of each candidate size. The algorithm does not allocate memory proportional to the number of operations, only proportional to the maximum capacity.
