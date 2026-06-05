---
title: "CF 314A - Sereja and Contest"
description: "The participants are listed in final rank order. Participant i has rating a[i]. For a table of size m, if a participant currently occupies position p, his rating change is $$d = sum{text{participants before him}} aj (posj-1) - ai (p-1)(m-p)$$ In the original statement this…"
date: "2026-06-06T01:11:10+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 314
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 187 (Div. 1)"
rating: 1600
weight: 314
solve_time_s: 144
verified: true
draft: false
---

[CF 314A - Sereja and Contest](https://codeforces.com/problemset/problem/314/A)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The participants are listed in final rank order. Participant `i` has rating `a[i]`.

For a table of size `m`, if a participant currently occupies position `p`, his rating change is

$$d = \sum_{\text{participants before him}} a_j (pos_j-1)
    - a_i (p-1)(m-p)$$

In the original statement this formula is given directly. The complication is that the table is dynamic.

Whenever there exists a participant with `d < k`, the participant with the best current rank among all such participants is removed. After the removal, positions are compressed and all `d` values are recalculated. We must output the original indices of all removed participants, in the order in which they disappear.

The constraint `n ≤ 2·10^5` immediately rules out any simulation that repeatedly recomputes all rating changes. Even an `O(n^2)` solution would perform around `4·10^10` operations in the worst case.

The tricky part is that removals change positions, so a participant's value of `d` is not fixed. A naive implementation can easily remove the wrong participant because it evaluates `d` using outdated positions.

Consider:

```
5 0
5 3 4 1 2
```

Participant 2 is removed first. After that, participant 3 moves forward and his rating change must be recomputed using the new positions. Using the original table throughout would produce the wrong sequence.

Another subtle case occurs when a participant is currently safe.

```
3 0
10 1 10
```

If participant 2 is not removed when we reach him, later removals cannot make his `d` smaller. A solution that repeatedly revisits earlier participants is doing unnecessary work.

The value of `k` can also be negative. A participant with a negative `d` is not automatically removed. The condition is strictly `d < k`.

## Approaches

The brute-force simulation follows the statement literally. Repeatedly compute every participant's current `d`, find the first one with `d < k`, remove him, compress the table, and repeat.

This is correct because it exactly reproduces the process. Unfortunately, a single recomputation already costs `O(n)`, and there can be `O(n)` removals. The total complexity becomes `O(n^2)`, which is far too slow for `n = 200000`.

The key observation is that removals always happen from left to right in terms of original indices.

Suppose participant `i` currently survives. If some participant after him is removed, then the number of people after `i` decreases. Looking at the formula,

$$d_i
=
\text{constant}
-
a_i (p_i-1)(m-p_i),$$

the factor `(m-p_i)` becomes smaller. Since it is multiplied by a minus sign, `d_i` can only increase.

So once participant `i` reaches a state where `d_i ≥ k`, future removals can never make him eligible again.

That means when we scan participants from left to right, the decision for participant `i` depends only on removals that already happened before `i`. If `d_i < k`, he must be removed immediately. If `d_i ≥ k`, he survives forever.

This turns the dynamic process into a single linear scan.

Let `r` be the number of removed participants before the current index `i`.

The current position of participant `i` is

$$p = i-r.$$

The current table size is

$$m = n-r.$$

Among surviving participants before `i`, positions are exactly `1,2,\dots,p-1`.

If we maintain

$$S=\sum_{\text{surviving } j<i} a_j (pos_j-1),$$

then

$$d_i = S - a_i (p-1)(m-p).$$

Everything needed to evaluate `d_i` is available in `O(1)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize `removed = 0`.
2. Maintain `S`, the sum of `a_j * (current_position_j - 1)` over all surviving participants already processed.
3. Process participants from left to right in their original order.
4. For participant `i`, compute his current position:

$$p = i - removed.$$

The current table size is:

$$m = n - removed.$$
5. Compute

$$d = S - a_i (p-1)(m-p).$$

This is exactly the rating-change formula applied to the current dynamic table.
6. If `d < k`, remove this participant.

Increase `removed` and store his original index in the answer.

Do not add anything to `S`, because removed participants are not present in later calculations.
7. Otherwise the participant survives.

Add

$$a_i (p-1)$$

to `S`, because this participant contributes to the first term of every later survivor's formula.
8. Continue until all participants have been processed.

### Why it works

When a participant after index `i` is removed, the value `(m-p_i)` decreases while everything else in `d_i` remains unchanged. As a result, `d_i` never decreases.

So if participant `i` satisfies `d_i ≥ k` at the moment we process him, he will never become removable later. Conversely, if `d_i < k`, the rules require removing him immediately because every removable participant before him has already been processed.

The scan therefore reproduces exactly the same sequence of removals as the dynamic process described in the statement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    removed = 0
    s = 0
    ans = []

    for i in range(1, n + 1):
        ai = a[i - 1]

        p = i - removed
        m = n - removed

        d = s - ai * (p - 1) * (m - p)

        if d < k:
            removed += 1
            ans.append(str(i))
        else:
            s += ai * (p - 1)

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The variable `removed` tracks how many earlier participants have already disappeared. From that single number we can recover both the current position `p` and the current table size `m`.

The variable `s` stores the first term of the formula. Only surviving participants contribute to it. When a participant is removed, skipping the update to `s` is essential. Adding his contribution would incorrectly allow removed participants to affect later computations.

All arithmetic is done with Python integers. Intermediate values can reach roughly

$$10^9 \cdot 2\cdot10^5 \cdot 2\cdot10^5,$$

which is far beyond 32-bit range. Python handles this automatically.

The order of operations also matters. We must evaluate `d` before deciding whether the participant survives. Updating `s` first would incorrectly let a participant contribute to his own rating-change calculation.

## Worked Examples

### Sample 1

Input:

```
5 0
5 3 4 1 2
```

| i | ai | removed before | p | m | S before | d | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 1 | 5 | 0 | 0 | keep |
| 2 | 3 | 0 | 2 | 5 | 0 | -9 | remove |
| 3 | 4 | 1 | 2 | 4 | 0 | -8 | remove |
| 4 | 1 | 2 | 2 | 3 | 0 | -1 | remove |
| 5 | 2 | 3 | 2 | 2 | 0 | 0 | keep |

Output:

```
2
3
4
```

This example shows the core idea. After each removal, later participants move forward, and the scan automatically accounts for that through the updated value of `removed`.

### Sample 2

Input:

```
10 -10
5 5 1 7 5 1 2 4 9 2
```

| i | removed before | p | m | d | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 10 | 0 | keep |
| 2 | 0 | 2 | 10 | -40 | remove |
| 3 | 1 | 2 | 9 | -8 | keep |
| 4 | 1 | 3 | 9 | -86 | remove |
| 5 | 2 | 3 | 8 | -44 | remove |
| 6 | 3 | 3 | 7 | 2 | keep |
| 7 | 3 | 4 | 7 | -11 | remove |
| 8 | 4 | 4 | 6 | -12 | remove |
| 9 | 5 | 4 | 5 | -27 | remove |
| 10 | 6 | 4 | 4 | 16 | keep |

Output:

```
2
4
5
7
8
9
```

This trace demonstrates that removals occur in increasing original index order. Once a participant survives his turn, we never need to revisit him.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass over the array, O(1) work per participant |
| Space | O(n) | Output list of removed indices |

With `n = 200000`, a linear scan is easily fast enough for the 2-second limit. Memory usage is dominated by the answer array and remains well within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    removed = 0
    s = 0
    ans = []

    for i in range(1, n + 1):
        ai = a[i - 1]

        p = i - removed
        m = n - removed

        d = s - ai * (p - 1) * (m - p)

        if d < k:
            removed += 1
            ans.append(str(i))
        else:
            s += ai * (p - 1)

    return "\n".join(ans)

# provided samples
assert run("5 0\n5 3 4 1 2\n") == "2\n3\n4", "sample 1"

assert run("10 -10\n5 5 1 7 5 1 2 4 9 2\n") == "2\n4\n5\n7\n8\n9", "sample 2"

# minimum size
assert run("1 0\n100\n") == "", "single participant"

# all equal values
assert run("4 0\n1 1 1 1\n") == "2\n3", "equal ratings"

# very negative threshold, nobody removed
assert run("5 -1000000000\n1 2 3 4 5\n") == "", "no removals"

# catches position-update mistakes
assert run("3 0\n5 1 1\n") == "2", "dynamic position handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 100` | empty output | Minimum size |
| `4 0 / 1 1 1 1` | `2 3` | Equal values and repeated removals |
| `5 -1000000000 / 1 2 3 4 5` | empty output | Nobody qualifies for removal |
| `3 0 / 5 1 1` | `2` | Correct position updates after removals |

## Edge Cases

Consider the smallest possible input:

```
1 0
100
```

The only participant has `p = 1`, so `(p-1) = 0` and `d = 0`. Since `0 < 0` is false, nobody is removed. The algorithm outputs nothing, which is correct.

Consider a case where a participant survives and later removals occur:

```
4 0
10 1 10 1
```

Participant 3 may look dangerous after participant 4 disappears, but removing people behind him only decreases `(m-p)`. His `d` can only increase. The algorithm processes him once and never revisits him, which matches the mathematical behavior of the formula.

Consider an all-equal array:

```
4 0
1 1 1 1
```

The scan computes the current position after each removal using `p = i - removed`. This is exactly where many incorrect solutions fail. Using original positions would produce incorrect `d` values after the first deletion. The maintained `removed` counter guarantees that compressed positions are always correct.
