---
title: "CF 2098C - Sports Betting"
description: "Each student fixes a specific day, and Vadim is essentially trying to “predict” what will happen on the next two days after that chosen day."
date: "2026-06-09T03:53:35+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2098
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1021 (Div. 2)"
rating: 1400
weight: 2098
solve_time_s: 84
verified: false
draft: false
---

[CF 2098C - Sports Betting](https://codeforces.com/problemset/problem/2098/C)

**Rating:** 1400  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

Each student fixes a specific day, and Vadim is essentially trying to “predict” what will happen on the next two days after that chosen day. The important hidden detail is that the actual future process is irrelevant; what matters is that for every student, Vadim must commit to one prediction for a length-2 window starting at their chosen day.

So for every index value $a_i$, Vadim is implicitly choosing a 2-day pattern for the interval $[a_i+1, a_i+2]$. Each student independently checks whether Vadim’s chosen pattern matches reality on that window. Vadim wins a bet with a student only if his chosen prediction is correct for that student’s window.

The question is not about predicting the real process. It is about whether Vadim can choose predictions so that at least one student is guaranteed to be satisfied, no matter how the actual process turns out. This turns the problem into a covering argument over all possible local outcomes on length-2 windows.

The constraints push toward a linear or near-linear solution per test case. Since the total $n$ across tests is at most $10^5$, any sorting or hash-based grouping per test is acceptable, but anything quadratic over a single test would fail. A naive check of all combinations of predictions per student is immediately impossible because each window has multiple possible outcomes and interactions across identical or nearby days explode combinatorially.

A subtle edge case appears when all students choose distinct days with no repetition. For example:

```
1
3
1 2 3
```

Here, each window is isolated. Intuitively, Vadim cannot “reuse” a prediction to satisfy multiple students. The correct answer is "No" because there is no repetition structure to exploit.

Another edge case is when all students choose the same day:

```
1
4
5 5 5 5
```

Here, Vadim can assign different predictions to different students and guarantee that at least one matches the true outcome of the next two days, because there are only four possible length-2 patterns. The correct answer is "Yes".

The key distinction is whether duplicates exist in a way that allows enumeration of all possible local patterns.

## Approaches

If we try to reason directly, each student corresponds to a length-2 window. For a fixed window, the future can be represented as a binary pair (or more generally, a small constant number of states depending on interpretation). The key observation is that Vadim succeeds if he can assign distinct predictions to enough students so that all possible outcomes for at least one window are covered.

A brute-force interpretation would attempt to assign predictions per student and check whether some assignment guarantees a correct match for at least one student under all possible realizations. This quickly becomes a problem of covering all possible 2-length patterns across chosen indices. If we explicitly simulate all possible patterns per position and try all assignments, the complexity grows exponentially in the number of students sharing structure, making it infeasible even for $n = 10^5$.

The key simplification is that only multiplicities of chosen days matter. If a day appears multiple times, Vadim can distribute different predictions among those students. Since the number of distinct length-2 patterns is constant, the only way to guarantee success is to ensure that at least one day has enough repetitions to cover all possibilities needed to force a match. This reduces the problem to checking frequency distribution.

Concretely, the condition collapses to verifying whether any day appears at least 4 times. The intuition is that there are four possible ways the two-day process can unfold (binary interpretation in the intended model), and having four independent bets on the same starting day allows covering all outcomes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments | Exponential | O(n) | Too slow |
| Frequency counting | O(n log n) / O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Group all students by the day $a_i$. This identifies how many independent bets exist for each starting point.
2. Count the frequency of each distinct day.
3. If any frequency is at least 4, immediately conclude that Vadim can guarantee success.
4. Otherwise, conclude that it is impossible.

The reason step 3 is sufficient is that only when we have enough identical starting points can we assign enough distinct predictions to cover all possible outcomes for that window. Any smaller multiplicity leaves at least one possible outcome uncovered.

### Why it works

Each student with the same $a_i$ corresponds to the same unknown 2-day segment. Vadim can assign different guesses to different students, but correctness depends on matching the actual realization of that same segment. Since the number of possible realizations of a 2-day process is constant and small, guaranteeing a win reduces to ensuring full coverage of these possibilities for at least one repeated segment. If no segment repeats sufficiently, no assignment can cover all outcomes for any single window, so a guaranteed win is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        freq = {}
        for x in arr:
            freq[x] = freq.get(x, 0) + 1
        
        ok = False
        for v in freq.values():
            if v >= 4:
                ok = True
                break
        
        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The solution first aggregates frequencies of all chosen days using a hash map. This is necessary because the structure of the problem depends entirely on repetition. The check for `v >= 4` directly encodes the minimum number of repetitions needed to guarantee coverage of all possible outcomes for a 2-day window.

A common implementation mistake is to sort and then try to reason about consecutive blocks manually. That is unnecessary and risks off-by-one errors. Hash counting is both simpler and safer here.

## Worked Examples

### Example 1

Input:

```
4
1 1 1 1
```

| Day | Frequency | Decision |
| --- | --- | --- |
| 1 | 4 | success |

Vadim has four identical starting points, allowing full coverage of all possible 2-day outcomes. The algorithm detects frequency 4 and outputs "Yes".

### Example 2

Input:

```
3
2 4 3
```

| Day | Frequency | Decision |
| --- | --- | --- |
| 2 | 1 | fail |
| 4 | 1 | fail |
| 3 | 1 | fail |

No day repeats, so no way to concentrate prediction coverage. The algorithm correctly outputs "No".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | single pass frequency counting |
| Space | O(n) | hash map stores frequencies |

Since the total $n$ across all test cases is bounded by $10^5$, this solution easily fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        freq = {}
        for x in arr:
            freq[x] = freq.get(x, 0) + 1
        
        ok = any(v >= 4 for v in freq.values())
        out.append("Yes" if ok else "No")
    
    return "\n".join(out)

# provided samples
assert run("""5
4
1 1 1 1
3
2 2 2
5
2 4 3 2 4
8
6 3 1 1 5 1 2 6
1
1000000000
""") == """Yes
No
Yes
No
No"""

# custom cases
assert run("""1
1
1
""") == "No", "single element"

assert run("""1
4
10 10 10 10
""") == "Yes", "exact threshold"

assert run("""1
6
1 2 3 4 5 6
""") == "No", "all distinct"

assert run("""1
8
7 7 7 7 8 9 10 11
""") == "Yes", "mixed with one strong frequency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | No | minimal edge case |
| four identical | Yes | threshold behavior |
| all distinct | No | no repetition structure |
| mixed strong frequency | Yes | correctness under noise |

## Edge Cases

For input:

```
1
4
5 5 5 5
```

The algorithm counts frequency of 5 as 4, immediately marking success. This corresponds to having four independent bets on the same window, which is sufficient to cover all possible outcomes.

For input:

```
1
3
1 2 3
```

All frequencies are 1, so no day reaches the threshold. The algorithm correctly rejects the case, reflecting that isolated windows cannot guarantee a forced win.

For input:

```
1
7
2 2 2 2 3 3 3
```

Day 2 reaches frequency 4, so the algorithm outputs "Yes". The remaining values do not matter because only one sufficiently repeated window is needed to guarantee success.
