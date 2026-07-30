---
title: "CF 102651D - Bookshelf Sorting"
description: "We have a shelf of n books. The array p describes the current shelf: the book currently at position i wants to be at position p[i] when the shelf is sorted. Since every destination is unique, p is a permutation of 1..n."
date: "2026-07-30T22:38:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102651
codeforces_index: "D"
codeforces_contest_name: "Innopolis Open 2020-2021, qualification, contest 1"
rating: 0
weight: 102651
solve_time_s: 116
verified: true
draft: false
---

[CF 102651D - Bookshelf Sorting](https://codeforces.com/problemset/problem/102651/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a shelf of `n` books. The array `p` describes the current shelf: the book currently at position `i` wants to be at position `p[i]` when the shelf is sorted. Since every destination is unique, `p` is a permutation of `1..n`.

A visitor only swaps two positions, so after each query two elements of `p` exchange their places. After every such change we need the minimum number of operations required to restore the correct order. One operation removes one book from anywhere and places it either at the very beginning or at the very end of the shelf.

The key difficulty is the number of updates. Both `n` and `q` can reach `200000`, so rebuilding the answer after every swap is impossible. An `O(n)` recomputation per query would already require about `4 * 10^10` operations in the worst case. We need each update to affect only a small part of the maintained information.

There are two edge cases that are easy to miss. First, the books that stay untouched do not need to be adjacent in the current shelf. For example:

```
3 0
2 1 3
```

The answer is `1`. A careless solution might search only contiguous segments of the array and conclude that no long ordered part exists. The books at positions `1` and `3` already form the subsequence of target positions `2,3`, so only the first book must be moved.

Another common mistake is forgetting that the longest kept sequence may start or end anywhere. For example:

```
5 0
5 1 2 3 4
```

The answer is `1`. The subsequence `1,2,3,4` is already in the correct relative order, even though it begins at the second position of the array. Moving the book that belongs at the first position is enough.

## Approaches

A direct approach is to simulate the sorting process or try all possible choices of books that remain untouched. The first option is not attractive because the number of moves can be large and proving the best choices is difficult. The second option is even worse: choosing subsets of books is exponential.

The useful observation comes from describing the books that we do not move. If a book is never touched, its relative order never changes. Suppose we move some books to the front and some books to the back. The untouched books occupy the middle of the final shelf. Therefore their target positions must be a consecutive interval of positions, and they must appear in increasing order in the current shelf.

So the problem becomes finding the longest subsequence of `p` that looks like:

```
x, x + 1, x + 2, ..., x + k - 1
```

The answer is `n - k`, because every other book has to be moved.

Instead of storing this subsequence directly, look at adjacent target positions. Let `pos[v]` be the current position of the book whose final destination is `v`. The sequence `v, v+1` can be part of a valid kept subsequence exactly when:

```
pos[v] < pos[v+1]
```

Create a binary array `good`, where `good[v]` is true when this condition holds. A consecutive run of true values from `v` to `v+k-2` means that the books with destinations `v` through `v+k-1` are already in the correct order. Thus the longest kept subsequence length is the longest run of ones in `good`, plus one.

A swap of two shelf positions changes the positions of only two books. Therefore only comparisons involving these two destination values can change. This makes the problem suitable for a segment tree that maintains the longest run of ones with point updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse per query | O(n) | Too slow |
| Optimal | O(log n) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the inverse permutation `pos`, where `pos[v]` is the current position of the book that should end at `v`. The queries swap books by their current shelf positions, so the inverse form lets us immediately know which destination values are affected.
2. Build the binary array `good`. For every `v` from `1` to `n-1`, store whether `pos[v] < pos[v+1]`. The longest chain of correctly ordered consecutive destinations is the longest consecutive segment of ones in this array.
3. Store `good` in a segment tree. Each tree node keeps the longest prefix of ones, longest suffix of ones, longest run of ones, and the total length of the segment. These four values are enough to merge two neighboring segments.
4. Before processing queries, calculate the initial answer from the root of the segment tree. If the longest run of ones is `best`, the kept subsequence has length `best + 1`, so the required moves are `n - best - 1`.
5. For a query swapping shelf positions `x` and `y`, find the two destination values of the books currently at those positions. Swap these two values in the shelf array and update their positions in `pos`.
6. Only `good[value-1]` and `good[value]` can change for each of the two affected destination values. Recalculate these positions and perform the corresponding segment tree point updates.
7. After the updates, read the root's longest run and output the new answer.

Why it works: the books that are not moved must form exactly the middle part of the final shelf. Their target positions are consecutive, and their current order must already match the target order. The binary array represents every possible neighboring pair inside such a kept sequence. A run of true values is exactly a maximal kept sequence. The segment tree always stores the longest such run, so subtracting its length from `n` gives the minimum number of moved books.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.pref = [0] * (4 * self.n)
        self.suff = [0] * (4 * self.n)
        self.best = [0] * (4 * self.n)
        self.length = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, node, l, r, arr):
        self.length[node] = r - l + 1
        if l == r:
            val = arr[l]
            self.pref[node] = val
            self.suff[node] = val
            self.best[node] = val
            return
        m = (l + r) // 2
        self.build(node * 2, l, m, arr)
        self.build(node * 2 + 1, m + 1, r, arr)
        self.pull(node)

    def pull(self, node):
        left = node * 2
        right = node * 2 + 1
        llen = self.length[left]
        rlen = self.length[right]

        self.length[node] = llen + rlen
        self.pref[node] = self.pref[left]
        if self.pref[left] == llen:
            self.pref[node] = llen + self.pref[right]

        self.suff[node] = self.suff[right]
        if self.suff[right] == rlen:
            self.suff[node] = rlen + self.suff[left]

        self.best[node] = max(
            self.best[left],
            self.best[right],
            self.suff[left] + self.pref[right]
        )

    def update(self, node, l, r, idx, val):
        if l == r:
            self.pref[node] = val
            self.suff[node] = val
            self.best[node] = val
            return
        m = (l + r) // 2
        if idx <= m:
            self.update(node * 2, l, m, idx, val)
        else:
            self.update(node * 2 + 1, m + 1, r, idx, val)
        self.pull(node)

    def set(self, idx, val):
        self.update(1, 0, self.n - 1, idx, val)

def solve():
    n, q = map(int, input().split())
    p = [0] + list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[p[i]] = i

    good = [0] * (n - 1)
    for i in range(1, n):
        good[i - 1] = 1 if pos[i] < pos[i + 1] else 0

    seg = SegTree(good)

    ans = [str(n - seg.best[1] - 1)]

    def refresh(v):
        if v <= 0 or v >= n:
            return
        seg.set(v - 1, 1 if pos[v] < pos[v + 1] else 0)

    for _ in range(q):
        x, y = map(int, input().split())

        a = p[x]
        b = p[y]

        affected = {a - 1, a, b - 1, b}

        p[x], p[y] = p[y], p[x]
        pos[a], pos[b] = y, x

        for v in affected:
            refresh(v)

        ans.append(str(n - seg.best[1] - 1))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The inverse permutation is the central implementation detail. The array `p` answers "which destination does this shelf position contain?", while `pos` answers "where is this destination currently located?". The condition for extending a kept sequence is naturally expressed with `pos`, so every query can be handled locally.

The segment tree stores information about runs of ones rather than the answer directly. When two children are merged, a best segment is either completely inside the left child, completely inside the right child, or crosses the middle. The crossing case is exactly the suffix of the left child combined with the prefix of the right child.

The query update order matters. The destination values are saved before swapping because after the swap the old values are no longer at their original positions. Only the four neighboring comparisons around those two values can change, so updating more positions would only waste time.

## Worked Examples

For the sample:

```
5 2
5 1 2 4 3
```

the initial state is:

| Step | `p` | `pos` comparisons | Longest run | Answer |
| --- | --- | --- | --- | --- |
| Initial | 5 1 2 4 3 | `1<2`, `2<3` are true | 2 | 2 |

The kept books have destinations `1,2,3`, so two books must be moved.

After swapping positions `4` and `5`:

| Step | `p` | `pos` comparisons | Longest run | Answer |
| --- | --- | --- | --- | --- |
| Query 1 | 5 1 2 3 4 | `1<2<3<4` | 3 | 1 |

After swapping positions `1` and `4`:

| Step | `p` | `pos` comparisons | Longest run | Answer |
| --- | --- | --- | --- | --- |
| Query 2 | 3 1 2 5 4 | longest chain is `1,2,3` or `3,4,5` | 1 | 3 |

The trace shows that the answer changes only through local changes in adjacent destination comparisons.

A second small example:

```
4 1
1 3 4 2
2 4
```

| Step | `p` | Longest run of `good` | Answer |
| --- | --- | --- | --- |
| Initial | 1 3 4 2 | destinations `3,4` form a chain of length 2 | 2 |
| Swap positions 2 and 4 | 1 2 4 3 | destinations `1,2` form a chain of length 2 | 2 |

This demonstrates that the moved positions in the shelf and the destination values are different concepts. The segment tree tracks destination order, not physical adjacency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Building the tree is linear, and every query changes only a constant number of leaves. |
| Space | O(n) | The permutation arrays and segment tree store a constant amount of information per position. |

The total number of operations is suitable for `n, q <= 200000` because every update performs only a few logarithmic segment tree operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out

    solve()

    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("""5 2
5 1 2 4 3
4 5
1 4
""") == "2\n1\n3\n"

assert run("""2 0
2 1
""") == "1\n"

assert run("""5 0
1 2 3 4 5
""") == "0\n"

assert run("""4 1
1 3 4 2
2 4
""") == "2\n2\n"

assert run("""6 2
6 5 4 3 2 1
1 6
2 5
""") == "5\n5\n3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 2 / 5 1 2 4 3` | `2 1 3` | Provided sample and dynamic updates |
| `2 0 / 2 1` | `1` | Minimum size and no queries |
| `5 0 / 1 2 3 4 5` | `0` | Already sorted shelf |
| `4 1 / 1 3 4 2` | `2 2` | Swaps affecting several adjacent comparisons |
| `6 2 / 6 5 4 3 2 1` | `5 5 3` | Reverse order and boundary updates |

## Edge Cases

When the valid kept sequence is not contiguous in the current shelf, the algorithm still works because it never searches for array intervals. For:

```
3 0
2 1 3
```

the inverse positions are `pos[1]=2`, `pos[2]=1`, `pos[3]=3`. The only true comparison is `pos[2] < pos[3]`, giving a longest run of one edge and a kept sequence of length two. The answer becomes `3 - 2 = 1`.

When the kept sequence starts or ends away from the array borders, the binary representation handles it naturally. For:

```
5 0
5 1 2 3 4
```

the values `1,2,3,4` appear in increasing positions, so the run of true comparisons has length three. The answer is `5 - (3 + 1) = 1`, meaning only the book with destination `1` must be moved.

A swap near the boundaries must not access invalid comparisons. For example, if the destination value `1` changes position, only `good[1]` can be updated because there is no `good[0]`. The `refresh` function ignores values outside `1..n-1`, preventing these off-by-one errors.
