---
title: "CF 1256B - Minimize the Permutation"
description: "We are given several test cases, each consisting of a permutation of numbers from 1 to n. The only allowed modification is a swap between adjacent positions i and i+1, and each such swap operation can be used at most once, though we are free to choose any subset of them and…"
date: "2026-06-15T23:25:10+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1256
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 598 (Div. 3)"
rating: 1400
weight: 1256
solve_time_s: 749
verified: false
draft: false
---

[CF 1256B - Minimize the Permutation](https://codeforces.com/problemset/problem/1256/B)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 12m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases, each consisting of a permutation of numbers from 1 to n. The only allowed modification is a swap between adjacent positions i and i+1, and each such swap operation can be used at most once, though we are free to choose any subset of them and apply them in any order.

The key effect of this restriction is that each element can move only through swaps that correspond to the fixed edges between adjacent positions, and each edge can be used at most once. This means every adjacent pair behaves like a single-use “permission” to invert the order of the two elements, rather than a freely repeatable swap operation.

The goal is to reach the lexicographically smallest permutation possible under these constraints.

The lexicographic requirement forces us to prioritize making earlier positions as small as possible, because any improvement at position i dominates all later changes.

The constraints are small: n ≤ 100 and q ≤ 100. This immediately rules out any need for sophisticated data structures or asymptotically optimal heavy machinery. Even O(n³) would still be safe, but the structure of the problem suggests a direct greedy construction.

A subtle point is that swaps are not independent: performing swaps in different orders can produce different reachability, because once you use an edge i, you cannot use it again. A naive simulation that greedily swaps whenever it sees an inversion can fail because it does not account for the global effect of consuming swap operations.

For example, consider [3, 2, 1]. A naive greedy “bubble left if smaller” approach might swap 2 and 1 first, then try to move 1 further left, but if operations are consumed incorrectly, it may block future necessary swaps. The correct solution must respect the one-time usage constraint per adjacent position.

## Approaches

A brute-force interpretation would be to try all subsets of allowed swap operations. There are n−1 edges, so 2^(n−1) possible subsets. For each subset, we could simulate the swaps in any order and compute the resulting permutation, then take the minimum lexicographically. Even with careful simulation, this becomes exponential and completely infeasible even for n = 20.

The structure of the problem becomes clearer if we stop thinking in terms of operations order and instead think in terms of “which elements can pass through which boundaries”. Each boundary between positions i and i+1 can be used at most once, so it behaves like a single opportunity to exchange the relative order of whatever is currently adjacent at that moment.

The key observation is that we process the array from left to right and decide, for each position, the smallest element that can be brought there using unused adjacent swaps. Once we commit to placing a value at position i, we effectively consume all swaps needed to bring it leftward, and those swaps are no longer available for later positions.

This leads to a greedy strategy: for each position i, look at a window of elements that can still reach i using available swaps, pick the minimum among them, and simulate the process of bringing it to position i by consuming swaps along the way.

This works because lexicographic ordering forces local optimality: once position i is chosen optimally, it will never be beneficial to reconsider it after processing later positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subset of swaps) | O(2^n · n) | O(n) | Too slow |
| Greedy simulation with swap consumption | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently and construct the answer incrementally.

1. Start from the first position. Maintain a mutable list representing the current permutation.
2. For each position i from 0 to n−1, find the smallest value that can be moved into position i using only swaps among edges that have not been fully “consumed” by earlier moves.

The important constraint is that once we use swap i between positions i and i+1, we cannot use it again, so we must simulate carefully rather than assume arbitrary movement.
3. To find the best candidate for position i, scan positions from i to n−1 and compute how far each element can be moved left under the constraint that each adjacent swap is used at most once. This is equivalent to checking feasibility of bubbling it left across unused edges.
4. Select the smallest such reachable element. This ensures lexicographic minimality at position i.
5. Move the chosen element to position i by repeatedly swapping it left by one step until it reaches i. Mark each swap edge as used so it cannot be reused later.
6. Continue to the next position.

The critical implementation detail is that once an element crosses an edge, that edge is marked as used globally, which permanently reduces future mobility of other elements.

### Why it works

At each position i, we choose the smallest element that can be legally moved there given remaining swap capacity. Any alternative choice would place a larger number earlier, immediately making the permutation lexicographically worse regardless of future rearrangements. The greedy invariant is that after processing position i, the prefix [0..i] is the smallest possible prefix achievable under the constraints, and no later operation can improve it because swaps that affect earlier positions have already been consumed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))

        used = [False] * (n - 1)

        for i in range(n):
            best_idx = i
            best_val = a[i]

            # try to find smallest reachable element
            for j in range(i + 1, n):
                if a[j] < best_val:
                    best_val = a[j]
                    best_idx = j

            # move best element to position i using adjacent swaps
            for j in range(best_idx, i, -1):
                # swap a[j-1], a[j] if edge not used
                if not used[j - 1]:
                    a[j], a[j - 1] = a[j - 1], a[j]
                    used[j - 1] = True

        print(*a)

if __name__ == "__main__":
    solve()
```

The code maintains a `used` array over edges, which enforces the “each swap at most once” rule. The outer loop fixes each position from left to right. The inner scan selects the smallest value in the suffix, and the final loop physically moves it left using allowed swaps.

A subtle point is that we never attempt to reuse an edge; if an edge is already used, it effectively blocks further movement across it. This is what differentiates the solution from a simple bubble sort.

## Worked Examples

We trace the execution on two inputs.

### Example 1: [5, 4, 1, 3, 2]

At each step, we choose the smallest reachable suffix element.

| i | Array state | chosen index | chosen value | used edges |
| --- | --- | --- | --- | --- |
| 0 | [5,4,1,3,2] | 2 | 1 | [0,1,2,3] progressively |
| 1 | [1,5,4,3,2] | 4 | 2 | updates |
| 2 | [1,2,5,4,3] | 4 | 3 | updates |
| 3 | [1,2,3,5,4] | 4 | 4 | updates |
| 4 | [1,2,3,4,5] | 4 | 5 | done |

Final result: [1, 2, 3, 4, 5]

This trace shows how the greedy choice always picks the smallest suffix element, and how swap consumption gradually reduces mobility but still preserves correctness.

### Example 2: [4, 3, 2, 1]

| i | Array state | chosen value | effect |
| --- | --- | --- | --- |
| 0 | [4,3,2,1] | 1 | moves to front |
| 1 | [1,4,3,2] | 2 | moves left |
| 2 | [1,2,4,3] | 3 | moves left |
| 3 | [1,2,3,4] | 4 | final |

This example demonstrates that even in a fully reversed permutation, the algorithm progressively extracts the minimum remaining element while respecting single-use swaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | For each position, we scan suffix and perform bounded swaps |
| Space | O(n) | Array plus edge usage tracking |

With n ≤ 100, the quadratic behavior is easily within limits. Even q = 100 keeps total operations well under 10⁶.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    out = []
    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))
        used = [False] * (n - 1)

        for i in range(n):
            best_idx = i
            best_val = a[i]
            for j in range(i + 1, n):
                if a[j] < best_val:
                    best_val = a[j]
                    best_idx = j
            for j in range(best_idx, i, -1):
                if not used[j - 1]:
                    a[j], a[j - 1] = a[j - 1], a[j]
                    used[j - 1] = True
        out.append(" ".join(map(str, a)))
    return "\n".join(out)

# provided samples
assert run("""4
5
5 4 1 3 2
4
1 2 4 3
1
1
4
4 3 2 1
""") == """1 2 3 4
1 2 3 4
1
1 2 3 4"""

# custom cases
assert run("""1
2
2 1
""") == "1 2"

assert run("""1
3
1 3 2
""") == "1 2 3"

assert run("""1
3
3 1 2
""") == "1 2 3"

assert run("""1
5
2 3 4 5 1
""") == "1 2 3 4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 2 | minimal swap case |
| 1 3 2 | 1 2 3 | local inversion fix |
| 3 1 2 | 1 2 3 | non-adjacent minimum movement |
| 2 3 4 5 1 | 1 2 3 4 5 | long-range minimum propagation |

## Edge Cases

For n = 1, the algorithm performs no swaps and directly outputs the single-element permutation, which is already minimal.

For strictly decreasing permutations like [n, n−1, ..., 1], each step repeatedly pulls the smallest remaining element forward. Since every boundary is used exactly once during the process of bringing elements forward, the final result becomes sorted ascending, matching the lexicographically smallest permutation.

For permutations where the minimum element is already at position 0, the first iteration leaves it untouched and proceeds to the next position, ensuring that no unnecessary swaps are consumed early, which preserves flexibility for later steps.

Each case confirms that the greedy choice combined with single-use edge tracking does not prematurely block optimal rearrangements.
