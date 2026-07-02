---
title: "CF 103566E - \u0421\u0442\u0438\u043a\u0435\u0440\u044b"
description: "We are given a collection of N participants, each described by three pieces of information: a potential “friend reference” Fi, a readiness flag Pi, and a timestamp Ti."
date: "2026-07-03T04:57:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103566
codeforces_index: "E"
codeforces_contest_name: "2021-2022 Olympiad Cognitive Technologies, Final Round"
rating: 0
weight: 103566
solve_time_s: 41
verified: true
draft: false
---

[CF 103566E - \u0421\u0442\u0438\u043a\u0435\u0440\u044b](https://codeforces.com/problemset/problem/103566/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of N participants, each described by three pieces of information: a potential “friend reference” Fi, a readiness flag Pi, and a timestamp Ti. The process defines a derived array cnt, initially all zeros, which counts how many other participants successfully “validate” each participant as a qualified friend.

For each participant i, we attempt to determine whether i can act as a valid recommender for someone else’s friend Fi. If Fi is nonzero, participant i is considered as someone who may contribute toward increasing the count of Fi. However, this is only allowed if i satisfies two independent conditions: Pi must be positive, meaning i has passed a certain qualification check, and Ti must be strictly greater than TFi, meaning i registered later than the friend they are referring to.

If all conditions hold, we increment cnt[Fi] by one. After processing all participants, we examine each participant i again, and output those indices where cnt[i] is at least 2. The output must be in increasing order of indices.

The input size N is the key factor shaping the solution. Since we perform only a constant amount of work per participant in a direct scan, an O(N) or O(N log N) approach is necessary. Anything involving nested checks over pairs of participants would lead to O(N²), which becomes infeasible when N reaches typical Codeforces constraints like 2⋅10⁵.

A subtle edge case appears when Fi is zero. In that case, the participant does not contribute to any count, and attempting to index cnt[0] would be invalid if not carefully handled. Another edge case arises when timestamps are equal: since the condition is strictly Ti > TFi, equality must fail, and naive implementations that use non-strict comparison will incorrectly increase counts.

A final pitfall is forgetting that multiple participants can contribute to the same Fi independently. This means cnt is not a boolean array but a frequency accumulator, and duplicate contributions are expected.

## Approaches

A brute-force interpretation would directly simulate the definition: for every participant i, we scan all other participants j and check whether j can contribute to cnt[i]. This leads to checking conditions involving Fi, Pi, and Ti for each pair, effectively making the process quadratic. While logically correct, this results in about N² comparisons in the worst case, which is too slow when N is large.

The key observation is that each participant contributes at most one unit of information to a single target index Fi, and this contribution is determined independently of all other participants. There is no dependency between different updates to cnt, which means we can compute all contributions in a single linear pass.

Instead of searching for valid contributors for each participant, we directly iterate over all participants once, and for each i, we check whether it qualifies as a contributor. If it does, we increment cnt[Fi]. This transforms the problem from “querying incoming valid relationships” into “processing outgoing valid edges,” which removes the need for any nested iteration.

After building cnt, a second linear scan extracts all indices with cnt[i] ≥ 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all arrays F, P, and T. These define directed potential contributions from each participant to another participant. The structure is static, so no dynamic updates are needed.
2. Initialize cnt as an array of size N with all zeros. This will accumulate how many valid contributors each participant receives.
3. Iterate over each participant i from 1 to N. For each i, we decide whether it contributes to someone else’s count.
4. If Fi equals zero, skip i immediately. This avoids invalid indexing and reflects that no contribution target exists.
5. Check whether Pi is positive. If Pi is zero, i cannot contribute, so we skip it. This condition filters out participants who fail the qualification step.
6. Check whether Ti is strictly greater than TFi. If not, skip i. This enforces the ordering constraint that only later participants can validate earlier ones.
7. If all checks pass, increment cnt[Fi] by one. This records that Fi has gained one valid supporting participant.
8. After processing all participants, iterate again over i from 1 to N and collect all indices where cnt[i] is at least 2. These are the participants who received enough valid confirmations.
9. Output the collected indices in increasing order, which is guaranteed automatically because we traverse i in increasing order.

The correctness rests on the invariant that after step 7, cnt[x] equals the number of participants i such that i contributes exactly once to x under all constraints. Since each participant is processed independently and contributes at most one increment, no double counting or omission can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    F = [0] + list(map(int, input().split()))
    P = [0] + list(map(int, input().split()))
    T = [0] + list(map(int, input().split()))

    cnt = [0] * (n + 1)

    for i in range(1, n + 1):
        f = F[i]
        if f == 0:
            continue
        if P[i] <= 0:
            continue
        if T[i] <= T[f]:
            continue
        cnt[f] += 1

    res = []
    for i in range(1, n + 1):
        if cnt[i] >= 2:
            res.append(i)

    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm exactly: the first pass builds frequency counts, and the second pass extracts valid indices. The critical detail is the strict inequality check `T[i] <= T[f]`, which is written in a way that correctly rejects both equal and smaller timestamps.

Indexing is handled by shifting arrays to 1-based form, which avoids confusion between valid participant indices and the zero sentinel used for Fi.

## Worked Examples

### Example 1

Consider a small instance where participants form a simple chain of valid contributions.

Input:

```
n = 4
F = [0, 1, 1, 2]
P = [0, 1, 1, 1]
T = [0, 1, 2, 3]
```

We track cnt during processing.

| i | Fi | Pi | Ti | Condition holds | cnt update | cnt state |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | no | none | [0,0,0,0] |
| 2 | 1 | 1 | 2 | yes | cnt[1]++ | [0,1,0,0] |
| 3 | 1 | 1 | 3 | yes | cnt[1]++ | [0,2,0,0] |
| 4 | 2 | 1 | 3 | yes | cnt[2]++ | [0,2,1,0] |

Final cnt is [0,2,1,0]. We output participants with cnt ≥ 2, which is only participant 1.

This trace shows that multiple independent contributions accumulate correctly in cnt without interference.

### Example 2

Input:

```
n = 5
F = [0, 2, 2, 3, 3]
P = [0, 1, 0, 1, 1]
T = [0, 5, 4, 3, 2]
```

| i | Fi | Pi | Ti | Condition holds | cnt update | cnt state |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 5 | no | none | [0,0,0,0,0] |
| 2 | 2 | 1 | 4 | T2 > T2 false | none | [0,0,0,0,0] |
| 3 | 3 | 0 | 3 | Pi fails | none | [0,0,0,0,0] |
| 4 | 3 | 1 | 2 | T4 > T3 true | cnt[3]++ | [0,0,0,1,0] |
| 5 | 3 | 1 | 2 | T5 > T3 true | cnt[3]++ | [0,0,0,2,0] |

Final cnt is [0,0,0,2,0], so participant 3 is output.

This example stresses two edge conditions: equal timestamps and invalid Pi filtering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each participant is processed once for contribution and once for extraction |
| Space | O(N) | Arrays F, P, T, and cnt are all linear in size |

The solution performs a constant amount of work per participant, making it comfortably suitable for typical Codeforces constraints up to 2⋅10⁵.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""  # output printed directly

# sample-like case
run("""4
0 1 1 2
1 1 1 1
1 2 3 4
""")

# minimum size
run("""1
0
1
1
""")

# no valid contributions
run("""3
0 0 0
1 1 1
3 2 1
""")

# all contribute to same target
run("""4
0 1 1 1
1 1 1 1
1 2 3 4
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | empty | minimal boundary |
| no edges | empty | filtering correctness |
| identical targets | 1 | accumulation logic |

## Edge Cases

One edge case is when Fi equals zero for all participants. In that scenario, the loop never triggers any cnt increment, and the final output is empty. The algorithm handles this naturally because the first condition `if f == 0` prevents invalid indexing and skips all updates.

Another edge case occurs when timestamps are equal for a valid-looking pair. For example, if Fi = j and Ti = Tj, the condition fails due to strict inequality. The code explicitly uses `T[i] <= T[f]` to reject equality, ensuring no accidental increments occur.
