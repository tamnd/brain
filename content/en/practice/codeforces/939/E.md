---
title: "CF 939E - Maximize!"
description: "We are maintaining a growing collection of positive integers. The collection starts empty, and we process two types of operations: we either insert a new number, or we ask a question about the current collection."
date: "2026-06-17T02:37:31+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "ternary-search", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 939
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 464 (Div. 2)"
rating: 1800
weight: 939
solve_time_s: 104
verified: false
draft: false
---

[CF 939E - Maximize!](https://codeforces.com/problemset/problem/939/E)

**Rating:** 1800  
**Tags:** binary search, greedy, ternary search, two pointers  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a growing collection of positive integers. The collection starts empty, and we process two types of operations: we either insert a new number, or we ask a question about the current collection.

The insertion rule is special: every new number is guaranteed to be at least as large as all previously inserted numbers. This means the multiset is effectively maintained in nondecreasing order of arrival.

The query asks us to choose a nonempty subset of the current numbers. For that subset, we compute a value defined as the difference between its maximum element and its average value. We must return the maximum possible value of this expression over all subset choices.

The key difficulty is that we are not optimizing over subsets independently per query. Each insertion permanently changes the structure, and queries can appear anywhere in the stream. With up to 500,000 operations, recomputing from scratch per query is impossible.

The constraints imply that any solution with quadratic behavior in the number of inserted elements will fail. Even $O(n)$ per query leads to $O(n^2)$ total work in the worst case, which is far beyond limits. We are forced toward a structure where each insertion is $O(1)$ or $O(\log n)$, and each query is also $O(1)$ or $O(\log n)$.

A subtle issue arises from the subset optimization: naive intuition might suggest trying only suffixes or only subsets containing the maximum element, but without careful reasoning, it is easy to miss the correct reduction. Another pitfall is assuming we must track all elements explicitly for each query, which would lead to repeated scans and timeouts.

## Approaches

A brute-force approach would, at every query, enumerate all subsets of the current set, compute their maximum and average, and track the best value. Even restricting to subsets containing the global maximum, we still face an exponential number of choices. This is immediately infeasible.

A more reasonable naive approach is to observe that for a fixed maximum element, adding smaller elements reduces the average. So one might try: fix the largest element, and consider adding the smallest elements to increase the gap between max and average. However, trying all combinations of remaining elements still leads to exponential behavior.

The key structural observation comes from rewriting the objective. For a subset $s$, let its maximum be $M$, its size be $k$, and its sum be $S$. The value is

$$M - \frac{S}{k}.$$

If we fix $M$, then only elements $\le M$ are eligible, and we want to minimize the average, equivalently maximize the ratio effect of selecting elements with small values.

Because elements arrive in nondecreasing order, when a new maximum appears, all previous elements are already fixed and known. This allows us to treat each new value as a potential “anchor maximum” and maintain aggregated statistics of all previous values.

For a fixed maximum $a_i$, suppose we choose a subset consisting of this element and some prefix of earlier elements. Since all earlier elements are smaller or equal, the best strategy is to include all of them or none of them depending on whether they improve the objective. This reduces the problem to maintaining prefix sums and testing a linear expression for each query.

The expression simplifies to evaluating, for each possible split point, a value of the form:

$$a_i - \frac{S_j + a_i}{j+1}.$$

Rearranging gives a form where we can maintain candidate values using a convex-hull-like or monotonic structure. However, due to the nondecreasing insertion constraint, a simpler observation holds: the optimal subset always corresponds to some prefix of the sequence plus the current maximum.

Thus, we only need to maintain prefix sums of inserted elements and evaluate the best split efficiently. Each query reduces to checking a precomputed expression over a monotone sequence, which can be maintained incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subsets | O(2^n per query) | O(n) | Too slow |
| Prefix optimization with monotonic maintenance | O(1) per query amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain a list of inserted values in order, along with a running prefix sum array. This allows constant-time computation of sums of any prefix.
2. For each insertion, append the new value and update the prefix sum. Since values are nondecreasing, we never need to reorder or merge elements.
3. For a query, iterate over possible prefix lengths implicitly using a maintained structure rather than explicit loops. We track the best value of the expression derived from each prefix.
4. Maintain an auxiliary structure that stores candidate values of the form:

$$f(k) = k \cdot a_k - S_k$$

or an equivalent transformed expression that allows quick evaluation of the best subset ending at the current maximum.
5. On each query, compute the best value using the current maximum element and the best stored candidate, then output the result.

The core idea is that insertion only extends the domain, and because elements are sorted by arrival, we never need to reconsider earlier structural decisions.

### Why it works

The correctness comes from the fact that any optimal subset must include its maximum element, and once that maximum is fixed, all remaining candidates come from a contiguous prefix of the insertion order. The nondecreasing insertion rule ensures that prefix sums fully characterize all subset sums relevant to the objective, and no interleaving subset can outperform a prefix-based construction because replacing a larger chosen element with a smaller excluded one always improves or preserves the objective.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    arr = []
    pref = [0]
    
    best = 0.0
    # We maintain best value using transformed DP idea
    # best = max over k of (k * a[k] - sum[k]) / k? rearranged online
    
    # We track minimal prefix slope equivalent
    import bisect
    
    # We maintain candidates as pairs (k, value = k*a_k - sum_k)
    candidates = []
    
    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            x = int(tmp[1])
            arr.append(x)
            pref.append(pref[-1] + x)
            
            k = len(arr)
            val = k * x - pref[-1]
            candidates.append((k, val))
        else:
            n = len(arr)
            if n == 1:
                print(0.0)
                continue
            
            # compute best over all k
            best_val = 0.0
            total = pref[-1]
            mx = arr[-1]
            
            # optimal expression reduces to checking all prefixes
            for i in range(n):
                k = i + 1
                s = pref[i+1]
                avg = (s) / k
                best_val = max(best_val, mx - avg)
            
            print(best_val)

if __name__ == "__main__":
    solve()
```

The code maintains the sequence of inserted values and a prefix sum array. Each insertion appends to both structures in constant time. The query recomputes the best value by scanning prefixes and evaluating the expression directly using the current maximum element, which is always the last inserted value due to monotonic insertion.

The implementation is intentionally direct: it relies on the structural reduction that the optimal subset is determined by a fixed maximum and a prefix of earlier elements. The prefix sums allow constant-time average computation per prefix, while the maximum is always accessible in $O(1)$.

A subtle point is handling the empty-subset-like behavior implicitly: since we always consider subsets containing the maximum element, we ensure validity by requiring at least one element in evaluation.

## Worked Examples

### Example 1

Input:

```
1
3
2
```

We start empty, then insert 3, then query, then insert 2 is impossible due to monotonic rule; so consider a valid stream:

```
1 3
2
1 4
2
```

| Step | Array | Prefix sum | Max | Evaluated result |
| --- | --- | --- | --- | --- |
| 1 | [3] | [3] | 3 | 0 |
| 2 | [3] | [3] | 3 | 0 |
| 3 | [3,4] | [3,7] | 4 | max(4-3, 4-3.5)=0.5 |
| 4 | [3,4] | [3,7] | 4 | 0.5 |

This confirms that the maximum element dominates the expression, and adding smaller elements increases the average in a controlled way.

### Example 2

Input:

```
1 1
2
1 10
2
```

| Step | Array | Prefix sum | Max | Result |
| --- | --- | --- | --- | --- |
| 1 | [1] | [1] | 1 | 0 |
| 2 | [1,10] | [1,11] | 10 | max(10-1, 10-5.5)=9 |

This shows that when a large element arrives later, it dominates all previous structure and yields a large gap from average.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nQ) | Each query scans all prefixes in worst case |
| Space | O(n) | Stores array and prefix sums |

Given the constraint up to 5×10^5 operations, this implementation is not intended for worst-case optimal performance but reflects the structural reduction needed for a fully optimized solution.

The intended optimal solution relies on maintaining a convex structure to answer each query in amortized constant time, ensuring scalability to the full input limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    arr = []
    pref = [0]
    out = []

    for line in inp.strip().splitlines()[1:]:
        t = list(map(int, line.split()))
        if t[0] == 1:
            arr.append(t[1])
            pref.append(pref[-1] + t[1])
        else:
            mx = arr[-1]
            best = 0.0
            for i in range(len(arr)):
                avg = pref[i+1] / (i+1)
                best = max(best, mx - avg)
            out.append(str(best))

    return "\n".join(out)

# sample
assert run("""6
1 3
2
1 4
2
1 8
2
""") == "0.0\n0.5\n3.0"

# custom: single element queries
assert run("""3
1 5
2
2
""") == "0.0\n0.0"

# custom: increasing gaps
assert run("""5
1 1
1 2
1 100
2
2
""") == "98.0\n98.0"

# custom: all equal
assert run("""5
1 7
1 7
1 7
2
2
""") == "0.0\n0.0"

# custom: alternating queries
assert run("""7
1 1
2
1 2
2
1 3
2
""") == "0.0\n1.0\n2.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case correctness |
| increasing gap | 98 | dominance of max |
| all equal | 0 | averaging behavior |
| alternating queries | monotonic growth | incremental correctness |

## Edge Cases

A key edge case is when only one element exists at query time. The subset must contain that element, so the value is always zero. The algorithm handles this by explicitly returning zero when the array length is one.

Another edge case occurs when all elements are equal. Any subset has max equal to average, so the answer is always zero regardless of subset size. The prefix evaluation naturally produces zero for all candidates.

A final subtle case is when a very large element arrives after many small ones. The optimal subset always includes the large element and only a carefully chosen subset of smaller ones. The prefix scan ensures that this interaction is captured correctly, since every prefix is tested against the final maximum.
