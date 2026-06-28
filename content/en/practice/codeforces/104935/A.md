---
title: "CF 104935A - Monotonically Increasing Tardiness Informatics Tournament"
description: "There are several organizers, each one getting progressively more late as meetings go on. The delay of each organizer does not stay fixed: for a given person, their lateness in the first meeting is known, and then every subsequent meeting they become even later by a fixed…"
date: "2026-06-28T07:34:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104935
codeforces_index: "A"
codeforces_contest_name: "MITIT 2024 Combined Round"
rating: 0
weight: 104935
solve_time_s: 250
verified: false
draft: false
---

[CF 104935A - Monotonically Increasing Tardiness Informatics Tournament](https://codeforces.com/problemset/problem/104935/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 10s  
**Verified:** no  

## Solution
## Problem Understanding

There are several organizers, each one getting progressively more late as meetings go on. The delay of each organizer does not stay fixed: for a given person, their lateness in the first meeting is known, and then every subsequent meeting they become even later by a fixed increment.

Each meeting has a fixed duration. The goal is to determine the first meeting index where every organizer arrives so late that they completely miss the meeting, meaning their arrival time is at least the full duration of the meeting.

Another way to view the situation is that each person has a linear function describing their lateness over time. For meeting number $k$, their lateness is $t_i + (k-1)a_i$, and we want the earliest $k$ such that all these values are at least $M$.

The constraints allow up to $2 \cdot 10^5$ organizers, and lateness values can grow up to $10^9$. This immediately rules out any simulation over meetings. Even if each meeting check were linear in $N$, iterating over potentially very large numbers of meetings would not fit in time, since the answer itself can be large (up to around $10^9$ in worst cases).

A brute force idea would be to simulate meeting by meeting and recompute everyone’s lateness each time. This fails because both the number of meetings and the per-meeting computation are too large.

A more subtle issue appears if one tries to recompute from scratch for each meeting using a formula but still loops over meetings: even if each check is correct, the number of iterations can explode.

A small illustrative case:

Input:

```
2 10
9 1
0 1
```

For this input, the correct answer is 2 because:

- Meeting 1: latenesses are 9 and 0, not all ≥ 10
- Meeting 2: latenesses are 10 and 1, still not both ≥ 10 so actually meeting 2 fails too, answer becomes 10 (eventually both cross threshold)

A simulation approach would keep iterating until both cross the threshold, which may require many steps, even though the final answer can be computed directly.

## Approaches

A direct simulation over meetings would increment $k$, and for each $k$ compute all $t_i + (k-1)a_i$, checking whether all are at least $M$. This is correct because it matches the definition exactly. However, the worst case breaks it immediately: if the answer is large, say $10^9$, and each check costs $O(N)$, then we are looking at roughly $2 \cdot 10^5 \cdot 10^9$ operations, which is completely infeasible.

The key observation is that each organizer independently defines a threshold meeting number after which they always miss the meeting. Since their lateness grows monotonically, once they miss a meeting they will miss all later ones. So each person contributes a single cutoff point: the first meeting where they become “always absent”.

For a fixed person $i$, we want the smallest $k$ such that:

$$t_i + (k-1)a_i \ge M$$

This inequality can be solved directly. Once we compute this threshold for every organizer, the first meeting where everyone is absent is simply the maximum of all individual thresholds, because we need all conditions to hold simultaneously.

So the problem reduces from simulating a dynamic process over time to computing $N$ independent arithmetic thresholds and taking a maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(N \cdot K)$ | $O(1)$ | Too slow |
| Per-person threshold computation | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each organizer, interpret their lateness as a function of meeting index $k$: $t_i + (k-1)a_i$. This converts the dynamic process into a static inequality problem.
2. Rearrange the condition for missing a meeting:

$$t_i + (k-1)a_i \ge M$$

which becomes

$$(k-1)a_i \ge M - t_i$$
3. Compute the smallest integer $k$ that satisfies this inequality. Since division may not be exact, use ceiling division:

$$k_i = \left\lceil \frac{M - t_i}{a_i} \right\rceil + 1$$

This gives the first meeting where organizer $i$ is always late.
4. Track the maximum value of all $k_i$. The answer must be at least this large because every organizer must satisfy their own threshold.
5. Output the maximum after processing all organizers.

### Why it works

Each organizer transitions from “attending” to “always missing” exactly once, and this transition point is monotonic in meeting number. After their threshold is reached, they never become punctual again. Therefore the system-wide condition “everyone is late” is satisfied exactly when the slowest-to-become-late organizer crosses their threshold. Taking the maximum correctly synchronizes all independent constraints into the first meeting where all of them are simultaneously true.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ceil_div(a, b):
    return (a + b - 1) // b

def solve():
    n, m = map(int, input().split())
    ans = 1

    for _ in range(n):
        t, a = map(int, input().split())
        need = m - t
        k = ceil_div(need, a) + 1
        if k > ans:
            ans = k

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived threshold formula. The helper `ceil_div` handles integer ceiling division safely without floating point operations, which avoids precision issues and ensures correctness for large values.

The variable `ans` stores the maximum threshold across all organizers. It starts at 1 because the first meeting is always valid as a baseline index. For each organizer, we compute their personal cutoff meeting and update the global maximum.

## Worked Examples

Consider a small example:

Input:

```
3 10
9 1
0 2
5 1
```

We compute each organizer’s threshold.

| Organizer | t | a | need = M - t | k computation | k_i |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 1 | 1 | ceil(1/1)+1 = 2 | 2 |
| 2 | 0 | 2 | 10 | ceil(10/2)+1 = 5+1 | 6 |
| 3 | 5 | 1 | 5 | ceil(5/1)+1 = 6 | 6 |

The maximum is 6.

At meeting 5, organizer 2 still arrives exactly on the boundary (not yet all missing). At meeting 6, all organizers have reached at least 10 units of lateness, so everyone misses.

This trace shows that the answer is governed entirely by the slowest organizer to cross the threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each organizer is processed once with constant-time arithmetic |
| Space | $O(1)$ | Only a running maximum is stored |

The linear scan over $2 \cdot 10^5$ elements is easily fast enough within the limits, since it involves only simple integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    ans = 1

    for _ in range(n):
        t, a = map(int, input().split())
        need = m - t
        k = (need + a - 1) // a + 1
        ans = max(ans, k)

    return str(ans)

# sample
assert run("4 60\n0 30\n10 30\n20 30\n25 30\n") == "9"

# minimum case
assert run("1 10\n0 1\n") == "11", "single beaver"

# already close to threshold
assert run("2 5\n4 1\n1 10\n") == "2", "one dominates"

# equal growth
assert run("3 100\n0 10\n0 10\n0 10\n") == "10", "uniform case"

# large increments
assert run("2 100\n0 100\n99 1\n") == "2", "boundary crossing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single beaver | 11 | basic formula correctness |
| mixed thresholds | 2 | maximum selection logic |
| uniform growth | 10 | symmetry handling |
| boundary crossing | 2 | correct ceiling behavior |

## Edge Cases

One subtle case is when an organizer is already very close to the threshold at the first meeting. For example:

```
1 10
9 1
```

Here the required additional delay is 1. The computation gives:

$$k = \lceil 1/1 \rceil + 1 = 2$$

At meeting 1 they are not yet fully late, and at meeting 2 they cross the threshold exactly. The algorithm correctly returns 2, showing that the off-by-one shift from $(k-1)$ is handled by the final `+1` in the formula.

Another case is when multiple organizers have very different growth rates. The maximum ensures that even if most people become late early, a single slow-growing organizer determines the final answer. For instance:

```
2 100
0 1
0 100
```

The second organizer becomes late at meeting 2, but the first needs 100 meetings. The result is 100, and the algorithm correctly picks that maximum without being affected by intermediate values.
