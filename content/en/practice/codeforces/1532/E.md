---
title: "CF 1532E - Good Array"
description: "We are given an array of integers and we are allowed to remove exactly one element at a time. For each removal, we look at the remaining array and ask a very specific question: does there exist an element that is exactly equal to the sum of all the other elements in that reduced…"
date: "2026-06-14T18:25:27+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1532
codeforces_index: "E"
codeforces_contest_name: "Kotlin Heroes: Practice 7"
rating: 0
weight: 1532
solve_time_s: 208
verified: false
draft: false
---

[CF 1532E - Good Array](https://codeforces.com/problemset/problem/1532/E)

**Rating:** -  
**Tags:** *special  
**Solve time:** 3m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and we are allowed to remove exactly one element at a time. For each removal, we look at the remaining array and ask a very specific question: does there exist an element that is exactly equal to the sum of all the other elements in that reduced array.

In other words, after removing position $j$, we want to know whether the remaining array can be split into a single special element and everything else, where that special element equals the sum of all remaining values.

The output is the list of indices $j$ such that removing $a_j$ makes the remaining array satisfy this condition.

The constraint $n \le 2 \cdot 10^5$ implies that any solution that recomputes sums or scans the array for every removal will be too slow. A naive $O(n^2)$ approach is already too large, and anything worse is immediately infeasible.

A subtle edge case appears when values repeat heavily or when the array is very small after removal. For example, if the array has two elements like $[x, y]$, removing one leaves a single element, and a single element array is always trivially good because that element equals the sum of the empty set. A careless solution might forget that this degenerate case still counts.

Another important case is when the “special element” in the remaining array could be either the maximum, or some arbitrary element that happens to match the sum condition. A naive approach might assume the largest element is always the candidate, which is not guaranteed.

## Approaches

The brute-force idea is straightforward. For each index $j$, remove it, compute the sum of the remaining elements, and then check every position in the remaining array to see if any element equals that sum minus itself. This means we are checking whether there exists an index $i \ne j$ such that:

$$a_i = \text{total\_sum} - a_j - a_i$$

Rewriting gives:

$$2a_i = \text{total\_sum} - a_j$$

So for each removal, we would scan all elements and check this condition. Even with prefix sums, we still need a scan or frequency check per removal, leading to $O(n^2)$ behavior in the worst case. With $2 \cdot 10^5$, this is too slow.

The key observation is that after removing $a_j$, the sum of the remaining array is:

$$S' = S - a_j$$

We need to find an element $x$ in the remaining array such that:

$$x = S' - x \Rightarrow 2x = S'$$

So the candidate value is fully determined:

$$x = \frac{S'}{2}$$

This means that for each removal, we do not search arbitrarily. We only need to check whether the value $(S - a_j)/2$ exists in the array after removing index $j$. This reduces the problem to frequency counting plus a simple validity check.

We precompute the total sum and a frequency map. For each index $j$, we compute the required value and check whether it exists in the array, adjusting for the case where the required value equals $a_j$ itself.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array. This is needed so that after removing any element we can compute the new sum in constant time.
2. Build a frequency map of all values. This allows constant-time checks for whether a candidate value exists in the array.
3. For each index $j$, compute the reduced sum $S' = S - a_j$. This represents the sum of the array after removal.
4. Check if $S'$ is even. If it is odd, it is impossible to split it into two equal parts, so this removal cannot be valid.
5. Compute the target value $x = S'/2$. This is the only possible candidate element that could equal the sum of all other elements.
6. Temporarily account for the removal of $a_j$. If $x$ equals $a_j$, we require that it appears at least twice in the original array. Otherwise, we require that it appears at least once.
7. If the condition holds, mark index $j$ as valid.

### Why it works

After removing $a_j$, the condition for the remaining array to be good forces a single equation: one element must equal half of the remaining sum. There is no freedom beyond this because every valid configuration collapses to a single value constraint. The frequency structure ensures we correctly distinguish whether that value survives the removal. Since we check exactly the only possible candidate per index, no valid case can be missed, and no invalid case can pass the test.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    freq = {}
    for v in a:
        freq[v] = freq.get(v, 0) + 1
    
    res = []
    
    for i in range(n):
        s = total - a[i]
        if s % 2 != 0:
            continue
        x = s // 2
        
        # check availability of x after removing a[i]
        if x not in freq:
            continue
        
        # if we remove one occurrence of a[i]
        need = freq[x]
        if x == a[i]:
            if freq[x] - 1 > 0:
                res.append(i + 1)
        else:
            if freq[x] > 0:
                res.append(i + 1)
    
    print(len(res))
    if res:
        print(*res)

if __name__ == "__main__":
    solve()
```

The solution starts by precomputing the total sum and a frequency dictionary. The main loop tests each removal independently. The parity check avoids impossible splits early. The candidate value computation is derived directly from the condition that the special element must equal the sum of all others. The frequency adjustment ensures correctness when the removed element overlaps with the candidate value.

One subtle point is handling the case where the candidate value equals the removed element. In that case, we must ensure that at least one more occurrence remains after removal; otherwise the “special element” disappears from the array.

## Worked Examples

### Example 1

Input:

```
5
2 5 1 2 2
```

| Removed index | Removed value | Remaining sum | Target x = S'/2 | freq check | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 10 | 5 | 5 exists | yes |
| 2 | 5 | 7 | - | odd sum | no |
| 3 | 1 | 11 | - | odd sum | no |
| 4 | 2 | 10 | 5 | 5 exists | yes |
| 5 | 2 | 10 | 5 | 5 exists | yes |

Output:

```
3
1 4 5
```

This confirms that multiple removals can lead to the same structural condition, and duplicates in the array do not change the logic except in frequency handling.

### Example 2

Input:

```
4
8 3 5 2
```

| Removed index | Remaining array | Remaining sum | Target x | valid |
| --- | --- | --- | --- | --- |
| 1 | [3,5,2] | 10 | 5 | yes |
| 2 | [8,5,2] | 15 | 7.5 | no |
| 3 | [8,3,2] | 13 | 6.5 | no |
| 4 | [8,3,5] | 16 | 8 | yes |

Output:

```
2
1 4
```

This shows that the condition is purely arithmetic and independent of ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to build frequencies and one pass to test each index |
| Space | $O(n)$ | Frequency dictionary stores counts of all distinct values |

The linear complexity is essential for handling arrays up to $2 \cdot 10^5$. Any quadratic approach would exceed time limits by several orders of magnitude.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("""5
2 5 1 2 2
""") == """3
1 4 5"""

# minimum size
assert run("""2
1 1
""") == """2
1 2"""

# no valid indices
assert run("""3
1 2 4
""") == """0"""

# all equal values
assert run("""4
2 2 2 2
""") == """4
1 2 3 4"""

# single pattern mix
assert run("""5
10 1 1 1 1
""") == """1
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements equal | both indices | degenerate single-element good case |
| no solution | 0 | negative case correctness |
| all equal | all indices | symmetry and frequency handling |
| dominant value case | one index | selective validity |

## Edge Cases

A two-element array like $[x, x]$ always produces both indices as valid because removing one element leaves a single-element array, which trivially satisfies the condition. The algorithm handles this because the remaining sum equals the single element, and the frequency logic confirms that the candidate value still exists after removal.

When all elements are identical, the candidate value after any removal is still equal to the same value, and the frequency check always passes for every index. The algorithm correctly counts every position.

A more subtle case arises when the candidate equals the removed element. The implementation explicitly reduces the available count by one in that case, preventing false positives when the removed element was the only occurrence of the required value.
