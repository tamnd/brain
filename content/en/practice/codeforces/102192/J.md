---
title: "CF 102192J - Taotao Picks Apples"
description: "We scan the apple heights from left to right. The first apple is always picked. After that, an apple is picked only when its height is strictly larger than the height of the most recently picked apple. Thus the picked heights form a strictly increasing sequence of prefix maxima."
date: "2026-08-18T02:11:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "J"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 155
verified: true
draft: false
---

[CF 102192J - Taotao Picks Apples](https://codeforces.com/problemset/problem/102192/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We scan the apple heights from left to right. The first apple is always picked. After that, an apple is picked only when its height is strictly larger than the height of the most recently picked apple. Thus the picked heights form a strictly increasing sequence of prefix maxima.

Each query is independent. It changes exactly one position `p` from its original height `h[p]` to `q`, then asks how many apples would be picked in the resulting array. The original array is restored before the next query. The problem and the official contest solution describe this as maintaining the information needed on the two sides of the modified position.

The values of `n` and `m` can both reach `100000`, and there can be up to ten test cases. A direct simulation of every query would require up to `10^10` array inspections in one test case when every query scans almost the entire array. That is far beyond what a 2-second limit can support. We need preprocessing close to linear or `O(n log n)`, followed by roughly logarithmic work per query.

The first subtle case is when the replacement value is not larger than the best height already seen before position `p`. For example, consider

```
1
3 1
1 5 6
2 3
```

The modified array is `[1, 3, 6]`, so the answer is `3`. A careless solution might always count the modified apple because it was explicitly changed, but `3` is not higher than the previous picked height `1` in this example it actually is, so it is picked. A more revealing case is

```
1
3 1
1 5 6
2 1
```

The modified array is `[1, 1, 6]`, and the answer is `2`. The apple at position `2` is equal to the previous picked height, so strict comparison rejects it. Treating the condition as `>=` would incorrectly produce `3`.

The second subtle case is when the modified apple becomes the new record. Consider

```
1
4 1
1 2 3 4
3 10
```

The modified array is `[1, 2, 10, 4]`, so the answer is `3`. Once `10` is picked, the later `4` cannot be picked. A solution that computes the suffix independently from the original prefix maximum could accidentally count the original `4`, because `4` was a record in the unmodified array. The suffix must instead start with the new threshold `10`.

The third boundary case is a modification at the first position:

```
1
3 1
1 2 3
1 5
```

The answer is `1`, because the array becomes `[5, 2, 3]`. There is no left prefix at all, so the replacement value itself is the initial threshold. Any implementation that accesses information for position `p - 1` without handling `p = 1` separately can produce an invalid result.

The fourth boundary case is a modification at the last position:

```
1
3 1
1 2 3
3 4
```

The answer is `3`. There is no suffix after position `3`, so after deciding whether position `3` is picked, the computation is finished. Code that searches for a greater element starting at `p + 1` must allow the search range to be empty.

## Approaches

The brute-force solution simply copies the original array conceptually, replaces `h[p]` by `q`, and scans all `n` positions. During the scan we maintain the height of the last picked apple and increment the answer whenever the current height is strictly larger. This is exactly the picking rule, so the method is correct.

The problem is its cost. One query takes `O(n)` time, and `m` queries take `O(nm)`. With `n = m = 100000`, the worst case is about `10^10` element inspections. Even before accounting for Python overhead, that is several orders of magnitude too large.

The brute-force method works because the state of the scan is only one number, the largest height picked so far. The useful observation is that changing position `p` cannot affect any decision before `p`. It only changes the threshold that the suffix sees.

For the prefix `[1, p-1]`, we can precompute how many apples are picked and what the maximum picked height is. After that, only two cases exist. If `q` is not greater than the prefix maximum, position `p` is skipped and the suffix continues with the old prefix maximum. If `q` is greater than the prefix maximum, position `p` is picked and the suffix continues with `q` as its threshold.

We are left with one operation: given a suffix starting at `l` and a threshold `x`, find the first element whose height is strictly greater than `x`. Once that element is found, the rest of the answer can be reused from preprocessing.

To make that reuse possible, compute `nxt[i]`, the first position to the right of `i` whose height is strictly greater than `h[i]`. If such a position does not exist, `nxt[i]` is zero. Let `dp[i]` be the number of apples picked when scanning from `i` and treating `h[i]` as the current first threshold. Then

`dp[i] = 1 + dp[nxt[i]]`

when `nxt[i]` exists, and `dp[i] = 1` otherwise. The `nxt` array can be built in linear time with a decreasing monotonic stack.

The remaining first-greater search can be handled by a segment tree storing the maximum height of every interval. Starting from a query position, the tree can discard every interval whose maximum is not greater than the threshold. When an interval can contain a valid position, descend toward its left child first, because we need the first such position. This takes `O(log n)` time.

This gives a linear preprocessing phase and logarithmic query time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` | `O(1)` extra | Too slow |
| Optimal | `O(n + m log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Precompute `prefix_count[i]`, the number of apples picked in the original prefix `[1, i]`, and `prefix_max[i]`, the largest picked height in that prefix. While scanning from left to right, an apple contributes exactly when its height is greater than the current maximum. These two arrays completely describe everything a query needs from the part before `p`.
2. Compute `nxt[i]` with a monotonic stack. Scan positions from right to left. While the stack top has height less than or equal to `h[i]`, remove it, because that position can never be the first strictly higher apple for position `i`. The remaining top is the first position to the right with height strictly greater than `h[i]`.
3. Compute `dp[i]` from right to left. If `nxt[i]` is zero, then `i` is the final picked apple in this chain and `dp[i] = 1`. Otherwise, after picking `i`, the next picked apple is exactly `nxt[i]`, so `dp[i] = 1 + dp[nxt[i]]`.
4. Build a segment tree over the original heights, storing the maximum value in each node's interval. Its purpose is not to count apples directly. It lets us find the first position at or after a given index whose height is strictly greater than a supplied threshold.
5. For a query `(p, q)`, first obtain the information for `[1, p-1]`. If `p = 1`, this prefix is empty, so use a threshold smaller than every possible height and a picked count of zero. Otherwise, `prefix_count[p-1]` is the number already picked and `prefix_max[p-1]` is the current threshold.
6. Compare `q` with that prefix maximum. If `q` is larger, position `p` is picked, so increment the answer and set the suffix threshold to `q`. If `q` is smaller or equal, position `p` is skipped and the suffix threshold remains the prefix maximum.
7. Search the segment tree for the first position `i > p` with `h[i] > threshold`. If there is no such position, there is no suffix contribution. Otherwise, that position is the first apple picked after the modified position, and the complete remaining contribution is `dp[i]`.
8. Add the prefix contribution, the possible contribution of position `p`, and the suffix contribution. Because queries are independent, the original arrays are never modified.

### Why it works

The key invariant is that after scanning any prefix, the only information relevant to the remaining positions is the height of the last picked apple. For a query at position `p`, the original prefix is unchanged, so its picked count and last picked height are already known. The modified position either becomes a new picked maximum or leaves that maximum unchanged. Once the suffix begins, its first picked apple must be the first element strictly greater than this threshold. After that first element is selected, the process is exactly the same process represented by `dp[i]`. Hence every apple contributing to the answer is counted once, and every apple that cannot be picked is excluded.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())
        h = [0] + list(map(int, input().split()))

        # prefix_count[i] = number of picked apples in [1, i]
        # prefix_max[i] = last picked height in [1, i]
        prefix_count = [0] * (n + 1)
        prefix_max = [0] * (n + 1)

        cur_max = 0
        cur_count = 0

        for i in range(1, n + 1):
            if h[i] > cur_max:
                cur_max = h[i]
                cur_count += 1
            prefix_max[i] = cur_max
            prefix_count[i] = cur_count

        # nxt[i] = first j > i with h[j] > h[i]
        nxt = [0] * (n + 1)
        stack = []

        for i in range(n, 0, -1):
            while stack and h[stack[-1]] <= h[i]:
                stack.pop()

            if stack:
                nxt[i] = stack[-1]

            stack.append(i)

        # dp[i] = number of picked apples in the chain
        # starting by picking position i.
        dp = [0] * (n + 1)

        for i in range(n, 0, -1):
            if nxt[i] == 0:
                dp[i] = 1
            else:
                dp[i] = dp[nxt[i]] + 1

        # Segment tree for range maximum.
        size = 1
        while size < n:
            size <<= 1

        seg = [0] * (2 * size)

        for i in range(1, n + 1):
            seg[size + i - 1] = h[i]

        for i in range(size - 1, 0, -1):
            seg[i] = max(seg[i << 1], seg[i << 1 | 1])

        def first_greater(left, value):
            """First index >= left with h[index] > value, or 0."""
            if left > n:
                return 0

            def search(node, nl, nr):
                if nr < left or seg[node] <= value:
                    return 0

                if nl == nr:
                    return nl

                mid = (nl + nr) >> 1

                res = search(node << 1, nl, mid)
                if res:
                    return res

                return search(node << 1 | 1, mid + 1, nr)

            return search(1, 1, size)

        out = []

        for _ in range(m):
            p, q = map(int, input().split())

            if p == 1:
                answer = 0
                threshold = 0
            else:
                answer = prefix_count[p - 1]
                threshold = prefix_max[p - 1]

            if q > threshold:
                answer += 1
                threshold = q

            first = first_greater(p + 1, threshold)

            if first:
                answer += dp[first]

            out.append(str(answer))

        sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The prefix preprocessing corresponds directly to the first part of the query decomposition. `prefix_count` records how many apples have already been selected, while `prefix_max` records the threshold passed to the modified position and its suffix.

The monotonic stack computes `nxt` in linear time. The comparison uses `<=`, not `<`, because the rule requires the next apple to be strictly higher. Equal heights cannot be the next picked apple.

The `dp` recurrence is evaluated from right to left because `dp[i]` depends on `dp[nxt[i]]`, and `nxt[i]` is always greater than `i`. Every value is at most `n`, so ordinary Python integers are more than sufficient.

The segment tree is indexed with one-based array positions. `first_greater(left, value)` deliberately searches for an index greater than or equal to `left`, so the query passes `p + 1` and never accidentally considers the modified position itself.

The search first checks the left child. That ordering is necessary because several elements may be greater than the threshold, but the required element is the first one. An entire subtree is discarded immediately when its maximum is at most the threshold, because no element inside it can satisfy the strict inequality.

The query never changes `h`, the segment tree, `nxt`, or `dp`. This is essential because every query describes a separate hypothetical modification rather than a sequence of cumulative modifications.

## Worked Examples

Consider the provided sample:

```
1
5 3
1 2 3 4 4
1 5
5 5
2 3
```

For the original array, the prefix information is `1, 2, 3, 4, 4` for the picked counts and `1, 2, 3, 4, 4` for the prefix maxima. The relevant `nxt` links are `1 -> 2`, `2 -> 3`, `3 -> 4`, while neither position `4` nor `5` has a strictly greater element to its right.

For the first query, the modified position is the first apple, so there is no prefix. The new threshold is `5`. No element to the right exceeds `5`.

| Query | Prefix count | Prefix max | Modified height | Pick `p`? | Suffix threshold | First greater | Suffix count | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `(1, 5)` | 0 | 0 | 5 | yes | 5 | none | 0 | 1 |
| `(5, 5)` | 4 | 4 | 5 | yes | 5 | none | 0 | 5 |
| `(2, 3)` | 1 | 1 | 3 | yes | 3 | 4 | 1 | 3 |

For `(5, 5)`, the first four original apples are already picked, and the new value `5` is greater than the previous threshold `4`, giving all five apples. For `(2, 3)`, the prefix contributes one apple, position `2` is picked, and position `4` becomes the next greater apple. Position `5` has equal height `4`, so it is not picked after position `4`.

A second example exercises the case where the modified apple is skipped:

```
1
5 3
2 5 5 7 9
2 3
3 6
4 1
```

For the first query, the modified array is `[2, 3, 5, 7, 9]`, so all five apples are picked. For the second query, the modified array is `[2, 5, 6, 7, 9]`, again giving five. For the third query, the modified array is `[2, 5, 5, 1, 9]`. Position `4` is skipped because `1` is not greater than the prefix maximum `5`, and then `9` is picked.

| Query | Prefix count | Prefix max | Modified height | Pick `p`? | Suffix threshold | First greater | Suffix count | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `(2, 3)` | 1 | 2 | 3 | yes | 3 | 3 | 3 | 5 |
| `(3, 6)` | 2 | 5 | 6 | yes | 6 | 4 | 2 | 5 |
| `(4, 1)` | 2 | 5 | 1 | no | 5 | 5 | 1 | 3 |

The third row demonstrates why the suffix threshold must remain `5` when the modified apple is skipped. Searching for an element greater than `1` would incorrectly select position `5` as the first greater element, but it would miss the fact that the prefix has already established a threshold of `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m log n)` | The prefix arrays, monotonic stack, DP, and segment tree construction take `O(n)`, while every query performs one segment-tree first-greater search in `O(log n)`. |
| Space | `O(n)` | The prefix arrays, `nxt`, `dp`, stack, and segment tree each require linear storage. |

For `n, m <= 100000`, the preprocessing performs only a constant number of linear scans, while each query performs about `O(log n)` segment-tree work. The total work is comfortably below the `O(nm)` brute-force approach, and the memory consumption is linear in the number of apples.

## Test Cases

The following tests assume the `solve()` function from the solution above is available. The helper temporarily replaces standard input and captures standard output, so the tests exercise the same parsing and query logic as the submitted program.

```python
import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()

    try:
        with redirect_stdout(output):
            solve()
        return output.getvalue().strip()
    finally:
        sys.stdin = old_stdin

# Provided sample
sample = """\
1
5 3
1 2 3 4 4
1 5
5 5
2 3
"""
assert run(sample) == "1\n5\n3", "provided sample"

# Minimum-size case
minimum = """\
1
1 3
7
1 1
1 7
1 1000000000
"""
assert run(minimum) == "1\n1\n1", "single apple"

# All equal values, including a replacement that becomes a new maximum
all_equal = """\
1
4 4
5 5 5 5
1 6
2 4
4 6
4 5
"""
assert run(all_equal) == "1\n1\n2\n1", "all equal values"

# Boundary cases at the first and last positions
boundaries = """\
1
5 4
1 2 3 4 5
1 10
1 1
5 6
5 1
"""
assert run(boundaries) == "1\n4\n5\n4", "first and last positions"

# Strict inequality and an off-by-one-sensitive suffix
strict = """\
1
5 4
2 5 5 7 9
2 3
3 6
4 1
3 5
"""
assert run(strict) == "5\n5\n3\n4", "strict comparison and suffix"

# Maximum-size stress case.
# Every original value is 1. A replacement of 1 gives one picked apple,
# while a replacement of 2 gives exactly two picked apples.
n = 100000
m = 100000
queries = []
expected = []

for i in range(1, m + 1):
    q = 1 if i & 1 else 2
    p = (i - 1) % n + 1
    queries.append(f"{p} {q}")
    expected.append("1" if q == 1 else "2")

maximum = (
    "1\n"
    f"{n} {m}\n"
    + ("1 " * (n - 1))
    + "1\n"
    + "\n".join(queries)
    + "\n"
)

assert run(maximum) == "\n".join(expected), "maximum-size stress case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1`, `h=[7]` | `1`, `1`, `1` | Empty prefix and suffix, minimum array size |
| `h=[5,5,5,5]` | `1`, `1`, `2`, `1` | Equal values must not be picked, including strict inequality |
| `h=[1,2,3,4,5]` with changes at positions `1` and `5` | `1`, `4`, `5`, `4` | First-position and last-position boundaries |
| `h=[2,5,5,7,9]` | `5`, `5`, `3`, `4` | Modified value becoming or failing to become the new threshold |
| `100000` equal values and `100000` queries | Alternating `1` and `2` | Linear preprocessing, logarithmic queries, maximum input size |

## Edge Cases

When `p = 1`, the prefix is empty. For example,

```
1
3 1
1 2 3
1 5
```

The algorithm sets `answer = 0` and `threshold = 0`. Since `5 > 0`, the modified first apple is picked, making the threshold `5`. The suffix search finds no value greater than `5`, so the output is `1`.

When `p = n`, the suffix is empty. For example,

```
1
3 2
1 2 3
3 4
3 1
```

For `(3,4)`, the prefix contributes two apples and `4 > 2`, so position `3` is picked and the answer is `3`. For `(3,1)`, position `3` is skipped because `1 <= 2`, so the answer remains `2`. The call searching from `p + 1 = 4` immediately returns no position.

When the replacement equals the prefix maximum, it must be skipped. For example,

```
1
3 1
2 5 8
3 5
```

The prefix before position `3` has maximum `5`. Since the replacement is also `5`, position `3` is not picked. The suffix is empty, so the answer is `2`. Using `>=` instead of `>` would incorrectly count the third apple.

When the replacement is larger than the prefix maximum, it becomes the new threshold and completely changes which suffix records survive. For example,

```
1
4 1
1 2 3 4
3 10
```

The prefix contributes `2` apples with maximum `2`. The replacement `10` is picked, giving a current answer of `3`. The suffix contains `4`, but `4` is not greater than `10`, so no suffix apple is added. The result is `3`.

When the prefix already has a high maximum and the replacement is small, the suffix must be searched using that old maximum, not the replacement. For example,

```
1
5 1
2 5 5 7 9
4 1
```

Before position `4`, the picked apples are `2` and `5`, so the threshold is `5`. The replacement `1` is skipped. The first value after position `4` greater than `5` is `9` at position `5`, and `dp[5] = 1`. The answer is `2 + 1 = 3`.

The equality case in the monotonic stack is equally significant. For

```
1
4 1
5 5 5 6
1 5
```

the modified array is `[5,5,5,6]`. Only the first `5` and the final `6` are picked, so the answer is `2`. While building `nxt`, positions with height `5` must remove earlier equal-height candidates, because an equal value is never a valid strictly greater next pick. Using `<` instead of `<=` in the stack condition would leave invalid equal-height links and corrupt the DP.
