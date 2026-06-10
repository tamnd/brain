---
title: "CF 1552B - Running for Gold"
description: "Each athlete is described by five rankings, one ranking from each past marathon. Smaller values are better because a rank of 1 means first place. For two athletes x and y, we say that x is superior to y if x has a better rank in at least three of the five marathons."
date: "2026-06-10T13:09:32+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1552
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 15"
rating: 1500
weight: 1552
solve_time_s: 103
verified: true
draft: false
---

[CF 1552B - Running for Gold](https://codeforces.com/problemset/problem/1552/B)

**Rating:** 1500  
**Tags:** combinatorics, graphs, greedy, sortings  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Each athlete is described by five rankings, one ranking from each past marathon. Smaller values are better because a rank of 1 means first place.

For two athletes `x` and `y`, we say that `x` is superior to `y` if `x` has a better rank in at least three of the five marathons. Since there are exactly five comparisons, one athlete wins the head-to-head comparison if they are better in a majority of dimensions.

Our task is to find an athlete who defeats every other athlete in this pairwise comparison. If such an athlete exists, output their index. Otherwise output `-1`.

The first thing to notice is that the superiority relation is not transitive. If athlete A beats B and B beats C, A does not necessarily beat C. This immediately rules out many standard sorting-based ideas. In fact, cycles can exist.

The constraints are the real clue. The total number of athletes across all test cases is at most 50,000. A quadratic algorithm would perform roughly

$$50{,}000^2 = 2.5 \times 10^9$$

pair comparisons in the worst case, which is far beyond what fits in one second. We need something close to linear in `n`.

Several edge cases are easy to mishandle.

Consider a cyclic relation:

```
3
10 10 20 30 30
20 20 30 10 10
30 30 10 20 20
```

Athlete 1 beats 2, athlete 2 beats 3, and athlete 3 beats 1. No athlete beats everyone else, so the answer is `-1`. Any approach that tries to choose the athlete with the "best average rank" would incorrectly return someone.

Another subtle case is when a candidate defeats many athletes but not all:

```
3
1 1 1 100 100
2 2 2 1 1
3 3 3 2 2
```

Athlete 1 beats athlete 2, but athlete 2 beats athlete 3. We still must explicitly verify that the final candidate beats every athlete. Eliminating opponents alone is not enough.

The smallest possible test case is also worth checking:

```
1
50000 1 50000 50000 50000
```

With only one athlete, that athlete trivially satisfies the requirement.

## Approaches

The brute-force idea is straightforward. For every athlete `i`, compare them against every other athlete `j`. If `i` beats all others, return `i`.

A comparison between two athletes takes constant time because there are only five rankings. The problem is the number of comparisons. We perform `O(n²)` pair checks. With `n = 50,000`, that becomes roughly 2.5 billion comparisons, which is far too slow.

To get something faster, we need to exploit the fact that there are only five dimensions.

Suppose a valid champion exists. Let that athlete be `C`.

Imagine scanning athletes from left to right while maintaining a current candidate. Whenever another athlete beats the current candidate, we replace the candidate.

Why is this interesting? If the current candidate loses to someone, then the current candidate can never be the global champion. A champion must defeat everybody. Losing even once disqualifies it immediately.

This is exactly the same elimination idea used in finding a dominant element or a tournament winner. Every comparison removes one athlete from consideration.

After one linear pass, only one candidate survives.

The remaining question is whether the survivor is actually valid. Because the superiority relation is not transitive, the survivor is only a potential champion. We must verify it against all athletes.

The key observation is:

If a champion exists, the elimination pass cannot eliminate it. Any athlete that faces the champion loses, so the champion eventually becomes or remains the candidate. Thus the elimination phase always ends with the true champion if one exists.

After obtaining the candidate, a second linear scan checks whether it beats every athlete. If any athlete defeats the candidate, no champion exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all athletes and store their five rankings.
2. Define a comparison function `better(a, b)` that returns true if athlete `a` has a smaller rank than athlete `b` in at least three of the five marathons.
3. Start with athlete `0` as the current candidate.
4. Scan athletes from left to right.
5. For each athlete `i`, compare `i` with the current candidate.
6. If athlete `i` beats the current candidate, replace the candidate with `i`.

The old candidate has now lost a head-to-head comparison, so it cannot possibly be superior to everyone.
7. After the scan finishes, we have a single surviving candidate.
8. Verify the candidate by comparing it against every athlete.
9. If there exists any athlete that defeats the candidate, output `-1`.
10. Otherwise output the candidate's 1-based index.

### Why it works

During the elimination pass, every replacement removes one athlete that cannot be the global champion. If athlete `A` loses to athlete `B`, then `A` is certainly not superior to all athletes.

Assume a valid champion `C` exists. Whenever `C` is compared against another athlete, `C` wins. Hence once `C` becomes the candidate, it can never be removed. Even before that happens, every athlete that eliminates another athlete is merely removing a non-champion. Eventually the scan ends with `C` as the candidate.

If no champion exists, the elimination pass still produces some survivor. The verification pass detects this by finding an athlete that defeats the survivor. Thus the algorithm returns a valid athlete exactly when one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def better(a, b):
    cnt = 0
    for k in range(5):
        if a[k] < b[k]:
            cnt += 1
    return cnt >= 3

t = int(input())

for _ in range(t):
    n = int(input())
    athletes = [list(map(int, input().split())) for _ in range(n)]

    cand = 0

    for i in range(1, n):
        if better(athletes[i], athletes[cand]):
            cand = i

    ok = True
    for i in range(n):
        if i != cand and not better(athletes[cand], athletes[i]):
            ok = False
            break

    print(cand + 1 if ok else -1)
```

The `better` function implements the problem's definition directly. It counts how many of the five marathons athlete `a` performed better in than athlete `b`. Winning at least three dimensions means winning the majority comparison.

The first loop performs the elimination phase. Whenever another athlete defeats the current candidate, the current candidate is discarded permanently.

The second loop is the crucial verification phase. The superiority relation is not transitive, so the survivor of the first pass is not automatically valid. We must explicitly check that it defeats every athlete.

Indices are stored internally as zero-based values because Python lists use zero-based indexing. The final answer adds one before printing because the problem uses one-based athlete numbering.

No special handling is required for `n = 1`. The elimination loop does nothing, the verification loop succeeds, and athlete 1 is printed.

## Worked Examples

### Example 1

Input:

```
3
1 1 1 1 1
2 2 2 2 2
3 3 3 3 3
```

Elimination phase:

| Step | Current Candidate | Challenger | Challenger Beats Candidate? | New Candidate |
| --- | --- | --- | --- | --- |
| Start | 1 | - | - | 1 |
| 1 | 1 | 2 | No | 1 |
| 2 | 1 | 3 | No | 1 |

Verification phase:

| Athlete Checked | Candidate Beats Athlete? |
| --- | --- |
| 2 | Yes |
| 3 | Yes |

The answer is athlete 1. This example shows the simplest successful case where one athlete dominates every comparison.

### Example 2

Input:

```
3
10 10 20 30 30
20 20 30 10 10
30 30 10 20 20
```

Elimination phase:

| Step | Current Candidate | Challenger | Challenger Beats Candidate? | New Candidate |
| --- | --- | --- | --- | --- |
| Start | 1 | - | - | 1 |
| 1 | 1 | 2 | No | 1 |
| 2 | 1 | 3 | Yes | 3 |

Verification phase:

| Athlete Checked | Candidate Beats Athlete? |
| --- | --- |
| 1 | Yes |
| 2 | No |

Since athlete 3 does not beat athlete 2, verification fails and the answer is `-1`.

This example demonstrates why the second pass is necessary. The elimination phase alone would incorrectly return athlete 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One elimination scan and one verification scan |
| Space | O(n) | Storing the athletes' rankings |
| Extra Space | O(1) | Aside from the input storage |

Each athlete participates in a constant number of comparisons, and every comparison examines only five rankings. Since the total number of athletes across all test cases is at most 50,000, the solution comfortably fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def better(a, b):
        cnt = 0
        for k in range(5):
            if a[k] < b[k]:
                cnt += 1
        return cnt >= 3

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        athletes = [list(map(int, input().split())) for _ in range(n)]

        cand = 0

        for i in range(1, n):
            if better(athletes[i], athletes[cand]):
                cand = i

        ok = True
        for i in range(n):
            if i != cand and not better(athletes[cand], athletes[i]):
                ok = False
                break

        ans.append(str(cand + 1 if ok else -1))

    print("\n".join(ans))

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

# provided sample
assert run(
"""4
1
50000 1 50000 50000 50000
3
10 10 20 30 30
20 20 30 10 10
30 30 10 20 20
3
1 1 1 1 1
2 2 2 2 2
3 3 3 3 3
6
9 5 3 7 1
7 4 1 6 8
5 6 7 3 2
6 7 8 8 6
4 2 2 4 5
8 3 6 9 4
"""
) == "1\n-1\n1\n5\n"

# n = 1
assert run(
"""1
1
1 2 3 4 5
"""
) == "1\n"

# clear champion
assert run(
"""1
3
1 1 1 1 1
2 2 2 2 2
3 3 3 3 3
"""
) == "1\n"

# cyclic relation
assert run(
"""1
3
10 10 20 30 30
20 20 30 10 10
30 30 10 20 20
"""
) == "-1\n"

# candidate must be verified
assert run(
"""1
3
1 1 1 100 100
2 2 2 1 1
3 3 3 2 2
"""
) == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single athlete | 1 | Trivial base case |
| Strict dominance ordering | 1 | Champion exists |
| Cyclic superiority relation | -1 | Verification phase is required |
| Mixed rankings with a valid winner | 1 | Candidate survives elimination and verification |

## Edge Cases

Consider the cyclic example:

```
3
10 10 20 30 30
20 20 30 10 10
30 30 10 20 20
```

The elimination pass ends with athlete 3. A careless solution might immediately output 3. During verification, athlete 2 defeats athlete 3, so the algorithm correctly returns `-1`.

Consider the single-athlete case:

```
1
50000 1 50000 50000 50000
```

The candidate starts as athlete 1. No elimination comparisons occur. Verification also performs no meaningful checks because there are no opponents. The algorithm outputs `1`, which matches the definition.

Consider a case where the champion is not initially the candidate:

```
3
2 2 2 2 2
1 1 1 1 1
3 3 3 3 3
```

The candidate begins as athlete 1. Athlete 2 defeats athlete 1 and becomes the new candidate. Athlete 3 cannot defeat athlete 2, so athlete 2 survives. Verification confirms athlete 2 beats everyone. The answer is `2`.

Consider a case where an athlete looks strong locally but is not a global winner:

```
3
1 1 1 100 100
2 2 2 1 1
3 3 3 2 2
```

Athlete 1 defeats athlete 2 in three dimensions and athlete 3 in three dimensions. The elimination pass keeps athlete 1. Verification confirms athlete 1 defeats every other athlete, so the answer is `1`. This shows that the algorithm relies on actual pairwise superiority rather than aggregate statistics such as sums or averages.
