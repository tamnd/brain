---
title: "CF 69B - Bets"
description: "Each athlete runs through a contiguous interval of sections. While an athlete is inside a section, they spend exactly t[i] time on that section, so the winner of a section is simply the active athlete with the smallest t."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 69
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 63 (Div. 2)"
rating: 1200
weight: 69
solve_time_s: 121
verified: true
draft: false
---

[CF 69B - Bets](https://codeforces.com/problemset/problem/69/B)

**Rating:** 1200  
**Tags:** greedy, implementation  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Each athlete runs through a contiguous interval of sections. While an athlete is inside a section, they spend exactly `t[i]` time on that section, so the winner of a section is simply the active athlete with the smallest `t`. If several athletes have the same time, the smaller index wins.

We are allowed to place at most one bet per section, and only on athletes actually running in that section. If we bet on the section winner, we gain that athlete's reward `c[i]`. Since sections are independent, the task becomes:

For every section, determine which athlete wins there, then add that athlete's profit.

The constraints are tiny, only up to 100 sections and 100 athletes. Even an `O(n * m^2)` solution would pass comfortably because the worst case is only about one million operations. This means we do not need complicated data structures or sweep-line optimizations. A direct simulation is enough.

The tricky part is not performance, it is implementing the winner rules correctly.

One easy mistake is forgetting the tie-breaking rule by index.

Consider:

```
3 2
1 3 5 10
1 3 5 20
```

Both athletes have equal speed everywhere. Athlete 1 wins every section because of the smaller index, so the answer is:

```
30
```

A careless implementation that picks the larger reward instead of the official winner would incorrectly output `60`.

Another subtle case is sections with no athletes.

```
5 1
2 4 3 10
```

Sections 1 and 5 have no participants, so no bet can win there. Only sections 2, 3, and 4 contribute profit. The correct answer is:

```
30
```

An implementation that assumes every section always has a winner would access invalid data or count extra profit.

A third common bug is checking total race time instead of per-section time.

```
4 2
1 4 10 5
2 2 1 100
```

Athlete 2 only appears in section 2, but there they are much faster and win that section. The correct total is:

Section 1 -> athlete 1, gain 5

Section 2 -> athlete 2, gain 100

Sections 3 and 4 -> athlete 1, gain 5 each

Total:

```
115
```

The whole race duration does not matter. Only the per-section time `t[i]` matters inside each section.

## Approaches

The most direct approach is to process every section independently. For a fixed section, we scan all athletes and keep only those whose interval covers this section. Among those active athletes, we select the one with the smallest `t`. If several athletes share the same `t`, we choose the smaller index. Then we add that athlete's reward to the answer.

This brute-force idea is already fast enough. There are at most 100 sections and 100 athletes, so we perform at most 10,000 athlete checks. Even if we add extra comparisons for tie-breaking, the runtime is negligible.

The reason this simple method works is that the problem has no interaction between sections. Betting on one section does not affect another section. Once we know the winner of a section, the optimal choice is forced: bet on that winner and collect the reward. There is never a reason to bet on anyone else.

A more complicated interpretation might suggest dynamic programming or interval processing because athletes occupy ranges of sections. But the key observation is that winners are determined locally, section by section. The intervals only tell us whether an athlete participates in a section.

We can think of the algorithm as simulating the race timeline. For every section:

1. Find all active athletes.
2. Pick the fastest.
3. Add their reward.

That is the entire solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Accepted |
| Optimal | O(n * m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of sections and athletes.
2. Store all athletes as tuples `(l, r, t, c)`.
3. Iterate through every section from `1` to `n`.
4. For the current section, scan all athletes and check whether the athlete is active there, meaning `l <= section <= r`.
5. Among all active athletes, keep the one with:

1. the smallest `t`
2. and if times are equal, the smallest athlete index

This exactly matches the race rules.
6. If at least one athlete is active in this section, add that winner's reward `c` to the answer.
7. After processing all sections, print the total profit.

### Why it works

For every section, the outcome is completely independent from every other section. The official winner is uniquely determined by the minimum section time and the tie-breaking rule on indices.

If we bet on anyone except the winner, we gain zero from that section. Betting on the winner gives exactly `c[i]`. Since there is no restriction connecting different sections, choosing the winner independently for every section maximizes the total profit.

The algorithm explicitly computes that official winner for every section, so the produced sum is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

athletes = []
for _ in range(m):
    l, r, t, c = map(int, input().split())
    athletes.append((l, r, t, c))

answer = 0

for section in range(1, n + 1):
    best_time = float('inf')
    best_index = -1

    for idx, (l, r, t, c) in enumerate(athletes):
        if l <= section <= r:
            if t < best_time:
                best_time = t
                best_index = idx
            elif t == best_time and idx < best_index:
                best_index = idx

    if best_index != -1:
        answer += athletes[best_index][3]

print(answer)
```

The program stores every athlete together with their interval, speed, and reward.

The outer loop processes sections one by one. For each section, we search for the winning athlete. `best_time` tracks the minimum section time seen so far, while `best_index` stores which athlete currently wins the tie-break.

The condition `l <= section <= r` determines whether the athlete participates in this section. Only active athletes are considered.

The tie-breaking logic deserves attention. Suppose two athletes have equal `t`. The rules say the smaller athlete index wins. Since Python indices start from zero and the input numbering effectively follows insertion order, comparing `idx` correctly reproduces the official rule.

The check `best_index != -1` handles empty sections safely. If no athlete covers the current section, no reward is added.

Because the constraints are tiny, there is no need for preprocessing or sorting.

## Worked Examples

### Sample 1

Input:

```
4 4
1 4 20 5
1 3 21 10
3 3 4 30
3 4 4 20
```

Processing trace:

| Section | Active Athletes | Winner | Profit Added | Total |
| --- | --- | --- | --- | --- |
| 1 | 1, 2 | 1 | 5 | 5 |
| 2 | 1, 2 | 1 | 5 | 10 |
| 3 | 1, 2, 3, 4 | 3 | 30 | 40 |
| 4 | 1, 4 | 4 | 20 | 60 |

At sections 1 and 2, athlete 1 beats athlete 2 because `20 < 21`. At section 3, athletes 3 and 4 both have time `4`, so athlete 3 wins due to smaller index. Section 4 is won by athlete 4 because athlete 3 is no longer active.

This example demonstrates both interval filtering and tie-breaking.

### Additional Example

Input:

```
5 3
1 5 10 5
2 4 3 20
3 3 1 100
```

Processing trace:

| Section | Active Athletes | Winner | Profit Added | Total |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 5 | 5 |
| 2 | 1, 2 | 2 | 20 | 25 |
| 3 | 1, 2, 3 | 3 | 100 | 125 |
| 4 | 1, 2 | 2 | 20 | 145 |
| 5 | 1 | 1 | 5 | 150 |

This example shows how a short interval athlete can still dominate a section if their time is smallest there. The winner is always determined locally for the current section.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | For every section, we scan all athletes |
| Space | O(1) excluding input storage | Only a few tracking variables are used |

With `n, m <= 100`, the worst-case runtime is only 10,000 checks, which is far below the limit. Memory usage is tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    athletes = []
    for _ in range(m):
        l, r, t, c = map(int, input().split())
        athletes.append((l, r, t, c))

    ans = 0

    for section in range(1, n + 1):
        best_time = float('inf')
        best_idx = -1

        for idx, (l, r, t, c) in enumerate(athletes):
            if l <= section <= r:
                if t < best_time:
                    best_time = t
                    best_idx = idx
                elif t == best_time and idx < best_idx:
                    best_idx = idx

        if best_idx != -1:
            ans += athletes[best_idx][3]

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""4 4
1 4 20 5
1 3 21 10
3 3 4 30
3 4 4 20
"""
) == "60", "sample 1"

# minimum size
assert run(
"""1 1
1 1 5 10
"""
) == "10", "single section single athlete"

# tie-breaking by smaller index
assert run(
"""3 2
1 3 5 10
1 3 5 20
"""
) == "30", "smaller index must win ties"

# sections without participants
assert run(
"""5 1
2 4 3 10
"""
) == "30", "empty sections give no reward"

# short interval fast athlete
assert run(
"""4 2
1 4 10 5
2 2 1 100
"""
) == "115", "winner determined per section"

# all athletes equal
assert run(
"""2 3
1 2 7 10
1 2 7 20
1 2 7 30
"""
) == "20", "first athlete wins all sections"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single athlete on one section | 10 | Minimum constraints |
| Equal times for all athletes | 30 | Correct tie-breaking |
| Empty boundary sections | 30 | No winner handling |
| Fast athlete on one section | 115 | Local section-based winner |
| All athletes identical | 20 | Stable smallest-index selection |

## Edge Cases

Consider equal speeds with different rewards:

```
3 2
1 3 5 10
1 3 5 20
```

For every section, both athletes are active and both have time `5`. The algorithm compares indices and always selects athlete 1. The total becomes `10 + 10 + 10 = 30`.

A buggy solution that greedily chooses the larger reward would incorrectly output `60`.

Now consider empty sections:

```
5 1
2 4 3 10
```

The algorithm processes each section independently.

Section 1:

No active athlete, nothing added.

Sections 2, 3, 4:

Athlete 1 wins, add `10` each time.

Section 5:

No active athlete again.

Final answer:

```
30
```

The `best_index != -1` check prevents adding profit for nonexistent winners.

Finally, consider a fast athlete with a tiny interval:

```
4 2
1 4 10 5
2 2 1 100
```

The algorithm checks activity per section.

| Section | Winner | Total |
| --- | --- | --- |
| 1 | Athlete 1 | 5 |
| 2 | Athlete 2 | 105 |
| 3 | Athlete 1 | 110 |
| 4 | Athlete 1 | 115 |

This confirms that winners depend only on the current section, not on total race duration or interval length.
