---
title: "CF 105216L - Lost Shoes"
description: "We are given a family of $N$ people, where each person currently holds two shoes: one right shoe and one left shoe. However, these shoes are mixed up."
date: "2026-06-24T17:11:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105216
codeforces_index: "L"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 105216
solve_time_s: 70
verified: false
draft: false
---

[CF 105216L - Lost Shoes](https://codeforces.com/problemset/problem/105216/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a family of $N$ people, where each person currently holds two shoes: one right shoe and one left shoe. However, these shoes are mixed up. For every person $i$, the right shoe they currently have belongs to some person $a_i$, and the left shoe they currently have belongs to some person $b_i$.

The goal is to rearrange shoes so that person $i$ ends up with both of their own shoes. The only allowed operation is a swap between two people, but only on the same side: right shoes can be swapped only with right shoes, and left shoes only with left shoes. Each swap exchanges the shoes of that side between two people.

We need to compute the minimum number of such swaps required to restore every person’s correct pair.

The key observation from constraints is that $N$ can be as large as $10^6$. This immediately rules out any solution that is quadratic or even close to quadratic. Any approach that tries to simulate swaps directly, or repeatedly search for misplaced shoes, will time out. The solution must be essentially linear in $N$, or at worst $O(N \log N)$, though logarithmic factors are risky at this scale.

A subtle aspect of the problem is that right shoes and left shoes move independently. There is no interaction between sides during swaps. This means any solution that mixes the two sides prematurely is likely to be incorrect.

Edge cases appear when cycles overlap or when both arrays are already correct but misaligned across sides. For example, if all right shoes are already correct but left shoes form a large cycle, the answer is still determined entirely by that left-side permutation structure. A naive “count mismatches and swap greedily” approach fails because swaps fix structure globally, not locally.

Another edge case is when both arrays are identical but not equal to identity mapping. For example, a pure permutation cycle such as $a = [2,3,1]$. Even though every position is “wrong”, it does not require two independent corrections per element, but rather cycle resolution.

## Approaches

If we try to simulate the process directly, we would repeatedly search for a person who holds a wrong shoe and swap it with the correct owner. Each swap requires locating a target, updating positions, and maintaining consistency for both left and right sides. Even with hashing, the repeated updates still form a process that can degrade toward $O(N^2)$ in adversarial cases because each correction might cascade into many further mismatches.

The key insight is that swaps within a side behave exactly like sorting a permutation using arbitrary swaps. Each side independently defines a permutation of size $N$: the right shoes define a mapping from current positions to owners, and the same for left shoes.

The problem reduces to fixing two independent permutations. For any permutation, the minimum number of swaps needed to restore identity is well-known: it equals $N -$ (number of cycles in the permutation). Each cycle of length $k$ requires exactly $k-1$ swaps to fix, since each swap can place one element into its correct position while reducing the cycle size by one.

Since left and right operations are independent, the total answer is simply the sum of swaps required for both permutations.

We therefore compute cycle decomposition for both arrays and sum the results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | $O(N^2)$ | $O(N)$ | Too slow |
| Cycle decomposition | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We process the right shoe mapping and left shoe mapping separately, treating each as a permutation on $N$ elements.

1. Build a visited array initialized to false for tracking which positions have been processed. This ensures each element is assigned to exactly one cycle.
2. For the right shoe array, iterate through each position from 1 to $N$. If a position is not visited, we start traversing its cycle by repeatedly following the mapping $i \rightarrow a_i$ until we return to the starting point. Each time we visit a new node in this traversal, we mark it visited and count the cycle size.
3. For each cycle of size $k$, we add $k-1$ to the answer. This corresponds to the number of swaps needed to fix that cycle independently.
4. After finishing all cycles in the right array, reset the visited structure.
5. Repeat the same cycle decomposition process for the left array $b$, again summing $k-1$ for each discovered cycle.
6. Output the total sum from both sides.

The crucial point is that we never actually perform swaps. We only compute how many swaps would be required if we were to resolve each permutation optimally.

### Why it works

Each side defines a permutation over $N$ items. A permutation decomposes uniquely into disjoint cycles, and within each cycle, elements are rotated among positions. A single swap can fix exactly one element in a cycle by placing it into its correct position, effectively reducing the cycle size by one while preserving structure of the remaining elements. This guarantees that a cycle of length $k$ always requires exactly $k-1$ swaps and no fewer, since each swap can fix at most one misplaced element in that cycle without disturbing correctness already achieved.

Since left and right operations are independent and do not interfere, the total minimum number of swaps is the sum of the optimal costs for each permutation separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_swaps(p):
    n = len(p) - 1
    vis = [False] * (n + 1)
    res = 0

    for i in range(1, n + 1):
        if not vis[i]:
            cur = i
            cycle_size = 0
            while not vis[cur]:
                vis[cur] = True
                cycle_size += 1
                cur = p[cur]
            res += cycle_size - 1

    return res

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    print(count_swaps(a) + count_swaps(b))

if __name__ == "__main__":
    solve()
```

The implementation builds a 1-indexed array for convenience so that positions align directly with person labels. The `count_swaps` function isolates the standard cycle decomposition logic. Each unvisited node starts a traversal that follows the permutation until it closes a loop, accumulating cycle size along the way.

A common pitfall here is forgetting that both arrays must be processed independently. Another subtle issue is incorrect indexing when reading input; using 1-based indexing avoids off-by-one mistakes when following permutations.

## Worked Examples

### Sample 1

Input:

```
2
1 2
2 1
```

Right permutation cycles:

Start at 1: 1 → 1 (cycle size 1)

Start at 2: 2 → 2 (cycle size 1)

Left permutation cycles:

Start at 1: 1 → 2 → 1 (cycle size 2)

| Step | Start | Cycle Traversal | Cycle Size | Contribution |
| --- | --- | --- | --- | --- |
| Right | 1 | 1 | 1 | 0 |
| Right | 2 | 2 | 1 | 0 |
| Left | 1 | 1 → 2 → 1 | 2 | 1 |

Total swaps = 1.

This shows that only the left side requires a swap, while the right side is already correct.

### Sample 2

Input:

```
3
1 3 2
2 1 3
```

Right permutation:

Cycle: 2 ↔ 3 (size 2)

Left permutation:

Cycle: 1 ↔ 2 (size 2)

| Side | Cycle | Size | Contribution |
| --- | --- | --- | --- |
| Right | (2 3) | 2 | 1 |
| Left | (1 2) | 2 | 1 |

Total swaps = 2.

Each side contributes one independent swap because each contains a single 2-cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each node is visited exactly once per permutation |
| Space | $O(N)$ | Visited array and input storage |

The algorithm runs in linear time, which is essential for $N = 10^6$. Memory usage remains proportional to input size and easily fits within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def count_swaps(p):
        n = len(p) - 1
        vis = [False] * (n + 1)
        res = 0
        for i in range(1, n + 1):
            if not vis[i]:
                cur = i
                cnt = 0
                while not vis[cur]:
                    vis[cur] = True
                    cnt += 1
                    cur = p[cur]
                res += cnt - 1
        return res

    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))
    return str(count_swaps(a) + count_swaps(b))

# sample 1
assert run("2\n1 2\n2 1\n") == "1"

# sample 2
assert run("3\n1 3 2\n2 1 3\n") == "2"

# sample 3
assert run("5\n4 5 1 2 3\n3 1 4 5 2\n") == "8"

# all correct already
assert run("1\n1\n1\n") == "0"

# single cycle
assert run("3\n2 3 1\n1 2 3\n") == "2"

# identity both sides
assert run("4\n1 2 3 4\n1 2 3 4\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, identity | 0 | no swaps needed |
| 3-cycle cases | 2 | cycle decomposition correctness |
| mixed permutations | 8 | independent side handling |

## Edge Cases

A minimal edge case is when $N = 1$. Both arrays must contain only 1. The algorithm marks the single node as a cycle of size 1, contributing zero swaps for each side, yielding correct output 0.

Another case is when both arrays form large cycles. For example, $a = [2,3,4,5,1]$. The traversal visits all nodes once, producing a cycle of size 5 and contributing 4 swaps. The same logic applies independently to the second array if it has a different cycle structure. The algorithm correctly separates them because visited state is reset between passes.

A more subtle case is when both permutations are identical but non-trivial. Even though the structure matches, each side still requires independent fixing. The algorithm correctly counts both contributions rather than attempting to cancel them, because swaps cannot be shared across sides.
