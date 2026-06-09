---
title: "CF 1881B - Three Threadlets"
description: "We are given three positive integers, each representing the length of a thread. In one move, we pick a single thread and split it into two smaller threads with integer lengths, both strictly positive, and their sum equal to the original length."
date: "2026-06-08T22:39:37+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1881
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 903 (Div. 3)"
rating: 900
weight: 1881
solve_time_s: 87
verified: true
draft: false
---

[CF 1881B - Three Threadlets](https://codeforces.com/problemset/problem/1881/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three positive integers, each representing the length of a thread. In one move, we pick a single thread and split it into two smaller threads with integer lengths, both strictly positive, and their sum equal to the original length. We are allowed at most three such splits in total across all threads. After performing some sequence of splits, we want all resulting threads to have exactly the same length.

The key output is a feasibility check: for each test case, we must decide whether it is possible to end up with a collection of equal-length pieces using no more than three splits.

The constraints are large in terms of test count, up to 10^4 cases, while each test case is constant size. This immediately rules out any approach that simulates arbitrary splitting configurations or searches over states, since even a moderately branching BFS over partitions would explode. Each test must be answered in constant or near-constant time.

A subtle point is that the number of pieces is not fixed. Every operation increases the total number of threadlets by one, so after at most three operations, we can have at most six pieces total. This hard cap on final state size is what makes a direct combinational reasoning possible.

Edge cases that tend to break naive thinking include situations where one value is much larger than others, such as (1, 1, 1000000000), or cases where two values are already equal but the third is slightly off, such as (5, 5, 6). These often tempt greedy “equalize by splitting largest” strategies, but those ignore the strict operation limit and the integer constraint on segment sizes.

## Approaches

A brute-force idea would be to simulate all possible ways of performing up to three cuts. Each cut selects a current segment and splits it into two positive integers. The branching factor grows with the length of segments, since a segment of length L has L−1 possible splits. Even with only three operations, this creates a large tree of possibilities, and many states repeat in different orders of cuts. The total number of configurations is far beyond what can be enumerated across 10^4 test cases.

The key observation is that we do not actually care about the intermediate configuration, only whether a uniform final length exists. If the final length is x, then every original segment must be decomposed into pieces of length x. This turns the problem into checking whether each number can be expressed as a sum of equal parts, with the additional restriction that we can only introduce at most three cuts total.

This restriction is extremely tight: each cut increases the number of pieces by exactly one, so starting from three segments, we can end with at most six segments. Therefore, the final configuration can have size 3, 4, 5, or 6. Since all pieces must have equal length, the total sum S must satisfy S mod k = 0 for k in {3,4,5,6}, where k is the final number of pieces. For each valid k, we check whether each original segment can be split into integers of size S/k, and whether the total number of cuts required does not exceed 3.

For a fixed target length x, a segment of length a contributes a cuts equal to (a/x − 1) if a is divisible by x, otherwise it is impossible. Summing this over all three segments gives the total number of operations needed. The answer is YES if there exists some feasible k in [3,6] that yields a valid x and requires at most 3 cuts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all splits | Exponential | High | Too slow |
| Try all final piece counts (3-6) with divisibility check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed by testing every possible final number of pieces.

1. Compute the total sum S of the three thread lengths. This is the total length that must be evenly divided among all final equal pieces.
2. For each candidate number of final pieces k from 3 to 6, check whether S is divisible by k. If not, this k cannot produce equal segments and is discarded.
3. For each valid k, compute the target piece length x = S / k. This is the only possible length of each final thread.
4. For each original segment a, check whether a is divisible by x. If not, this configuration is impossible because we cannot cut into fractional pieces.
5. If divisible, compute how many cuts are needed inside that segment as a / x − 1. This comes from the fact that splitting a into m equal chunks requires exactly m − 1 cuts.
6. Sum these cut counts across all three segments. If the total is at most 3, then this configuration is achievable, so we can immediately return YES.
7. If no k in [3,6] works, return NO.

### Why it works

Every operation increases the number of segments by exactly one, so starting from three segments we can only reach configurations with at most six segments. This bounds the final number of equal pieces to a small constant range. For a fixed final segmentation size, the structure of cuts inside each original segment is forced: equal pieces imply a unique target length, and each segment independently determines how many cuts it contributes. Since segments do not interact except through the shared final length constraint, checking feasibility reduces to summing independent costs and verifying the global cut budget.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(a, b, c):
    total = a + b + c

    for k in range(3, 7):
        if total % k != 0:
            continue
        x = total // k

        cuts = 0
        ok = True

        for v in (a, b, c):
            if v % x != 0:
                ok = False
                break
            cuts += v // x - 1

        if ok and cuts <= 3:
            return True

    return False

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    print("YES" if possible(a, b, c) else "NO")
```

The implementation directly follows the observation that only final partition sizes from 3 to 6 are relevant. The loop over k enumerates all possible end states, and for each one we verify whether it can be constructed with at most three cuts.

The computation of cuts uses the identity that splitting a segment into m equal parts requires exactly m−1 operations. This avoids simulating the splitting process explicitly. The boolean flag ensures we discard invalid decompositions early when divisibility fails.

## Worked Examples

Consider the case (6, 3, 3). The total sum is 12.

| k | x = S/k | Valid divisibility | Cuts from 6 | Cuts from 3 | Total cuts | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 4 | yes | 6/4 invalid | - | - | skip |
| 4 | 3 | yes | 6→3,3 = 1 | 3→3 = 0 | 1 | YES |
| 5 | - | no | - | - | skip |  |
| 6 | 2 | yes | 6→2,2,2 = 2 | 3 invalid | - | skip |

This demonstrates that k = 4 works because we can split 6 into two parts of 3 (one cut), while the others already match or require no cuts.

Now consider (1, 3, 2). The sum is 6.

| k | x | Valid | Cuts from 1 | Cuts from 3 | Cuts from 2 | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 2 | yes | impossible | 3→2+1 (1) | 2→2 (0) | invalid |
| 4 | 1.5 | no | - | - | - | skip |
| 5 | 1.2 | no | - | - | - | skip |
| 6 | 1 | yes | 0 | 2 | 1 | 3 YES |

This confirms that the algorithm correctly finds a valid configuration only when total cuts stay within the allowed limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test | Only four candidate values of k are checked, each with constant work |
| Space | O(1) | No auxiliary structures are used |

The constant number of operations per test case ensures the solution easily handles 10^4 inputs within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        a, b, c = map(int, input().split())
        total = a + b + c
        for k in range(3, 7):
            if total % k != 0:
                continue
            x = total // k
            cuts = 0
            ok = True
            for v in (a, b, c):
                if v % x != 0:
                    ok = False
                    break
                cuts += v // x - 1
            if ok and cuts <= 3:
                return "YES"
        return "NO"

    t = int(input())
    return "\n".join(solve() for _ in range(t))

# provided samples (partial check due to brevity)
assert run("1\n1 3 2\n") == "YES"
assert run("1\n5 5 5\n") == "YES"

# custom cases
assert run("1\n1 1 1\n") == "YES"  # already equal
assert run("1\n1 1 100\n") == "NO"  # impossible under 3 cuts
assert run("1\n6 3 3\n") == "YES"  # classic split case
assert run("1\n2 2 8\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | YES | already uniform |
| 1 1 100 | NO | large imbalance cannot be fixed in 3 cuts |
| 6 3 3 | YES | multi-level splitting feasibility |
| 2 2 8 | YES | multiple segments contributing cuts |

## Edge Cases

A case like (1, 1, 100) stresses the limitation that cuts are globally bounded. The algorithm tries all k in [3,6], but for any valid x derived from these k values, the large segment forces too many splits or breaks divisibility, so all candidates fail and the output is NO.

For (6, 3, 3), the correct solution requires recognizing that only one segment needs to be split, and that split produces exactly the right number of pieces without exceeding the operation limit. The algorithm captures this by computing exact per-segment cut counts instead of simulating any sequence.

For already equal inputs like (5, 5, 5), the k = 3 case with x = 5 yields zero cuts, which immediately satisfies the constraint, producing YES without performing any operations.
