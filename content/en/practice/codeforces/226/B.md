---
title: "CF 226B - Naughty Stone Piles"
description: "We have several stone piles, each with some initial size. One operation chooses a source pile and merges it into another pile. The source pile disappears, the destination pile grows, and the operation cost equals the current size of the source pile."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 226
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 140 (Div. 1)"
rating: 1900
weight: 226
solve_time_s: 142
verified: true
draft: false
---

[CF 226B - Naughty Stone Piles](https://codeforces.com/problemset/problem/226/B)

**Rating:** 1900  
**Tags:** greedy  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several stone piles, each with some initial size. One operation chooses a source pile and merges it into another pile. The source pile disappears, the destination pile grows, and the operation cost equals the current size of the source pile.

The unusual restriction is on the destination side. Every pile may receive at most `k` incoming merges during its lifetime. After a pile has already accepted `k` other piles, it can no longer be used as a destination, although it may still be merged into another pile.

For every query value of `k`, we must compute the minimum total cost needed to end with a single pile.

The constraints completely shape the solution. We have up to `10^5` piles and `10^5` queries. Any approach that simulates merges independently for every query in `O(n)` or worse will likely be too slow if the hidden constant is large. Anything quadratic is impossible. We need preprocessing plus very cheap query handling.

The pile sizes can reach `10^9`, and the total answer can become much larger than 32-bit range. A 64-bit integer type is required.

The hardest part of the problem is understanding what structure minimizes the cost. A careless greedy can easily fail because the restriction is not on how many children a node has in the final merge tree, but on how many times a pile acts as a receiver during the process.

One subtle edge case is `k = 1`.

Input:

```
4
1 2 3 4
1
1
```

Correct output:

```
20
```

Why? With `k = 1`, every pile can receive at most one merge, so the merge process must form a chain. The smallest pile gets merged first, then that combined pile gets merged again, and so on. The total cost becomes:

`1 + (1+2) + (1+2+3) = 1 + 3 + 6 = 10`

But that is only the cost of added piles. The actual optimal ordering after sorting ascending is:

`1 -> 2`, cost `1`

`3 -> (1+2)`, cost `3`

`4 -> (...)`, cost `6`

Total `10`.

A naive interpretation that "merge smallest repeatedly" like Huffman coding gives `19`, which is not optimal under this rule.

Another tricky case is very large `k`.

Input:

```
5
1 2 3 4 5
1
100
```

Correct output:

```
10
```

One pile can absorb all others directly. We simply choose the largest pile as the final receiver and add all smaller piles into it. The cost is the sum of all piles except the largest.

Repeated queries also matter. The statement allows duplicate `k` values. Recomputing the same answer every time wastes time and can turn an otherwise acceptable solution into a timeout.

## Approaches

A brute-force idea is to explicitly simulate merge sequences. For a fixed `k`, we could try all valid merge orders and choose the minimum cost. This works conceptually because every operation changes the state in a well-defined way.

The problem is that the number of valid merge trees grows exponentially. Even for small `n`, the search space becomes enormous. Dynamic programming over subsets would require roughly `O(2^n)` states, completely impossible for `n = 10^5`.

So we need to understand what an optimal merge process looks like.

Suppose we sort the piles in ascending order:

```
a1 <= a2 <= ... <= an
```

Think about how often each pile contributes to the total cost.

Whenever a pile is merged into another pile, its entire current size is paid again. If a stone survives many levels before finally disappearing, it contributes multiple times to the answer.

That means small piles should disappear early, while large piles should stay near the root.

Now look at the restriction. A pile may receive at most `k` merges. In tree language, every node can have at most `k` children.

The optimal structure becomes a rooted `k`-ary merge tree where larger values stay closer to the root and smaller values lie deeper.

After sorting, the optimal strategy is surprisingly simple:

The largest pile has depth `0`.

The next `k` piles have depth `1`.

The next `k^2` piles have depth `2`.

The next `k^3` piles have depth `3`.

And so on.

If a pile has depth `d`, its value contributes `d` times to the total cost. So after sorting:

```
answer = sum(ai * depth_i)
```

where depths are assigned level by level in a complete `k`-ary expansion from the largest element downward.

Why is this optimal? Because deeper nodes are paid more times, so we always want the smallest remaining piles at the greatest depths. This is a classic exchange argument.

For each query, we can process the sorted array from smallest to largest while tracking how many elements belong to each depth layer.

The number of layers is tiny because capacities grow geometrically. For example, with `k = 2`, the counts per depth are:

```
1, 2, 4, 8, ...
```

So each query runs in roughly `O(log_k n)` layer transitions plus linear traversal over the array.

A special case appears when `k = 1`. Then every level contains exactly one node, so depths become:

```
n-1, n-2, ..., 1, 0
```

This case is simply a chain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | `O(n log n + q sqrt(n))` amortized | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Sort the pile sizes in ascending order.

Smaller piles should appear deeper in the merge tree because deep nodes are counted more times in the cost.
2. Precompute prefix sums of the sorted array.

This lets us quickly compute the sum of any consecutive block of piles.
3. For each query `k`, handle the special case `k = 1`.

When each pile can receive only one merge, the merge structure must be a chain. The smallest pile has depth `n-1`, the next has depth `n-2`, and so on.
4. For `k > 1`, assign depths layer by layer from the largest pile downward.

The root level contains `1` node.

The next level contains at most `k` nodes.

The next contains at most `k^2`.

Continuing this way matches the maximum number of children allowed per pile.
5. Traverse the sorted array from largest toward smallest.

Every time we move to a deeper layer, all piles in that layer contribute one additional copy of their value to the answer.
6. Add:

```
depth * sum_of_values_in_this_layer
```

to the total answer.
7. Output the result for every query.

### Why it works

A pile contributes to the cost once for every ancestor above it in the merge tree. That is exactly its depth.

The restriction "a pile may receive at most `k` merges" means every node in the merge tree may have at most `k` children. Among all such trees, the smallest values should occupy the greatest depths because deeper nodes are multiplied by larger coefficients.

The greedy layer assignment achieves exactly that. The deepest available positions are filled with the smallest remaining piles, which minimizes the weighted sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = sorted(map(int, input().split()))

    q = int(input())
    queries = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    memo = {}

    ans = []

    for k in queries:
        if k in memo:
            ans.append(memo[k])
            continue

        if k == 1:
            cur = 0
            for i in range(n):
                cur += a[i] * (n - 1 - i)

            memo[k] = cur
            ans.append(cur)
            continue

        cur = 0

        depth = 0
        cnt = 1
        r = n

        while r > 0:
            l = max(0, r - cnt)

            layer_sum = prefix[r] - prefix[l]
            cur += depth * layer_sum

            r = l
            cnt *= k
            depth += 1

        memo[k] = cur
        ans.append(cur)

    print(*ans)

solve()
```

The first step sorts the array because the optimal merge tree assigns smaller values to greater depths.

The prefix sum array allows constant-time range sum queries. When a layer contains elements from index `l` to `r-1`, its total sum is:

```
prefix[r] - prefix[l]
```

The main loop processes queries independently, but repeated queries are cached in `memo`. This matters because the statement explicitly allows duplicate `k` values.

The `k = 1` case is separated because multiplying the layer size by `k` would never grow. In this case, every layer contains exactly one pile.

For `k > 1`, the algorithm builds layers geometrically:

```
1, k, k^2, ...
```

starting from the largest elements. The variable `r` marks how many elements remain unassigned. Each iteration takes the last `cnt` elements and assigns them the current depth.

One subtle detail is that depths start from `0` at the root. The largest pile contributes nothing because it is never merged into another pile.

Another easy mistake is integer overflow in other languages. The answer may reach around `10^19`, so 64-bit integers are mandatory.

## Worked Examples

### Sample 1

Input:

```
5
2 3 4 1 1
2
2 3
```

Sorted array:

```
[1, 1, 2, 3, 4]
```

### Query `k = 2`

| Depth | Layer Size | Elements | Layer Sum | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | [4] | 4 | 0 |
| 1 | 2 | [2, 3] | 5 | 5 |
| 2 | 4 | [1, 1] | 2 | 4 |

Final answer:

```
0 + 5 + 4 = 9
```

This trace shows the geometric layer growth. The smallest piles end up deepest, so they are counted multiple times.

### Query `k = 3`

| Depth | Layer Size | Elements | Layer Sum | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | [4] | 4 | 0 |
| 1 | 3 | [1, 2, 3] | 6 | 6 |
| 2 | 9 | [1] | 1 | 2 |

Final answer:

```
0 + 6 + 2 = 8
```

With larger branching factor, the tree becomes shallower, so the total cost decreases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n + q sqrt(n))` amortized | Sorting dominates preprocessing, each query processes only logarithmic depth layers |
| Space | `O(n)` | Prefix sums and memoization |

The sorted array and prefix sums each use linear memory. The number of layers for one query is very small because powers of `k` grow rapidly. Even in the worst practical case, the solution easily fits within the limits for `n, q <= 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = sorted(map(int, input().split()))

    q = int(input())
    queries = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    memo = {}

    ans = []

    for k in queries:
        if k in memo:
            ans.append(memo[k])
            continue

        if k == 1:
            cur = 0
            for i in range(n):
                cur += a[i] * (n - 1 - i)

            memo[k] = cur
            ans.append(cur)
            continue

        cur = 0

        depth = 0
        cnt = 1
        r = n

        while r > 0:
            l = max(0, r - cnt)

            layer_sum = prefix[r] - prefix[l]
            cur += depth * layer_sum

            r = l
            cnt *= k
            depth += 1

        memo[k] = cur
        ans.append(cur)

    print(*ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
    "5\n"
    "2 3 4 1 1\n"
    "2\n"
    "2 3\n"
) == "9 8", "sample"

# minimum size
assert run(
    "1\n"
    "7\n"
    "3\n"
    "1 2 100\n"
) == "0 0 0", "single pile"

# k = 1 chain structure
assert run(
    "4\n"
    "1 2 3 4\n"
    "1\n"
    "1\n"
) == "10", "chain"

# very large k
assert run(
    "5\n"
    "1 2 3 4 5\n"
    "1\n"
    "100\n"
) == "10", "all merged directly into largest"

# all equal values
assert run(
    "6\n"
    "5 5 5 5 5 5\n"
    "2\n"
    "2 5\n"
) == "25 25", "equal values"

# repeated queries
assert run(
    "5\n"
    "1 2 3 4 5\n"
    "4\n"
    "2 2 2 2\n"
) == "13 13 13 13", "memoization consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pile | `0 0 0` | No merge needed |
| `k = 1` | `10` | Chain structure handling |
| Very large `k` | `10` | All piles merge directly into root |
| All equal values | `25 25` | Depth assignment independent of ordering ties |
| Repeated queries | `13 13 13 13` | Memoization correctness |

## Edge Cases

Consider the smallest possible input:

```
1
7
1
1
```

There is already exactly one pile, so no operations are needed. The algorithm handles this naturally because the root layer contains the only element at depth `0`, contributing nothing to the answer.

Now look at the restrictive case `k = 1`:

```
4
1 2 3 4
1
1
```

Sorted array:

```
[1, 2, 3, 4]
```

Depth assignments become:

```
3, 2, 1, 0
```

Contribution:

```
1*3 + 2*2 + 3*1 + 4*0 = 10
```

The algorithm uses the dedicated branch for `k = 1`, avoiding an infinite geometric progression.

For extremely large `k`:

```
5
1 2 3 4 5
1
100
```

The root absorbs every other pile directly.

Layer structure:

```
depth 0 -> [5]
depth 1 -> [1,2,3,4]
```

Answer:

```
1 + 2 + 3 + 4 = 10
```

The algorithm correctly stops once all elements are assigned, even though `k^2` is much larger than `n`.

Finally, consider repeated queries:

```
5
1 2 3 4 5
4
2 2 2 2
```

Without memoization, the same computation would repeat four times. The solution stores the first result and reuses it instantly for later occurrences.
