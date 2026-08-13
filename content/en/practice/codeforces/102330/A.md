---
title: "CF 102330A - \u0414\u043e\u043a\u0442\u043e\u0440 \u0410\u0439\u0431\u043e\u043b\u0438\u0442"
description: "We have an array a of n animals. The value a[i] is the amount of time Doctor Aibolit needs to examine animal i. The doctor handles one animal at a time, so the animals form a single queue. For a chosen order, the first animal waits 0 time units."
date: "2026-08-14T01:00:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102330
codeforces_index: "A"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2019.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102330
solve_time_s: 309
verified: true
draft: false
---

[CF 102330A - \u0414\u043e\u043a\u0442\u043e\u0440 \u0410\u0439\u0431\u043e\u043b\u0438\u0442](https://codeforces.com/problemset/problem/102330/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `a` of `n` animals. The value `a[i]` is the amount of time Doctor Aibolit needs to examine animal `i`. The doctor handles one animal at a time, so the animals form a single queue.

For a chosen order, the first animal waits `0` time units. The second waits for the entire examination of the first animal. The third waits for the first two examinations, and so on. We need to choose the order of the array elements so that the sum of all waiting times is as small as possible.

For example, if the examination times are `[5, 1, 2]` and we use the order `[1, 2, 5]`, the waiting times are `0`, `1`, and `3`, giving a total of `4`.

The number of animals can reach `10^6`, while every examination time is at most `10^5`. An algorithm such as `O(n^2)` would already require around `10^12` operations in the worst case, which is far beyond a one-second limit. Even `O(n log n)` must be implemented reasonably efficiently because the input itself contains one million numbers, but it is easily feasible. The answer can be much larger than a 32-bit integer: if all `10^6` examination times equal `10^5`, the answer is about `5 * 10^16`. Python integers handle this automatically.

There are several small cases that can expose mistakes. With one animal, for example, the input is

```
1
7
```

and the answer is `0`, because nobody waits. An implementation that adds the current examination time before accumulating the answer would incorrectly produce `7`.

With equal examination times, every order is equivalent. For

```
5
2 2 2 2 2
```

the waiting times are `0, 2, 4, 6, 8`, so the answer is `20`. A solution that accidentally sorts in descending order would not fail on this case, which makes equal values useful for checking that the formula itself is correct rather than relying only on the ordering.

The other common edge case is that the shortest animal must be processed first even if it appeared later in the input. For

```
3
7 1 2
```

the optimal order is `1, 2, 7`, giving waiting times `0, 1, 3` and answer `4`. Simply processing animals in their input order gives `0 + 7 + 8 = 15`, so an implementation that never reorders the array fails immediately.

## Approaches

A direct brute-force approach would try every possible order of the animals. For each permutation, we could scan it from left to right, keep the total examination time already performed, and add that value to the answer for every animal. This is correct because every possible schedule is considered and we can choose the one with the smallest waiting-time sum.

The problem is the number of permutations. There are `n!` possible orders, and evaluating one order takes `O(n)` time, so the total complexity is `O(n · n!)`. Even for `n = 20`, this is already enormous. For `n = 10^6`, it is not merely too slow, it is impossible to begin enumerating the schedules.

The structure of the waiting time gives us a much stronger observation. Suppose two consecutive animals have examination times `x` and `y`, and everything before them has already taken `T` time. If the order is `x, y`, their contribution to the total waiting time is

`T + (T + x) = 2T + x`.

If we swap them to `y, x`, their contribution becomes

`T + (T + y) = 2T + y`.

The difference depends only on `x` and `y`. If `x > y`, putting `y` first makes the total smaller. Thus whenever a longer examination is immediately before a shorter one, swapping them improves the schedule.

By repeatedly removing such inversions, the examination times become sorted in nondecreasing order. Since every inversion can only make the answer worse, an optimal schedule is obtained by sorting the array from smallest to largest.

Once the order is known, there is no need to explicitly store every waiting time. Maintain `prefix`, the total examination time of all animals already processed. The current animal waits exactly `prefix` time units, so add `prefix` to the answer and then increase `prefix` by the current examination time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · n!)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read `n` and the `n` examination times into an array. The original positions do not matter because the goal is only to find the best ordering.
2. Sort the array in nondecreasing order. A shorter examination should be placed earlier because every animal after it benefits from the smaller amount of time added to its waiting time.
3. Initialize `prefix = 0` and `answer = 0`. Here `prefix` represents the total examination time of all animals already placed before the current animal.
4. Traverse the sorted array from left to right. For the current examination time `x`, add `prefix` to `answer`, because exactly `prefix` time units have elapsed before this animal can enter the doctor's office.
5. Add `x` to `prefix`. The current animal has now been processed, so its examination time becomes part of the waiting time for every subsequent animal.
6. After all animals have been processed, output `answer`. The first animal contributes zero because `prefix` is initially zero.

### Why it works

Consider any schedule containing two adjacent examination times `x` and `y` with `x > y`. Everything before these two animals takes some fixed amount `T`. In the order `x, y`, their total contribution is `2T + x`, while in the order `y, x` it is `2T + y`. Since `y < x`, swapping them strictly decreases the total waiting time.

Consequently, an optimal schedule cannot contain an adjacent inversion. If an array is not sorted, it has an inversion, and repeatedly swapping inverted adjacent pairs eventually produces the nondecreasing order without increasing the answer. Thus the sorted order is optimal. After sorting, the prefix sum exactly equals the waiting time of each current animal, so accumulating it produces the minimum possible total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    prefix = 0
    answer = 0

    for x in a:
        answer += prefix
        prefix += x

    print(answer)

if __name__ == "__main__":
    solve()
```

The first two lines read the number of animals and the examination times. There is only one test case in this problem, so no outer test-case loop is needed.

`a.sort()` puts the examination times into the required shortest-first order. Python's built-in sort runs in `O(n log n)` time and is implemented efficiently enough for one million integers.

The loop deliberately adds `prefix` to `answer` before adding the current `x` to `prefix`. This order is essential. The current animal does not wait for its own examination, it only waits for examinations of animals before it. For an array `[1, 2, 3]`, the sequence of prefixes used for the answer is `0, 1, 3`, not `1, 3, 6`.

Python's integer type also avoids overflow. The maximum possible answer is on the order of `5 * 10^16`, which would exceed a signed 32-bit integer, but Python represents such values exactly.

The input size is large, so the solution uses `sys.stdin.readline` as requested. The memory usage is dominated by storing the one-million-element array.

## Worked Examples

### Sample 1

The first sample is

```
5
2 2 2 2 2
```

Sorting changes nothing. Each animal requires two units of examination time.

| Animal | Examination time | Prefix before animal | Added to answer | Answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | 0 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 2 | 4 | 4 | 6 |
| 4 | 2 | 6 | 6 | 12 |
| 5 | 2 | 8 | 8 | 20 |

The final answer is `20`. This also demonstrates that the first animal contributes no waiting time, while every later animal waits for all examinations before it.

### Sample 2

The second sample is

```
5
5 1 2 7 3
```

After sorting, the examination times are `[1, 2, 3, 5, 7]`.

| Animal | Examination time | Prefix before animal | Added to answer | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 1 | 1 |
| 3 | 3 | 3 | 3 | 4 |
| 4 | 5 | 6 | 6 | 10 |
| 5 | 7 | 11 | 11 | 21 |

The final answer is `21`. The trace shows the central invariant directly: before processing each animal, `prefix` is exactly the amount of time that animal must wait.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting dominates the linear scan |
| Space | `O(n)` | The array stores all `n` examination times |

For `n = 10^6`, sorting one million integers is practical, while the following scan takes only `O(n)` additional operations. The answer can reach roughly `5 * 10^16`, and Python integers safely represent it.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    prefix = 0
    answer = 0

    for x in a:
        answer += prefix
        prefix += x

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("5\n2 2 2 2 2\n") == "20", "sample 1"
assert run("5\n5 1 2 7 3\n") == "21", "sample 2"

# Minimum-size input
assert run("1\n7\n") == "0", "one animal waits zero time"

# Already sorted, checks that the prefix is added before the current duration
assert run("3\n1 2 3\n") == "4", "already sorted input"

# Reverse order, checks that sorting is actually performed
assert run("3\n7 2 1\n") == "4", "reverse order"

# All values at the maximum boundary
assert run("4\n100000 100000 100000 100000\n") == "600000", "maximum ai"

# Large n and large values, checks that the answer exceeds 32-bit range
assert run("1000000\n" + "100000 " * 1000000) == "49999950000000000", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum size and zero waiting time for the first animal |
| `3 / 1 2 3` | `4` | Prefix must be added before the current duration |
| `3 / 7 2 1` | `4` | Sorting is necessary |
| `4 / 100000 100000 100000 100000` | `600000` | Maximum examination-time boundary |
| `1000000 / all values 100000` | `49999950000000000` | Maximum `n` and large integer result |

The last test is intentionally large. It checks both the asymptotic behavior and the fact that the implementation does not accidentally use a fixed-width 32-bit accumulator.

## Edge Cases

For one animal, the input

```
1
7
```

is sorted unchanged. The loop starts with `prefix = 0`, so the answer receives `0`. Then `prefix` becomes `7`, but there is no next animal that could wait for it. The output is `0`.

For equal examination times,

```
5
2 2 2 2 2
```

every possible ordering has exactly the same result. The algorithm processes the five values and adds prefixes `0, 2, 4, 6, 8`, producing `20`. There is no special handling for equal values because the exchange argument only requires that a strictly longer examination must not precede a shorter one.

For an input where the shortest animal appears last,

```
3
7 1 2
```

sorting changes the order to `1, 2, 7`. The prefixes are `0, 1, 3`, so the answer is `4`. The original order would produce `15`, demonstrating why preserving input order is not valid.

For maximum examination times,

```
4
100000 100000 100000 100000
```

the prefixes are `0, 100000, 200000, 300000`, giving `600000`. The values themselves fit comfortably in ordinary integer ranges, but the accumulated answer grows much faster.

For the maximum number of animals with maximum examination time, every animal except the first waits for an increasing multiple of `100000`. The resulting sum is

`100000 * (0 + 1 + 2 + ... + 999999) = 49999950000000000`.

The implementation computes this directly using the prefix-sum invariant, with no simulation of individual units of time and no quadratic behavior.
