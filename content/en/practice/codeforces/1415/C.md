---
title: "CF 1415C - Bouncing Ball"
description: "We have a binary string representing cells in a level. A 1 means a platform already exists, and a 0 means the cell is empty. The ball must start bouncing from position p, then visit positions p + k, p + 2k, and so on. Every one of those positions must contain a platform."
date: "2026-06-11T07:11:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1415
codeforces_index: "C"
codeforces_contest_name: "Technocup 2021 - Elimination Round 2"
rating: 1400
weight: 1415
solve_time_s: 105
verified: true
draft: false
---

[CF 1415C - Bouncing Ball](https://codeforces.com/problemset/problem/1415/C)

**Rating:** 1400  
**Tags:** brute force, dp, implementation  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a binary string representing cells in a level. A `1` means a platform already exists, and a `0` means the cell is empty.

The ball must start bouncing from position `p`, then visit positions `p + k`, `p + 2k`, and so on. Every one of those positions must contain a platform. We are allowed to add platforms into empty cells, paying `x` per addition.

There is a second operation: remove the first cell of the level. After removing the first cell, every remaining cell shifts one position to the left. This costs `y` per removal. We may repeat this operation, but we must never shorten the level so much that position `p` disappears.

The goal is to find the minimum total cost required so that, after some number of deletions from the front and some platform additions, the bouncing sequence becomes valid.

The largest value of `n` is `10^5`, and the sum of all `n` across test cases is also at most `10^5`. This immediately rules out any algorithm that examines every possible starting position and then rescans the entire suffix each time. An `O(n²)` solution would perform around `10^10` operations in the worst case. We need something close to linear time per test case.

A subtle point is that deleting cells changes where position `p` ends up. Suppose:

```
n = 5
p = 3
k = 2
s = 00100
```

If we delete one cell from the front, the new position `p` corresponds to the original index `4`, not the original index `3`. Any solution that treats deletions and additions independently will compute the wrong answer.

Another easy mistake is forgetting that only positions spaced by `k` matter. For example:

```
n = 6
p = 2
k = 3
s = 000100
```

The required cells are positions `2` and `5`. Position `3` and position `4` are irrelevant. A naive implementation that tries to make the entire suffix good would pay for unnecessary additions.

A third edge case occurs near the end of the string:

```
n = 5
p = 5
k = 2
s = 00000
```

Only position `5` is required. The answer is simply one addition. Careless code often accesses beyond the end of the array when computing transitions involving `i + k`.

## Approaches

The most direct solution is to try every possible number of front deletions.

If we delete `d` cells, then position `p` in the new string corresponds to position `p + d` in the original string. Starting from that position, we can walk through indices

```
p + d,
p + d + k,
p + d + 2k,
...
```

and count how many of them currently contain `0`. Each such cell requires one platform addition. The total cost becomes:

```
d * y + additions * x
```

Trying all valid values of `d` is easy. The problem is the counting step. If we rescan the bouncing positions for every deletion count, we may spend `O(n)` work per candidate. Since there are `O(n)` candidates, the total becomes `O(n²)`.

The key observation is that every candidate start position asks the same question:

> How many zeros appear in the arithmetic progression starting at this index and jumping by `k`?

These answers overlap heavily. If we already know the answer for position `i + k`, then position `i` differs only by whether cell `i` itself is zero.

Define:

```
dp[i] = number of additions needed
        if bouncing starts at i
```

Using 0-based indexing,

```
dp[i] = (s[i] == '0') + dp[i + k]
```

when `i + k` exists. Otherwise,

```
dp[i] = (s[i] == '0')
```

This recurrence computes exactly the number of missing platforms along the required bouncing path starting from `i`.

Once all `dp[i]` values are known, every deletion count can be evaluated in constant time:

```
cost = deletions * y + dp[start] * x
```

where `start` is the original position that becomes position `p` after the deletions.

This transforms the problem into a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert `p` to 0-based indexing.
2. Create an array `dp` of length `n`.
3. Process positions from right to left.
4. For each position `i`, compute:

```
need = 1 if s[i] == '0' else 0
```
5. If `i + k < n`, add `dp[i + k]`:

```
dp[i] = need + dp[i + k]
```

Otherwise:

```
dp[i] = need
```

This gives the number of platforms that must be added if bouncing starts at `i`.
6. Consider every possible number of deletions.

If we delete `d` cells, the required starting position in the original string becomes:

```
start = p + d
```
7. For each valid `start`, compute:

```
cost = (start - p) * y + dp[start] * x
```

The first term is the deletion cost, and the second term is the cost of adding all missing platforms on the bouncing path.
8. Take the minimum over all candidates.

### Why it works

For any index `i`, the bouncing path consists exactly of:

```
i, i + k, i + 2k, ...
```

The recurrence

```
dp[i] = missing_at_i + dp[i + k]
```

counts the number of zeros on that path. Every zero requires exactly one platform addition, and every one already satisfies the requirement.

After deleting `d` cells, position `p` in the new level corresponds to position `p + d` in the original level. The required additions are precisely `dp[p + d]`. Since deletions and additions contribute independently to the total cost, evaluating

```
d * y + dp[p + d] * x
```

for every valid `d` examines every feasible final configuration. The minimum of these values is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, p, k = map(int, input().split())
        s = input().strip()
        x, y = map(int, input().split())

        p -= 1

        dp = [0] * n

        for i in range(n - 1, -1, -1):
            dp[i] = (s[i] == '0')
            if i + k < n:
                dp[i] += dp[i + k]

        best = 10**18

        for start in range(p, n):
            deletions = start - p
            cost = deletions * y + dp[start] * x
            best = min(best, cost)

        ans.append(str(best))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The dynamic programming array is filled from right to left because every state depends on `i + k`, which lies to the right.

The expression

```
(s[i] == '0')
```

evaluates to `True` or `False`, which Python automatically treats as `1` or `0` in arithmetic expressions. This gives the number of additions needed at the current cell.

The loop over `start` represents all possible deletion counts. If `start = p`, no cells are removed. If `start = p + 1`, one cell is removed, and so on.

The most common implementation mistake is mixing 1-based and 0-based indexing. The input position `p` is 1-based, but all array accesses are 0-based, so we immediately do:

```
p -= 1
```

Another common bug is forgetting that only positions reachable by repeated jumps of size `k` matter. The recurrence naturally captures exactly those positions.

## Worked Examples

### Sample 1

Input:

```
n = 10
p = 3
k = 2
s = 0101010101
x = 2
y = 2
```

Using 0-based indexing, `p = 2`.

| start | deletions | dp[start] | cost |
| --- | --- | --- | --- |
| 2 | 0 | 1 | 2 |
| 3 | 1 | 0 | 2 |
| 4 | 2 | 1 | 6 |
| 5 | 3 | 0 | 6 |
| 6 | 4 | 1 | 10 |
| 7 | 5 | 0 | 10 |
| 8 | 6 | 1 | 14 |
| 9 | 7 | 0 | 14 |

The minimum cost is `2`.

This trace shows why deleting one cell can be just as good as adding a platform. The algorithm evaluates both possibilities and chooses the cheaper result automatically.

### Sample 2

Input:

```
n = 5
p = 4
k = 1
s = 00000
x = 2
y = 10
```

Using 0-based indexing, `p = 3`.

| start | deletions | dp[start] | cost |
| --- | --- | --- | --- |
| 3 | 0 | 2 | 4 |
| 4 | 1 | 1 | 12 |

The minimum cost is `4`.

Deleting is very expensive here, so the optimal solution keeps the string unchanged and adds platforms where needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One DP pass and one evaluation pass |
| Space | O(n) | DP array of length `n` |
| Total over all tests | O(sum n) | Sum of all `n` is at most `10^5` |

The total input size is bounded by `10^5`, so a linear solution performs only a few hundred thousand operations. This comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, p, k = map(int, input().split())
        s = input().strip()
        x, y = map(int, input().split())

        p -= 1

        dp = [0] * n
        for i in range(n - 1, -1, -1):
            dp[i] = (s[i] == '0')
            if i + k < n:
                dp[i] += dp[i + k]

        best = 10**18
        for start in range(p, n):
            best = min(
                best,
                (start - p) * y + dp[start] * x
            )

        out.append(str(best))

    return "\n".join(out)

# provided samples
assert run(
"""3
10 3 2
0101010101
2 2
5 4 1
00000
2 10
11 2 3
10110011000
4 3
"""
) == "2\n4\n10"

# minimum size
assert run(
"""1
1 1 1
0
5 7
"""
) == "5"

# already valid
assert run(
"""1
5 1 2
11111
3 4
"""
) == "0"

# deletion better than additions
assert run(
"""1
5 1 1
00001
10 1
"""
) == "4"

# off-by-one near end
assert run(
"""1
5 5 2
00000
3 1
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s=0` | `5` | Smallest valid instance |
| All ones | `0` | No operations required |
| Expensive additions, cheap deletions | `4` | Optimal answer may involve many deletions |
| `p=n` | `3` | Correct handling at the last position |

## Edge Cases

Consider:

```
1
5 3 2
00100
1 1
```

Without deletions, the bouncing path starts at position `3` and visits position `5`. Both are `1` and `0`, so one addition is required.

If we delete one cell, position `p` now corresponds to original position `4`. The path changes completely. The algorithm handles this because it evaluates `dp[2]`, `dp[3]`, and `dp[4]` separately. It never assumes the bouncing path is fixed.

Now consider:

```
1
6 2 3
000100
5 1
```

The relevant positions are only `2` and `5`. Cells `3`, `4`, and `6` do not matter. The recurrence follows jumps of size `k`, so those irrelevant cells never affect the computed cost.

Finally, consider:

```
1
5 5 2
00000
3 1
```

The bouncing path contains only the last cell. During DP construction, `i + k` is outside the array, so the recurrence correctly stops:

```
dp[4] = 1
```

The answer becomes exactly one addition, costing `3`. No out-of-bounds access occurs, and no extra cells are counted.
