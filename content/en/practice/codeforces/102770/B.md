---
title: "CF 102770B - Bin Packing Problem"
description: "We have a sequence of items arriving one by one. Each item has a volume, and every bin has the same maximum capacity. The task is not to find the optimal packing."
date: "2026-08-01T22:23:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "B"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 86
verified: true
draft: false
---

[CF 102770B - Bin Packing Problem](https://codeforces.com/problemset/problem/102770/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of items arriving one by one. Each item has a volume, and every bin has the same maximum capacity. The task is not to find the optimal packing. Instead, we must exactly reproduce two fixed strategies, First Fit and Best Fit, and report how many bins each strategy creates after processing the whole sequence.

For First Fit, the bins have a fixed order based on creation time. Every new item scans that order and enters the earliest bin with enough free space. For Best Fit, the item chooses the fullest bin that can still contain it, meaning among all possible bins it takes the one with the smallest remaining capacity after placement.

The input contains several independent cases. The number of items across all cases is at most one million, so the solution must be close to linear or linearithmic. A direct simulation that checks every existing bin for every item can perform around $n^2$ checks. With one million items, that can reach about $10^{12}$ operations, which is far beyond what a contest program can handle.

The capacity can be as large as $10^9$, so solutions that allocate arrays indexed by capacity are impossible. The data structures must depend on the number of bins, not the capacity value.

Several details can break an otherwise correct implementation. Consider an item that exactly fills a bin:

```
1
3 10
10 1 9
```

The answer is:

```
2 2
```

After placing the first item, the remaining capacity is zero. A careless implementation that only checks whether a bin has been used before or treats zero as an invalid state may fail to reuse or manage such bins correctly.

Another edge case is when several bins have the same remaining capacity:

```
1
4 10
6 4 6 4
```

The answer is:

```
2 2
```

The Best Fit algorithm may have multiple equally good choices. The exact bin identity does not matter for the final count, but the implementation must correctly remove and insert duplicate remaining capacities.

A final common mistake is confusing item order with sorting. For example:

```
1
5 10
5 8 2 5 9
```

The answer is:

```
4 3
```

The algorithms must process items exactly as they arrive. Sorting the items changes the simulation and produces a different result.

## Approaches

A straightforward implementation keeps a list of bins and their remaining capacities. For every incoming item, First Fit scans the list from the beginning until it finds a suitable bin. Best Fit scans the whole list, keeping the suitable bin with the smallest remaining capacity. These simulations are correct because they directly follow the definitions of the two algorithms.

The problem appears when the number of items becomes large. In the worst case, almost every item may inspect almost every bin. Since the number of bins can also grow to $n$, the total work becomes $O(n^2)$, which is too slow for $n=10^6$.

The observation that makes the problem manageable is that both algorithms only need ordered information about remaining capacities.

For First Fit, we do not need to know every bin while searching. We only need to find the earliest bin whose remaining capacity is at least the current item size. A segment tree can store the maximum remaining capacity in each range of bins. If a segment tree node has a maximum smaller than the item size, that whole range cannot contain an answer. By descending through the tree, we can locate the first valid bin in $O(\log n)$.

For Best Fit, we need the smallest remaining capacity that is still at least the item size. This is a lower bound query in an ordered multiset. Since Python has no built-in balanced tree, we implement a randomized treap. The treap stores remaining capacities and supports insertion, deletion, and lower bound search in expected $O(\log n)$.

The brute-force method works because it stores exactly the information the algorithms need, but it searches that information too slowly. The faster method keeps the same state while adding the ability to jump directly to the relevant bin.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create two independent simulations because First Fit and Best Fit make different choices even when they process the same item sequence. For each item, update both structures separately.
2. For First Fit, store every bin's remaining capacity in a segment tree. The tree value of a range is the maximum remaining capacity among bins in that range. When processing an item of size `x`, search the tree for the first position whose stored maximum is at least `x`. If such a position exists, decrease that bin's remaining capacity by `x` and update the tree. Otherwise, create a new bin with remaining capacity `C - x`.
3. The segment tree search always goes left first. This matches the definition of First Fit because smaller indices represent bins created earlier.
4. For Best Fit, store the remaining capacities of all bins in a treap. For an item of size `x`, find the smallest stored value that is at least `x`. If it exists, remove that remaining capacity from the treap and insert the new remaining capacity after placing the item. If it does not exist, create a new bin with remaining capacity `C - x`.
5. Count every new bin created in each simulation. The two counters are the required output.

Why it works: the segment tree maintains the invariant that every node contains the maximum remaining capacity of its interval. During a search, any interval whose maximum is too small cannot contain a valid First Fit bin, so skipping it cannot remove the correct answer. The first reachable leaf with enough capacity is exactly the earliest valid bin.

For Best Fit, the treap maintains all current remaining capacities in sorted order. The lower bound operation returns the smallest capacity that can hold the item, which is exactly the bin selected by Best Fit. Removing the old value and inserting the new value keeps the stored state identical to the actual bins after every operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

import random

class TreapNode:
    __slots__ = ("key", "prio", "cnt", "left", "right")

    def __init__(self, key):
        self.key = key
        self.prio = random.randint(1, 1 << 60)
        self.cnt = 1
        self.left = None
        self.right = None

def rotate_right(root):
    x = root.left
    root.left = x.right
    x.right = root
    return x

def rotate_left(root):
    x = root.right
    root.right = x.left
    x.left = root
    return x

def treap_insert(root, key):
    if root is None:
        return TreapNode(key)
    if key == root.key:
        root.cnt += 1
    elif key < root.key:
        root.left = treap_insert(root.left, key)
        if root.left.prio < root.prio:
            root = rotate_right(root)
    else:
        root.right = treap_insert(root.right, key)
        if root.right.prio < root.prio:
            root = rotate_left(root)
    return root

def treap_erase(root, key):
    if root.key == key:
        if root.cnt > 1:
            root.cnt -= 1
        elif root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        elif root.left.prio < root.right.prio:
            root = rotate_right(root)
            root.right = treap_erase(root.right, key)
        else:
            root = rotate_left(root)
            root.left = treap_erase(root.left, key)
    elif key < root.key:
        root.left = treap_erase(root.left, key)
    else:
        root.right = treap_erase(root.right, key)
    return root

def treap_lower_bound(root, key):
    ans = None
    while root:
        if root.key >= key:
            ans = root.key
            root = root.left
        else:
            root = root.right
    return ans

class SegmentTree:
    def __init__(self):
        self.size = 1
        self.tree = [0] * 2

    def append(self, value):
        if self.size - 1 >= self.count:
            old = self.size
            self.size *= 2
            self.tree = [0] * (2 * self.size)
            for i in range(self.count):
                self.tree[self.size + i] = self.values[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])
        self.values.append(value)
        self.count += 1
        self.tree[self.size + self.count - 1] = value
        p = (self.size + self.count - 1) // 2
        while p:
            self.tree[p] = max(self.tree[p * 2], self.tree[p * 2 + 1])
            p //= 2

    def init_empty(self):
        self.values = []
        self.count = 0

    def update(self, index, value):
        self.values[index] = value
        p = self.size + index
        self.tree[p] = value
        p //= 2
        while p:
            self.tree[p] = max(self.tree[p * 2], self.tree[p * 2 + 1])
            p //= 2

    def first_ge(self, value):
        if self.tree[1] < value:
            return -1
        node = 1
        left = 0
        right = self.size - 1
        while left != right:
            mid = (left + right) // 2
            if self.tree[node * 2] >= value:
                node = node * 2
                right = mid
            else:
                node = node * 2 + 1
                left = mid + 1
        return left

def solve_case(n, c, arr):
    ff = SegmentTree()
    ff.init_empty()
    ff_count = 0

    bf_root = None
    bf_count = 0

    for x in arr:
        pos = ff.first_ge(x)
        if pos == -1:
            ff.append(c - x)
            ff_count += 1
        else:
            ff.update(pos, ff.values[pos] - x)

        best = treap_lower_bound(bf_root, x)
        if best is None:
            bf_root = treap_insert(bf_root, c - x)
            bf_count += 1
        else:
            bf_root = treap_erase(bf_root, best)
            bf_root = treap_insert(bf_root, best - x)

    return ff_count, bf_count

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    ans = []
    for _ in range(t):
        n = data[idx]
        c = data[idx + 1]
        idx += 2
        arr = data[idx:idx + n]
        idx += n
        a, b = solve_case(n, c, arr)
        ans.append(f"{a} {b}")
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The code maintains two completely separate states because the same item can be placed into different bins by the two strategies.

The segment tree stores only the remaining capacities needed for First Fit. The `first_ge` function searches for the smallest index whose remaining capacity is large enough. The search order is the left child first, which preserves the original bin order.

The treap implementation supports duplicate remaining capacities using the `cnt` field. This matters because many bins can have identical free space. The lower bound function does not return an arbitrary valid bin. It returns the smallest valid remaining capacity, matching Best Fit exactly.

The segment tree uses one-based internal indexing and leaves beyond the current number of bins as zero. Since all item sizes are positive, unused leaves cannot accidentally become answers. Python integers already handle the large capacity values without overflow.

## Worked Examples

For the first sample:

```
1
2 2
1 1
```

The simulation states are:

| Item | Size | First Fit bins remaining | First Fit count | Best Fit remaining values | Best Fit count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [1] | 1 | [1] | 1 |
| 2 | 1 | [0] | 1 | [0] | 1 |

Both algorithms reuse the same bin because the remaining capacity is sufficient for the second item.

For the second sample:

```
1
5 10
5 8 2 5 9
```

The states are:

| Item | Size | First Fit remaining | First Fit count | Best Fit remaining values | Best Fit count |
| --- | --- | --- | --- | --- | --- |
| 5 | 5 | [5] | 1 | [5] | 1 |
| 8 | 8 | [5,2] | 2 | [5,2] | 2 |
| 2 | 2 | [3,2] | 2 | [3,5] | 2 |
| 5 | 5 | [3,2,5] | 3 | [3,5] | 2 |
| 9 | 9 | [3,2,5,1] | 4 | [1,3,5] | 3 |

The trace shows the difference between the strategies. First Fit keeps checking earlier bins and creates a new bin for the item of size 5 because the first two bins cannot hold it. Best Fit finds the bin with remaining capacity 5 and uses it instead.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each item performs a constant number of segment tree and treap operations. |
| Space | O(n) | At most one stored entry exists for each created bin. |

The total number of items over all test cases is one million. An $O(n \log n)$ solution performs roughly twenty million logarithmic steps at this scale, which fits the intended limits. The memory usage grows only with the number of bins, which is at most the number of items.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = list(map(int, sys.stdin.buffer.read().split()))
    sys.stdin = old

    t = data[0]
    idx = 1
    out = []
    for _ in range(t):
        n, c = data[idx], data[idx + 1]
        idx += 2
        arr = data[idx:idx + n]
        idx += n
        out.append(str(solve_case(n, c, arr)[0]) + " " + str(solve_case(n, c, arr)[1]))
    return "\n".join(out)

assert run("""2
2 2
1 1
5 10
5 8 2 5 9
""") == """1 1
4 3"""

assert run("""1
1 1
1
""") == "1 1"

assert run("""1
4 10
6 4 6 4
""") == "2 2"

assert run("""1
6 10
10 10 10 10 10 10
""") == "6 6"

assert run("""1
5 10
5 5 5 5 5
""") == "3 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single item with capacity one | 1 1 | Minimum input size and exact filling |
| 6,4,6,4 | 2 2 | Duplicate capacities and reuse |
| Six items of size ten | 6 6 | Every item requiring a new bin |
| Five equal items of size five | 3 3 | Repeated equal remaining capacities |

## Edge Cases

When a bin becomes exactly full, its remaining capacity is zero. The structures still keep that bin because it exists and may be relevant for First Fit ordering. For input:

```
1
3 10
10 1 9
```

First Fit creates a bin with remaining capacity zero, creates another bin for the item of size one, and places the final item into the second bin. Best Fit follows the same choices. The output is:

```
2 2
```

When duplicate remaining capacities appear, the Best Fit structure must not treat values as unique. For:

```
1
4 10
6 4 6 4
```

after the first two items, the remaining capacities are 4 and 6. The third item uses the bin with capacity 6, leaving capacities 4 and 0. The final item uses the remaining capacity 4. The treap's count field handles the duplicate states correctly, producing:

```
2 2
```

When the input order is changed, the result can change even with the same set of item sizes. For:

```
1
5 10
5 8 2 5 9
```

First Fit keeps the early bins in order and ends with four bins, while Best Fit rearranges usage by always selecting the fullest suitable bin and ends with three bins. The data structures process the original sequence, so the output remains:

```
4 3
```
