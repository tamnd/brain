---
title: "CF 102367E - XOR Pairing"
description: "We have an even number of indexed stones, and each stone carries an integer between 0 and 1000. We must partition all stones into pairs."
date: "2026-08-12T23:43:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102367
codeforces_index: "E"
codeforces_contest_name: "Fall 2019 ICPC-style Waterloo Local Contest"
rating: 0
weight: 102367
solve_time_s: 411
verified: true
draft: false
---

[CF 102367E - XOR Pairing](https://codeforces.com/problemset/problem/102367/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an even number of indexed stones, and each stone carries an integer between 0 and 1000. We must partition all stones into pairs. A pair containing stones `i` and `j` contributes `x[i] ^ x[j]` to the total cost, and we want both the minimum possible total cost and the number of different pairings attaining that minimum, modulo `10^9 + 7`.

The indices matter even when two stones contain the same value. For example, four stones containing `5 5 5 5` have three different pairings, because the stones themselves are distinct even though all pair costs are zero.

The official sample has `N = 6`, followed by `7 14 17 4 2 1`, and its answer is `31 3`.

The upper bound `N <= 74` is small enough for algorithms around `O(N^2)` or `O(N^2 log V)`, but completely rules out enumerating all pairings. There are `(N-1)!!` perfect pairings, so for `N = 74` a brute-force search has `(73)!!` leaves, and every leaf requires 37 XOR computations. The exact number of pair-cost evaluations is `37 * 73!!`, which is on the order of `10^55`. The value bound `x[i] <= 1000` is especially useful because only bits `0` through `9` can occur, giving us a binary decomposition with only 10 levels.

There are several edge cases that a careless implementation can mishandle. With two stones, such as

```
2
0 1000
```

the only pairing has cost `1000`, so the answer is `1000 1`. An implementation that assumes every recursive node has two nonempty children can fail here because one side of the binary split may be empty.

Duplicate values require counting indexed stones separately. For

```
4
5 5 5 5
```

the answer is `0 3`, because all three perfect pairings have cost zero. Counting only distinct value arrangements would incorrectly return one.

A more subtle case occurs when both sides of a bit split have odd size. For the official sample,

```
6
7 14 17 4 2 1
```

the highest bit separates `{17}` from `{7,14,4,2,1}`, so both sides are odd. Exactly one pair must cross this split, but there are multiple possible choices for that pair. A greedy choice based only on the immediate XOR can miss the globally optimal pairing and, even worse, can miss some optimal pairings when counting.

The boundary value `1000` also deserves attention. For

```
4
0 1000 511 512
```

the optimal pairs are `(0, 511)` and `(1000, 512)`, with costs `511` and `488`, giving `999 1`. Treating values as if they only occupied the lowest nine bits would put `1000` in the wrong partition.

## Approaches

The direct approach is to generate every perfect matching recursively. Pick one currently unused stone, pair it with every other unused stone, and recurse. This is correct because every perfect matching has exactly one partner for the first chosen stone, so the recursion eventually visits every pairing exactly once. The problem is the number of leaves. With `N` stones there are `(N-1)!!` pairings, and each pairing contains `N/2` edges. At `N = 74`, that means exactly `37 * 73!!` pair-cost calculations, far beyond what any implementation can perform.

The useful structure comes from looking at the highest differing bit of two values. Suppose a binary trie node represents values whose higher bits are already identical, and suppose its two children differ at bit `b`. Any edge crossing between the two children has bit `b` set, so it contributes at least `2^b`.

The crucial exchange argument is that an optimal matching can contain at most one edge crossing between the two children. Suppose two crossing pairs are `(a,b)` and `(c,d)`, where `a,c` belong to the left child and `b,d` belong to the right child. Their two edges together contribute at least `2^(b+1)` from the current bit alone. Replace them by `(a,c)` and `(b,d)`. Both new edges have the current bit equal to zero, and each has value strictly below `2^b`, so their combined cost is strictly below `2^(b+1)`. The replacement is always better.

This gives a very strong recursive structure. If both children have even size, an optimal solution uses no crossing pair. If both children have odd size, an optimal solution uses exactly one crossing pair. If the whole node has odd size, its two children have opposite parity, and an optimal solution uses no crossing pair, leaving one unmatched stone in the odd child.

The remaining question is what information an odd-sized subtree must return. We cannot simply return one number, because the parent needs to know which stone is left unmatched. We instead compute, for every stone `i` in an odd subtree, the minimum cost of pairing all other stones and leaving `i` unmatched, together with the number of ways to attain that cost. Since there are at most 74 stones, storing one state per stone is cheap.

At a node with two odd children, we try every possible unmatched stone `i` from the left child and `j` from the right child. Those two stones become the unique crossing pair, while the remaining stones are optimally matched inside their respective children. This is the only place where a quadratic transition is needed.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O((N/2) * (N-1)!!)` | `O(N)` | Too slow |
| Optimal | `O(N^2 log V)` | `O(N log V)` | Accepted |

Here `V <= 1000`, so `log V <= 10`.

## Algorithm Walkthrough

1. Precompute `ways[k]`, the number of perfect pairings of `k` indexed stones. For even `k`, the recurrence is `ways[k] = (k - 1) * ways[k - 2]`, with `ways[0] = 1`. This also gives the number of ways to match all but one stone in an odd-sized set, because `ways[k - 1]` is the required count.
2. Recursively process a set of stone indices from the most significant bit toward the least significant bit. Split the indices according to the current bit. If all values in the set have the same bit, there is only one nonempty child, so we simply continue to the next bit.
3. For an even-sized node whose two children are both even, combine their independent optimal matchings. No crossing pair is needed, because two crossing pairs would be strictly worse and zero crossing pairs are feasible. The cost is the sum of the two child costs, and the number of ways is their product.
4. For an even-sized node whose two children are both odd, exactly one crossing pair is required. For every stone `i` in the left child and every stone `j` in the right child, use their odd-subtree states and calculate

`dp_left[i] + dp_right[j] + (x[i] ^ x[j])`.

Keep the smallest value and sum the counts whenever another choice reaches the same minimum. Every resulting pairing has a unique crossing pair, so there is no double counting.
5. For an odd-sized node, exactly one child is odd and the other is even. The optimal solution has no crossing pair. The unmatched stone must consequently come from the odd child. Add the complete matching cost of the even child to every unmatched-stone state of the odd child, and multiply the corresponding counts.
6. When the recursion reaches below the last bit, all values in the current set are equal. Every pair has XOR zero. If the set has even size `m`, return cost zero and `ways[m]` pairings. If it has odd size, for each possible unmatched stone return cost zero and `ways[m - 1]` pairings.
7. Start the recursion with all indices and bit `9`, because 1000 is smaller than `2^10`. The returned even-state cost is the minimum total XOR, and its count is the number of minimum pairings modulo `10^9 + 7`.

### Why it works

The invariant is that every recursive state contains the optimal solution under the precise condition represented by that state. An even state represents a complete pairing of its stones, while an odd state indexed by `i` represents a pairing of every stone except `i`.

The exchange argument proves that an optimal matching never needs two edges crossing the two children of the current trie node. Consequently, an even node either has zero crossing edges when both children are even or exactly one crossing edge when both are odd. An odd node cannot use one crossing edge because its child parities differ, and using two or more would be strictly worse than the feasible zero-crossing construction. Thus every optimal matching has exactly one of the recursive forms considered by the transition.

At a leaf, all XOR values are zero, so the base cases count every optimal pairing. At internal nodes, the transitions enumerate every structurally possible optimal matching exactly once. Inductively, the returned minimum cost and count are correct for the root.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAX_BIT = 9

def solve_case(a):
    n = len(a)

    # ways[k] = number of perfect pairings of k indexed elements,
    # for even k.
    ways = [0] * (n + 1)
    ways[0] = 1
    for k in range(2, n + 1, 2):
        ways[k] = ways[k - 2] * (k - 1) % MOD

    def dfs(ids, bit):
        m = len(ids)

        # All remaining bits are equal, so every XOR is zero.
        if bit < 0:
            if m & 1:
                cnt = ways[m - 1]
                return [(0, cnt) for _ in ids]
            return (0, ways[m])

        mask = 1 << bit
        left = []
        right = []

        for i in ids:
            if a[i] & mask:
                right.append(i)
            else:
                left.append(i)

        # The current bit does not distinguish these values.
        if not left or not right:
            return dfs(ids, bit - 1)

        dl = dfs(left, bit - 1)
        dr = dfs(right, bit - 1)

        nl = len(left)
        nr = len(right)

        if m & 1:
            # Exactly one child is odd and the other is even.
            if nl & 1:
                odd_dp = dl
                even_cost, even_count = dr
            else:
                odd_dp = dr
                even_cost, even_count = dl

            result = []
            for cost, count in odd_dp:
                result.append(
                    (cost + even_cost, count * even_count % MOD)
                )
            return result

        # The current node is even.
        if (nl & 1) == 0:
            # Both children are even, so no crossing pair is needed.
            left_cost, left_count = dl
            right_cost, right_count = dr
            return (
                left_cost + right_cost,
                left_count * right_count % MOD
            )

        # Both children are odd, so exactly one crossing pair is needed.
        best_cost = None
        best_count = 0

        for i, (cost_i, count_i) in zip(left, dl):
            for j, (cost_j, count_j) in zip(right, dr):
                cand_cost = cost_i + cost_j + (a[i] ^ a[j])
                cand_count = count_i * count_j % MOD

                if best_cost is None or cand_cost < best_cost:
                    best_cost = cand_cost
                    best_count = cand_count
                elif cand_cost == best_cost:
                    best_count = (best_count + cand_count) % MOD

        return best_cost, best_count

    return dfs(list(range(n)), MAX_BIT)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    cost, count = solve_case(a)
    print(cost, count)

if __name__ == "__main__":
    solve()
```

The `ways` array handles the combinatorial base cases. For example, `ways[4] = 3`, corresponding to the three ways to partition four indexed stones into two pairs. Keeping these values modulo `10^9 + 7` is sufficient because every later count is formed from sums and products of these counts.

The recursive function returns two different types of states. An even-sized subtree returns one `(cost, count)` pair because all of its stones are matched. An odd-sized subtree returns one `(cost, count)` pair for every possible unmatched index. This distinction is what allows the parent to decide which two stones should form its unique crossing pair.

The partition uses `1 << bit`, with bit `9` as the starting bit. Since `1000 < 1024`, no higher bit can occur. The recursive call with `bit - 1` eventually reaches `-1`, where all remaining values are identical with respect to every possible bit.

The quadratic loop is only executed when both children are odd. Each candidate crossing pair uses one state from each child. The multiplication of counts combines independent optimal choices from the two subtrees, while the final sum accumulates different choices of the crossing edge. Counts are reduced modulo `MOD` after every multiplication or addition.

Python integers do not overflow, so the cost calculations need no special integer type. The maximum actual cost is at most `37 * 1023`, which is tiny anyway.

## Worked Examples

The official sample is

```
6
7 14 17 4 2 1
```

At bit 4, the values split into `{7,14,4,2,1}` and `{17}`. Both groups are odd, so exactly one crossing pair must be chosen. The first group needs one unmatched stone, and the table shows the optimal cost of matching the other four stones for each possible unmatched index.

| Unmatched in `{7,14,4,2,1}` | Internal cost | Number of ways | XOR with `17` | Total |
| --- | --- | --- | --- | --- |
| `7` | 13 | 1 | 22 | 35 |
| `14` | 6 | 1 | 31 | 37 |
| `4` | 12 | 1 | 21 | 33 |
| `2` | 14 | 1 | 19 | 33 |
| `1` | 15 | 3 | 16 | 31 |

The minimum is obtained by leaving `1` unmatched inside the lower group and pairing it with `17`. There are three optimal ways to match `{7,14,4,2}` with cost 15, so the final answer is `31 3`. The three possibilities are different because the stones are indexed.

For a second example, consider

```
4
0 1 2 3
```

At bit 1, the two children are `{0,1}` and `{2,3}`, both of which are even. The optimal structure consequently contains no crossing pair at this bit.

| Bit | Left group | Right group | Left state | Right state | Combined result |
| --- | --- | --- | --- | --- | --- |
| `1` | `0,1` | `2,3` | cost `1`, count `1` | cost `1`, count `1` | cost `2`, count `1` |
| `0` | inside `{0,1}` | inside `{2,3}` | pair `0,1` | pair `2,3` | unchanged |

The unique optimal pairing is `(0,1)` and `(2,3)`, with XOR costs `1` and `1`. The answer is `2 1`. This example demonstrates the even-even transition, where the two halves can be solved independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N^2 log V)` | At each bit, pairs of elements are considered only when they lie in opposite children of the same trie node. Across one level there are `O(N^2)` such pairs. |
| Space | `O(N log V)` | Each element participates in one recursive state per bit, and each odd state stores one pair of values. |

Here `V <= 1000`, so `log V` is at most 10. With `N <= 74`, the quadratic factor is only a few thousand operations per bit, plus the small recursive overhead. The algorithm is comfortably inside the 3 second and 256 MB limits.

## Test Cases

The following tests assume the submitted solution is available as `solution.py` and exposes `solve_case(a)`.

```python
import sys
import io

from solution import solve_case

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]
    cost, count = solve_case(a)
    return f"{cost} {count}"

# Provided sample
assert run("""
6
7 14 17 4 2 1
""") == "31 3", "sample 1"

# Minimum-size input
assert run("""
2
0 1000
""") == "1000 1", "minimum size"

# All values equal, with four indexed stones
assert run("""
4
5 5 5 5
""") == "0 3", "all equal"

# Boundary values and a highest-bit split
assert run("""
4
0 1000 511 512
""") == "999 1", "boundary values"

# A slightly larger case where every optimal pair has XOR 1
assert run("""
6
0 1 2 3 4 5
""") == "3 1", "adjacent XOR pairs"

# Maximum-size input. For equal values the minimum cost is zero,
# and every perfect pairing is optimal.
MOD = 10**9 + 7
ways = [0] * 75
ways[0] = 1
for k in range(2, 75, 2):
    ways[k] = ways[k - 2] * (k - 1) % MOD

max_input = "74\n" + " ".join(["1000"] * 74) + "\n"
assert run(max_input) == f"0 {ways[74]}", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 0 1000` | `1000 1` | Minimum `N` and a split with an empty recursive side |
| `4 / 5 5 5 5` | `0 3` | Indexed duplicates and combinatorial counting |
| `4 / 0 1000 511 512` | `999 1` | Highest allowed value and bit-boundary behavior |
| `6 / 0 1 2 3 4 5` | `3 1` | Multiple trie levels with a unique optimal structure |
| `74 / 1000 ... 1000` | `0 73!! mod MOD` | Maximum `N` and the largest possible number of optimal pairings |

## Edge Cases

For the two-stone case

```
2
0 1000
```

the root eventually contains only those two stones. The odd/even transitions reduce to a single even leaf containing two equal-with-respect-to-the-current-recursion values only after all distinguishing bits have been processed. The two stones must form one pair, giving cost `0 ^ 1000 = 1000` and exactly one pairing. The output is `1000 1`.

For duplicate values,

```
4
5 5 5 5
```

all four indices reach the same leaf. The leaf has four stones, so its cost is zero and `ways[4] = 3`. The algorithm never merges equal-valued stones into one object, so all three indexed pairings are counted. The output is `0 3`.

For the official sample,

```
6
7 14 17 4 2 1
```

the highest bit separates one stone from five stones. Both sides are odd, forcing exactly one cross pair. The dynamic state for the five-stone side keeps the identity of its unmatched stone, and trying each possible unmatched index reveals that `1` paired with `17` gives the minimum total of `31`. There are three optimal internal matchings for the other four stones, producing `31 3`.

For the boundary case,

```
4
0 1000 511 512
```

the best pairing is `(0,511)` and `(1000,512)`. Their XOR values are `511` and `488`, respectively, so the total is `999`. The other possible pairings have larger totals. The trie begins at bit 9, where `1000` and `512` are on the high side while `0` and `511` are on the low side, so the algorithm handles the boundary without any special numerical case. The output is `999 1`.

For the maximum input,

```
74
1000 1000 ... 1000
```

every XOR is zero. The recursive process reaches a single leaf containing all 74 indexed stones. The cost is zero, and every perfect matching is optimal. The count is exactly `73!!`, computed modulo `10^9 + 7` by the `ways` recurrence. This case exercises both the maximum recursion state size and the modular counting logic.
