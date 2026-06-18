---
problem: 980C
contest_id: 980
problem_index: C
name: "Posterized"
contest_name: "Codeforces Round 480 (Div. 2)"
rating: 1700
tags: ["games", "greedy"]
answer: passed_samples
verified: true
solve_time_s: 67
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a56a-75ec-83ec-8c82-16909b3df43c
---

# CF 980C - Posterized

**Rating:** 1700  
**Tags:** games, greedy  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 7s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a56a-75ec-83ec-8c82-16909b3df43c  

---

## Solution

## Problem Understanding

We are given a sequence of pixel intensities, each an integer between 0 and 255. The task is to “simplify” this sequence by first partitioning the entire value range $[0, 255]$ into contiguous segments. Each segment has length at most $k$, and every integer in the range must belong to exactly one segment. For each segment, we choose a representative value called its key. After that, every pixel value is replaced by the key of the segment it belongs to.

The final output is the transformed pixel array. Among all valid ways to partition the range and choose keys, we want the lexicographically smallest resulting array.

The important interaction is that the transformation depends only on the segmentation of values, not on positions in the array. Once we decide which value maps to which key, all occurrences of that value are replaced consistently.

The constraints are small on the value domain (only 256 possible colors), but large on the array length $n \le 10^5$. This immediately suggests that any solution should precompute a mapping for all 256 values and then apply it in linear time over the array.

A naive approach would try all segmentations of $[0,255]$. Since each segment has length at most $k$, this becomes a combinatorial partitioning problem with exponential choices. Even though 256 is small, branching over all possible segment boundaries still leads to an explosion in possibilities.

A second naive idea is to greedily choose a partition that minimizes the transformed array without considering global interactions. This is where subtle failures happen: early decisions about segment boundaries affect future keys, and a locally optimal choice can increase the lexicographic value later.

A typical failing scenario comes from choosing a segment key that is not the minimum in its block. For example, if we group $[2,3,4]$ with key $3$, but we could have chosen key $2$, then every occurrence of 2 becomes worse in lexicographic order. Even if later segments improve other positions, lexicographic order is decided at the first differing index.

So the key difficulty is: segment boundaries and chosen keys must be coordinated to optimize lexicographic order globally.

## Approaches

The brute-force approach would enumerate every valid partition of $[0,255]$ into segments of length at most $k$. For each partition, we would try every possible choice of a key inside each segment and compute the resulting mapping for all 256 values, then apply it to the array and compare results lexicographically. Even if we only consider segmentations, the number of ways to cut a 256-length array with maximum block size $k$ grows exponentially in 256, making this infeasible.

The key observation is that the value domain is fixed and small, so we should not think in terms of positions in the array but in terms of mapping each value $v \in [0,255]$ to its final representative. Once this mapping is fixed, constructing the output is straightforward.

Now consider how lexicographic order of the final array behaves. The earliest position in the array that differs depends entirely on the smallest pixel value that gets a different mapped result. This suggests that smaller values should be handled as early and as favorably as possible.

Within any segment, choosing a larger key can only make values worse or equal compared to choosing a smaller key inside the same segment. Therefore, for a fixed segment, the best choice is always its minimum value.

This reduces the problem to choosing only segment boundaries. Each segment $[l, r]$ (with $r - l + 1 \le k$) maps every value in it to $\min(l, r)$ is incorrect; instead, it maps to $\min$ of values present in that segment conceptually, but since all integers exist in the range, the best representative is simply $l$. So each segment becomes a block where all values map to its left endpoint.

Now we must choose where to cut the range. The greedy strategy is to always take the largest possible segment starting from 0 that improves lexicographic order earliest. But the crucial simplification is even stronger: we can decide mapping for each value in increasing order, always ensuring that we extend a segment as far as possible up to size $k$, because delaying a cut only forces larger values to share a smaller representative earlier, which is always lexicographically optimal.

This leads to a simple greedy: we walk through values 0 to 255, assign each value to the current segment, and whenever the segment reaches size $k$, we start a new one. Each segment’s key is its first value.

This produces a fixed mapping of all 256 values, and then we apply it to the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force partitions | Exponential | O(1) | Too slow |
| Greedy fixed-size segmentation | O(256 + n) | O(256) | Accepted |

## Algorithm Walkthrough

We build a mapping from each value $0 \ldots 255$ to its final compressed value.

1. Initialize an empty mapping array `mp` of size 256. Set a variable `start = 0`, which marks the beginning of the current segment.
2. Iterate through values `v` from 0 to 255.
3. Assign `mp[v] = start`, meaning all values in the current segment map to the segment start.
4. If we have assigned $k$ values since the last segment start, we move `start = v + 1`, beginning a new segment.

This ensures each segment has size at most $k$, and we always choose the earliest possible representative.
5. After processing all values, we have a complete mapping for every possible pixel intensity.
6. Transform the input array by replacing each value `p[i]` with `mp[p[i]]`.

The reason this works is that once a value is assigned to a segment starting at `start`, assigning it any larger representative would only increase the value in the final array at all positions where it appears. Since lexicographic order is decided from left to right, making any early value larger cannot be compensated later. The greedy segmentation ensures we never delay a boundary in a way that could increase earlier mapped values.

The invariant is that for every processed prefix of values, the mapping is already optimal for all arrays that contain only those values, because each segment always uses the smallest possible representative and never exceeds size $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    mp = [0] * 256
    
    start = 0
    cnt = 0
    
    for v in range(256):
        mp[v] = start
        cnt += 1
        if cnt == k:
            start = v + 1
            cnt = 0
    
    res = [str(mp[x]) for x in arr]
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The code first builds the mapping over the fixed domain of 256 possible pixel values. The variable `start` tracks the left boundary of the current segment. Every time we assign `k` values to a segment, we reset `start` to begin a new block.

The transformation step is direct: each pixel is replaced by its precomputed mapped value in constant time.

A subtle point is that we never need to explicitly store segment ranges. The pair `(start, cnt)` implicitly defines the current segment. Also, we do not need to worry about ending exactly at 255 with a full segment, because partial segments are allowed and automatically handled.

## Worked Examples

### Example 1

Input:

```
4 3
2 14 3 4
```

We compute mapping over values:

| v | start | cnt | mp[v] |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 0 |
| 1 | 0 | 2 | 0 |
| 2 | 0 | 3 → reset | 0 |
| 3 | 3 | 1 | 3 |
| 4 | 3 | 2 | 3 |
| 5 | 3 | 3 → reset | 3 |
| ... | ... | ... | ... |
| 12 | 12 | 1 | 12 |
| 13 | 12 | 2 | 12 |
| 14 | 12 | 3 | 12 |

Applying mapping:

```
2 → 0
14 → 12
3 → 3
4 → 3
```

Output:

```
0 12 3 3
```

This confirms that each value is mapped to the start of its segment.

### Example 2

Input:

```
5 2
0 1 2 3 4
```

Mapping:

| v | mp[v] |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 2 | 2 |
| 3 | 2 |
| 4 | 4 |

Output:

```
0 0 2 2 4
```

This shows how smaller segments force earlier grouping and produce a lexicographically minimal sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 256) | One pass over value range and one over input array |
| Space | O(256) | Fixed mapping array |

The solution comfortably fits constraints since the heavy computation is independent of $n$, and the array processing is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    mp = [0] * 256
    start = 0
    cnt = 0
    for v in range(256):
        mp[v] = start
        cnt += 1
        if cnt == k:
            start = v + 1
            cnt = 0
    
    return " ".join(str(mp[x]) for x in arr)

# provided sample
assert run("4 3\n2 14 3 4\n") == "0 12 3 3"

# all equal
assert run("5 2\n7 7 7 7 7\n") == "6 6 6 6 6"

# k = 1 (identity mapping)
assert run("3 1\n1 2 3\n") == "1 2 3"

# maximum k
assert run("4 256\n0 100 200 255\n") == "0 0 0 0"

# boundary around segment break
assert run("6 3\n0 1 2 3 4 5\n") == "0 0 0 3 3 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 | identity | no compression allowed |
| k=256 | single segment | full collapse |
| consecutive break | grouped blocks | boundary correctness |
| all equal | stability | uniform mapping |

## Edge Cases

A key edge case is when $k = 1$. The algorithm forces every value to start a new segment immediately, so `mp[v] = v`. This produces the identity mapping, which is correct because no two distinct values can share a group.

Another case is $k = 256$, where the entire range becomes a single segment. Here all values map to 0, since the segment starts at 0 and never resets. The algorithm correctly produces a fully flattened array.

A more subtle case is when values in the input are sparse, for example only large values like 200 to 210. The mapping is still determined globally over the full range 0 to 255, so these values may fall into different segments than expected. The algorithm still works because segmentation is fixed independently of input distribution, which is required by the problem definition.