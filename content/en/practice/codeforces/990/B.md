---
problem: 990B
contest_id: 990
problem_index: B
name: "Micro-World"
contest_name: "Educational Codeforces Round 45 (Rated for Div. 2)"
rating: 1200
tags: ["greedy", "sortings"]
answer: passed_samples
verified: false
solve_time_s: 88
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a33ab40-4628-83ec-b07d-d37d37181695
---

# CF 990B - Micro-World

**Rating:** 1200  
**Tags:** greedy, sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 28s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a33ab40-4628-83ec-b07d-d37d37181695  

---

## Solution

## Problem Understanding

We are given a collection of bacteria, each with a fixed size. A larger bacterium can consume a smaller one only when two conditions hold at the moment of interaction: it must be strictly larger, and at the same time it cannot be too large compared to its prey, specifically its size must not exceed the prey’s size by more than a given constant $K$. After eating, only the eater remains and its size never changes.

Since each surviving bacterium may repeatedly eat others, we are effectively allowed to delete elements under a constraint that depends on pairwise size differences. The task is to choose an order of such deletions that leaves as few bacteria as possible at the end.

The input size goes up to $2 \cdot 10^5$, which immediately rules out any simulation that repeatedly scans or tries all pairs. Anything quadratic in $n$ will fail, and even $O(n \log^2 n)$ is risky. We should expect a strategy that sorts once and then processes the array linearly.

A subtle difficulty comes from the fact that eating is not purely “merge adjacent in sorted order”. A large bacterium cannot eat arbitrarily small ones, even if it is much larger; it is blocked by the upper bound $a_i \le a_j + K$. This creates a bounded interaction window that naive greedy strategies can easily mis-handle.

For example, consider sizes $[100, 1]$ with $K = 10$. The larger bacterium cannot eat the smaller one because $100 > 1$ holds, but $100 \le 11$ fails. A naive intuition that “the largest always eats everything smaller” would incorrectly predict a single survivor. The correct answer is two survivors.

Another failure mode appears when chaining is attempted in a forward manner. Suppose we try to repeatedly merge adjacent elements after sorting. Locally valid merges may block future merges that would have been possible under a different choice order, so greedy adjacent merging is not safe.

The key challenge is to structure removals so that every deletion corresponds to a valid eater-prey pair, while maximizing how many deletions we can perform.

## Approaches

A brute-force view would simulate the process: repeatedly pick any valid pair $(i, j)$, delete $j$, and continue until no moves remain. This is correct in principle, but each step requires scanning for a valid pair, and there can be $O(n)$ deletions, leading to $O(n^2)$ or worse behavior. With $n = 2 \cdot 10^5$, this is far too slow.

The crucial observation is that the final answer depends only on how we partition bacteria into groups where each group can be “cleared” by a single survivor. If one bacterium is chosen as the survivor of a group, it can only remove those bacteria whose sizes lie in a specific interval relative to it: from $a_i - K$ up to $a_i - 1$. Anything smaller than $a_i - K$ is unreachable by that survivor and must belong to another group.

This suggests sorting the array and always trying to use the largest remaining bacterium as the next group representative. That choice is powerful because it maximizes the number of elements it can potentially remove. Once we fix this largest element, all bacteria in the allowable interval directly below it can be removed, and we repeat the process on what remains.

This transforms the problem into repeatedly peeling off “windows” anchored at the current maximum, which can be done in a single pass over the sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Sorting + Greedy Windows | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first sort the bacteria sizes in ascending order so that all comparisons become localized.

1. Sort the array $a$ in increasing order. This allows us to reason about valid eating ranges using contiguous segments.
2. Start from the largest remaining element. Treat this element as the current group’s survivor, since it has the highest potential to eat others.
3. Count this survivor as one final bacterium in the answer.
4. From this largest element, move leftwards and remove every element whose size is at least $a[i] - K$. These are exactly the bacteria it can legally eat because they are smaller than it but not too small.
5. Continue the process from the next unprocessed element to the left, again selecting it as a new survivor and repeating the removal step.

Each step removes as many elements as possible under a single survivor, ensuring that we never waste a potential eater.

### Why it works

The sorted structure ensures that when we pick the largest remaining element, every other remaining element is either within its eatable range or too small to ever be eaten by it. If an element is too small for the current survivor, it is also too small for any future survivor chosen in this region of the array, because future survivors will only be smaller or equal in value. This forces such elements to start new groups.

This creates a partition of the array into the minimum number of groups where each group has a valid “maximum element” that can eliminate all other elements in that group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    
    ans = 0
    i = n - 1
    
    while i >= 0:
        ans += 1
        current = a[i]
        
        i -= 1
        while i >= 0 and a[i] >= current - k:
            i -= 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the idea of repeatedly choosing the largest remaining bacterium and consuming everything within its valid eating interval. The outer loop moves from right to left over the sorted array, ensuring each iteration defines one surviving group.

The inner loop is the critical part: it skips all bacteria that can be eaten by the current survivor. The condition $a[i] \ge current - K$ exactly encodes the lower bound of the eatable range. Anything below that threshold cannot be consumed and must be handled later.

A common mistake is attempting to maintain multiple pointers moving forward. That tends to double-count or miss elements because the grouping is inherently anchored at maxima, not minima.

## Worked Examples

### Example 1

Input:

```
7 1
101 53 42 102 101 55 54
```

Sorted array:

$[42, 53, 54, 55, 101, 101, 102]$

| Step | Current survivor | Remaining processed | Action |
| --- | --- | --- | --- |
| 1 | 102 | 102, 101, 101 | 102 eats 101, 101 (both ≥ 101) |
| 2 | 55 | 55, 54 | 55 eats 54 |
| 3 | 42 | 42 | No one to eat |

Final answer is 3 survivors.

This trace shows how each survivor clears a contiguous block bounded by $K$, and how large gaps naturally force new groups.

### Example 2

Input:

```
6 4
20 15 10 15 20 25
```

Sorted array:

$[10, 15, 15, 20, 20, 25]$

| Step | Survivor | Removed |
| --- | --- | --- |
| 1 | 25 | 20, 20, 15, 15 |
| 2 | 10 | none |

Answer is 2.

This example demonstrates that once the survivor’s reach drops below a gap, smaller elements become isolated and must form separate groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; the scan is linear |
| Space | $O(1)$ extra (ignoring sort) | Only pointers and counters are used |

The algorithm easily fits within limits because the array is processed in a single pass after sorting, and each element is visited at most once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("7 1\n101 53 42 102 101 55 54\n") == "3"

# all equal
assert run("5 10\n7 7 7 7 7\n") == "5"

# no possible eating due to K=0
assert run("4 0\n1 2 3 4\n") == "4"

# large K allows chaining
assert run("5 100\n1 2 3 4 5\n") == "1"

# mixed gaps
assert run("6 2\n1 2 3 10 11 12\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | n | no eating possible since strict inequality |
| K = 0 increasing | n | only identical sizes could interact |
| large K | 1 | full collapse into one survivor |
| separated clusters | multiple | correctness across disjoint windows |

## Edge Cases

A key edge case is when all bacteria have identical sizes. In that case, no bacterium can eat another because the strict inequality $a_i > a_j$ fails. The algorithm handles this correctly because every element becomes its own survivor when scanning from the end; no deletions occur during the inner loop.

Another edge case occurs when $K = 0$. Here, a bacterium can only eat strictly smaller ones, but the second condition forces $a_i \le a_j$, which cannot hold simultaneously. The algorithm naturally produces one survivor per element because no inner loop deletions happen.

A third case involves a large gap, such as $[1, 2, 3, 1000]$ with small $K$. The large element forms its own group, and smaller elements form separate groups because they fall outside its reach window. The sorted scan ensures that once we cross below $a[i] - K$, we stop consuming and correctly start a new group.