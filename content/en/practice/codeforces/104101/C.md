---
title: "CF 104101C - Add 9 Zeros"
description: "We are given a collection of problems, each characterized by a single integer value that represents how many trailing zeros its difficulty scale has in a power of ten."
date: "2026-07-02T02:07:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104101
codeforces_index: "C"
codeforces_contest_name: "The 2022 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 104101
solve_time_s: 46
verified: true
draft: false
---

[CF 104101C - Add 9 Zeros](https://codeforces.com/problemset/problem/104101/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of problems, each characterized by a single integer value that represents how many trailing zeros its difficulty scale has in a power of ten. Concretely, the i-th problem has difficulty $10^{a_i}$, so we can think of each problem as being labeled by its exponent $a_i$. All $a_i$ values are distinct, so every difficulty level is unique.

From this set, we are allowed to choose some subset of problems. For each chosen problem with exponent $a$, we generate a new problem whose exponent becomes $a + 9$, effectively multiplying its difficulty by $10^9$. These transformed problems form a new set B. However, we are not allowed to create a transformed problem that already exists in the original set A. In other words, if $a + 9$ is already present among the original exponents, we cannot include $a$ in our chosen subset.

The task is to maximize how many problems we can select under this restriction.

The input size can be as large as $5 \times 10^5$, which immediately rules out any quadratic or even $O(n \log n)$ approach that repeatedly searches or simulates conflicts between pairs. The structure suggests that each value interacts only with a single other value, namely $a + 9$, which hints at a direct lookup or hashing-based solution.

A subtle failure case appears when multiple values chain indirectly via repeated additions, for example if $a$, $a+9$, and $a+18$ all exist. A naive greedy that processes in arbitrary order can easily make inconsistent choices if it does not explicitly enforce a global consistency rule. Another pitfall is treating this as a sorting problem without recognizing that only exact +9 collisions matter, not relative ordering.

For example, if the input is:

```
a = [1, 10, 19]
```

then choosing 1 forbids 10, and choosing 10 forbids 19, but choosing 1 and 19 together is valid since 1+9=10 exists but 19+9=28 does not exist. The correct answer is 2, but a careless greedy that always blocks neighbors in sorted order might incorrectly undercount.

## Approaches

The brute-force view is straightforward: for each subset of indices, check whether selecting it is valid. For a chosen set S, we verify that for every $a \in S$, the value $a+9$ is not in the original array. This requires checking membership for each element, and trying all subsets leads to $O(2^n)$, which is completely infeasible even for small constraints.

Even if we try to improve this by checking each candidate independently, we run into a dependency structure: choosing a value affects at most one other value. The key observation is that each number only conflicts with exactly one possible partner, the number nine larger than it. There are no longer-range dependencies. This means the problem reduces to pairing elements and avoiding picking both ends of certain directed edges $a \to a+9$.

Once seen this way, the structure becomes a directed graph where each node has at most one outgoing edge. The optimal strategy is simply to avoid selecting nodes that are “blocked” by the presence of their incoming counterpart. If $a$ exists and $a-9$ exists, then choosing $a-9$ forbids $a$. Thus each pair $(a, a+9)$ contributes at most one usable element. Every element not involved in such a pair can always be chosen.

We can therefore compute the answer by iterating through all values and counting how many are not of the form $x+9$ for some existing $x$, or equivalently counting all elements and subtracting those that are “invalid starters” in a conflict pair. A cleaner view is: for every $a$, if $a-9$ exists, then $a$ cannot be chosen if we want to maximize selections without double counting conflicts, so each such relation reduces potential choices by enforcing a pairwise constraint.

A direct and optimal method is to store all values in a hash set and count how many values are “unpaired in a forced exclusion sense”. Since each number only has one possible conflict, we effectively resolve all pairs independently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(2^n)$ | $O(n)$ | Too slow |
| Hash Set Pair Checking | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We convert the list of exponents into a set for constant-time membership queries. The goal is to determine how many elements can be selected such that we never pick both $a$ and $a+9$.

1. Store all values in a hash set. This allows us to test existence of $x+9$ in constant time.
2. Initialize a counter for the answer as zero.
3. Iterate over every value $a$ in the array.
4. Check whether $a-9$ exists in the set.
5. If $a-9$ does not exist, increment the answer by one, because $a$ is not forced to be excluded by a smaller element.
6. Otherwise, skip it, since it is part of a conflict pair where the smaller element already represents the optimal representative.

The reasoning behind this rule is that in every conflict pair $(a, a+9)$, only the smaller value is allowed to be counted. By always preferring the smaller endpoint, we ensure that no pair contributes more than one selected element, and every independent element is still counted.

### Why it works

Each conflict is local: if $a$ and $a+9$ both exist, they form a single dependency where selecting both is forbidden. The algorithm assigns exactly one representative per such chain by always favoring the smallest element in any consecutive sequence linked by +9 differences. Since no node can belong to more than one independent chain branching structure (each node has at most one predecessor and one successor in this relation), counting only elements without a predecessor guarantees exactly one per valid component.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    s = set(arr)
    
    ans = 0
    for a in arr:
        if (a - 9) not in s:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies entirely on set membership. The key design choice is iterating over elements and only counting those that are not “covered” by a predecessor differing by 9. This avoids double counting in chains like $1 \to 10 \to 19$, where only the first element in the chain is counted.

A common mistake is checking $a+9$ instead of $a-9$, which leads to double counting or inconsistent direction handling. Using the predecessor check enforces a unique representative per chain.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, 10, 19]
```

| a | a-9 in set? | counted |
| --- | --- | --- |
| 1 | no | yes |
| 10 | yes | no |
| 19 | yes | no |

Output is 1.

This demonstrates that all three values form a single chain, and only the smallest element is counted.

### Example 2

Input:

```
n = 4
a = [2, 11, 5, 20]
```

| a | a-9 in set? | counted |
| --- | --- | --- |
| 2 | no | yes |
| 11 | yes | no |
| 5 | no | yes |
| 20 | yes | no |

Output is 2.

Here we have two independent chains: $2 \to 11$ and $5 \to 14$ (though 14 is absent), so 2 and 5 are independent representatives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is processed once with constant-time hash lookup |
| Space | $O(n)$ | Set stores all input values |

The constraints allow up to $5 \times 10^5$ elements, and a linear pass with hashing fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal
assert run("1\n5\n") == "1"

# no conflicts
assert run("3\n1 2 3\n") == "3"

# single chain
assert run("3\n1 10 19\n") == "1"

# mixed chains
assert run("4\n2 11 5 20\n") == "2"

# larger mixed
assert run("5\n1 10 2 11 100\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case |
| no conflicts | n | independence case |
| 1 10 19 | 1 | chained dependency |
| 2 11 5 20 | 2 | multiple independent pairs |
| 1 10 2 11 100 | 3 | overlapping chains |

## Edge Cases

A key edge case is a long chain of +9 differences, such as:

```
1 10 19 28 37
```

The algorithm processes each element and counts only those without a predecessor:

- 1 has no 1-9, counted
- 10 has 1 in set, skipped
- 19 has 10 in set, skipped
- 28 has 19 in set, skipped
- 37 has 28 in set, skipped

Output is 1, which matches the intended rule that only one representative per chain is selected.

Another edge case is disjoint pairs:

```
1 10 3 12
```

Both chains behave independently, and the algorithm counts exactly 2 elements, selecting the minimal element of each pair.
