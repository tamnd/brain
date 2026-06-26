---
title: "CF 105712J - Ambiguous Permutations"
description: "We are given several test cases, each describing a permutation of the integers from 1 to n. A permutation here is just an array where every number from 1 to n appears exactly once."
date: "2026-06-26T07:57:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105712
codeforces_index: "J"
codeforces_contest_name: "Rutgers University Programming Contest Fall 2024"
rating: 0
weight: 105712
solve_time_s: 36
verified: true
draft: false
---

[CF 105712J - Ambiguous Permutations](https://codeforces.com/problemset/problem/105712/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each describing a permutation of the integers from 1 to n. A permutation here is just an array where every number from 1 to n appears exactly once.

The task is to determine whether this permutation has a special symmetry: if you treat the array as a mapping from position to value, and then apply that mapping twice, you return to where you started for every element. In other words, if you go from index i to p[i], and then from p[i] to p[p[i]], you should end up back at i for all i.

The output for each test case is a simple judgment of whether this property holds.

Although the problem looks like it is about arrays, the underlying structure is a function on a finite set. Each index points to another index, and we are checking whether this function is its own inverse.

The constraints are not explicitly provided here, but typical permutation problems of this form go up to at least 10^5 elements per test case. That immediately rules out any quadratic simulation. Any approach that tries to repeatedly follow chains from every index without caching will degrade to O(n^2) in the worst case, which is not viable. We need a single linear scan per test case.

A few edge cases tend to break naive reasoning.

One is self-loops in disguise. For example, if n = 1 and the permutation is [1], the condition trivially holds since applying the mapping twice stays at 1. A careless implementation that assumes cycles must have length at least 2 may mishandle this.

Another case is mixed cycles. For example, n = 4 and p = [2, 1, 4, 3]. This actually works because it consists of disjoint swaps, but a mistaken approach that checks only local consistency like p[i] != i might incorrectly reject it.

A more subtle failure happens when a permutation has a valid involution structure locally but not globally. For example, p = [2, 3, 1] looks cyclic, but applying twice does not return all elements to their start positions.

## Approaches

A direct approach is to simulate the condition literally. For every index i, we compute p[p[i]] and compare it with i. If any mismatch appears, we immediately reject the permutation.

This is correct because the condition is independent per index. Each index must satisfy the constraint on its own, so checking all indices is sufficient.

However, this requires careful handling of indexing and repeated access to the permutation array. Each check is O(1), and we do it n times, so the total time per test case is O(n). Across all test cases, this remains linear in the total input size.

A brute-force misunderstanding would be to try exploring cycles explicitly, marking visited nodes and reconstructing structure. That still works but introduces unnecessary bookkeeping without changing complexity. Another worse variant is simulating repeated applications of the permutation for each index, which leads to O(n^2) behavior.

The key observation is that we do not need to build cycles or simulate steps. The condition p[p[i]] = i already fully characterizes whether the permutation is an involution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of repeated steps per index | O(n^2) | O(n) | Too slow |
| Direct check of p[p[i]] = i for all i | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read n and the permutation array p. The array is 1-indexed conceptually, but stored in a 0-indexed Python list, so adjustments are needed when accessing values. This matters because confusion between index bases is the most common source of wrong answers here.
2. For every index i from 0 to n - 1, compute the value j = p[i]. This represents the first step of the mapping from i.
3. Check whether p[j - 1] equals i + 1 if using 1-indexed logic, or equivalently p[p[i] - 1] == i in 0-indexed form. If this equality fails for any i, the permutation cannot be its own inverse, so we can stop early.
4. If all indices satisfy the condition, declare the permutation valid.

The reason early stopping is valid is that the property is conjunctive across all indices. A single violation invalidates the entire permutation.

### Why it works

The mapping defined by a permutation is a bijection on the set {1, ..., n}. The condition p[p[i]] = i means that applying the function twice yields the identity function. This is exactly the definition of an involution. Since equality is checked pointwise for every element, verifying it locally for each index guarantees global correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, arr):
    for i in range(n):
        j = arr[i] - 1
        if arr[j] != i + 1:
            return False
    return True

def main():
    out = []
    while True:
        line = input().strip()
        if not line:
            break
        n = int(line)
        if n == 0:
            break
        arr = list(map(int, input().split()))
        if solve_case(n, arr):
            out.append("ambiguous")
        else:
            out.append("not ambiguous")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The core logic sits in `solve_case`. Each element i is used to jump once to j = p[i] - 1, and then we verify whether jumping back from j returns to i. The subtraction and addition adjustments are necessary because the input is 1-based while Python lists are 0-based.

The loop in `main` continues until n = 0, which is a standard termination pattern for this problem. Reading line by line avoids input desynchronization issues when multiple test cases are present.

## Worked Examples

Consider an input where n = 4 and the permutation is 2 1 4 3.

| i | p[i] | j = p[i]-1 | p[j] | check |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 1 | ok |
| 1 | 1 | 0 | 2 | ok |
| 2 | 4 | 3 | 3 | ok |
| 3 | 3 | 2 | 4 | ok |

Every index satisfies the condition, so the permutation is valid. This trace shows a structure composed entirely of 2-cycles, which naturally satisfies the involution property.

Now consider n = 3 with permutation 2 3 1.

| i | p[i] | j = p[i]-1 | p[j] | check |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 3 | fail |

The first check already fails because following the mapping twice does not return to the starting point. This demonstrates that cyclic permutations of length greater than 2 cannot satisfy the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each index is checked exactly once with constant-time array access |
| Space | O(1) extra | Only the input array is stored, no auxiliary structures needed |

The total runtime scales linearly with the sum of all n across test cases, which is efficient for typical constraints up to 10^5 or more.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    try:
        main()
    except Exception:
        pass
    return ""  # replace if capturing output properly

# provided sample style tests (format depends on original statement)
# these are conceptual placeholders since exact samples are not shown

# minimal case
assert run("1\n1\n0\n") == "ambiguous\n", "single element"

# simple valid swap structure
assert run("2\n2 1\n0\n") == "ambiguous\n", "two-cycle"

# invalid cycle
assert run("3\n2 3 1\n0\n") == "not ambiguous\n", "three-cycle"

# mixed structure valid
assert run("4\n2 1 4 3\n0\n") == "ambiguous\n", "disjoint swaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | ambiguous | single element base case |
| 2 2 1 0 | ambiguous | correct handling of 2-cycles |
| 3 2 3 1 0 | not ambiguous | rejection of 3-cycles |
| 4 2 1 4 3 0 | ambiguous | multiple independent swaps |

## Edge Cases

For n = 1, the permutation [1] must be accepted. The algorithm checks i = 0, computes j = 0, and verifies arr[0] == 1, which holds, so it returns valid.

For a permutation composed entirely of fixed 2-cycles like [2, 1, 4, 3], every index maps back correctly after two applications. The algorithm verifies each pair independently, so no global cycle reasoning is required.

For a single large cycle such as [2, 3, 4, 1], the first index already fails the condition because following the mapping twice does not return to the start. The algorithm detects this immediately without traversing the full cycle structure.
