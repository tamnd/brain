---
title: "CF 1690G - Count the Trains"
description: "Each carriage has its own maximum speed. When all carriages start moving, a carriage cannot move faster than any carriage in front of it, so its actual speed becomes the minimum value seen so far from the left."
date: "2026-06-09T23:23:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1690
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 797 (Div. 3)"
rating: 2000
weight: 1690
solve_time_s: 285
verified: false
draft: false
---

[CF 1690G - Count the Trains](https://codeforces.com/problemset/problem/1690/G)

**Rating:** 2000  
**Tags:** binary search, data structures, greedy, sortings  
**Solve time:** 4m 45s  
**Verified:** no  

## Solution
## Problem Understanding

Each carriage has its own maximum speed. When all carriages start moving, a carriage cannot move faster than any carriage in front of it, so its actual speed becomes the minimum value seen so far from the left.

If the maximum speeds are

```
a = [10, 13, 5, 2, 6]
```

then the final speeds are

```
[10, 10, 5, 2, 2]
```

because every carriage is capped by the slowest carriage before it.

A train is a maximal consecutive segment of equal final speeds. In the example above the trains are

```
[10,10] [5] [2,2]
```

so the answer is 3.

After that, we receive updates. An update decreases one element of the array. After every update we must report the new number of trains.

The crucial observation is that the final speed of carriage `i` is

```
min(a[1], a[2], ..., a[i])
```

A new train begins exactly when this prefix minimum decreases.

That means the number of trains is equal to the number of positions that create a new prefix minimum.

The constraints are large enough that recomputing all prefix minima after every update is impossible. Across all test cases, both `n` and `m` sum to `10^5`, so we need something around `O((n + m) log n)`. Any solution that scans the entire array after each update would perform about `10^10` operations in the worst case.

A subtle point is that updates only decrease values. Nothing ever increases. This monotonicity is what makes an efficient dynamic structure possible.

Consider:

```
a = [5, 8, 6]
```

The train starts are positions:

```
1 (value 5)
```

Now decrease `a[2]` to `4`.

```
a = [5, 4, 6]
```

Position 2 becomes a new train start because it is smaller than every previous value.

A careless solution that only updates information at index 2 would miss the fact that train boundaries farther to the right may disappear.

Another tricky case is equality:

```
a = [5, 5, 5]
```

There is only one train.

A position creates a new train only when its value is **strictly smaller** than all previous prefix minima. Using `<=` instead of `<` would incorrectly count three trains.

## Approaches

The brute force solution follows the definition directly.

After every update, rebuild the prefix minima array. Every time the prefix minimum decreases, a new train begins. Counting these decreases gives the answer.

This is correct because the final speed of each carriage is exactly its prefix minimum. Unfortunately, rebuilding prefix minima costs `O(n)` per query, leading to `O(nm)` work overall. With both values around `10^5`, this is far too slow.

The key observation is that we do not actually care about every carriage. We only care about positions that create new prefix minima.

Let us call such positions **leaders**.

For example:

```
a = [10, 13, 5, 2, 6]
```

The leaders are:

```
1 (10)
3 (5)
4 (2)
```

The number of leaders is exactly the number of trains.

Now look at what happens after a decrease.

Suppose position `k` becomes smaller. Only two things can happen.

First, `k` may become a new leader if it drops below the previous leader's value.

Second, once `k` becomes a leader (or an existing leader becomes even smaller), some leaders to its right may stop being leaders because the new prefix minimum reaches them earlier.

The leaders are naturally ordered by position, and their values are strictly decreasing. This allows us to remove affected leaders by walking right until we encounter a leader with a smaller value.

We maintain the current set of leaders dynamically. An ordered structure lets us find the previous and next leaders in `O(log n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((n + m) log n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the initial set of leaders.

Scan from left to right while maintaining the smallest value seen so far. Position `i` becomes a leader if `a[i]` is strictly smaller than that minimum.
2. Store leaders in an ordered structure.

We need to quickly find the leader immediately before or after any position. A Fenwick tree over leader positions provides this functionality.
3. Process an update `(k, d)`.

Decrease `a[k]` by `d`.
4. Find the previous leader before `k`.

If there is no previous leader, then `k = 1` effectively has no restriction from the left.
5. Check whether `k` should be a leader.

Position `k` is a leader exactly when

```
a[k] < value_of_previous_leader
```

or when it is the first position.
6. If `k` becomes a leader and is not already one, insert it into the leader structure.
7. If `k` is currently a leader, remove invalid leaders to its right.

Repeatedly look at the next leader after `k`.

While its value is greater than or equal to `a[k]`, it can no longer create a new prefix minimum, so remove it.

Stop as soon as a leader with a smaller value is reached.
8. The current number of leaders is the answer after this update.

### Why it works

A leader is exactly a position where the prefix minimum decreases. Since train boundaries occur precisely at decreases of the prefix minimum, leaders and trains are the same object.

The set of leaders always has strictly decreasing values. When a value at position `k` decreases, only prefix minima starting at `k` can change. Positions before `k` are unaffected.

If `a[k]` becomes smaller than the previous leader value, `k` must become a new leader. Any later leader whose value is not smaller than `a[k]` can no longer represent a decrease of the prefix minimum, so it must be removed. The first later leader with a smaller value remains valid, and every leader after it also remains valid because leader values are strictly decreasing.

Thus the maintained leader set is always exactly the set of prefix-minimum positions, so its size is always the number of trains.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, delta):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx):
        bit = self.bit
        res = 0
        while idx > 0:
            res += bit[idx]
            idx -= idx & -idx
        return res

    def kth(self, k):
        idx = 0
        bitmask = 1 << (self.n.bit_length() - 1)

        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bitmask >>= 1

        return idx + 1

def solve():
    t = int(input())

    for _ in range(t):
        line = input()
        while line.strip() == "":
            line = input()

        n, m = map(int, line.split())
        a = [0] + list(map(int, input().split()))

        fw = Fenwick(n)
        leader = [False] * (n + 1)

        cur_min = 10**18
        trains = 0

        for i in range(1, n + 1):
            if a[i] < cur_min:
                cur_min = a[i]
                leader[i] = True
                fw.add(i, 1)
                trains += 1

        def next_leader(pos):
            cnt = fw.sum(pos)
            if cnt >= trains:
                return 0
            return fw.kth(cnt + 1)

        ans = []

        for _ in range(m):
            k, d = map(int, input().split())
            a[k] -= d

            cnt_before = fw.sum(k - 1)

            if cnt_before == 0:
                should_be_leader = True
            else:
                prev_leader = fw.kth(cnt_before)
                should_be_leader = a[k] < a[prev_leader]

            if should_be_leader and not leader[k]:
                leader[k] = True
                fw.add(k, 1)
                trains += 1

            if leader[k]:
                nxt = next_leader(k)

                while nxt and a[nxt] >= a[k]:
                    leader[nxt] = False
                    fw.add(nxt, -1)
                    trains -= 1
                    nxt = next_leader(k)

            ans.append(str(trains))

        print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores a `1` at every leader position and `0` elsewhere. This allows us to find predecessors and successors among leaders without storing a balanced BST.

The `kth()` method is the standard Fenwick order-statistics operation. Given a rank, it returns the position of that leader.

The update logic mirrors the proof. First we decide whether `k` becomes a leader. Then, if `k` is a leader, we repeatedly remove dominated leaders to its right.

A common mistake is using `<=` when deciding whether a position becomes a leader. Equal values do not create a new prefix minimum, so the condition must be strictly `<`.

Another easy mistake is removing leaders with `>` instead of `>=`. If two leaders have equal values, the later one is not a genuine prefix-minimum position and must disappear.

## Worked Examples

### Sample 1

```
n = 4
a = [6, 2, 3, 7]
```

Initial leaders:

```
1 (6), 2 (2)
```

Number of trains = 2.

First update:

```
(3, 2)
```

Array becomes:

```
[6, 2, 1, 7]
```

| Step | Leaders |
| --- | --- |
| Before update | {1, 2} |
| Position 3 drops to 1 | {1, 2, 3} |
| Position 4 has value 7 ≥ 1 | removed |
| Final | {1, 2, 3} |

Answer: `3`.

Second update:

```
(4, 7)
```

Array becomes:

```
[6, 2, 1, 0]
```

| Step | Leaders |
| --- | --- |
| Before update | {1, |
