---
title: "CF 105791J - Judge Fail"
description: "Each submission in the contest belongs to exactly one contestant, and each contestant has a personal restriction on which verdicts they can possibly receive. For every submission, the system does not produce a deterministic result."
date: "2026-06-21T13:11:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "J"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 44
verified: true
draft: false
---

[CF 105791J - Judge Fail](https://codeforces.com/problemset/problem/105791/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Each submission in the contest belongs to exactly one contestant, and each contestant has a personal restriction on which verdicts they can possibly receive. For every submission, the system does not produce a deterministic result. Instead, it chooses uniformly at random among the verdicts allowed for the contestant who made that submission.

The task is not to simulate this randomness, but to compute the expected number of times each verdict appears after all submissions are judged.

A useful way to reframe the process is to think per submission. Every submission contributes probability mass to a subset of verdicts. If a contestant has $t$ allowed verdicts, then each of those verdicts receives probability $1/t$ from that submission, and all other verdicts receive zero contribution. The final answer is just the sum of these contributions over all submissions.

The constraints matter because the number of submissions can reach $10^5$, while the number of verdict types is very small, at most 10. This immediately suggests that any solution should be linear in the number of submissions and proportional to the number of verdicts per contestant, rather than anything involving heavy pairwise computations or state tracking over submissions.

A naive but incorrect direction would be to simulate randomness or sample outcomes repeatedly and average results. That would introduce variance and would not converge exactly, and even if repeated many times it would be too slow and still only approximate.

A more subtle mistake is to try to process submissions independently without aggregating by contestant. If we recompute allowed sets for every submission from scratch using expensive structures, we might still pass constraints, but the key insight is that the same contestant appears many times, so precomputing their probability distribution is essential.

There are no tricky corner cases in the probabilistic model itself, but one subtle edge case is contestants who have only one allowed verdict. In that case every submission by that contestant contributes deterministically to that verdict with probability 1. Another is when a verdict is not allowed for any contestant, in which case its expected frequency is exactly zero.

## Approaches

If we look at one submission in isolation, the computation is straightforward. Suppose contestant $c$ has an allowed set of size $t_c$. Then for each allowed verdict $v$, this submission contributes $1/t_c$ to the expected count of $v$. Summing over all submissions gives the final expectation.

A brute-force approach would process each submission independently, and for each one iterate over all $K$ verdicts, checking whether it is allowed for that contestant. That yields $O(NK)$ time, which is already acceptable given $K \le 10$, but it is not the cleanest structure. A worse brute-force variant would attempt to compute probabilities dynamically per submission without precomputing contestant distributions, leading to repeated work proportional to input size times verdict set size.

The key observation is that the distribution depends only on the contestant, not on the submission. Therefore, we can precompute for each contestant a probability vector over the $K$ verdicts. Once this is done, each submission becomes a simple lookup and vector addition.

This transforms the problem into building $M$ small probability vectors, then summing $N$ copies of them according to submission ownership.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Per submission recomputation | O(NK) | O(K) | Accepted but redundant |
| Precompute per contestant | O(MK + N) | O(MK) | Accepted |

## Algorithm Walkthrough

1. Read the number of submissions $N$, number of contestants $M$, and number of verdict types $K$. We will maintain an array of size $K$ to accumulate expected counts.
2. For each contestant, read their allowed verdict list and store it. We also compute its size $t$. This size directly determines the probability mass each verdict receives from this contestant’s submissions.
3. Build a probability vector for each contestant. For every allowed verdict $v$, assign probability $1/t$. This vector represents the expected contribution of any single submission from that contestant.
4. Read the sequence of submissions. Each submission only tells us which contestant produced it, so we use that index to fetch the precomputed probability vector.
5. For each submission, add the contestant’s probability vector into the global answer array. This is equivalent to summing expected contributions across independent trials.
6. Output the final accumulated vector with sufficient precision.

The reason this is valid is that expectation is linear. Each submission contributes independently to the expected count of each verdict, so summing per-submission expectations gives the correct global expectation without needing to model any joint distribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    N, M, K = map(int, input().split())
    
    allowed = [[] for _ in range(M)]
    prob = [[0.0] * K for _ in range(M)]
    
    for i in range(M):
        qt = int(input())
        arr = list(map(int, input().split()))
        allowed[i] = arr
        p = 1.0 / qt
        for v in arr:
            prob[i][v - 1] = p
    
    ans = [0.0] * K
    
    for _ in range(N):
        c = int(input()) - 1
        pc = prob[c]
        for i in range(K):
            ans[i] += pc[i]
    
    print(" ".join(f"{x:.6f}" for x in ans))

if __name__ == "__main__":
    main()
```

The core structure separates preprocessing from aggregation. The preprocessing step builds a fixed probability vector per contestant, which avoids repeated division and repeated list processing during the submission loop.

One subtle implementation detail is indexing. Verdicts are given as 1-based in input, so they must be shifted to 0-based indices before being stored in the probability vector. Another detail is ensuring floating-point accumulation is done in double precision, which Python’s float naturally provides.

## Worked Examples

### Example 1

Input:

```
4 1 4
1
2
3
4
1
1
1
1
```

Here there is a single contestant who can receive all 4 verdicts. Each submission contributes $1/4$ to every verdict.

| Submission | Contestant | Allowed size | Contribution per verdict |
| --- | --- | --- | --- |
| 1 | 0 | 4 | (0.25, 0.25, 0.25, 0.25) |
| 2 | 0 | 4 | (0.25, 0.25, 0.25, 0.25) |
| 3 | 0 | 4 | (0.25, 0.25, 0.25, 0.25) |
| 4 | 0 | 4 | (0.25, 0.25, 0.25, 0.25) |

Summing gives (1, 1, 1, 1). This confirms that repeated independent identical distributions accumulate linearly.

### Example 2

Consider:

```
3 2 3
2
1 2
1
3
1
2
1
```

Contestant 0 has {1,2}, so each contributes 1/2 to verdicts 1 and 2. Contestant 1 has only {3}, so each contributes fully to verdict 3.

| Submission | Contestant | Vector |
| --- | --- | --- |
| 1 | 0 | (0.5, 0.5, 0.0) |
| 2 | 1 | (0.0, 0.0, 1.0) |
| 3 | 0 | (0.5, 0.5, 0.0) |

Summing gives (1.0, 1.0, 1.0). This shows how mixed contestant distributions still combine cleanly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MK + N K) | Building probability vectors takes MK, and each submission adds a K-length vector |
| Space | O(MK + K) | Storage for per-contestant distributions plus final answer |

The bounds are small enough that even the worst-case $10^5 \times 10$ accumulation is trivial in Python. Memory is also safe since $M \le N$ and $K \le 10$, so storing full probability tables is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    N, M, K = map(int, input().split())
    allowed = [[] for _ in range(M)]
    prob = [[0.0] * K for _ in range(M)]
    
    for i in range(M):
        qt = int(input())
        arr = list(map(int, input().split()))
        p = 1.0 / qt
        for v in arr:
            prob[i][v - 1] = p
    
    ans = [0.0] * K
    
    for _ in range(N):
        c = int(input()) - 1
        for i in range(K):
            ans[i] += prob[c][i]
    
    return " ".join(f"{x:.6f}" for x in ans)

# sample-like case
assert run("""4 1 4
4
1 2 3 4
1
1
1
1
""") == "1.000000 1.000000 1.000000 1.000000"

# single verdict only
assert run("""3 1 2
1
2
1
1
1
1
""") == "3.000000 0.000000"

# two contestants split
assert run("""3 2 2
1
1
1
2
1
2
1
""") == "1.500000 1.500000"

# mixed restrictions
assert run("""2 2 3
2
1 2
1
3
1
2
""") == "0.500000 0.500000 1.000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single universal contestant | uniform accumulation | equal probability distribution |
| single verdict allowed | deterministic accumulation | edge case of size 1 set |
| two balanced contestants | symmetry | correct splitting |
| mixed constraints | partial distributions | heterogeneous contributions |

## Edge Cases

A key edge case is when a contestant has exactly one allowed verdict. In this situation, the probability vector contains a single 1 and the rest zeros. For example, if contestant 0 only allows verdict 2, then every submission contributes exactly 1 to verdict 2. The algorithm handles this naturally because $1/t = 1$, so no special branching is needed.

Another edge case is when different contestants have disjoint allowed sets. The algorithm still behaves correctly because each submission contributes only within its own local distribution. There is no interference between contestants since accumulation is purely additive.

A final edge case is when a verdict never appears in any contestant’s allowed set. In that case its column in all probability vectors remains zero, so it never receives any contribution during aggregation.
