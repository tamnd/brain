---
title: "CF 105023B - Truck Traffic"
description: "We are given a one-dimensional representation of what Bob sees along a freeway, encoded as a string of length $N$. Each position is either a truck segment marked as T or an empty road segment marked as .."
date: "2026-06-28T01:43:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105023
codeforces_index: "B"
codeforces_contest_name: "HPI 2024 Novice"
rating: 0
weight: 105023
solve_time_s: 78
verified: false
draft: false
---

[CF 105023B - Truck Traffic](https://codeforces.com/problemset/problem/105023/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional representation of what Bob sees along a freeway, encoded as a string of length $N$. Each position is either a truck segment marked as `T` or an empty road segment marked as `.`. We can think of this as a binary array where some positions contribute visibility and others do not.

Bob is considering adding an additional contiguous truck segment of length $l_i$ onto this same line. The key freedom is that this new segment can be placed starting at any valid position, as long as it fits within the length $N$. Once placed, overlapping positions with existing trucks naturally remain trucks, so the total visible truck count becomes the number of positions that are `T` either originally or covered by the new segment.

For each query length $l_i$, we must choose an optimal placement of this added segment to maximize the total number of `T` positions after insertion.

The constraints are small: $N, Q \le 100$. This immediately tells us that any solution up to roughly $O(N^3)$ would still pass comfortably, since the total operations are bounded around $10^6$.

A naive mistake would be to assume the best placement is always centered or always aligned to existing trucks. For example, given `T..T` and a long segment, placing greedily near existing clusters might miss that covering multiple small gaps yields a better total.

Another subtle failure case is misunderstanding overlap: if we add a segment over existing `T`, we do not double count, so any approach that simply adds counts without masking overlap will overestimate.

A small illustrative edge case:

Input:

```
5 1
T.T.T
3
```

Placing the segment over positions 2-4 covers two dots but also overlaps a truck at position 3. The correct answer is not “existing 3 trucks + 3 added”, but the size of the union.

## Approaches

The brute-force approach is straightforward. For each query length $l$, we try every possible starting position of the added truck segment. For each placement, we recompute the total number of `T` positions in the union of the original string and the placed segment. This requires scanning the entire string for each placement, leading to $O(N)$ work per placement and $O(N)$ placements, giving $O(N^2)$ per query and $O(N^3)$ overall across all queries.

Since $N \le 100$, this already works, but it is unnecessarily repetitive. The key observation is that when we place a segment of length $l$ starting at position $i$, the only region affected is that window. Everything outside it remains fixed, and inside it we are effectively replacing some `.` with `T`.

So instead of recomputing from scratch, we can precompute prefix sums of existing trucks and then evaluate each placement in $O(1)$. The gain is that each window score becomes computable in constant time, reducing each query to $O(N)$.

We compute, for a chosen segment $[i, i+l-1]$, the contribution as:

existing trucks outside window + full window length (since all positions inside become `T` after insertion, but overlapping trucks are already counted, so we correct via prefix sums).

This reduces each query to scanning all valid positions and evaluating a simple formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(QN^3)$ | $O(1)$ | Too slow in general form |
| Prefix Sum Window | $O(QN)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Convert the string into a binary array where `T = 1` and `.` = 0. This allows arithmetic counting of trucks.
2. Build a prefix sum array so we can query the number of existing trucks in any interval in constant time.
3. For each query length $l$, iterate over all possible starting positions $i$ from $0$ to $N-l$.
4. For each position $i$, compute how many original trucks lie inside the window $[i, i+l-1]$.
5. Compute the resulting total truck count if we place the new segment there as:

existing total trucks + (window length - trucks inside window).

This formula reflects that every empty cell in the window becomes a truck, while existing trucks are already counted.
6. Track the maximum value across all placements and output it for the query.

The subtle point is step 5. We are not recomputing the whole string; we are only measuring how many zeros get converted into ones in that window.

### Why it works

The algorithm implicitly maintains the invariant that every position outside the chosen window contributes exactly its original value, while inside the window every position becomes a truck regardless of its initial state. Therefore, the final count is the original total plus exactly the number of empty cells inside the chosen window. Since every placement is evaluated exactly once, and all transformations are correctly accounted for without double counting, the maximum over all windows is the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, Q = map(int, input().split())
    s = input().strip()

    a = [1 if c == 'T' else 0 for c in s]

    pref = [0] * (N + 1)
    for i in range(N):
        pref[i + 1] = pref[i] + a[i]

    total = pref[N]

    def range_sum(l, r):
        return pref[r] - pref[l]

    for _ in range(Q):
        L = int(input())
        best = 0

        for i in range(N - L + 1):
            j = i + L
            inside = range_sum(i, j)
            candidate = total + (L - inside)
            if candidate > best:
                best = candidate

        print(best)

if __name__ == "__main__":
    solve()
```

The solution first compresses the input into a binary representation, which simplifies reasoning about overlaps. The prefix sum array allows us to compute how many trucks already exist inside any candidate placement window in constant time.

For each query, we evaluate every possible placement of the new truck segment. The expression `total + (L - inside)` captures the net gain: every empty cell becomes a truck, while existing trucks in the window do not increase the total because they are already counted once.

The nested loop structure is safe because both $N$ and $Q$ are small.

## Worked Examples

### Example 1

Input:

```
N = 5, s = T.T.T
L = 3
```

Prefix sum:

| i | s[i] | pref |
| --- | --- | --- |
| 0 | T | 1 |
| 1 | . | 1 |
| 2 | T | 2 |
| 3 | . | 2 |
| 4 | T | 3 |

Now we evaluate windows:

| start i | window | inside trucks | candidate |
| --- | --- | --- | --- |
| 0 | T.T | 2 | 3 + (3 - 2) = 4 |
| 1 | .T. | 1 | 3 + (3 - 1) = 5 |
| 2 | T.T | 2 | 4 |

Best is 5.

This shows that the optimal placement is not necessarily aligned with existing trucks; covering two empty positions yields the best improvement.

### Example 2

Input:

```
N = 6, s = TT..T.
L = 2
```

Total trucks = 3.

| start i | window | inside | candidate |
| --- | --- | --- | --- |
| 0 | TT | 2 | 3 + 0 = 3 |
| 1 | T. | 1 | 3 + 1 = 4 |
| 2 | .. | 0 | 3 + 2 = 5 |
| 3 | .T | 1 | 3 + 1 = 4 |
| 4 | T. | 1 | 4 |

Best is 5.

This confirms that the best strategy is to maximize the number of empty cells covered by the added segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(QN)$ | Each query scans all $N$ placements, each computed in O(1) using prefix sums |
| Space | $O(N)$ | Prefix sum array over the string |

Given $N, Q \le 100$, the total operations are at most $10^4$, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, Q = map(int, input().split())
    s = input().strip()

    a = [1 if c == 'T' else 0 for c in s]
    pref = [0] * (N + 1)
    for i in range(N):
        pref[i + 1] = pref[i] + a[i]
    total = pref[N]

    out = []
    for _ in range(Q):
        L = int(input())
        best = 0
        for i in range(N - L + 1):
            inside = pref[i + L] - pref[i]
            best = max(best, total + (L - inside))
        out.append(str(best))

    return "\n".join(out) + "\n"

# provided sample
assert run("8 3\nTT..T.T.\n1\n3\n8\n") == "5\n6\n8\n"

# minimum case
assert run("1 1\n.\n1\n") == "1\n"

# all trucks
assert run("5 1\nTTTTT\n2\n") == "5\n"

# all empty
assert run("5 1\n.....\n3\n") == "3\n"

# alternating
assert run("6 1\nT.T.T.\n2\n") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all empty | L | full gain from placement |
| all trucks | N | no improvement possible |
| alternating | 4 | overlap handling correctness |
| minimum size | 1 | boundary correctness |

## Edge Cases

A fully empty string is the most sensitive case for off-by-one mistakes. For example, `.....` with $L=3$ should return 3, since any placement fully converts the chosen segment. The algorithm handles this because `inside = 0` for every window, so the gain is always exactly $L$.

A fully filled string is the opposite extreme. For `TTTTT`, any placement yields no improvement, since `L - inside = 0` everywhere. The algorithm correctly keeps the answer at $N$ because prefix sums always match window length.

A mixed alternating pattern like `T.T.T.` ensures that partial overlaps are handled correctly. The prefix sum subtraction isolates exactly how many trucks are already present inside each window, preventing double counting and making the computed gain precise.
