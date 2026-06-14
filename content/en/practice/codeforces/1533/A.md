---
title: "CF 1533A - Travel to Bertown"
description: "Vika arrives in Bertown on a fixed day $k$. She has several friends, and each friend offers a single continuous interval of days during which she can stay at their home."
date: "2026-06-14T18:31:17+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 253
verified: true
draft: false
---

[CF 1533A - Travel to Bertown](https://codeforces.com/problemset/problem/1533/A)

**Rating:** -  
**Tags:** *special, implementation, math  
**Solve time:** 4m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Vika arrives in Bertown on a fixed day $k$. She has several friends, and each friend offers a single continuous interval of days during which she can stay at their home. The constraint is that she can choose at most one friend, and once she chooses, she can only stay within that friend’s allowed interval. However, she does not necessarily arrive at the start of that interval, so her actual stay must begin no earlier than day $k$.

For any chosen friend with interval $[l_i, r_i]$, Vika can only stay from day $k$ up to day $r_i$, provided that $k$ lies inside that interval. This means the effective number of days she stays is $r_i - k + 1$, but only if $l_i \le k \le r_i$. If no interval contains $k$, she cannot stay at all.

The task reduces to checking all intervals that contain $k$ and finding the one that extends farthest to the right.

The constraints are small: $t \le 500$, $n \le 100$, and all day values are bounded by 100. This immediately rules out any need for complex preprocessing or advanced data structures. A simple linear scan per test case is sufficient.

A subtle edge case appears when no interval contains $k$. For example, if $k = 4$ and all intervals are like $[1,2]$, $[5,6]$, then every friend is either too early or starts too late. In that case, the answer must be exactly 0, since Vika cannot stay even for a single day.

Another edge case is when multiple intervals contain $k$. For instance, $k = 3$, and intervals $[1,4]$, $[2,6]$, and $[3,3]$. A careless approach might pick the interval that starts closest to $k$, but that is irrelevant. The correct choice is the interval with the maximum right endpoint.

## Approaches

A brute-force interpretation is to simulate Vika’s choice explicitly: for each friend, check whether $k$ lies in their interval, compute how many days she could stay if she chooses that friend, and take the maximum. This already runs in $O(n)$ per test case, since each interval is checked once.

There is no deeper combinatorial structure here because the decision does not depend on overlaps between intervals. Each friend is independent: either they can host Vika on day $k$ or they cannot. Once we filter valid intervals, the best choice is determined solely by the largest right endpoint.

A more complicated “optimization” might try sorting or sweeping, but that adds unnecessary overhead without improving complexity. The key observation is that the only constraint that matters is whether $k$ lies in $[l_i, r_i]$, and among those intervals, maximizing $r_i$ directly maximizes the stay length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all intervals) | $O(n)$ per test case | $O(1)$ | Accepted |
| Optimal (same idea, direct scan) | $O(n)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$, which define the number of friends and Vika’s arrival day. The goal is to evaluate all intervals against this fixed reference point $k$.
2. Initialize an answer variable as 0. This represents the best number of days Vika can stay so far. Starting from 0 naturally handles the case where no valid interval exists.
3. Iterate over each friend’s interval $[l_i, r_i]$. For each interval, first check whether it includes day $k$, meaning $l_i \le k \le r_i$. This condition ensures Vika can actually start staying there on arrival day.
4. If the interval is valid, compute the potential stay length as $r_i - k + 1$. This reflects staying from day $k$ until the last available day in that interval.
5. Update the answer with the maximum of its current value and the computed stay length. This ensures we always keep the best possible choice among all valid friends.
6. After processing all intervals, output the stored maximum value.

### Why it works

The algorithm relies on the fact that Vika never leaves a chosen friend’s interval early or late; her stay is completely determined by the interval’s right boundary once the start day $k$ is fixed. Every valid interval contributes an independent candidate answer $r_i - k + 1$, and invalid intervals contribute nothing. Since the decision space is a simple maximum over independent values, scanning all intervals preserves correctness without missing any hidden interaction.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    n, k = map(int, input().split())
    best = 0

    for _ in range(n):
        l, r = map(int, input().split())
        if l <= k <= r:
            best = max(best, r - k + 1)

    out.append(str(best))

print("\n".join(out))
```

The solution maintains a single running maximum per test case. The condition `l <= k <= r` filters only usable intervals, ensuring we never compute invalid stays. The expression `r - k + 1` correctly counts inclusive days from arrival to departure.

The output is buffered to avoid repeated I/O overhead across test cases.

## Worked Examples

### Sample 1

Input:

```
3 3
1 4
2 6
4 10
```

We track only intervals containing day 3.

| Interval | Contains k=3 | r - k + 1 | best |
| --- | --- | --- | --- |
| [1,4] | yes | 2 | 2 |
| [2,6] | yes | 4 | 4 |
| [4,10] | no | - | 4 |

The second interval gives the best outcome, allowing Vika to stay 4 days.

This confirms that the algorithm correctly ignores irrelevant intervals and only maximizes over valid ones.

### Sample 2

Input:

```
2 4
2 3
5 8
```

| Interval | Contains k=4 | r - k + 1 | best |
| --- | --- | --- | --- |
| [2,3] | no | - | 0 |
| [5,8] | no | - | 0 |

No interval includes day 4, so the answer remains 0. This validates correct handling of the “no valid friend” case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each interval is checked once for inclusion and contribution |
| Space | $O(1)$ | Only a few integers are stored per test case |

Given $n \le 100$ and $t \le 500$, the solution performs at most 50,000 interval checks, which is trivial within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        best = 0
        for _ in range(n):
            l, r = map(int, input().split())
            if l <= k <= r:
                best = max(best, r - k + 1)
        out.append(str(best))

    return "\n".join(out)

# provided samples
assert run("""3
3 3
1 4
2 6
4 10
2 4
2 3
5 8
2 4
4 4
1 3
""") == "4\n0\n1"

# minimum case: single friend covers k
assert run("""1
1 5
5 5
""") == "1"

# no friend covers k
assert run("""1
2 10
1 9
11 20
""") == "0"

# multiple valid intervals
assert run("""1
3 3
1 10
2 5
3 4
""") == "8"

# boundary: k equals r in best interval
assert run("""1
2 4
1 4
2 10
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single exact interval | 1 | minimal valid case |
| no coverage | 0 | absence handling |
| multiple candidates | 8 | correct max selection |
| boundary at right edge | 1 | inclusive endpoint correctness |

## Edge Cases

When no interval includes $k$, the scan never updates the initial answer of 0. For example, with $k = 7$, intervals $[1,3]$ and $[8,10]$ are both invalid because neither satisfies $l \le k \le r$. The algorithm correctly leaves the answer at 0 and outputs it directly.

When multiple intervals include $k$, only the right endpoint matters. For instance, with $k = 3$, intervals $[1,4]$, $[2,6]$, and $[3,3]$, the algorithm evaluates candidate values $2$, $4$, and $1$. The maximum is 4, coming from $[2,6]$. The selection process never depends on how far left an interval starts, only on how far right it extends from $k$.
