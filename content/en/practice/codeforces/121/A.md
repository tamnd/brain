---
title: "CF 121A - Lucky Sum"
description: "We need to evaluate a sum over an interval [l, r]. For every integer x in that range, we compute next(x), where next(x) means the smallest lucky number greater than or equal to x. A lucky number is a positive integer whose decimal digits are only 4 and 7."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 121
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 91 (Div. 1 Only)"
rating: 1100
weight: 121
solve_time_s: 96
verified: true
draft: false
---

[CF 121A - Lucky Sum](https://codeforces.com/problemset/problem/121/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to evaluate a sum over an interval `[l, r]`. For every integer `x` in that range, we compute `next(x)`, where `next(x)` means the smallest lucky number greater than or equal to `x`.

A lucky number is a positive integer whose decimal digits are only `4` and `7`. Examples are `4`, `7`, `44`, `47`, `74`, `77`, and so on.

The task is not to count lucky numbers. We must sum the value of the next lucky number for every integer in the interval.

For example, if `l = 2` and `r = 7`:

- `next(2) = 4`
- `next(3) = 4`
- `next(4) = 4`
- `next(5) = 7`
- `next(6) = 7`
- `next(7) = 7`

The answer is `4 + 4 + 4 + 7 + 7 + 7 = 33`.

The constraints are small in an unusual way. The interval itself can be huge because `r` may reach `10^9`, so iterating through every value from `l` to `r` is impossible in the worst case. A loop over one billion numbers would take far too long for a 2 second time limit.

At the same time, the number of lucky numbers up to `10^9` is tiny. A lucky number has at most 10 digits here, and each digit has only 2 choices, `4` or `7`. That means the total count is:

`2^1 + 2^2 + ... + 2^10 = 2046`

Working with a few thousand values is trivial. The entire problem is designed around exploiting this gap.

Several edge cases can silently break a careless implementation.

Consider:

```
4 4
```

The answer is `4`, because `next(4) = 4`. A buggy implementation that searches for the first lucky number strictly larger than `x` would incorrectly use `7`.

Another tricky case is when the interval crosses multiple lucky-number ranges:

```
5 8
```

The correct contributions are:

- `5,6,7 -> 7`
- `8 -> 44`

So the answer is:

```
7 + 7 + 7 + 44 = 65
```

A naive grouping implementation can easily forget to process the tail after the last lucky number inside the interval.

Large boundaries also matter:

```
999999999 1000000000
```

The next lucky number for both values is `4444444444`, which exceeds `10^9`. If we generate lucky numbers only up to `10^9`, we miss the correct answer entirely.

## Approaches

The brute-force idea is straightforward. For every integer `x` from `l` to `r`, generate or search for the smallest lucky number greater than or equal to `x`, then add it to the answer.

This works logically because the definition of the sum is direct. The problem is performance. In the worst case, the interval length is close to `10^9`. Even an `O(1)` operation per value would already be far too slow.

The structure of lucky numbers gives us a better path. The value of `next(x)` stays constant over entire ranges.

For example:

| x range | next(x) |
| --- | --- |
| 1..4 | 4 |
| 5..7 | 7 |
| 8..44 | 44 |
| 45..47 | 47 |

Instead of processing every integer individually, we can process these ranges in blocks.

The key observation is that once we know the sorted list of lucky numbers, every interval between two consecutive lucky numbers contributes the same value repeatedly.

Suppose the current lucky number is `44`, and the previous lucky number was `7`. Then every number from `8` through `44` contributes `44`.

That means we only need to:

1. Generate all lucky numbers.
2. Sort them.
3. Walk through the lucky numbers and compute how much of `[l, r]` falls into each segment.

Since there are only about two thousand lucky numbers, this solution is extremely fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r - l + 1) | O(1) | Too slow |
| Optimal | O(2^10) | O(2^10) | Accepted |

## Algorithm Walkthrough

1. Generate every lucky number with up to 10 digits using recursion.

At each step, append either `4` or `7` to the current number. This explores the full binary tree of lucky-number constructions.
2. Store all generated lucky numbers in a list.

We include values larger than `10^9` because `next(x)` for numbers near the upper limit may exceed `10^9`.
3. Sort the lucky numbers.

Recursive generation does not naturally guarantee sorted order.
4. Initialize:

- `ans = 0`
- `cur = l`

The variable `cur` tracks the first value in the interval that has not yet been processed.
5. Iterate through the lucky numbers in increasing order.

For each lucky number `v`:

- If `v < cur`, skip it because its segment is already behind us.
- Otherwise, the interval from `cur` up to `min(r, v)` all has `next(x) = v`.
6. Compute how many numbers belong to this segment.

The count is:

$\text{count}=\min(r,v)-cur+1$
7. Add this segment’s contribution.

$\text{contribution}=v \times \text{count}$
8. Move `cur` to the first unprocessed value after this segment.

Set:

```
cur = v + 1
```
9. Stop once `cur > r`.

Every value in the interval has now been accounted for.

### Why it works

The algorithm relies on a partition of the number line by lucky numbers.

For a lucky number `v`, every integer strictly larger than the previous lucky number and at most `v` has `next(x) = v`.

These segments are disjoint and together cover the entire interval `[l, r]`.

During iteration, `cur` always points to the first unprocessed integer. When we process a lucky number `v`, we add exactly the contribution of all integers whose next lucky number equals `v`. After advancing `cur` to `v + 1`, no processed value is revisited.

Because every integer in `[l, r]` belongs to exactly one such segment, the final sum is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

l, r = map(int, input().split())

lucky = []

def gen(x):
    if x > 10**10:
        return

    if x > 0:
        lucky.append(x)

    gen(x * 10 + 4)
    gen(x * 10 + 7)

gen(0)

lucky.sort()

ans = 0
cur = l

for v in lucky:
    if cur > r:
        break

    if v < cur:
        continue

    right = min(r, v)
    cnt = right - cur + 1

    ans += v * cnt
    cur = right + 1

print(ans)
```

The recursive generator builds every lucky number by repeatedly appending `4` and `7`.

Starting from `0` is convenient because:

- `0` itself is not stored.
- Its children become `4` and `7`.

The recursion depth is tiny, at most 10 levels, so recursion is perfectly safe here.

The stopping condition uses `10^10` instead of `10^9`. This is subtle but necessary. If `x = 10^9`, its next lucky number is actually `4444444444`, not some value below `10^9`.

After sorting, the main loop processes lucky numbers in ascending order. For each lucky number `v`, the interval `[cur, min(r, v)]` contributes `v`.

The line:

```
cnt = right - cur + 1
```

is easy to get wrong. The interval is inclusive on both ends, so we need the `+1`.

Another subtle point is:

```
cur = right + 1
```

not `v + 1`.

Suppose `r < v`. Then only part of the segment is used. Advancing directly to `v + 1` still works logically, but using `right + 1` matches the actual processed boundary and avoids mistakes if the code is modified later.

Python integers automatically handle large values, which matters because the answer may exceed 32-bit integer range.

## Worked Examples

### Example 1

Input:

```
2 7
```

Generated lucky numbers begin with:

```
4, 7, 44, 47, ...
```

| cur | lucky number v | processed range | count | added value | ans |
| --- | --- | --- | --- | --- | --- |
| 2 | 4 | 2..4 | 3 | 12 | 12 |
| 5 | 7 | 5..7 | 3 | 21 | 33 |

Final answer:

```
33
```

This trace shows how the algorithm groups many integers into one contribution instead of handling them individually.

### Example 2

Input:

```
7 7
```

| cur | lucky number v | processed range | count | added value | ans |
| --- | --- | --- | --- | --- | --- |
| 7 | 7 | 7..7 | 1 | 7 | 7 |

Final answer:

```
7
```

This case confirms that when the interval endpoint itself is lucky, we correctly use that value rather than the next larger lucky number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^10) | About 2046 lucky numbers are generated and processed |
| Space | O(2^10) | Storage for all lucky numbers |

The actual runtime is tiny. Even with recursion, sorting, and iteration, the total work is only a few thousand operations. This comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    l, r = map(int, input().split())

    lucky = []

    def gen(x):
        if x > 10**10:
            return

        if x > 0:
            lucky.append(x)

        gen(x * 10 + 4)
        gen(x * 10 + 7)

    gen(0)

    lucky.sort()

    ans = 0
    cur = l

    for v in lucky:
        if cur > r:
            break

        if v < cur:
            continue

        right = min(r, v)
        cnt = right - cur + 1

        ans += v * cnt
        cur = right + 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("2 7\n") == "33", "sample 1"
assert run("7 7\n") == "7", "sample 2"

# minimum-size interval
assert run("1 1\n") == "4", "minimum case"

# single lucky number
assert run("4 4\n") == "4", "exact lucky number"

# crossing into next lucky segment
assert run("5 8\n") == "65", "crossing segments"

# large boundary case
assert run("999999999 1000000000\n") == "8888888888", "needs lucky number above 1e9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `4` | Smallest possible interval |
| `4 4` | `4` | Exact lucky-number boundary |
| `5 8` | `65` | Transition between lucky segments |
| `999999999 1000000000` | `8888888888` | Correct handling of lucky numbers above `10^9` |

## Edge Cases

Consider the input:

```
4 4
```

The algorithm starts with `cur = 4`.

When it reaches lucky number `4`, it processes the range:

```
[4, min(4, 4)] = [4, 4]
```

The contribution is:

```
4 * 1 = 4
```

Then `cur` becomes `5`, which ends the loop. The output is correct because `next(4)` is `4`, not `7`.

Now consider:

```
5 8
```

The relevant lucky numbers are `7` and `44`.

The algorithm processes:

- `5..7` using value `7`
- `8..8` using value `44`

So the answer becomes:

```
7 + 7 + 7 + 44 = 65
```

This confirms that the transition between lucky-number ranges is handled correctly.

Finally, examine:

```
999999999 1000000000
```

The next lucky number after both values is `4444444444`.

When the iteration reaches that lucky number, the processed range is:

```
999999999..1000000000
```

with count `2`.

The contribution becomes:

```
2 * 4444444444 = 8888888888
```

This demonstrates why generating lucky numbers beyond `10^9` is necessary.
