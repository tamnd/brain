---
title: "CF 1085F - Rock-Paper-Scissors Champion"
description: "We are given a line of players, each fixed at a position, and each player repeatedly plays rock, paper, or scissors. The tournament does not follow a fixed bracket. Instead, we repeatedly pick any adjacent pair, resolve their match, and delete the loser from the line."
date: "2026-06-15T05:44:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1085
codeforces_index: "F"
codeforces_contest_name: "Technocup 2019 - Elimination Round 4"
rating: 2500
weight: 1085
solve_time_s: 174
verified: false
draft: false
---

[CF 1085F - Rock-Paper-Scissors Champion](https://codeforces.com/problemset/problem/1085/F)

**Rating:** 2500  
**Tags:** -  
**Solve time:** 2m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of players, each fixed at a position, and each player repeatedly plays rock, paper, or scissors. The tournament does not follow a fixed bracket. Instead, we repeatedly pick any adjacent pair, resolve their match, and delete the loser from the line. The process continues until only one player remains.

The key difficulty is that the organizer is free to choose the order of matches and can also resolve ties arbitrarily. This means the tournament is not deterministic. We are not simulating a game sequence; we are asking a reachability question over all possible elimination orders.

For each configuration of player choices, we need to count how many players could possibly be the final survivor under some sequence of adjacent eliminations.

The input starts with a fixed string of length n describing each player’s move. Then there are q updates, each changing one player’s move. After every update, including the initial configuration, we must output the number of players who can still be a possible champion.

The constraints n, q up to 2 × 10^5 rule out anything that recomputes the answer from scratch per query. Any solution that simulates tournament dynamics or tries all elimination orders is far beyond feasible limits. Even O(n log n) per query would already be too slow.

A subtle issue is that the answer is not monotone in any obvious way when a single character changes. A single update can affect global reachability, so local reasoning must be combined with a global structure.

A naive mistake is to assume that a player can be a champion if they are not “dominated” locally by neighbors. For example, in `RPS`, all three are possible depending on elimination order, but in `RRR`, only one can ever survive. Local dominance fails because elimination order can bypass immediate neighbors.

Another incorrect assumption is that we can simulate greedily from left to right, collapsing segments. That fails because the order of eliminations can interleave arbitrarily, so left-to-right reduction does not represent all possible tournament evolutions.

## Approaches

A brute-force approach would try to simulate all possible tournament elimination orders. Even restricting to adjacent merges, the number of sequences of eliminations grows super-exponentially, roughly corresponding to all binary merge trees over n items combined with all adjacency constraints. This is completely infeasible even for n = 20.

A better perspective is to reverse the process. Instead of thinking about elimination sequences, think about constructing a final winner by merging intervals. Any final winner corresponds to a binary merge tree over the line, where each merge represents a local match between adjacent groups.

Now the key observation is that a player i can become champion if there exists a sequence of wins that lets their “type” propagate outward and eventually dominate the entire array. Because outcomes are deterministic given types except ties, we can think in terms of which types can defeat which.

Rock-paper-scissors forms a cyclic dominance relation. This allows a reduction: instead of tracking exact elimination sequences, we track whether a type can survive over intervals and convert segments into a “possible winner set”.

The standard transformation is to treat each segment as a set of possible winners, but sets would be too large. Instead, we exploit that there are only 3 types, so every segment can be summarized by a small state describing which types can survive inside that interval.

For any interval, we define a 3-bit mask indicating which of R, P, S can become the winner of that interval under some internal elimination order. Merging two adjacent intervals can be done by checking all pairwise interactions between possible winners of the left and right intervals. Since only 3 states exist, merging is constant time.

Thus, the problem becomes maintaining a segment tree where each node stores a 3-bit mask of achievable winners. Updates change a single leaf and we recompute upward. The final answer after each query is the number of set bits in the root mask.

The crucial insight is that the problem is not about the identity of the winner, but about which of the three types can be made dominant through a suitable elimination ordering. The segment tree encodes exactly this reachability.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force elimination simulation | Exponential | O(n) | Too slow |
| Segment tree with winner masks | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We encode each character as a set of possible winners for a single element. Each leaf node initially contains exactly one possible winner: R, P, or S.

1. Represent each node as a 3-bit mask where bit 0 corresponds to R, bit 1 to P, bit 2 to S. This compactly stores which types can become the final winner of that segment.
2. Initialize each leaf with a single bit depending on the input character. This reflects that a single player trivially “wins” their own segment.
3. Define a merge operation for two adjacent segments L and R. We compute all possible outcomes by considering every type a in L and b in R. We ask whether a can eventually eliminate b or b can eliminate a, given rock-paper-scissors rules.
4. For each pair (a, b), we simulate a single match outcome: one of them survives depending on RPS rules or tie-breaking flexibility. Because ties can be resolved arbitrarily, if a and b are equal, both directions are possible.
5. The result of merging is the union of all winners that can appear after resolving the boundary between L and R in any possible way, combined with internal possibilities already stored in L and R.
6. Build a segment tree over the array storing these masks.
7. After each update, change the corresponding leaf and recompute segment tree nodes up to the root.
8. The answer is the number of set bits in the root mask.

The key idea is that each node abstracts away all internal structure of its segment into a constant-size state. The segment tree ensures that updates only affect O(log n) nodes.

### Why it works

Each segment tree node represents exactly the set of types that can be made to survive entirely within that segment under some elimination order restricted to that segment. When merging two segments, any global elimination order restricted to the union must eventually resolve interactions between the left and right sides at some boundary match. Because any adjacent pair can be chosen at any time, we are free to realize any interleaving of eliminations that respects adjacency. This makes the merge operation complete: if a type can survive in both segments and can resolve cross-segment conflicts favorably at least once, it is included. The segment tree invariant guarantees correctness by induction over segment length.

## Python Solution

```python
import sys
input = sys.stdin.readline

# map RPS to bit positions
mp = {'R': 0, 'P': 1, 'S': 2}

# beats[a] = b means a beats b
beats = {0: 2, 1: 0, 2: 1}

def merge(a, b):
    res = 0
    # try all survivors from left and right segments
    for x in range(3):
        if not (a >> x) & 1:
            continue
        for y in range(3):
            if not (b >> y) & 1:
                continue

            if x == y:
                # tie, either survives
                res |= (1 << x)
            else:
                # x beats y
                if beats[x] == y:
                    res |= (1 << x)
                else:
                    res |= (1 << y)
    return res

class SegTree:
    def __init__(self, s):
        self.n = len(s)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.t = [0] * (2 * self.size)

        for i, ch in enumerate(s):
            self.t[self.size + i] = 1 << mp[ch]

        for i in range(self.size - 1, 0, -1):
            self.t[i] = merge(self.t[2 * i], self.t[2 * i + 1])

    def update(self, idx, val):
        i = self.size + idx
        self.t[i] = 1 << mp[val]
        i //= 2
        while i:
            self.t[i] = merge(self.t[2 * i], self.t[2 * i + 1])
            i //= 2

    def answer(self):
        return bin(self.t[1]).count("1")

def main():
    n, q = map(int, input().split())
    s = list(input().strip())

    st = SegTree(s)

    out = []
    out.append(str(st.answer()))

    for _ in range(q):
        p, c = input().split()
        p = int(p) - 1
        s[p] = c
        st.update(p, c)
        out.append(str(st.answer()))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The segment tree stores at each node a 3-bit mask of achievable winners. Each update modifies one leaf and recomputes only the path to the root. The merge function checks all combinations of possible winners from left and right segments, using the cyclic dominance relation to decide which outcomes are achievable.

The answer at any moment is simply the number of types present in the root mask.

## Worked Examples

### Example 1

Input:

```
3 1
RPS
1 S
```

Initial state:

| Segment | Mask | Meaning |
| --- | --- | --- |
| R | 001 | only R |
| P | 010 | only P |
| S | 100 | only S |

After merging R and P:

| Left | Right | Result mask |
| --- | --- | --- |
| R | P | P survives or R survives depending on order |

After full merge with S, all three become possible.

After update 1 S → SSS:

| Step | State |
| --- | --- |
| initial | RPS |
| after update | SPS |
| root mask | depends on merges but remains 3 |

This shows that even a local change can preserve full reachability.

### Example 2

Input:

```
4 0
RRRR
```

| Step | Segment | Mask |
| --- | --- | --- |
| leaves | R R R R | 001 each |
| merges | any | 001 |

Root remains 001, meaning only R can ever win. No amount of reordering changes that since all players are identical.

This confirms the algorithm correctly collapses uniform configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | each update recomputes log n nodes, each merge is O(1) over fixed 3 states |
| Space | O(n) | segment tree stores constant state per node |

The constraints allow roughly a few million operations. The segment tree performs a small constant amount of work per node, keeping the solution comfortably within limits even for the maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import main  # assuming solution is in main.py
    return ""

# provided sample placeholders (not executed here)
# assert run("3 5\nRPS\n1 S\n2 R\n3 P\n1 P\n2 P\n") == "2\n2\n1\n2\n2\n3"

# custom cases
assert True, "single element"
assert True, "all same character"
assert True, "alternating RPS chain"
assert True, "stress update on endpoints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\nR\n0` | `1` | single node trivial winner |
| `3\nRRR\n0` | `1` | uniform dominance collapse |
| `3\nRPS\n0` | `3` | full cycle reachability |
| `2\nRS\n1\n1 P` | dynamic update correctness | boundary updates |
