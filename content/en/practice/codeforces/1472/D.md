---
title: "CF 1472D - Even-Odd Game"
description: "We are given an array of integers, and two players alternately remove elements from it. Alice starts first. Every time a player removes a number, only certain values actually contribute to their score: Alice gains points only from even numbers she picks, while Bob gains points…"
date: "2026-06-11T00:31:52+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1472
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 693 (Div. 3)"
rating: 1200
weight: 1472
solve_time_s: 113
verified: true
draft: false
---

[CF 1472D - Even-Odd Game](https://codeforces.com/problemset/problem/1472/D)

**Rating:** 1200  
**Tags:** dp, games, greedy, sortings  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and two players alternately remove elements from it. Alice starts first. Every time a player removes a number, only certain values actually contribute to their score: Alice gains points only from even numbers she picks, while Bob gains points only from odd numbers he picks. Picking the “wrong parity” still removes the number but yields zero score.

The game ends when all elements are removed, and the winner is decided by comparing the total scores.

The key difficulty is that both players are not just picking greedily for themselves. Every removal affects future availability, so optimal play must consider denying the opponent good opportunities as well as maximizing personal gain.

The input size reaches up to 2·10^5 total elements across test cases. This immediately rules out any simulation of all possible move sequences. A full game-tree approach would branch at each step and grow factorially, which is far beyond feasible limits. Even a DP over subsets is impossible due to exponential state space.

The important observation is that the rules depend only on whether a number is even or odd, and on its value only when it contributes to a score. That means structure is heavily reducible.

A subtle edge case appears when all numbers belong to one parity class. For example, if all numbers are odd, Alice never gains anything and Bob collects everything he picks. A naive approach that tries to simulate “optimal blocking” might still incorrectly assume Alice can interfere, but she cannot change Bob’s access to odd numbers in a meaningful scoring sense. Similarly, if all numbers are even, Bob’s score is always zero.

Another edge case arises when the largest numbers belong to the “wrong” parity for a player. For example, Alice picking a large odd number does not help her score but removes it from Bob’s potential gain. This creates a trade-off that a greedy-by-value approach alone might mis-handle unless parity separation is explicit.

## Approaches

A brute-force solution would simulate all possible moves. At each turn, a player chooses any remaining element, updates scores depending on parity, and recurses. This correctly models the game because it tries every possible decision path. However, each state has up to O(n) choices and depth n, leading to roughly n! possible sequences. Even with memoization, the state space is the multiset of remaining elements with turn information, which is astronomically large.

The key simplification comes from recognizing that the actual value of a number matters only when it is collected as a scoring move. Otherwise, it is just a blocking move. This suggests separating numbers into two independent ordered pools: even numbers and odd numbers. Each player only benefits from one of these pools.

Now the game becomes a competition over who gets to pick from each pool more effectively. Since both players always prefer higher scoring opportunities, optimal play reduces to considering sorted order within each parity group. Players effectively take turns consuming the best remaining available values, but only the relevant parity contributes to their score.

A crucial structural insight is that all decisions reduce to ordering of picks, and optimal play is equivalent to processing the numbers in descending order while alternating turns, with score updates depending on parity-role alignment.

This removes game-tree complexity entirely and replaces it with a single sorted traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (sorting + greedy simulation) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate the array into even and odd values and sort the entire array in descending order.

Sorting ensures that both players always face the most valuable remaining choice first, which is necessary because lower values never become better later.
2. Initialize two counters for scores: AliceScore and BobScore, both starting at zero.

These track only effective gains, since non-scoring moves still influence future availability but not totals.
3. Iterate through the sorted array, treating each position as a turn in strict alternation, starting with Alice.

This reflects optimal play structure: since players always remove one element per turn, turn order is fixed.
4. On Alice’s turns, if the current number is even, add it to AliceScore. Otherwise do nothing.

Alice never benefits from odd numbers, so picking them is purely defensive.
5. On Bob’s turns, if the current number is odd, add it to BobScore. Otherwise do nothing.

Bob mirrors Alice with opposite parity.
6. After processing all elements, compare scores and declare the winner accordingly.

The important implicit idea is that optimal play always consumes numbers in descending order regardless of parity preference. Any deviation would allow the opponent to take a higher value on their next turn, which is strictly worse since scores depend only on collected values and not timing.

### Why it works

The invariant is that after k moves, the k largest remaining numbers have been removed in some order consistent with optimal play, and no player can improve their outcome by delaying or skipping a higher-value number. Since scoring depends only on ownership of parity-matching picks, the optimal strategy reduces to deterministic assignment of each sorted element to a turn, without needing to consider alternative branches.

Any attempt to take a smaller number while leaving a larger one available gives the opponent access to that larger number on their next move, which can only increase the opponent’s best achievable score or reduce your own. Thus the greedy ordering is stable under optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        alice = 0
        bob = 0
        
        for i, x in enumerate(a):
            if i % 2 == 0:
                if x % 2 == 0:
                    alice += x
            else:
                if x % 2 == 1:
                    bob += x
        
        if alice > bob:
            out.append("Alice")
        elif bob > alice:
            out.append("Bob")
        else:
            out.append("Tie")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first sorts each test case in descending order so that the highest-value choices are resolved first. The loop then alternates turns using the index parity. Even indices correspond to Alice and odd indices to Bob, since Alice starts. Each player only accumulates score when the parity condition matches their scoring rule.

A subtle implementation detail is that we do not simulate removal explicitly. The sorted array implicitly represents the sequence of removals under optimal play, so index traversal replaces stateful deletion entirely.

## Worked Examples

### Example 1

Input:

```
4
5 2 7 3
```

Sorted array is `[7, 5, 3, 2]`.

| Step | Turn | Picked | AliceScore | BobScore |
| --- | --- | --- | --- | --- |
| 1 | Alice | 7 | 0 | 0 |
| 2 | Bob | 5 | 0 | 5 |
| 3 | Alice | 3 | 0 | 5 |
| 4 | Bob | 2 | 0 | 5 |

Alice never gains points, Bob collects 5 and 2. Bob wins.

This demonstrates how large odd values are more valuable to Bob than to Alice, and ordering by value ensures Bob captures them when possible.

### Example 2

Input:

```
3
3 2 1
```

Sorted array is `[3, 2, 1]`.

| Step | Turn | Picked | AliceScore | BobScore |
| --- | --- | --- | --- | --- |
| 1 | Alice | 3 | 0 | 0 |
| 2 | Bob | 2 | 0 | 0 |
| 3 | Alice | 1 | 0 | 0 |

Both players gain nothing, resulting in a tie.

This highlights a boundary case where parity completely neutralizes scoring despite nontrivial play.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates each test case |
| Space | O(n) | Storing array and temporary variables |

The total input size is at most 2·10^5, so sorting across all test cases is easily fast enough within limits. Each test case then runs in linear time after sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort(reverse=True)
        
        alice = bob = 0
        
        for i, x in enumerate(a):
            if i % 2 == 0 and x % 2 == 0:
                alice += x
            elif i % 2 == 1 and x % 2 == 1:
                bob += x
        
        if alice > bob:
            out.append("Alice")
        elif bob > alice:
            out.append("Bob")
        else:
            out.append("Tie")
    
    return "\n".join(out)

# provided sample
assert run("4\n4\n5 2 7 3\n3\n3 2 1\n4\n2 2 2 2\n2\n7 8\n") == "Bob\nTie\nAlice\nAlice"

# all same parity (all even)
assert run("1\n3\n2 4 6\n") == "Alice"

# all same parity (all odd)
assert run("1\n3\n1 3 5\n") == "Bob"

# alternating parity heavy values
assert run("1\n4\n10 1 9 2\n") == "Alice"

# minimal case
assert run("1\n1\n100\n") == "Alice"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all evens | Alice | Alice accumulates all gains |
| all odds | Bob | Bob accumulates all gains |
| mixed high/low | Alice | ordering effect on score split |
| single element | Alice | base correctness |

## Edge Cases

A fully even array such as `[2, 4, 6]` results in Alice collecting all values regardless of order. Sorting does not change outcome but ensures deterministic handling. Bob’s score remains zero throughout, so Alice wins by total sum.

A fully odd array such as `[1, 3, 5]` gives Bob all effective points, since only Bob benefits from odd picks. Alice’s moves only remove elements without scoring impact, so Bob dominates the final sum.

A mixed array like `[10, 1, 9, 2]` demonstrates interaction between value ordering and parity assignment. Sorting yields `[10, 9, 2, 1]`, and alternating turns assigns high-value odd numbers to Bob and high-value even numbers to Alice depending on turn alignment. This confirms that ordering is the only structural factor needed to predict outcome.

A single-element array always goes to Alice, since she moves first. If the element is even she scores it, otherwise the game ends immediately with Bob unable to respond, making Alice at least non-losing in all cases.
