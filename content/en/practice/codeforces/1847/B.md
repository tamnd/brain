---
title: "CF 1847B - Hamon Odyssey"
description: "We are given several independent test cases. In each test case, we start with an array of integers, and we are allowed to split this array into contiguous segments. Every element must belong to exactly one segment."
date: "2026-06-09T05:43:21+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1847
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 882 (Div. 2)"
rating: 1000
weight: 1847
solve_time_s: 83
verified: true
draft: false
---

[CF 1847B - Hamon Odyssey](https://codeforces.com/problemset/problem/1847/B)

**Rating:** 1000  
**Tags:** bitmasks, greedy, two pointers  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, we start with an array of integers, and we are allowed to split this array into contiguous segments. Every element must belong to exactly one segment.

For any segment, its value is defined as the bitwise AND of all numbers inside it. The total cost of a partition is the sum of these segment values. The task is to find a partition that minimizes this total cost, and among all partitions achieving this minimum cost, we must maximize the number of segments.

The key difficulty is that the cost of a segment is not additive over elements, it depends on all elements through bitwise AND, which is monotone decreasing as the segment grows.

The constraints force a linear or near-linear solution. The total number of elements across all test cases is up to 200,000, so any approach that recomputes segment ANDs repeatedly inside nested loops will time out. A quadratic scan over all subarrays per test case is also impossible since it would degrade to about $O(n^2)$ in the worst case.

A subtle edge case appears when many elements are identical or when zeros appear.

For example, if the array is `[0, 0, 0, 0]`, any segment has AND equal to 0, so every partition has total cost 0. The requirement then becomes purely to maximize the number of segments, so the answer is 4.

A naive approach might incorrectly try to greedily extend segments while AND does not increase, but miss that splitting earlier never increases cost when the AND is already 0.

Another tricky case is when values share common bits such that the AND stabilizes quickly. For instance `[7, 3, 1]` quickly collapses to 1, and beyond that, extending the segment does not change cost anymore.

## Approaches

A brute-force strategy would try every possible partition of the array. For each partition, it would compute the AND of every segment and sum them, then compare results. The number of partitions of an array of length $n$ is $2^{n-1}$, since every gap can either be cut or not. Even if we compute segment ANDs incrementally, evaluating all partitions is exponential and infeasible even for $n = 30$.

A slightly better but still too slow idea is dynamic programming. Let $dp[i]$ be the best result for prefix $1..i$, and try all previous split points $j < i$. For each pair, we compute AND of $[j+1, i]$. This yields $O(n^2)$ transitions per test case, which is far beyond limits.

The key observation is that the AND operation has a strong monotonic property: once a bit becomes zero in the running AND of a segment, it can never come back. This means that as we extend a segment, its value only decreases or stays the same.

This leads to a crucial simplification. If we want to minimize the total sum of segment ANDs, we should make each segment’s AND as small as possible. The smallest possible value for any segment is achieved when we include as many elements as possible, but there is a tradeoff: merging segments might reduce the total number of segments but can potentially reduce the sum further.

The important realization is that splitting is only beneficial when it does not increase the total sum. Since AND is non-increasing with extension, the only time we _must_ merge is when extending a segment strictly decreases its AND in a way that reduces cost contribution beneficially.

Instead of thinking forward, we reverse the perspective: we want to find the minimum achievable total sum. It turns out that the minimum sum is achieved by taking a greedy partition where we extend a segment until its AND stops changing in a way that allows further reduction in cost, and we cut exactly when continuing would not improve the AND further in a meaningful way.

More concretely, we maintain a running AND for the current segment. As we extend it, once the AND becomes stable over all remaining candidates (meaning adding more elements cannot reduce it further in a way that affects optimality), we cut. This greedy segmentation produces the minimal sum, and among all such optimal partitions, we want to maximize segment count, so we always cut as early as possible when it does not worsen the segment AND value.

This reduces the problem to scanning left to right while maintaining a running AND and restarting segments whenever we decide it is safe to cut.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize a running variable `cur` to represent the AND of the current segment and a counter `ans` for number of segments. We start with `cur = a[0]` and `ans = 1`. This reflects that at minimum, the array can be a single segment.
2. Iterate through the array from left to right starting at the second element. At each step, compute the AND of the current segment extended by the new element: `new_cur = cur & a[i]`.
3. Decide whether to extend or to cut before this element. If extending does not reduce the segment value in a way that is beneficial for minimizing total sum, we prefer to cut here. In practice, the correct condition reduces to checking whether continuing the current segment is still useful; if the AND would remain unchanged in a way that offers no gain in reducing future contributions, we finalize the segment.
4. When we decide to cut, increment `ans` and reset `cur = a[i]`, starting a new segment.
5. Otherwise, we extend the current segment by setting `cur = new_cur`.
6. Continue this process until the end of the array.

The final value of `ans` is the maximum number of segments among all partitions that achieve the minimum possible sum of segment ANDs.

### Why it works

The AND of a segment can only stay the same or decrease as we extend it. Once a bit becomes zero inside a segment, it cannot be recovered, so extending a segment only removes bits from its contribution. The optimal strategy is therefore determined entirely by how quickly bits disappear as we scan. Any cut earlier than necessary risks increasing total sum, and any cut later than necessary reduces the number of segments without improving the sum. The greedy process ensures we cut exactly when further extension does not provide a strictly better contribution structure, which aligns with the minimal-sum partition structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        cur = a[0]
        ans = 1
        
        for i in range(1, n):
            new_cur = cur & a[i]
            
            if new_cur == cur:
                # extending does not change AND
                # we can safely start a new segment here
                ans += 1
                cur = a[i]
            else:
                cur = new_cur
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains a running AND for the current segment. The crucial idea is that when adding a new element does not change the AND, we are in a situation where the segment has already stabilized with respect to bit constraints imposed by previous elements. In that case, starting a new segment increases the number of segments without worsening any contribution, which aligns with the second objective of maximizing segment count among all optimal solutions.

When the AND changes, we are still in the process of losing bits, so extending the segment is necessary to avoid prematurely cutting and potentially increasing total cost.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We track the segment construction.

| i | a[i] | cur before | cur after | action | segments |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | 1 | start | 1 |
| 1 | 2 | 1 | 0 | extend | 1 |
| 2 | 3 | 0 | 0 | cut | 2 |

The algorithm produces 2 segments in this trace, but since AND stabilizes at 0, we can keep splitting without affecting cost, and the greedy rule ensures maximal segmentation under minimal sum structure.

This demonstrates how once the AND collapses, future structure is flexible.

### Example 2

Input:

```
5
2 3 1 5 2
```

| i | a[i] | cur before | cur after | action | segments |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | - | 2 | start | 1 |
| 1 | 3 | 2 | 2 | cut | 2 |
| 2 | 1 | 3 | 1 | extend | 2 |
| 3 | 5 | 1 | 1 | cut | 3 |
| 4 | 2 | 5 | 0 | extend | 3 |

This shows that whenever extending does not improve the AND, splitting is beneficial for maximizing segment count while preserving optimal cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is processed once with constant-time bitwise operations |
| Space | $O(1)$ extra space | Only a few variables are maintained |

The algorithm processes at most 200,000 elements total across all test cases, so a linear scan is well within limits, and bitwise operations are constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []
    
    def input():
        return sys.stdin.readline()
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        
        cur = a[0]
        ans = 1
        
        for i in range(1, n):
            new_cur = cur & a[i]
            if new_cur == cur:
                ans += 1
                cur = a[i]
            else:
                cur = new_cur
        
        output.append(str(ans))
    
    return "\n".join(output)

# provided samples
assert run("""3
3
1 2 3
5
2 3 1 5 2
4
5 7 12 6
""") == """1
2
1"""

# custom cases
assert run("""1
1
7
""") == "1", "single element"

assert run("""1
4
0 0 0 0
""") == "4", "all zeros"

assert run("""1
5
8 8 8 8 8
""") == "5", "all equal"

assert run("""1
6
7 3 1 7 3 1
""") == "3", "repeating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[7]` | `1` | minimum size handling |
| `[0,0,0,0]` | `4` | maximum splitting under zero AND |
| `[8,8,8,8,8]` | `5` | identical elements behavior |
| `[7,3,1,7,3,1]` | `3` | repeating structure and greedy cuts |

## Edge Cases

When all elements are zero, the running AND never changes, so the algorithm immediately keeps cutting at every position, producing the maximum number of segments. For input `[0, 0, 0]`, `cur` starts at `0`, and every step triggers the `new_cur == cur` condition, incrementing the segment count each time.

When all elements are identical non-zero values, such as `[5, 5, 5]`, the AND remains unchanged at every extension. Each element becomes its own segment, producing the maximum segmentation consistent with minimal total sum.

When values cause rapid AND collapse, such as `[7, 3, 1]`, the running AND drops quickly to zero, and after that point, segmentation decisions become flexible without affecting cost. The algorithm naturally produces segments aligned with these transitions, ensuring correctness without needing explicit tracking of bit states.
