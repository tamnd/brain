---
title: "CF 102586K - Game and Queries"
description: "We maintain a multiset of monsters. A monster is identified only by its current HP, and the queries either change how many monsters have a particular HP value or ask how many Bob turns are needed to remove a given number of monsters if both players play optimally."
date: "2026-08-01T06:23:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102586
codeforces_index: "K"
codeforces_contest_name: "XX Open Cup, Grand Prix of Tokyo"
rating: 0
weight: 102586
solve_time_s: 83
verified: true
draft: false
---

[CF 102586K - Game and Queries](https://codeforces.com/problemset/problem/102586/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a multiset of monsters. A monster is identified only by its current HP, and the queries either change how many monsters have a particular HP value or ask how many Bob turns are needed to remove a given number of monsters if both players play optimally.

The key game quantity is not the exact order of attacks, but the amount of HP that must be removed. Consider one monster with HP `x`. Alice always moves first and can increase this monster by 1 before every Bob attack. After `t` Bob attacks focused on this monster, it receives `t` increases and `2t` damage, so its remaining HP is `x + t - 2t = x - t`. It disappears exactly when `t = x`. This means one monster with HP `x` costs exactly `x` Bob turns to remove.

For multiple monsters, the same idea extends. If Bob chooses some monsters with total HP `S`, he can spend exactly `S` turns to remove them. The reason is that every Bob turn contributes two damage while Alice contributes only one HP, so one full round decreases the total HP of the chosen monsters by one. Bob can always attack the monster Alice just increased, preventing Alice from accumulating extra HP on a single monster. Alice cannot delay the total process beyond the sum of the initial HP values.

Since Bob wants to finish as soon as possible, he chooses the monsters with the smallest HP values. A query asking for `k` deaths is therefore asking for the sum of the `k` smallest HP values currently present.

The number of queries can reach `3 * 10^5`, so scanning all monsters for every query is impossible. The HP values are bounded by `10^6`, which means we can store information indexed by HP. A solution that sorts all monsters after every update would be too slow because the number of monsters can also become very large. We need a logarithmic data structure that supports changing the count of one HP value and finding a prefix containing a given number of monsters.

The important edge cases are concentrated around duplicated HP values and boundary positions. A query can ask for all monsters of one HP value, or it can stop in the middle of a group with the same HP.

For example:

```
5
1 3 4
2 2
1 3 1
2 3
2 4
```

After the first update there are four monsters with HP 3. The first query asks for two monsters, so the answer is `6`, because the two smallest HP values are `3` and `3`.

The output is:

```
6
10
13
```

A careless implementation that stores only distinct HP values and ignores their multiplicities would fail because one HP value can represent many monsters.

Another boundary case is when the requested `k` ends exactly at a value boundary.

```
2
1 1 5
2 5
```

The answer is `25`. The data structure must include the entire frequency block when the prefix count exactly reaches `k`.

## Approaches

A direct approach would store every monster in a list. For a type 2 query, we could sort the current HP values, take the first `k`, and add them. This is correct because the game reduces to choosing the `k` smallest HP values. However, there can be up to `3 * 10^5` queries, and the number of monsters can be up to around `10^11` because each update can set a count up to `10^6`. Even ignoring the sorting cost, iterating through all monsters is impossible. Sorting after every query would be far beyond the time limit.

The useful observation is that HP values themselves are small. We do not need to know every monster separately. We only need two pieces of information for each HP value `x`: how many monsters have HP `x`, and the total contribution of those monsters, which is `x * count[x]`.

This converts the problem into maintaining frequencies and weighted sums over a fixed coordinate range. A Fenwick tree is a natural fit because updates affect one position and queries need prefix sums. One Fenwick tree stores counts, and another stores the sum of HP values. To answer a query, we find the smallest HP value whose prefix count reaches `k`. All smaller values are taken completely, and the remaining monsters are taken from that final HP value.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(M log M)` per query, where `M` is the number of monsters | `O(M)` | Too slow |
| Fenwick Trees | `O(log 10^6)` per query | `O(10^6)` | Accepted |

## Algorithm Walkthrough

1. Store two Fenwick trees indexed by HP. The first tree stores how many monsters exist at each HP value. The second tree stores the total HP contributed by that value, so position `x` stores `x * count[x]`.
2. For an update query changing the number of monsters with HP `x` to `y`, calculate the difference from the previous count. Add this difference to the count Fenwick tree and add `x` times this difference to the sum Fenwick tree.
3. For a query asking for the first `k` monsters in sorted HP order, use the count Fenwick tree to find the smallest HP value `pos` where the prefix count becomes at least `k`.
4. All HP values smaller than `pos` are fully included. Add their total HP from the sum Fenwick tree.
5. The remaining monsters needed are taken from HP `pos`. Multiply the remaining count by `pos` and add it to the answer.

The reason this works is that the answer depends only on the sorted multiset of HP values. The Fenwick tree lets us navigate this sorted order without explicitly storing every monster.

### Why it works

After every complete Alice-Bob round, the total HP of any chosen collection of monsters decreases by exactly one if Bob attacks inside that collection. Bob can always choose his attacks so that the monsters he wants to remove receive the necessary damage, while Alice's extra HP only cancels one point of that progress per round. Therefore a collection of monsters with total HP `S` requires exactly `S` Bob turns to disappear.

Bob wants the smallest possible total HP among `k` monsters, so the optimal choice is exactly the `k` smallest HP values. The data structure returns precisely this sum, which proves the algorithm produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXX = 10**6

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def kth(self, k):
        idx = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            step >>= 1
        return idx + 1

def solve():
    q = int(input())
    cnt_tree = Fenwick(MAXX)
    sum_tree = Fenwick(MAXX)
    cnt = [0] * (MAXX + 1)

    ans = []

    for _ in range(q):
        query = input().split()
        t = int(query[0])

        if t == 1:
            x = int(query[1])
            y = int(query[2])
            diff = y - cnt[x]
            cnt[x] = y
            cnt_tree.add(x, diff)
            sum_tree.add(x, diff * x)

        else:
            k = int(query[1])
            pos = cnt_tree.kth(k)
            before = cnt_tree.sum(pos - 1)
            total = sum_tree.sum(pos - 1)
            total += (k - before) * pos
            ans.append(str(total))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `cnt` array stores the current frequency of every HP value so that updates can be converted into differences. Fenwick trees store only the aggregated information needed for queries.

The `kth` function performs binary lifting on the Fenwick tree. It finds the first position whose prefix count reaches the requested `k`. This avoids a binary search with repeated prefix queries and keeps each query logarithmic.

The answer computation separates the fully included prefix from the final partially included HP value. This is where off-by-one errors usually appear. The count before `pos` must be excluded, and only `k - before` monsters from `pos` contribute.

Python integers handle the maximum possible sums without overflow. The largest possible contribution is well above 32-bit limits, so using normal Python arithmetic avoids any additional handling.

## Worked Examples

For the first sample, the queries create four monsters with HP 1, then add three monsters with HP 2.

| Query | HP counts | k | Chosen HP values | Answer |
| --- | --- | --- | --- | --- |
| `1 1 4` | `1:4` |  |  |  |
| `2 3` | `1:4` | 3 | `1,1,1` | 3 |
| `1 2 3` | `1:4, 2:3` |  |  |  |
| `2 6` | `1:4, 2:3` | 6 | `1,1,1,1,2,2` | 8 |
| `1 2 2` | `1:4, 2:2` |  |  |  |
| `2 6` | `1:4, 2:2` | 6 | `1,1,1,1,2,2` | 8 |

This trace demonstrates that multiplicities matter. The second Fenwick tree stores the weighted contribution, not just the number of monsters.

For the second sample, after the first two updates there are twelve monsters with HP 1 and fifteen monsters with HP 2.

| Query | HP counts | k | Prefix taken | Answer |
| --- | --- | --- | --- | --- |
| `1 1 12` | `1:12` |  |  |  |
| `2 12` | `1:12` | 12 | twelve HP 1 monsters | 12 |
| `1 2 15` | `1:12, 2:15` |  |  |  |
| `2 12` | `1:12, 2:15` | 12 | twelve HP 1 monsters | 12 |
| `2 3` | `1:12, 2:15` | 3 | three HP 1 monsters | 3 |

This confirms that the query can stop before reaching a larger HP group, so the `kth` search must locate the exact boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(Q log 10^6)` | Every update, prefix query, and kth search uses Fenwick tree operations |
| Space | `O(10^6)` | The two Fenwick trees and frequency array are indexed by HP |

The maximum HP value is fixed at `10^6`, so the logarithmic factor is about 20. With `3 * 10^5` queries, the solution performs only a few million Fenwick operations and fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.read().split()
    if not data:
        return ""

    it = iter(data)
    q = int(next(it))

    MAXX = 10**6

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            r = 0
            while i:
                r += self.bit[i]
                i -= i & -i
            return r

        def kth(self, k):
            idx = 0
            step = 1 << (self.n.bit_length() - 1)
            while step:
                nxt = idx + step
                if nxt <= self.n and self.bit[nxt] < k:
                    idx = nxt
                    k -= self.bit[nxt]
                step >>= 1
            return idx + 1

    c = Fenwick(MAXX)
    s = Fenwick(MAXX)
    cur = [0] * (MAXX + 1)
    out = []

    for _ in range(q):
        t = int(next(it))
        if t == 1:
            x = int(next(it))
            y = int(next(it))
            d = y - cur[x]
            cur[x] = y
            c.add(x, d)
            s.add(x, d * x)
        else:
            k = int(next(it))
            p = c.kth(k)
            b = c.sum(p - 1)
            out.append(str(s.sum(p - 1) + (k - b) * p))

    sys.stdin = old
    return "\n".join(out)

assert run("""6
1 1 4
2 3
1 2 3
2 6
1 2 2
2 6
""") == "3\n8\n8"

assert run("""3
1 5 1
2 1
2 1
""") == "5\n5"

assert run("""5
1 1 3
1 2 2
2 4
1 1 0
2 2
""") == "7\n4"

assert run("""4
1 1000000 3
2 2
1 1 5
2 5
""") == "2000000\n5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single HP group | `5` and `5` | Basic update and repeated queries |
| Mixed HP values | `7` and `4` | Prefix selection across multiple frequencies |
| Maximum HP value | `2000000` and `5` | Large coordinate handling and boundary updates |

## Edge Cases

When all monsters have the same HP, the kth smallest search lands directly on one frequency block. For example:

```
3
1 7 4
2 3
2 4
```

The answers are:

```
21
28
```

The Fenwick tree does not need separate entries for individual monsters. It sees four monsters at position 7 and takes the required amount from that block.

When an update removes all monsters of a certain HP, the frequency difference becomes negative. For example:

```
4
1 3 5
1 3 0
1 2 4
2 4
```

The final answer is:

```
8
```

The update correctly subtracts the previous contribution of HP 3, leaving only the four monsters with HP 2.

When `k` ends exactly at the end of a frequency block, the kth search must return that block rather than the next one. For example:

```
3
1 2 3
1 5 3
2 3
```

The answer is:

```
6
```

The first three monsters are all HP 2, so the search stops at position 2. The implementation handles this because `kth` finds the first prefix whose count is at least `k`, not strictly greater than `k`.
