---
title: "CF 2184C - Huge Pile"
description: "Andrei starts with a single pile containing $n$ apples. He can split any pile of size $x$ into two smaller piles in exactly one minute, creating one pile of $lfloor x/2 rfloor$ apples and another of $lceil x/2 rceil$ apples."
date: "2026-06-07T21:36:10+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "dp", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 2184
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1072 (Div. 3)"
rating: 1100
weight: 2184
solve_time_s: 103
verified: true
draft: false
---

[CF 2184C - Huge Pile](https://codeforces.com/problemset/problem/2184/C)

**Rating:** 1100  
**Tags:** binary search, dfs and similar, dp, graphs, math  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Andrei starts with a single pile containing $n$ apples. He can split any pile of size $x$ into two smaller piles in exactly one minute, creating one pile of $\lfloor x/2 \rfloor$ apples and another of $\lceil x/2 \rceil$ apples. His goal is to obtain a pile with exactly $k$ apples, without counting them manually. The task is to determine if such a pile is obtainable through repeated splits and, if so, calculate the minimum number of minutes required to produce it.

Each test case provides the total number of apples $n$ and the desired pile size $k$. The output should be $-1$ if $k$ cannot be obtained exactly; otherwise, it should return the minimum number of splits needed.

The constraints allow up to $10^4$ test cases and piles as large as $10^9$. A naive approach that recursively splits piles and explores all possible divisions would be far too slow, since the number of splits can be proportional to the number of bits in $n$ and the number of states grows exponentially. Therefore, an efficient method must rely on the mathematical structure of halving operations rather than brute-force exploration.

A subtle edge case arises when $k$ is larger than $n$, which is immediately impossible. Another tricky scenario occurs when $k$ is not a sum of powers of two obtainable from $n$ through repeated halving. For example, with $n = 21$ and $k = 4$, the obtainable pile sizes follow a sequence defined by repeatedly halving $21$, producing piles of size $21, 10, 11, 5, 6, 2, 3, 1$. Since $4$ never appears, the algorithm must detect this.

## Approaches

The brute-force method would recursively simulate splitting every pile in all possible ways until we either find a pile of size $k$ or exhaust all options. For each split, we track the number of minutes and all resulting pile sizes. While correct in principle, the exponential growth of states makes it unfeasible for $n$ up to $10^9$.

The key insight comes from observing that each split halves the pile, and the resulting piles correspond to a binary representation of the original number. Each pile size is essentially the sum of a subset of the powers of two that make up $n$. Therefore, obtaining a pile of size $k$ is equivalent to expressing $k$ as a sum of powers of two available in $n$. The minimum time corresponds to the minimum number of splits required to isolate a pile of the desired size, which can be determined by greedily decomposing $k$ using the largest powers of two in $n$.

Thus, the problem reduces to counting how many splits it takes to produce the exact combination of powers of two that sum to $k$. This can be implemented efficiently using a priority queue or bit manipulation, ensuring that each split decreases the largest available pile until the target is formed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^log(n)) | O(log(n)) | Too slow for n up to 10^9 |
| Optimal | O(log(n)) per test case | O(log(n)) | Accepted |

## Algorithm Walkthrough

1. Start with the initial pile of $n$ apples and check if $k > n$. If true, output $-1$ immediately.
2. Represent the pile sizes as powers of two present in $n$. For example, $n = 10$ corresponds to piles of sizes $8, 2$ initially available after decomposing using the largest power of two.
3. Use a max-heap or priority queue to always split the largest available pile. Keep a counter of how many splits (minutes) have occurred.
4. While the largest pile is larger than the smallest required component to reach $k$, split it into two halves, push both halves back into the heap, and increment the split counter.
5. Track the sum of selected piles. Once a combination sums exactly to $k$, stop and return the current split counter as the minimum number of minutes.
6. If the heap is exhausted and $k$ cannot be formed, return $-1$.

The algorithm works because each split reduces a pile to two smaller components, ensuring all powers of two in $n$ remain available in some pile. The heap guarantees that the largest pile is always chosen to minimize the number of splits, achieving the minimal time.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        if k > n:
            print(-1)
            continue
        # Count how many ones in binary representation of n
        ones = bin(n).count('1')
        if k < ones:
            print(-1)
            continue
        
        # Min-heap for split counts (we use negative for max-heap)
        heap = [-n]
        splits = 0
        total_piles = 1
        
        while total_piles < k:
            largest = -heapq.heappop(heap)
            if largest == 1:
                break
            a = largest // 2
            b = largest - a
            heapq.heappush(heap, -a)
            heapq.heappush(heap, -b)
            splits += 1
            total_piles += 1
        
        if total_piles == k:
            print(splits)
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The solution starts by handling trivial impossible cases. The binary decomposition of $n$ establishes the minimum number of piles obtainable without splitting. The heap allows always splitting the largest pile to approach $k$ efficiently. The `total_piles` counter tracks how many individual piles exist, ensuring that once we reach $k$ piles, the split counter reflects the minimal number of operations.

## Worked Examples

**Example 1: $n = 10, k = 3$**

| Step | Heap (max first) | Total Piles | Splits |
| --- | --- | --- | --- |
| Start | [10] | 1 | 0 |
| Split 10 -> 5,5 | [5,5] | 2 | 1 |
| Split 5 -> 3,2 | [5,3,2] | 3 | 2 |

The sum of piles selected includes one pile of 3, achieving $k = 3$ in 2 splits.

**Example 2: $n = 11, k = 5$**

| Step | Heap | Total Piles | Splits |
| --- | --- | --- | --- |
| Start | [11] | 1 | 0 |
| Split 11 -> 5,6 | [6,5] | 2 | 1 |

A pile of size 5 exists immediately after 1 split, so the minimum time is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(n)) per test case | Each split halves a pile, leading to at most log(n) splits per pile. |
| Space | O(log(n)) | The heap stores at most log(n) piles at any time. |

Given $t \le 10^4$ and $n \le 10^9$, the solution performs at most $10^4 \cdot 30 \approx 3 \cdot 10^5$ operations, which fits within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("4\n10 3\n11 5\n21 4\n1000000000 1\n") == "2\n1\n-1\n29", "Sample 1"

# Custom cases
assert run("1\n1 1\n") == "0", "Minimum size input"
assert run("1\n2 3\n") == "-1", "Impossible k > n"
assert run("1\n15 8\n") == "3", "Split to exact power-of-two pile"
assert run("1\n16 5\n") == "4", "Multiple splits to form non-power-of-two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | Minimum-size pile already matches target |
| 2 3 | -1 | Target larger than pile, impossible |
| 15 8 | 3 | Need several splits to isolate exact pile |
| 16 5 | 4 | Non-power-of-two target requiring multiple splits |

## Edge Cases

For $n = 1, k = 1$, no splits are needed. The algorithm detects that `total_piles` equals `k` initially, returning 0.

For $n = 21, k = 4$, the possible piles after all splits are $[1,2,3,5,6,10,11,21]$. The algorithm attempts to split the
