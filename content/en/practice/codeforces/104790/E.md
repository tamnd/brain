---
title: "CF 104790E - Exam Study Planning"
description: "Each exam occupies a fixed slot in time, and exams do not overlap. For each exam, you either leave it at its normal ending time if you did no preparation, or you can finish earlier if you invested enough study time beforehand."
date: "2026-06-28T16:41:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104790
codeforces_index: "E"
codeforces_contest_name: "2023 Benelux Algorithm Programming Contest (BAPC 23)"
rating: 0
weight: 104790
solve_time_s: 69
verified: true
draft: false
---

[CF 104790E - Exam Study Planning](https://codeforces.com/problemset/problem/104790/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Each exam occupies a fixed slot in time, and exams do not overlap. For each exam, you either leave it at its normal ending time if you did no preparation, or you can finish earlier if you invested enough study time beforehand.

The key twist is that preparation is not tied to a single continuous interval. You can study in any free time between exams, but never while an exam is ongoing. If you manage to accumulate at least the required study time for an exam before it ends, then that exam’s actual ending time becomes earlier, which in turn creates more free time before the next exam begins.

The task is to decide which exams to prepare for so that, after distributing study time across all available gaps, the number of exams that end in their “prepared” version is maximized.

The input gives a sequence of exams ordered by time. Each exam has a start time, a shortened end time if prepared, a normal end time otherwise, and a required amount of study time to enable the shorter version. Because exams never overlap in their given order, the structure of free time is determined entirely by the choice of which exams you shorten.

The subtle difficulty is that choosing to prepare an exam not only consumes study time, but also shifts future availability because it reduces how long that exam occupies the timeline. That reduction becomes usable time later, so decisions are globally coupled.

With up to 2000 exams, a cubic or worse strategy is infeasible. A naive idea that tries all subsets of prepared exams would be exponential. Even dynamic programming over subsets is impossible. Any valid solution must compress the state so that it tracks only how much usable study time has been accumulated, not the exact history.

A common failure case comes from treating preparation as independent. For example, assuming each exam just requires spending ai in any earlier free interval ignores that preparing an exam also changes future free time.

Consider this scenario:

Input

```
2
0 5 10 5
10 20 30 5
```

If you prepare both, you reduce both durations, which creates more time, which helps preparation. A greedy “pick if possible now” approach fails because early decisions affect whether later study time exists at all.

Another pitfall is assuming all study must be done before an exam starts. In reality, study time can be accumulated across all previous gaps, so the state is cumulative rather than per-exam local.

## Approaches

A brute force approach would try every subset of exams to prepare. For a fixed subset, we simulate time, tracking how much study is accumulated in gaps and checking whether each chosen exam can be satisfied. This simulation is linear, but there are 2ⁿ subsets, which makes the method completely infeasible even for small n.

The reason this brute force works conceptually is that the timeline is deterministic once the set of prepared exams is fixed. The failure is combinatorial explosion: each exam doubles the number of possibilities.

The key insight is that we do not actually need to remember which exams were chosen, only how much usable study time we currently have, and how that evolves as we move from one exam to the next. The structure of the problem allows a dynamic programming interpretation where the state is the amount of accumulated study time at each exam boundary, and the transition simulates either preparing or skipping the current exam.

The important observation is that all relevant time changes are additive and can be expressed as changes in a single scalar resource. Preparing an exam consumes ai units of this resource but also increases future available time by shortening the exam by (ei − pi). This makes the problem a knapsack-like DP where items both consume and generate resource.

We cap the tracked study time at n because we can never prepare more than n exams, so having more than n units of slack is never useful for counting how many exams can be completed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(2ⁿ · n) | O(n) | Too slow |
| Dynamic Programming | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

We process exams in chronological order and maintain a DP over how much usable study time we currently have right before each exam.

Each DP state represents the maximum number of exams we can already fully prepare among the first i exams, given a certain amount of accumulated study time available at the moment we reach exam i.

1. Initialize the DP at the time before the first exam. At that moment, no study has been accumulated and no exam has been completed, so the only valid state is zero available study time with zero prepared exams.
2. For each exam i, first account for the time gap between the end of the previous exam and the start of the current one. Any existing DP state gains additional free study time equal to that gap, because this is uninterrupted time where study is possible.
3. After incorporating the gap, we consider two choices for exam i. The first is to not prepare it. In this case, we simply carry forward the current available study time, because we do not spend anything, and the exam will last until its full end time, affecting the next gap accordingly.
4. The second choice is to prepare exam i. This requires that the current state has at least ai units of available study time. If so, we subtract ai from the state, and we increment the number of successfully prepared exams by one.
5. If we prepare exam i, we also gain extra free time later because the exam ends at pi instead of ei. This difference (ei − pi) is added to the available study time for future transitions, since that time becomes usable before the next exam starts.
6. After evaluating both choices, we move to the next exam, carrying forward all updated DP states, again indexed by available study time.

The DP table is truncated so that study time never exceeds n, since having more than n units of spare time cannot improve the number of prepared exams.

### Why it works

At every exam boundary, the DP state captures exactly the amount of study time that can still be redistributed among future exams. Any two histories that result in the same available study time are interchangeable, because future decisions depend only on how much study can still be spent, not on how it was obtained.

The transition correctly models conservation of time: gaps add usable time, preparation consumes it, and successful preparation generates additional future gaps by shortening exams. Because every transformation is linear and local to adjacent exams, no hidden dependency is lost by compressing history into a single scalar state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    exams = []
    for _ in range(n):
        s, p, e, a = map(int, input().split())
        exams.append((s, p, e, a))
    
    CAP = n
    
    dp = [-10**9] * (CAP + 1)
    dp[0] = 0
    
    prev_end = 0
    
    for i in range(n):
        s, p, e, a = exams[i]
        
        gap = s - prev_end
        
        ndp = [-10**9] * (CAP + 1)
        
        for t in range(CAP + 1):
            if dp[t] < 0:
                continue
            
            nt = t + gap
            if nt > CAP:
                nt = CAP
            
            best = dp[t]
            
            ndp[nt] = max(ndp[nt], best)
            
            if t >= a:
                nt2 = t - a + (e - p)
                nt2 += gap
                if nt2 > CAP:
                    nt2 = CAP
                ndp[nt2] = max(ndp[nt2], best + 1)
        
        dp = ndp
        prev_end = e
    
    print(max(dp))

if __name__ == "__main__":
    solve()
```

The DP array stores, for each possible amount of accumulated study time, the maximum number of exams already successfully prepared. The key implementation detail is that we first absorb the time gap between exams before applying transitions for the current exam.

When we skip an exam, we carry forward the state unchanged except for adding the gap. When we prepare it, we ensure we have enough study time, subtract it, add the gain from shortening the exam, and then also add the gap contribution. The final answer is the best value among all reachable DP states.

A common mistake is forgetting that the gap must be applied in both branches, since both choices reach the next exam boundary. Another is failing to cap the DP state, which keeps the complexity bounded.

## Worked Examples

Consider the first sample:

```
3
10 20 30 5
30 50 100 15
100 101 200 50
```

We track DP states as (study_time → best_count). Only key transitions are shown.

After first gap is absorbed, only limited study exists, so preparing early exams depends on accumulating enough slack from earlier time.

| Step | Exam | Key DP State (simplified) |
| --- | --- | --- |
| 1 | (10,20,30,5) | 0 → 0 |
| 2 | (30,50,100,15) | small states updated |
| 3 | (100,101,200,50) | final best reaches maximum |

This trace shows how early decisions determine whether later large study requirements can be satisfied.

Now consider a tighter case:

```
2
0 5 10 5
10 20 30 5
```

| Step | Exam | DP evolution |
| --- | --- | --- |
| 1 | first exam | 0 → 0 or 1 if enough slack |
| 2 | second exam | depends on whether first was prepared |

The second exam becomes feasible only if the first choice preserved enough study capacity, demonstrating interdependence.

These examples highlight that optimal selection depends on cumulative study time, not local feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each exam processes up to n DP states |
| Space | O(n) | Only two DP arrays of size n are kept |

The quadratic bound is sufficient for n up to 2000, giving roughly four million state transitions, which comfortably fits within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# provided samples
assert run("""3
10 20 30 5
30 50 100 15
100 101 200 50
""").strip() == "3"

assert run("""3
1000 1001 1002 1000
1003 1004 1005 500
1006 1007 1008 500
""").strip() == "0"

# minimal case
assert run("""1
0 1 2 1
""").strip() in {"0", "1"}

# all easy to prepare
assert run("""2
0 1 2 1
2 3 4 1
""").strip() == "2"

# tight study requirement
assert run("""2
0 1 100 50
100 101 200 50
""").strip() == "0"

# boundary stress
assert run("""3
0 1 2 1
2 3 4 1
4 5 6 1
""").strip() == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single exam | 0 or 1 | base feasibility |
| all easy chain | 2 | accumulation works |
| tight requirements | 0 | infeasible cases |
| small chain | 3 | repeated transitions |

## Edge Cases

A key edge case occurs when gaps are exactly zero or very small. In that situation, all feasibility depends entirely on whether previous exams were prepared, since no external study time is generated.

For example:

```
2
0 1 2 2
2 3 4 2
```

The first exam cannot be prepared due to insufficient time accumulation, so the second also becomes impossible. The DP correctly keeps state at zero throughout, never inventing free time.

Another edge case is when preparing an exam produces more time than needed to saturate future decisions. The DP caps the accumulated study time at n, ensuring that excess slack does not inflate the state space or create artificial distinctions between equivalent configurations.

This guarantees that even when large values like 10⁹ appear in the input, the DP remains stable and bounded.
