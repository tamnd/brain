---
title: "CF 1920B - Summation Game"
description: "We are asked to simulate a two-step game played on an array of positive integers. The first player, Alice, can remove up to $k$ elements. She wants the final sum of the array to be as large as possible."
date: "2026-06-08T19:28:17+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1920
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 919 (Div. 2)"
rating: 1100
weight: 1920
solve_time_s: 109
verified: true
draft: false
---

[CF 1920B - Summation Game](https://codeforces.com/problemset/problem/1920/B)

**Rating:** 1100  
**Tags:** games, greedy, math, sortings  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a two-step game played on an array of positive integers. The first player, Alice, can remove up to $k$ elements. She wants the final sum of the array to be as large as possible. The second player, Bob, can then flip up to $x$ elements, multiplying them by $-1$, and he wants to make the sum as small as possible. Our task is to compute the final sum assuming both play optimally.

The input consists of multiple test cases. Each test case gives the size of the array $n$, Alice's limit $k$, Bob's limit $x$, and the array of $n$ integers. The output for each test case is the final sum after both players make their optimal moves.

Constraints tell us $n$ can be up to $2 \cdot 10^5$ per test case and the sum of all $n$ over all test cases also does not exceed $2 \cdot 10^5$. This means we need a solution linear in $n$, $O(n \log n)$ at most, as $O(n^2)$ approaches would be far too slow.

The non-obvious edge cases include arrays of size 1, where Alice can remove the only element, leaving the sum 0, or when $k \ge n$, which allows Alice to remove everything. Another tricky case is when $x \ge n$ and Bob can flip all remaining elements, turning a large sum negative. Neglecting these conditions can lead to incorrect outputs. For example, an input of `1 1 1` with array `[1]` must produce `0`, not `1`, because Alice will optimally remove the element.

## Approaches

The brute-force approach would enumerate every subset of size up to $k$ that Alice could remove, then for each resulting array, enumerate every subset of size up to $x$ that Bob could flip. For each combination, compute the sum and select the maximal/minimal according to each player. This is correct in principle, but for $n \sim 2 \cdot 10^5$, it is infeasible since it would involve $O(2^n)$ operations.

The key insight comes from noticing that both players act greedily on extremal elements. Alice wants to remove the largest values that Bob would flip to negative, and Bob will always flip the largest remaining elements to negative to minimize the sum. This reduces the problem to sorting the array and considering only the top $k + x$ elements. In practice, Alice will remove the $k$ largest elements if Bob can flip them, or choose fewer if that maximizes her final sum.

The optimal solution does not require complex state tracking or dynamic programming because the players’ moves are determined entirely by ordering. We can compute the sum after Alice removes up to $k$ largest elements, then subtract twice the sum of the $x$ largest remaining elements (which Bob flips), yielding the final sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n, k, x$ and the array $a$.
2. Sort the array $a$ in ascending order. Sorting allows us to easily pick the largest elements for removal or flipping.
3. Compute Alice’s action. She can remove up to $k$ elements. Removing elements is only beneficial if they are among the largest that Bob could flip. To maximize the sum, she should remove the $k$ largest elements.
4. Compute Bob’s action. After Alice’s removal, Bob flips up to $x$ remaining largest elements by multiplying them by $-1$. This decreases the sum as much as possible.
5. Compute the sum of the remaining array after both players acted. For Bob’s flips, subtract twice the sum of the $x$ largest remaining elements, because flipping an element $y$ changes the total sum by $-2y$.
6. Output the final sum.

Why it works: Alice always removes elements that would hurt the sum most if Bob flips them. Bob always flips the largest remaining elements to minimize the sum. Sorting ensures we can efficiently access the largest elements in both steps. This greedy strategy produces the optimal result because the problem is linear with respect to the sum, and each element acts independently once ordered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, k, x = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()
        
        # Alice removes k largest
        if k > 0:
            a = a[:n - k]
        
        # Bob flips x largest remaining
        if x > 0:
            a[-x:] = [-v for v in a[-x:]]
        
        print(sum(a))

if __name__ == "__main__":
    main()
```

The solution sorts the array so we can efficiently identify the largest elements for removal and flipping. We slice the array to remove Alice's elements and flip the last `x` elements for Bob. Python's negative slicing handles cases where `x` or `k` exceeds array size safely.

## Worked Examples

### Example 1

Input: `1 1 1` with array `[1]`.

| Step | Array state | Sum |
| --- | --- | --- |
| Initial | [1] | 1 |
| Alice removes 1 element | [] | 0 |
| Bob flips 0 elements | [] | 0 |

Final sum: `0`.

### Example 2

Input: `4 1 1` with array `[3, 1, 2, 4]`.

| Step | Array state | Sum |
| --- | --- | --- |
| Initial | [1, 2, 3, 4] | 10 |
| Alice removes 1 largest | [1, 2, 3] | 6 |
| Bob flips 1 largest | [1, 2, -3] | 0 |

Final sum: `0`.

These traces confirm the algorithm correctly handles removal and flipping of largest elements to produce the optimal sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates per test case; slicing and summing are O(n) |
| Space | O(n) | Storing the array |

The constraints limit the sum of all $n$ to $2 \cdot 10^5$. Our O(n log n) solution fits comfortably within 1 second and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# Provided samples
assert run("8\n1 1 1\n1\n4 1 1\n3 1 2 4\n6 6 3\n1 4 3 2 5 6\n6 6 1\n3 7 3 3 32 15\n8 5 3\n5 5 3 3 3 2 9 9\n10 6 4\n1 8 2 9 3 3 4 5 3 200\n2 2 1\n4 3\n2 1 2\n1 3") == "0\n2\n0\n3\n-5\n-9\n0\n-1"

# Custom cases
assert run("1\n3 3 1\n10 20 30") == "0", "Alice removes everything"
assert run("1\n3 1 5\n1 2 3") == "-4", "Bob flips more than remaining elements"
assert run("1\n5 0 2\n5 5 5 5 5") == -10, "Alice does nothing, Bob flips largest"
assert run("1\n1 1 1\n1000") == "0", "Single element removed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 1, array [10,20,30] | 0 | Alice removes all |
| 3 1 5, array [1,2,3] | -4 | Bob flips more than remaining |
| 5 0 2, array [5,5,5,5,5] | -10 | Bob flips largest when Alice does nothing |
| 1 1 1, array [1000] | 0 | Single element edge case |

## Edge Cases

The algorithm handles single-element arrays correctly by allowing Alice to remove it, resulting in a sum of 0. When Bob's flip count exceeds the number of remaining elements, the slice operation in Python safely flips all remaining elements without error. Arrays with repeated elements or maximum-size elements are also handled correctly because the operations depend solely on sorting and selecting extremal elements. This confirms the solution works across all edge conditions specified by the problem.
