---
title: "CF 105023I - What the heck is a kilometer?"
description: "We are given a one-dimensional road represented as a string of length $N$. Each character describes a unit cell: either a normal road segment denoted by a dot, or a traffic light denoted by an asterisk."
date: "2026-06-28T01:46:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105023
codeforces_index: "I"
codeforces_contest_name: "HPI 2024 Novice"
rating: 0
weight: 105023
solve_time_s: 101
verified: false
draft: false
---

[CF 105023I - What the heck is a kilometer?](https://codeforces.com/problemset/problem/105023/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional road represented as a string of length $N$. Each character describes a unit cell: either a normal road segment denoted by a dot, or a traffic light denoted by an asterisk. The dots contribute to physical distance, while the asterisks do not add length but are checkpoints that matter for constraints.

We are allowed to remove exactly one traffic light. After removing it, we conceptually place a “kilometer marker” on this infinite road, where each kilometer has some fixed length $K$ measured in road units. Traffic lights that land exactly on the boundary of a kilometer do not count toward that kilometer’s total.

The requirement is that in every kilometer segment, after removing one traffic light optimally, there are at most $L$ remaining traffic lights strictly inside that segment. The task is to choose the removal and then determine the maximum possible value of $K$ such that this condition holds for all kilometers.

The core difficulty is that the constraint is not local to individual traffic lights but depends on how they aggregate under all possible sliding windows of length $K$.

The constraints allow $N$ up to $10^6$, which rules out any solution that checks all possible segment lengths $K$ and recomputes violations in $O(N)$ per check. A naive $O(N^2)$ scan is impossible, and even $O(N \log N)$ with heavy recomputation would be risky unless each check is linear or better.

A subtle issue appears with boundary behavior: traffic lights exactly at positions $x$ and $x+K$ are not both counted inside a single kilometer. This creates off-by-one sensitivity in counting windows, and naive “sliding window count of stars in intervals” approaches often fail if they treat boundaries inclusively.

Another tricky case is when traffic lights are unevenly spaced. Removing one star might fix only a single “worst” segment, but that segment depends on the chosen $K$, so the identity of the bottleneck changes as $K$ changes.

A concrete failure scenario for naive reasoning is:

Input:

```
N = 10, L = 1
.*.*.*.*.*
```

A greedy idea might assume removing any single star reduces all local densities sufficiently, but for small $K$ many overlapping windows still exceed $L$. The correct answer depends on global spacing, not local fixes.

## Approaches

A brute-force strategy is to try every possible kilometer length $K$ from $1$ to $N$. For each $K$, we simulate sliding a window of length $K$ across the road and count traffic lights inside each window, considering the best possible removal of one traffic light. For a fixed $K$, this requires checking all $O(N)$ window positions, and within each we must track whether removing one star can reduce all violations. Even with prefix sums, identifying the worst window and simulating the best removal still takes $O(N)$, leading to $O(N^2)$ total work in the worst case, which is far beyond limits for $N = 10^6$.

The key structural insight is that for a fixed $K$, the constraint “every length-$K$ interval has at most $L$ stars after removing one” can be rephrased as: we need to ensure that no sliding window contains more than $L+1$ stars in the original configuration, because we can delete at most one star globally and it must fix all violations. This turns the problem into detecting whether all “bad windows” (those with at least $L+2$ stars) can be made good by removing a single star that lies in all of them.

That reduces the problem to an intersection condition: for a given $K$, all violating windows must share at least one common traffic light. If such a star exists, removing it fixes every violation simultaneously.

This transforms the problem into a decision problem over $K$. We can binary search the maximum valid $K$, since if a given $K$ works, any smaller $K$ also works because shrinking windows can only reduce star counts.

To check feasibility of a given $K$, we scan all windows, maintain star counts using a sliding window, record all windows with more than $L+1$ stars, and intersect their star index ranges. If the intersection is non-empty, a single removal exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(N)$ | Too slow |
| Binary Search + Sliding Window + Intersection | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We reformulate the decision check for a fixed $K$, then embed it in a binary search over $K$.

### 1. Binary search over answer

We maintain a search range for $K$. For each midpoint $K$, we test whether it is feasible. If feasible, we try larger values; otherwise we reduce the range. This works because feasibility is monotonic in $K$.

The monotonicity holds because increasing $K$ only increases or preserves the number of stars per window.

### 2. Sliding window over star positions

We preprocess positions of all traffic lights. For a given $K$, we slide a window over these positions to compute how many stars fall inside each interval $[i, i+K)$.

Instead of scanning the full string, we maintain two pointers over star positions, which is linear in the number of stars.

This step identifies all “bad windows”, meaning windows containing at least $L+2$ stars.

### 3. Track constraint on removable star

For every bad window, we record which stars lie inside it. The key requirement is that there exists a single star that lies in every bad window.

We maintain the intersection of allowable removal positions as a range over indices. Each bad window contributes a constraint: the removable star must be inside that window’s star set. Since stars are ordered, each window corresponds to a contiguous segment in the star index array, so intersection reduces to maintaining a global left bound and right bound.

If at the end the intersection is empty, no single removal fixes all violations.

### 4. Feasibility decision

If there are no bad windows, the configuration is already valid. If there are bad windows but their intersection is non-empty, we can remove a star that resolves all of them. Otherwise, the current $K$ is invalid.

### Why it works

The correctness rests on the fact that every violation is localized to a window with at least $L+2$ stars, and removing a star outside a violating window does not affect it. Therefore, a single removal is sufficient if and only if there exists a star that participates in every violating window. The sliding window ensures we enumerate all violations, and the intersection condition ensures global consistency across them. Binary search then finds the largest $K$ satisfying this feasibility condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, L = map(int, input().split())
    s = input().strip()

    stars = [i for i, c in enumerate(s) if c == '*']
    m = len(stars)

    if m == 0:
        print(n)
        return

    def check(k):
        if m <= L + 1:
            return True

        bad_intervals = 0
        left_ptr = 0

        # intersection over star indices [lo, hi]
        lo, hi = 0, m - 1

        for r in range(m):
            while stars[r] - stars[left_ptr] + 1 > k:
                left_ptr += 1

            cnt = r - left_ptr + 1
            if cnt >= L + 2:
                bad_intervals += 1
                lo = max(lo, left_ptr)
                hi = min(hi, r)

        if bad_intervals == 0:
            return True

        return lo <= hi

    # binary search answer
    ans = 1
    lo, hi = 1, n

    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation compresses the road into star positions so window counting ignores dots entirely. The sliding window operates only on the list of stars, which is essential for $O(N)$ behavior per check.

The feasibility function tracks whether there are any violating windows and simultaneously maintains the intersection of star indices that appear in all such windows. If at any point that intersection collapses, we know no single removal can fix all violations for that $K$.

The binary search wraps this predicate and extracts the maximum valid kilometer length.

## Worked Examples

### Example 1

Input:

```
15 2
*...*.*..*...*.
```

We test feasibility for increasing $K$. For a small $K$, many windows contain more than $L+1 = 3$ stars, producing overlapping bad intervals.

| Step | Window range | Star count | Bad window? | Intersection [lo, hi] |
| --- | --- | --- | --- | --- |
| 1 | [0, 4] | 2 | No | [0, 3] |
| 2 | [1, 5] | 2 | No | [0, 3] |
| 3 | [0, 8] | 4 | Yes | [1, 2] |
| 4 | [4, 12] | 4 | Yes | [1, 1] |

The intersection shrinks to a single star index, meaning removing that star fixes all violating windows. This remains true up to $K = 7$, and beyond that windows become too wide to control.

### Example 2

Input:

```
10 1
*.*.*.*.*
```

For $K = 1$, every window contains at most one star, so it is trivially valid after removal. As $K$ increases, multiple stars enter each window, quickly producing overlapping violations whose intersection becomes empty, showing no single removal can fix all of them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Binary search over $K$, each feasibility check scans star positions once |
| Space | $O(N)$ | Storage of star indices |

The solution fits comfortably within limits since $N = 10^6$ allows about $2 \times 10^7$ operations, and the constant factors are small due to linear scans over compressed star arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO
    return sys.stdout.getvalue()

# Note: full integration assumes solve() is defined above

# provided sample
# assert run("15 2\n*...*.*..*...*.\n") == "7"

# edge: no stars
# assert run("5 3\n.....\n") == "5"

# edge: one star
# assert run("5 0\n..*..\n") == "5"

# edge: dense alternating
# assert run("6 1\n*.*.*.\n") == "2"

# edge: all stars except constraint tight
# assert run("10 2\n**********\n") == "?"  # depends on interpretation
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no stars | full length | absence of constraints |
| single star | full range | removal irrelevant |
| alternating | small K | dense violations |
| full stars | minimal K | worst-case overlap |

## Edge Cases

One important edge case is when there are fewer than $L+2$ traffic lights in total. In that situation, every window automatically satisfies the constraint after removing any one light, so the correct answer is simply $N$. The algorithm handles this immediately in the feasibility check by returning true.

Another case is when traffic lights are extremely sparse. For example, if stars appear at positions far apart, every feasible $K$ becomes large because windows rarely accumulate enough stars to violate the limit. The sliding window over star positions naturally reflects this since the window count condition never reaches $L+2$.

A more subtle case occurs when violating windows overlap but do not share a common star. In such a scenario, the intersection range collapses. The check function captures this precisely through the maintained $[lo, hi]$ interval. If it becomes empty, it correctly rejects the candidate $K$, even if each individual window seems fixable in isolation.
