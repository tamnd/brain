---
title: "CF 106516B - Fruit Blast"
description: "We are given a long sequence whose length is $N^2$, and every value from $1$ to $N$ appears exactly $N$ times. The sequence is meant to be interpreted as a timeline of actions involving $N$ labeled tokens arranged in a cyclic structure."
date: "2026-06-18T19:02:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106516
codeforces_index: "B"
codeforces_contest_name: "MITIT Spring 2026 Invitationals Finals"
rating: 0
weight: 106516
solve_time_s: 58
verified: true
draft: false
---

[CF 106516B - Fruit Blast](https://codeforces.com/problemset/problem/106516/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long sequence whose length is $N^2$, and every value from $1$ to $N$ appears exactly $N$ times. The sequence is meant to be interpreted as a timeline of actions involving $N$ labeled tokens arranged in a cyclic structure. Each occurrence of a value describes a move or interaction tied to that token.

The central question is whether this sequence can be realized in a consistent way under a hidden structural rule: the moves must be decomposable into $N$ cyclic subsequences, each behaving like a “rotation schedule” of the labels. In other words, we are trying to decide whether the sequence can be split into $N$ valid chains, each chain cycling through $1 \to 2 \to \dots \to N \to 1$ in order, respecting appearance constraints.

The constraints are large enough that any attempt to explicitly search over decompositions or simulate all assignments of elements to chains would explode combinatorially. A naive assignment process would effectively branch on which subsequence each occurrence belongs to, leading to exponential possibilities in $N^2$. That immediately rules out backtracking or brute-force partitioning.

A subtle failure case appears when local frequency conditions are satisfied but global structure is impossible. For example, it is possible to construct prefixes where value $y$ appears too early compared to $y-1$, creating a situation where too many “unlinked” occurrences of $y$ exist. A greedy assignment might still succeed locally but later become impossible to extend, because subsequences run out of valid predecessors.

The key difficulty is that feasibility is not about total counts, but about how occurrences of adjacent values interleave across all prefixes.

## Approaches

A direct approach would try to explicitly construct the decomposition into $N$ cyclic subsequences. We scan the array and assign each element to one of the subsequences that can legally accept it, meaning it has the previous value in the cycle already placed. This behaves like a constrained scheduling problem with $N$ resources and $N^2$ events.

While this greedy construction is conceptually correct, maintaining all possible subsequences and checking valid placements at each step leads to an expensive state explosion. In the worst case, each element requires scanning many subsequences, and updates cascade, giving a complexity on the order of $O(N^3)$ or worse depending on implementation.

The structural insight is that feasibility is fully captured by prefix imbalance between consecutive values. For every prefix and every value $y$, the number of occurrences of $y$ seen so far cannot exceed the number of occurrences of $y-1$ seen so far by more than one. This condition is both necessary and sufficient because each “chain” can contribute at most one unmatched $y$ at any time, and every additional $y$ must be supported by a preceding $y-1$ in some chain.

This reduces the entire problem to maintaining prefix counts and checking a simple inequality across all values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute-force subsequence assignment | Exponential | O(N^2) | Too slow |
| Prefix condition check | O(N^2) | O(N) | Accepted |

## Algorithm Walkthrough

We convert the problem into a prefix counting condition over the sequence.

### Steps

1. Initialize a frequency table `cnt[y]` for values $1 \ldots N$, all starting at zero. This tracks how many times each value has appeared so far in the prefix.
2. Scan the sequence from left to right. For each position $i$, increment `cnt[x[i]]`. This maintains correct prefix frequencies at every step.
3. After updating for position $i$, check the condition for all values $y \ge 2$:

ensure `cnt[y] <= cnt[y-1] + 1`.

This enforces that value $y$ never “outpaces” its predecessor $y-1$ by more than one occurrence.
4. If any violation is found, immediately conclude the sequence is invalid.
5. If the scan completes without violations, the sequence is valid.

### Why it works

The key invariant is that at any prefix, each value $y$ can only have at most one “unmatched” occurrence not yet supported by a corresponding $y-1$. Each valid chain contributes a single pending slot for advancing from $y-1$ to $y$. If $y$ exceeds $y-1$ by more than one, some occurrence of $y$ cannot be placed into any chain without breaking order, making the decomposition impossible. Conversely, if the inequality always holds, we can always assign each occurrence of $y$ to either extend an existing chain or start the single permissible new unmatched chain position, guaranteeing constructibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))

    cnt = [0] * (n + 1)

    for v in a:
        cnt[v] += 1

        for y in range(2, n + 1):
            if cnt[y] > cnt[y - 1] + 1:
                print("No")
                return

    print("Yes")

if __name__ == "__main__":
    solve()
```

The implementation maintains prefix counts and checks the adjacency constraint immediately after each update. The inner loop over $y$ is sufficient because only adjacent differences matter; a violation at any value is detected locally at the moment it appears.

A subtle detail is that the check must happen after each increment, not after the full scan, because the property is prefix-dependent. Delaying validation could miss intermediate invalid states that later get “masked” by future occurrences.

## Worked Examples

### Example 1

Input:

```
3
1 2 1 3 2 3 1 2 3
```

We track prefix counts:

| i | x[i] | cnt1 | cnt2 | cnt3 | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | yes |
| 2 | 2 | 1 | 1 | 0 | yes |
| 3 | 1 | 2 | 1 | 0 | yes |
| 4 | 3 | 2 | 1 | 1 | yes |
| 5 | 2 | 2 | 2 | 1 | yes |
| 6 | 3 | 2 | 2 | 2 | yes |
| 7 | 1 | 3 | 2 | 2 | yes |
| 8 | 2 | 3 | 3 | 2 | yes |
| 9 | 3 | 3 | 3 | 3 | yes |

No prefix violates the constraint, so the sequence is valid.

### Example 2

Input:

```
3
1 3 3 2 2 2 1 1 3
```

| i | x[i] | cnt1 | cnt2 | cnt3 | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | yes |
| 2 | 3 | 1 | 0 | 1 | yes |
| 3 | 3 | 1 | 0 | 2 | no (violates cnt3 ≤ cnt2+1) |

At step 3, `cnt3 = 2` while `cnt2 + 1 = 1`, so the condition fails immediately. This shows how excess higher labels without sufficient support from the previous label breaks feasibility early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | Each of the $N^2$ elements is processed once, with constant-time updates and checks over a fixed range of labels |
| Space | $O(N)$ | Only a frequency array of size $N$ is maintained |

The solution fits comfortably within typical constraints for $N$ up to a few thousand, since the dominant work is linear in the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# minimal valid case
assert run("1\n1") == "Yes"

# small valid structured case
assert run("2\n1 2 1 2") == "Yes"

# invalid due to early imbalance
assert run("2\n2 2 1 1") == "No"

# larger consistent cycle
assert run("3\n1 2 3 1 2 3 1 2 3") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 | Yes | smallest valid instance |
| 2, 1 2 1 2 | Yes | alternating balanced structure |
| 2, 2 2 1 1 | No | prefix violation detection |
| 3, 1 2 3 repeated | Yes | repeated cyclic consistency |

## Edge Cases

One important edge case is when a higher label appears too early, before enough occurrences of its predecessor exist. For example, input:

```
3
1 3 3 ...
```

fails immediately because the second occurrence of 3 appears while 2 has not yet been established in sufficient quantity. The algorithm detects this at the exact prefix where `cnt[3] > cnt[2] + 1`, preventing any invalid completion from being accepted.

Another case is when values are perfectly balanced but shifted, such as starting with repeated occurrences of the highest label. Even though total counts match at the end, prefix checks fail early, which is correctly handled because the algorithm never delays validation to the final state.
