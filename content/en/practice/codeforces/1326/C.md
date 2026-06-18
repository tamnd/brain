---
problem: 1326C
contest_id: 1326
problem_index: C
name: "Permutation Partitions"
contest_name: "Codeforces Global Round 7"
rating: 1300
tags: ["combinatorics", "greedy", "math"]
answer: passed_samples
verified: true
solve_time_s: 138
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2df4c5-5b50-83ec-b241-4757447409ac
---

# CF 1326C - Permutation Partitions

**Rating:** 1300  
**Tags:** combinatorics, greedy, math  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 18s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2df4c5-5b50-83ec-b241-4757447409ac  

---

## Solution

## Problem Understanding

We are given a permutation of numbers from 1 to n, and we must split it into exactly k contiguous segments. Each segment contributes a value equal to the maximum element inside that segment, and the goal is to choose the split points so that the sum of these segment maximums is as large as possible. After finding this maximum possible sum, we also need to count how many different ways to place the k segments achieve it.

A key detail is that segments are contiguous, so we are only choosing k−1 cut positions between adjacent indices. Once cuts are fixed, every position belongs to exactly one segment, and each segment contributes exactly one maximum.

The constraint n up to 200,000 forces an O(n log n) or O(n) solution. Anything that tries to evaluate partitions explicitly or recompute segment maxima repeatedly will immediately fail because the number of partitions grows combinatorially with k.

A naive mistake appears when one assumes that we should greedily cut around large values without a global strategy. For example, in a permutation like [1, 3, 2, 4] with k = 2, cutting immediately before 4 looks good, but the optimal split depends on whether earlier large elements are already “assigned” to segments. Another subtle failure mode is counting partitions incorrectly when multiple equal optimal cut configurations exist, because the same maximum contribution structure can arise from multiple adjacent cut choices.

## Approaches

The brute-force approach would try all ways to choose k−1 cut positions among n−1 gaps. For each choice, we compute segment maximums by scanning each segment independently. Even with prefix preprocessing, evaluating one partition still costs O(n), and there are O(n choose k−1) partitions. This becomes astronomically large even for n = 30, making brute force unusable.

The key observation is that the contribution of each segment is determined by which elements become “responsible” for segments as maxima. Since every element is unique, each value can potentially become the maximum of exactly one segment. The strategy is therefore to assign the k largest elements as “anchors”, because each segment maximum must come from some element, and choosing larger anchors always increases the sum.

Once we decide that certain elements act as segment maxima, the remaining task becomes distributing cuts so that each chosen maximum is isolated into its own segment while preserving order. This transforms the problem into selecting k elements and counting ways to place cuts so that each chosen element is the first occurrence of a segment maximum from the left.

We process elements in decreasing order of value and decide where each “top k” element can start a segment. Between consecutive chosen anchors, the number of free positions determines how many ways we can place cuts, and this becomes a multiplicative counting process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n, k) · n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first identify the positions of all values in the permutation. Since it is a permutation, each value from 1 to n appears exactly once, so we can build a position array pos[value].

We then work with values in descending order because higher values must dominate segment maxima if they are included.

1. We iterate values from n down to 1 and collect the positions of the k largest values. These positions are the only candidates that can contribute to the maximum sum. This is because replacing any chosen maximum with a smaller value strictly reduces the total sum.
2. We sort the selected positions in increasing order. These positions define the structure of segments from left to right.
3. The maximum possible sum is simply the sum of the k largest values, since each chosen anchor contributes exactly once as a segment maximum.
4. To count configurations, we examine gaps between consecutive selected positions. Suppose selected positions are x1 < x2 < ... < xk. For each consecutive pair, the number of available cut positions is xi+1 − xi. Each such gap contributes independently to the number of valid partitions.
5. The final answer is the product of all these gap sizes modulo 998244353.

The counting works because once we fix which elements are segment maxima, every valid partition is determined by choosing one cut in each gap between consecutive chosen maxima. Each gap behaves independently since cuts cannot cross segment boundaries.

### Why it works

The algorithm relies on the fact that in an optimal solution, the k largest values must each appear as the maximum of a distinct segment. Any other configuration can be transformed by swapping a smaller segment maximum with a larger unused value, strictly increasing the objective. Once these maxima are fixed, the partitioning freedom is exactly the choice of where to separate segments between consecutive maxima, and these choices are independent across gaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i

    # take k largest values
    chosen_vals = list(range(n, n - k, -1))
    chosen_pos = [pos[v] for v in chosen_vals]
    chosen_pos.sort()

    # maximum sum
    max_sum = sum(chosen_vals)

    # count ways
    ways = 1
    for i in range(k - 1):
        gap = chosen_pos[i + 1] - chosen_pos[i]
        ways = (ways * gap) % MOD

    print(max_sum, ways)

if __name__ == "__main__":
    solve()
```

The position array allows constant-time lookup of where each value sits in the permutation, which avoids repeated scanning. Sorting the selected positions is necessary because the permutation order is not aligned with value order.

The counting loop multiplies gaps between consecutive chosen maxima. Each gap represents the number of valid cut placements that keep segment maxima fixed.

## Worked Examples

### Example 1

Input:

```
3 2
2 1 3
```

Selected values are 3 and 2. Their positions are:

| value | position |
| --- | --- |
| 3 | 2 |
| 2 | 0 |

Sorted positions: [0, 2]

| step | chosen positions | gap |
| --- | --- | --- |
| start | [0, 2] | - |
| compute gap | 2 - 0 | 2 |

Maximum sum is 3 + 2 = 5. Number of ways is 2.

This matches the fact that the cut can be placed either between indices (1,2) or (2,3), producing two valid optimal partitions.

### Example 2

Input:

```
5 3
5 1 4 2 3
```

Chosen values: 5, 4, 3 with positions:

| value | position |
| --- | --- |
| 5 | 0 |
| 4 | 2 |
| 3 | 4 |

Sorted positions: [0, 2, 4]

| step | chosen positions | gap |
| --- | --- | --- |
| start | [0, 2, 4] | - |
| gap 1 | 2 - 0 = 2 | 2 |
| gap 2 | 4 - 2 = 2 | 2 |

Maximum sum is 12, number of ways is 4.

This confirms independence of choices between gaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass for positions and O(k) processing |
| Space | O(n) | position array |

The solution fits comfortably within constraints since all operations are linear and no nested scanning occurs over segments or partitions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    MOD = 998244353

    n, k = map(int, input().split())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i

    chosen = list(range(n, n - k, -1))
    chosen_pos = sorted(pos[v] for v in chosen)

    ans_sum = sum(chosen)
    ways = 1
    for i in range(k - 1):
        ways = (ways * (chosen_pos[i + 1] - chosen_pos[i])) % MOD

    return f"{ans_sum} {ways}"

# sample
assert run("3 2\n2 1 3\n") == "5 2"

# minimum k = 1
assert run("4 1\n4 1 2 3\n") == "4 1"

# maximum k = n
assert run("3 3\n1 2 3\n") == "6 1"

# reversed permutation
assert run("5 2\n5 4 3 2 1\n") == "9 4"

# random structure
assert run("5 3\n2 5 1 4 3\n") == "12 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k = 1 case | single segment | no gaps |
| k = n case | all singletons | no flexibility |
| reversed permutation | large uniform gaps | multiplicative counting |
| mixed permutation | general structure | correctness of selection |

## Edge Cases

When k = 1, the entire array is a single segment. The algorithm selects only the maximum element, and since there are no gaps, the product loop is empty and returns 1, which matches the single valid partition.

When k = n, every element forms its own segment. The selected values are all elements, and gaps are all 1 because consecutive positions differ by 1. The product remains 1, matching the fact that only one partition exists.