---
title: "CF 242B - Big Segment"
description: "We are given several segments on a number line. Each segment has a left endpoint and a right endpoint. The task is to determine whether one of these segments completely contains every other segment."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 242
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 149 (Div. 2)"
rating: 1100
weight: 242
solve_time_s: 527
verified: true
draft: false
---

[CF 242B - Big Segment](https://codeforces.com/problemset/problem/242/B)

**Rating:** 1100  
**Tags:** implementation, sortings  
**Solve time:** 8m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several segments on a number line. Each segment has a left endpoint and a right endpoint. The task is to determine whether one of these segments completely contains every other segment.

If segment `[L, R]` is the answer, then for every other segment `[l, r]`, we must have:

$$L \le l \le r \le R$$

We must print the index of such a segment using the original input order. If no segment covers all others, we print `-1`.

The constraints are large enough to matter. There can be up to $10^5$ segments, so any algorithm that compares every pair of segments directly will perform about $10^{10}$ checks in the worst case, which is far too slow for a 2-second limit. We need either linear or near-linear work.

The coordinates themselves can be as large as $10^9$, but that does not create difficulty because we never need to build arrays over the coordinate range. We only compare endpoints.

Several edge cases are easy to mishandle.

Consider completely disjoint segments:

```
3
1 1
2 2
3 3
```

No segment contains the others, so the answer is:

```
-1
```

A careless implementation that only checks for the largest length might incorrectly choose `[1,1]`, `[2,2]`, or `[3,3]`.

Another tricky case is when the covering segment appears in the middle of the input:

```
3
2 5
1 10
3 4
```

The correct answer is:

```
2
```

The algorithm cannot assume the first segment is special.

Nested segments also require careful boundary handling:

```
3
1 5
1 4
2 5
```

The correct answer is:

```
1
```

The segment `[1,5]` contains both others. Using strict inequalities instead of inclusive comparisons would incorrectly reject it.

Finally, the problem guarantees that no two segments are identical. Without that guarantee, multiple valid answers could exist. Here, if a covering segment exists, it is unique.

## Approaches

The brute-force solution is straightforward. For every segment, we check whether it contains every other segment. Segment `i` is valid if:

$$l_i \le l_j \quad \text{and} \quad r_j \le r_i$$

for all `j`.

This works because the definition of containment is direct. If we test all pairs, we cannot miss the correct answer.

The problem is the running time. With $n = 10^5$, checking every pair requires roughly:

$$10^5 \times 10^5 = 10^{10}$$

comparisons. That is several orders of magnitude too slow.

The key observation is that a segment covering all others must have:

1. The smallest left endpoint among all segments.
2. The largest right endpoint among all segments.

If a segment starts later than some other segment, it cannot contain that segment. If it ends earlier than some other segment, it also fails immediately.

This transforms the problem into a simple search. We compute:

$$\text{minLeft} = \min(l_i)$$

$$\text{maxRight} = \max(r_i)$$

Then we look for a segment exactly equal to:

$$[\text{minLeft}, \text{maxRight}]$$

If such a segment exists, it contains every segment. Otherwise, no valid answer exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all segments one by one.

While reading, keep track of the smallest left endpoint and the largest right endpoint seen so far.
2. Store each segment together with its original index.

The output must use 1-based input order, so we cannot lose that information.
3. After processing all segments, iterate through the stored segments again.

We check whether a segment has:

$$l_i = \text{minLeft}$$

and

$$r_i = \text{maxRight}$$
4. If such a segment exists, print its index immediately.

Any segment with both extreme endpoints automatically covers every other segment.
5. If no segment matches both extremes, print `-1`.

### Why it works

Suppose a segment covers all others.

Since it contains every segment, its left endpoint must be less than or equal to every other left endpoint. That means it is the global minimum left endpoint.

Similarly, its right endpoint must be greater than or equal to every other right endpoint. That means it is the global maximum right endpoint.

So any valid answer must equal `[minLeft, maxRight]`.

Conversely, if a segment equals `[minLeft, maxRight]`, then every other segment starts no earlier and ends no later, so all of them are contained inside it.

These two directions prove the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    segments = []

    min_left = 10**18
    max_right = -1

    for i in range(1, n + 1):
        l, r = map(int, input().split())

        segments.append((l, r, i))

        min_left = min(min_left, l)
        max_right = max(max_right, r)

    for l, r, idx in segments:
        if l == min_left and r == max_right:
            print(idx)
            return

    print(-1)

solve()
```

The first loop reads all segments while maintaining the two global extremes. This avoids any extra passes over the data.

The list `segments` stores `(l, r, index)` so we can later recover the original numbering required by the problem statement.

The second loop searches for the unique segment matching both extremes. The moment we find it, we print its index and terminate.

The comparisons must be inclusive. A segment `[1,5]` does contain `[1,4]` and `[2,5]`, so using strict `<` or `>` would introduce incorrect rejections.

Python integers safely handle the endpoint limits, so overflow is never a concern.

## Worked Examples

### Example 1

Input:

```
3
1 1
2 2
3 3
```

Trace:

| Step | Segment | min_left | max_right |
| --- | --- | --- | --- |
| 1 | [1,1] | 1 | 1 |
| 2 | [2,2] | 1 | 2 |
| 3 | [3,3] | 1 | 3 |

Second pass:

| Segment | Matches [1,3]? |
| --- | --- |
| [1,1] | No |
| [2,2] | No |
| [3,3] | No |

Output:

```
-1
```

This example shows that having either the minimum left endpoint or the maximum right endpoint alone is not enough. A valid segment must have both.

### Example 2

Input:

```
4
2 5
1 10
3 4
5 7
```

Trace:

| Step | Segment | min_left | max_right |
| --- | --- | --- | --- |
| 1 | [2,5] | 2 | 5 |
| 2 | [1,10] | 1 | 10 |
| 3 | [3,4] | 1 | 10 |
| 4 | [5,7] | 1 | 10 |

Second pass:

| Segment | Matches [1,10]? |
| --- | --- |
| [2,5] | No |
| [1,10] | Yes |

Output:

```
2
```

This trace demonstrates the core invariant. Once `[1,10]` becomes the segment with the smallest left endpoint and largest right endpoint, it must contain every other segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute extremes, one pass to find the answer |
| Space | O(n) | Stores all segments with indices |

With $10^5$ segments, linear processing is easily fast enough within the 2-second limit. The memory usage is also small because we only store a few integers per segment.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        segments = []

        min_left = 10**18
        max_right = -1

        for i in range(1, n + 1):
            l, r = map(int, input().split())

            segments.append((l, r, i))

            min_left = min(min_left, l)
            max_right = max(max_right, r)

        for l, r, idx in segments:
            if l == min_left and r == max_right:
                return str(idx)

        return "-1"

    return solve()

# provided sample
assert run(
"""3
1 1
2 2
3 3
""") == "-1", "sample 1"

# minimum size input
assert run(
"""1
5 5
""") == "1", "single segment always works"

# covering segment in the middle
assert run(
"""3
2 5
1 10
3 4
""") == "2", "middle segment covers all"

# nested boundary case
assert run(
"""3
1 5
1 4
2 5
""") == "1", "inclusive boundaries"

# no covering segment
assert run(
"""4
1 3
2 5
4 6
7 8
""") == "-1", "disjoint structure"

# large coordinate values
assert run(
"""2
1 1000000000
2 999999999
""") == "1", "large endpoints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single segment | 1 | Minimum-size input |
| Covering segment in middle | 2 | Correct original indexing |
| Nested boundary case | 1 | Inclusive containment logic |
| Disjoint structure | -1 | Rejects partial overlap |
| Large coordinates | 1 | Handles large endpoint values correctly |

## Edge Cases

Consider completely disjoint segments:

```
3
1 1
2 2
3 3
```

The algorithm computes:

$$\text{minLeft} = 1$$

$$\text{maxRight} = 3$$

No segment equals `[1,3]`, so the answer is `-1`.

This correctly rejects cases where no segment spans the full range covered collectively by all segments.

Now consider a covering segment that is not first:

```
3
2 5
1 10
3 4
```

After scanning all segments:

$$\text{minLeft} = 1$$

$$\text{maxRight} = 10$$

The second segment matches these values exactly, so the algorithm prints `2`.

The solution does not depend on input order.

Finally, consider boundary sharing:

```
3
1 5
1 4
2 5
```

The extreme values are still `1` and `5`.

The first segment matches `[1,5]`, so it is returned.

This confirms the algorithm handles inclusive containment correctly. Segments touching at endpoints are still considered covered.
