---
title: "CF 106259D - The AND, The OR, and The XOR"
description: "We are given an array of integers, and we need to pick a subsequence of length at least two. For any chosen subsequence, we compute two bitwise aggregates: the bitwise AND of all selected numbers and the bitwise OR of all selected numbers."
date: "2026-06-18T23:38:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106259
codeforces_index: "D"
codeforces_contest_name: "CUET Inter University Programming Contest 2025"
rating: 0
weight: 106259
solve_time_s: 46
verified: true
draft: false
---

[CF 106259D - The AND, The OR, and The XOR](https://codeforces.com/problemset/problem/106259/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we need to pick a subsequence of length at least two. For any chosen subsequence, we compute two bitwise aggregates: the bitwise AND of all selected numbers and the bitwise OR of all selected numbers. The score of the subsequence is the XOR between these two results. The task is to minimize this score over all valid subsequences.

The key observation is that AND collapses bits downward while OR expands bits upward. The XOR between them measures the disagreement in the final bit pattern produced by these two extreme compressions of the same set. We are searching over all subsets of size at least two, so the search space is exponential, and a direct enumeration is impossible.

The constraints are large, with the total number of elements across all test cases up to three hundred thousand. This immediately eliminates any approach that inspects all subsets or even all pairs with extra per-pair processing. An acceptable solution must be linear or nearly linear per test case.

A naive approach might try all pairs first and assume larger subsequences cannot improve the answer. This is already suspicious because adding elements changes both AND and OR in nontrivial ways. For example, adding a third number can reduce the AND dramatically while keeping OR unchanged, potentially lowering the XOR result. This means pairwise reasoning alone is insufficient without justification.

A second subtle issue is that subsequences, not subarrays, are allowed. This removes any locality constraints and reinforces that only value distribution matters, not ordering.

## Approaches

The brute-force method enumerates all subsequences of size at least two, computes their AND and OR, and evaluates the XOR. For each subset, computing AND and OR takes linear time in subset size, so overall complexity is on the order of all subsets, which is exponential in n. Even restricting to pairs gives O(n²), which already fails for n up to 3·10⁵.

The key insight comes from examining how AND and OR behave across multiple elements. For a fixed bit position, AND is 1 only if every chosen element has that bit set, while OR is 1 if at least one element has that bit set. For any bit, the pair (AND bit, OR bit) can only be (0,0), (0,1), or (1,1). The XOR contributes only when these differ, which happens precisely when OR has a bit set but AND does not. That condition means: among the chosen elements, not all values share that bit.

Now consider what happens if we look at pairs. For any pair (x, y), the AND is x & y and OR is x | y, so the score becomes (x & y) XOR (x | y). A classical identity shows this equals x XOR y. This is because for every bit, AND and OR differ exactly when the bits differ between x and y, matching XOR behavior.

This simplifies the problem dramatically. For any subsequence of size at least two, its score depends only on whether there exists at least one pair inside it achieving a small XOR-like contribution. Since adding more elements cannot reduce the minimum pairwise XOR inside the chosen set, the best subsequence will always be achieved by some pair. Any larger set only introduces additional pairs, and the score cannot drop below the best pair.

Thus the problem reduces to finding the minimum value of (a[i] & a[j]) XOR (a[i] | a[j]) over all pairs, which is equivalent to finding the minimum XOR over all pairs of the array.

This reduces the task to the classical “minimum XOR pair” problem, solvable using a bitwise trie in linear time per insertion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(1) | Too slow |
| Bitwise trie for minimum pair XOR | O(n log A) | O(n log A) | Accepted |

## Algorithm Walkthrough

### Optimal approach

1. Treat each number as a 31-bit integer and process numbers one by one, inserting them into a binary trie. Each trie node stores two children corresponding to bit 0 and bit 1. This structure lets us efficiently find the closest previously inserted number in XOR sense.
2. For each incoming number, before inserting it, query the trie to find the number that minimizes XOR with it. This is done by greedily trying to follow the same bit if possible, since matching bits produce a 0 contribution in XOR, otherwise we are forced to take the opposite branch.
3. While querying, accumulate the XOR value along the path. Each time we are forced to diverge, we add a cost at that bit position. This constructs the best possible match among previously inserted numbers.
4. Update the global answer with the minimum XOR found for each element. This ensures we consider all pairs, since every element is paired against all earlier ones exactly once.
5. Insert the current number into the trie so it becomes available for future queries.

### Why it works

The trie guarantees that for each number, we are effectively choosing another number that minimizes bitwise disagreement from the most significant bit downward. This greedy construction is optimal because any improvement at a higher bit dominates all lower bits. Since every pair is considered once in this asymmetric manner, the minimum XOR over all pairs is captured exactly once and cannot be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("child",)
    def __init__(self):
        self.child = [None, None]

def insert(root, x):
    node = root
    for b in range(30, -1, -1):
        bit = (x >> b) & 1
        if node.child[bit] is None:
            node.child[bit] = Node()
        node = node.child[bit]

def query(root, x):
    node = root
    res = 0
    for b in range(30, -1, -1):
        bit = (x >> b) & 1
        if node.child[bit] is not None:
            node = node.child[bit]
        else:
            node = node.child[bit ^ 1]
            res |= (1 << b)
    return res

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        root = Node()
        insert(root, arr[0])

        ans = float('inf')

        for i in range(1, n):
            x = arr[i]
            ans = min(ans, query(root, x))
            insert(root, x)

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds a binary trie per test case. Each number is inserted bit by bit from the most significant bit downward. The query function walks the trie preferring matching bits, only diverging when necessary, and accumulates the resulting XOR cost. The first element is inserted before processing to ensure every subsequent element has at least one candidate partner.

The choice of 31 bits matches the constraint that values are up to 10⁹. Using a fixed depth avoids overhead from dynamic bit length checks.

## Worked Examples

### Example 1

Input:

```
1
3
1 2 3
```

We insert 1 first.

| Step | Current x | Best match in trie | XOR result | Best answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 3 | 3 |
| 2 | 3 | 1 | 2 | 2 |

Then inserting 2 and 3 ensures all pairs are considered. The minimum is 1, achieved by pairing 2 and 3.

This trace shows that every element is compared against earlier ones, guaranteeing full pair coverage without recomputing all pairs.

### Example 2

Input:

```
1
4
5 1 7 3
```

| Step | Current x | Best match in trie | XOR result | Best answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 4 | 4 |
| 2 | 7 | 5 | 2 | 2 |
| 3 | 3 | 1 | 2 | 2 |

The final answer is 2, achieved by multiple pairs. This shows how multiple candidates can produce the same optimal XOR, and the trie ensures all are implicitly checked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each insertion and query traverses 31 bits |
| Space | O(n log A) | Each number contributes up to 31 trie nodes |

The total sum of n is 3·10⁵, and each operation is constant factor 31, which fits comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    class Node:
        __slots__ = ("child",)
        def __init__(self):
            self.child = [None, None]

    def insert(root, x):
        node = root
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            if node.child[bit] is None:
                node.child[bit] = Node()
            node = node.child[bit]

    def query(root, x):
        node = root
        res = 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            if node.child[bit] is not None:
                node = node.child[bit]
            else:
                node = node.child[bit ^ 1]
                res |= (1 << b)
        return res

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        root = Node()
        insert(root, arr[0])
        ans = inf
        for i in range(1, n):
            ans = min(ans, query(root, arr[i]))
            insert(root, arr[i])
        out.append(str(ans))
    return "\n".join(out)

# sample
assert run("1\n3\n1 2 3\n") == "1"

# minimum size
assert run("1\n2\n0 0\n") == "0"

# identical values
assert run("1\n4\n7 7 7 7\n") == "0"

# increasing pattern
assert run("1\n4\n1 2 4 8\n") == "3"

# mixed case
assert run("1\n5\n5 1 7 3 2\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 0 | identical values |
| 1 2 4 8 | 3 | structured bit patterns |
| 5 1 7 3 2 | 1 | mixed interactions |

## Edge Cases

For arrays where all values are identical, every pair yields zero XOR, and the trie immediately finds identical matches, producing zero. The algorithm inserts the first value and every subsequent query finds the same bit path at every level.

For strictly increasing powers of two, each number differs in exactly one bit position, and the trie forces divergence at the highest differing bit, producing predictable XOR values. The greedy traversal correctly identifies nearest neighbors in bit space.

For cases with zeros, inserting zero first ensures that all future queries can immediately match zero bits, often producing very small XOR values. The trie correctly handles the all-zero branch without special casing.
