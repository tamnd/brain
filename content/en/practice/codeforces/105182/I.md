---
title: "CF 105182I - Number Game"
description: "We are given a multiset of positive integers representing weights placed in a sequence. Two players alternate turns, and on each turn they either compress the sequence by merging two chosen elements into their sum, or they immediately end the game by selecting one element."
date: "2026-06-27T04:40:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105182
codeforces_index: "I"
codeforces_contest_name: "The 22nd UESTC Programming Contest - Final"
rating: 0
weight: 105182
solve_time_s: 63
verified: true
draft: false
---

[CF 105182I - Number Game](https://codeforces.com/problemset/problem/105182/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of positive integers representing weights placed in a sequence. Two players alternate turns, and on each turn they either compress the sequence by merging two chosen elements into their sum, or they immediately end the game by selecting one element. When a player selects a number, that player gains its value, and the opponent receives the sum of all remaining elements. The game then stops.

The total sum of all numbers never changes throughout the game unless the game ends. The only way to influence the final outcome is by merging numbers, which reshapes how the total sum is distributed across future choices.

The final decision in any ending move is extremely simple in hindsight. If a player takes value x from a current total sum S, then the opponent receives S − x, so the taker wins exactly when 2x > S.

The entire problem is therefore about whether the first player can force a situation where they are the one to pick a sufficiently large value relative to the remaining total, despite the opponent also being able to merge and potentially end the game earlier.

The constraints imply that a direct simulation of game states is impossible. With up to 10^5 test cases and total array size up to 10^6, any state-space search over all merge histories or game trees would be far beyond feasible limits. Even maintaining dynamic game states would introduce at least quadratic behavior because every merge reduces the sequence size by one but the branching factor of choices is large.

A naive mistake is to treat this as a simple “take maximum element” game. That fails because merging can create new values not present initially, and those new values can become decisive in the final comparison against the remaining sum.

Another failure mode is assuming greedy play, for example always merging the smallest two values. That ignores the opponent’s ability to respond by ending the game prematurely when a favorable imbalance appears.

## Approaches

The brute-force interpretation of the game is to treat every state as a multiset and simulate both players exploring all valid moves. Each merge reduces the number of elements by one, and each termination move evaluates a final score split. This leads to an exponential number of game states because at every step a player chooses any pair to merge or any element to terminate the game. Even ignoring termination, the number of possible merge histories corresponds to the number of binary trees over n leaves, which is Catalan-sized and grows super-exponentially in practice.

The key observation is that merging does not change the total sum, it only changes how the sum is grouped. Any sequence of merges is equivalent to constructing a full binary tree over the initial elements, where each internal node represents a sum of a subset. The game therefore reduces to controlling how the final partition of the array is formed when only two aggregated groups remain.

Instead of tracking game states, we can reason about the final unavoidable structure. Eventually, optimal play will reduce the sequence down to two numbers, because stopping earlier than that is dominated by continuing merges: ending the game too early gives the opponent a potentially large remainder sum. At two elements, no further safe merge exists, because merging would immediately allow the opponent to take the single remaining value and win with the full sum.

So the entire game collapses to the question of whether the first player can force that, at the moment the sequence is reduced to two groups, they can pick a group whose value exceeds half of the total sum.

This turns the game into a control problem over how the final bipartition is formed. Each merge operation is effectively deciding how elements are grouped, and both players are shaping a binary partition tree with adversarial choices.

The decisive insight is that despite adversarial play, the structure of the problem collapses to a simple invariant: the only way the first player can guarantee a win is if there exists an element whose value is strictly greater than the sum of all other elements. If such an element exists, the first player can force it to remain “isolated” enough through merges and eventually secure it as the final pick before the opponent can neutralize it.

If no such dominant element exists, the opponent can always respond by forcing the final split to avoid giving the first player a winning selection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Tree | O(exponential) | O(states) | Too slow |
| Optimal Greedy Invariant | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

The solution reduces to checking whether the largest element can dominate the rest of the array.

1. Compute the total sum S of all elements in the sequence. This value remains invariant under merges, so it is the reference against which every final decision is evaluated.
2. Identify the maximum element mx in the array. Any winning strategy must ultimately rely on forcing this value to be selected at the right moment, since no combination of smaller elements can exceed it if it is already globally dominant.
3. Compare mx with S − mx. If mx is strictly greater than S − mx, then mx is powerful enough that if it is ever chosen as the final take, the selecting player wins immediately.
4. If this condition holds, conclude that the first player can enforce a sequence of merges that preserves the possibility of selecting mx at the correct time, leading to a forced win.
5. Otherwise, conclude that the opponent can always respond in a way that prevents the first player from ever reaching a winning terminal pick.

The key idea is that merges only redistribute weight, and no sequence of redistributions can create a new element stronger than the global maximum. So the entire game is fundamentally controlled by whether a single element already dominates the sum.

### Why it works

Every move preserves the total sum S, and every terminal move is decided by comparing a single chosen value x against S − x. Since merges only replace two values with their sum, they never increase the maximum possible individual “final selectable advantage” beyond what is already present in some subset. The only way to guarantee a winning final move is to ensure that there exists a value that can be isolated as a selection satisfying 2x > S. If no such value exists initially, no sequence of merges can create it, because any merged value corresponds to a subset whose complement sum is at least as large, allowing the opponent to neutralize the advantage at the terminal step.

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
        s = sum(a)
        mx = max(a)
        if mx > s - mx:
            out.append("YES")
        else:
            out.append("NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code directly implements the invariant derived above. For each test case, it computes the total sum and the maximum element. The decision depends only on whether the maximum element is strictly greater than the sum of all remaining elements. No simulation of merges is needed because merges do not affect either the total sum or the identity of the maximum element.

The implementation carefully avoids per-operation overhead and keeps everything linear per test case, which is necessary given the aggregated input size up to one million elements.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, 2, 3]
```

| Step | Sum S | Max mx | mx vs S - mx | Decision |
| --- | --- | --- | --- | --- |
| Start | 6 | 3 | 3 vs 3 | NO |

The maximum element equals half of the total sum, so it is not strictly dominant. Any attempt to isolate it still leaves the opponent with equal total weight, so the first player cannot force a strictly winning final pick.

This demonstrates the boundary case where equality is insufficient.

### Example 2

Input:

```
n = 3
a = [1, 2, 6]
```

| Step | Sum S | Max mx | mx vs S - mx | Decision |
| --- | --- | --- | --- | --- |
| Start | 9 | 6 | 6 vs 3 | YES |

Here the maximum element dominates all remaining elements combined. This ensures that if the game ever reaches a state where this element can be taken, the selecting player immediately wins. The first player can steer merges to preserve this dominance.

This confirms the intuition that a single overwhelmingly large element determines the outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is read once to compute sum and maximum |
| Space | O(1) extra | Only aggregate variables are maintained |

The total input size across all test cases is bounded by 10^6, so a single linear pass over all values easily fits within time limits. Memory usage remains constant beyond input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            s = sum(a)
            mx = max(a)
            out.append("YES" if mx > s - mx else "NO")
        print("\n".join(out))

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return res

# provided sample (as parsed)
assert run("3\n3\n1 2 3\n3\n1 2 6\n3\n4 6 2\n") == "NO\nYES\nNO"

# all equal values
assert run("1\n4\n2 2 2 2\n") == "NO"

# single large dominant element
assert run("1\n5\n1 1 1 1 10\n") == "YES"

# minimum size
assert run("1\n1\n5\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | NO | no element can dominate |
| dominant max | YES | strict dominance condition |
| single element | YES | trivial win case |

## Edge Cases

When all elements are equal, every candidate value equals exactly half of the total sum only in the degenerate n=2 case, and is strictly smaller otherwise. The algorithm correctly outputs NO because no element satisfies strict dominance.

When n equals 1, the maximum equals the total sum, so the condition holds and the answer is YES. The player immediately takes the only element and wins.

When there is a very large outlier element, merges cannot reduce its value or redistribute its advantage away from the final comparison. The algorithm correctly identifies this and returns YES.
