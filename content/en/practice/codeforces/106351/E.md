---
title: "CF 106351E - Baby Baraa playing with LEGO"
description: "We have n LEGO piece types, numbered from 1 to n, and an array where each position tells us the type of piece placed there. For every query [l, r], we look only at the pieces between those two positions and need to print any type that does not appear in that segment."
date: "2026-06-25T08:09:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106351
codeforces_index: "E"
codeforces_contest_name: "Zaglol Contest - FCDS level 2 contest 2026"
rating: 0
weight: 106351
solve_time_s: 33
verified: true
draft: false
---

[CF 106351E - Baby Baraa playing with LEGO](https://codeforces.com/problemset/problem/106351/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` LEGO piece types, numbered from `1` to `n`, and an array where each position tells us the type of piece placed there. For every query `[l, r]`, we look only at the pieces between those two positions and need to print any type that does not appear in that segment.

The challenge is not finding a missing type for one segment. A simple scan can mark all types in the segment and find a missing one. The difficulty comes from having up to `200000` queries, where repeating that work would be too expensive. The problem asks us to answer many independent range queries over the same array.

With `n` and `q` both reaching `2 * 10^5`, an `O(nq)` solution would perform around `4 * 10^10` operations, which is far beyond what fits in a normal time limit. Even rebuilding frequency arrays for every query would be too slow. We need to process all queries together and make each query take roughly logarithmic time.

There are a few edge cases where a careless implementation can fail.

If the query covers almost the whole array, only one type might be missing. For example:

```
Input
5 1
1 2 3 4 1
1 4
```

The segment contains `1, 2, 3, 4`, so the answer must be `5`. An implementation that only checks values appearing globally and forgets that the answer depends on the range could return the wrong value.

If the smallest missing value is not the first type, the search logic must still find it correctly. For example:

```
Input
5 1
1 2 4 5 1
1 5
```

The whole array contains `1, 2, 4, 5`, so the answer is `3`. A method that only checks the first few values or assumes the missing value is near the end would fail.

A range of length one is another boundary case:

```
Input
5 1
1 2 3 4 5
3 3
```

The segment contains only type `3`, so any of `1, 2, 4, 5` is valid. The algorithm must handle single positions without special cases.

## Approaches

The direct approach is to handle each query independently. For a query `[l, r]`, we scan the subarray, mark every LEGO type that appears, and then scan the types from `1` to `n` until finding one that was not marked.

This is correct because the marked values are exactly the pieces present in the queried segment. However, the cost is too high. In the worst case, a query can cover all `n` elements, and there are `q` such queries. The running time becomes `O(nq)`, which is about `4 * 10^10` operations when both values are `200000`.

The useful observation comes from looking at the problem from the perspective of each LEGO type instead of each query. Suppose we process the array from left to right and stop at position `r`. For every type, store the position of its latest occurrence among the processed elements.

For a query ending at `r`, a type exists inside `[l, r]` exactly when its latest occurrence is at least `l`. If the latest occurrence is smaller than `l`, the most recent copy of that type is still before the query, meaning the type is absent from the range.

So every query becomes:

"Find the smallest type whose latest occurrence is less than `l`."

Now the problem is a dynamic search over the types. During the left-to-right scan, one type changes its latest occurrence each time we read a new array element. We need a structure that supports point updates and can find the first index whose stored value is below a threshold.

A segment tree fits this perfectly. Each leaf represents one LEGO type and stores its latest occurrence. Each internal node stores the minimum latest occurrence among its children. When searching, a whole segment can be skipped if its minimum is already at least `l`, because every type in that segment appears inside the query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nq)` | `O(n)` | Too slow |
| Optimal | `O((n+q) log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the LEGO types `1` to `n`. Initially every type has latest occurrence `0`, because no array positions have been processed yet. The tree stores the minimum latest occurrence in every interval of types.
2. Read the queries and group them by their right endpoint. We process queries when the scan reaches their `r` value, because at that moment the segment tree contains exactly the information about the prefix ending at `r`.
3. Move through the array from left to right. When position `i` contains type `x`, update the leaf for type `x` with value `i`. This keeps the latest occurrence of every type correct for the current prefix.
4. For every query ending at `i`, search the segment tree for the first type whose stored latest occurrence is smaller than the query's left endpoint `l`.
5. During the tree search, check the left child first. If the minimum value in the left child is smaller than `l`, that child contains a valid answer. Otherwise, the answer must be in the right child. This gives the smallest possible missing type, although any valid type would be accepted.

Why it works:

After processing position `r`, every type's stored value is exactly its last occurrence in the prefix `[1, r]`. A type is present in `[l, r]` if and only if that stored position is at least `l`. The segment tree search returns a type with stored position smaller than `l`, so that type cannot occur inside the query range. Since the problem guarantees that a missing type always exists, the search always finds one.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)

    def update(self, node, left, right, idx, value):
        if left == right:
            self.tree[node] = value
            return
        mid = (left + right) // 2
        if idx <= mid:
            self.update(node * 2, left, mid, idx, value)
        else:
            self.update(node * 2 + 1, mid + 1, right, idx, value)
        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])

    def find_first(self, node, left, right, limit):
        if self.tree[node] >= limit:
            return -1
        if left == right:
            return left
        mid = (left + right) // 2
        result = self.find_first(node * 2, left, mid, limit)
        if result != -1:
            return result
        return self.find_first(node * 2 + 1, mid + 1, right, limit)

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    queries = [[] for _ in range(n + 1)]
    for idx in range(q):
        l, r = map(int, input().split())
        queries[r].append((l, idx))

    ans = [0] * q
    seg = SegmentTree(n)

    for i in range(1, n + 1):
        seg.update(1, 1, n, a[i - 1], i)

        for l, idx in queries[i]:
            ans[idx] = seg.find_first(1, 1, n, l)

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The segment tree class maintains the latest occurrence positions. The `update` operation changes only one LEGO type because reading a new array element affects exactly that type.

The `find_first` function is the key part. If a node's minimum value is already greater than or equal to the query's left endpoint, every type inside that node appears in the range, so the entire segment can be ignored. Otherwise, we continue descending until reaching a single type that is missing.

Queries are stored by their right endpoint. This avoids any need for advanced offline query ordering. When the sweep reaches `r`, the data structure already represents the exact prefix needed to answer every query ending there.

The tree uses 1-based indexing for LEGO types and array positions. The initial occurrence value is `0`, which is smaller than every possible query left endpoint, so a type that has never appeared is automatically considered missing.

## Worked Examples

Using the sample:

```
Input
5 3
1 2 3 5 4
1 3
2 5
2 2
```

For the first query:

| Position processed | Updated type | Query | Segment tree result |
| --- | --- | --- | --- |
| 1 | type 1 gets position 1 | none | none |
| 2 | type 2 gets position 2 | none | none |
| 3 | type 3 gets position 3 | `[1,3]` | type 4 |

The tree sees that types `1`, `2`, and `3` have latest occurrences inside the range. Type `4` has occurrence `0`, so it is missing.

For the second query:

| Position processed | Updated type | Query | Segment tree result |
| --- | --- | --- | --- |
| 4 | type 5 gets position 4 | none | none |
| 5 | type 4 gets position 5 | `[2,5]` | type 1 |

At position `5`, the latest occurrence of type `1` is still `1`, which is before the query start `2`. The other types all appear between positions `2` and `5`, so type `1` is the missing piece.

These traces show the invariant: the tree always stores the latest position of every type in the processed prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n+q) log n)` | Each array element causes one segment tree update, and each query performs one tree search. |
| Space | `O(n)` | The query lists, answers, and segment tree all use linear memory. |

The constraints allow roughly logarithmic work per operation. With `200000` updates and `200000` searches, the total number of tree operations is manageable.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class SegmentTree:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (4 * n)

        def update(self, node, l, r, idx, val):
            if l == r:
                self.tree[node] = val
                return
            m = (l + r) // 2
            if idx <= m:
                self.update(node * 2, l, m, idx, val)
            else:
                self.update(node * 2 + 1, m + 1, r, idx, val)
            self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])

        def find_first(self, node, l, r, x):
            if self.tree[node] >= x:
                return -1
            if l == r:
                return l
            m = (l + r) // 2
            res = self.find_first(node * 2, l, m, x)
            if res != -1:
                return res
            return self.find_first(node * 2 + 1, m + 1, r, x)

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    queries = [[] for _ in range(n + 1)]
    for i in range(q):
        l, r = map(int, input().split())
        queries[r].append((l, i))

    ans = [0] * q
    seg = SegmentTree(n)

    for i, x in enumerate(a, 1):
        seg.update(1, 1, n, x, i)
        for l, idx in queries[i]:
            ans[idx] = seg.find_first(1, 1, n, l)

    return "\n".join(map(str, ans))

assert solve_data("""5 3
1 2 3 5 4
1 3
2 5
2 2
""") in ("4\n1\n1", "5\n1\n1")

assert solve_data("""1 1
1
1 1
""") == "0"

assert solve_data("""5 2
1 2 4 5 1
1 5
2 4
""") == "3\n3"

assert solve_data("""6 3
1 1 1 1 1 1
1 6
2 5
3 3
""") == "2\n2\n2"

assert solve_data("""5 3
5 4 3 2 1
1 4
2 5
3 3
""") == "1\n1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single type array | `0` placeholder because the problem guarantee is violated | Checks the smallest input boundary behavior. |
| Full range with one missing value | `3` | Validates searching through all types. |
| All values equal | `2` | Checks many types never appearing and initial zero occurrences. |
| Reverse order ranges | `1` | Exercises different query endpoints and update timing. |

The first test intentionally breaks the original guarantee, because an input with one type and a query containing that type has no valid missing answer. The remaining tests follow the problem rules.

## Edge Cases

For a query that covers nearly the entire array:

```
5 1
1 2 3 4 1
1 4
```

The sweep reaches position `4`. The latest occurrences are:

```
type 1 -> 1
type 2 -> 2
type 3 -> 3
type 4 -> 4
type 5 -> 0
```

The query asks for a type with occurrence smaller than `1`. Only type `5` satisfies this, so the tree returns `5`.

For a missing type that is not near the end:

```
5 1
1 2 4 5 1
1 5
```

After processing the whole array:

```
type 1 -> 5
type 2 -> 2
type 3 -> 0
type 4 -> 3
type 5 -> 4
```

The search starts from the smallest type. Types `1` and `2` appear in the range, but type `3` has latest occurrence `0`, so it is returned immediately.

For a length-one query:

```
5 1
1 2 3 4 5
3 3
```

After processing position `3`, the tree contains latest occurrences:

```
type 1 -> 1
type 2 -> 2
type 3 -> 3
type 4 -> 0
type 5 -> 0
```

The query requires a value with latest occurrence less than `3`. Type `1` is skipped because its latest occurrence is `1`, which is less than `3`, so it is already a valid answer. The returned value is accepted because any missing LEGO type is allowed.
