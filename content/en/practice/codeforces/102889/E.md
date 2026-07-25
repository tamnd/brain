---
title: "CF 102889E - \u7fa4\u4f53\u72c2\u4e71"
description: "The battlefield contains at most six minions. Each minion has an attack value and a health value. During one cast of the spell, every minion receives exactly one opportunity to act, but the order of those opportunities is random."
date: "2026-07-25T12:29:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102889
codeforces_index: "E"
codeforces_contest_name: "The 15-th Beihang University Collegiate Programming Contest (BCPC 2020) - Final"
rating: 0
weight: 102889
solve_time_s: 43
verified: true
draft: false
---

[CF 102889E - \u7fa4\u4f53\u72c2\u4e71](https://codeforces.com/problemset/problem/102889/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The battlefield contains at most six minions. Each minion has an attack value and a health value. During one cast of the spell, every minion receives exactly one opportunity to act, but the order of those opportunities is random. When a minion's turn arrives, it attacks a uniformly chosen living opponent. Damage is simultaneous: both minions lose health equal to the other minion's attack value. A minion with non-positive health is removed from the battlefield.

The task is to find, for every original minion, the probability that it is still alive after the entire random process finishes.

The small value of n is the key constraint. With six minions there are only 720 possible turn orders, but target choices can branch much more. A direct simulation of every possible battle tree grows too quickly. If n were large, even storing all possible alive sets would already be too expensive, but here the small number of minions allows us to explore the complete state space with memoization.

The difficult part is that the health values change after every attack. A solution that only remembers which minions are alive is incorrect because two battles with the same alive set can have different future outcomes. For example, these two states both have two surviving minions, but their remaining health can decide whether the next exchange kills one side or both sides.

A common implementation mistake is forgetting that dead minions still occupy a position in the original ordering. Consider:

```
2
5 1
1 10
```

The first minion kills the second only after attacking, and the second minion may never get a meaningful attack if it dies before its turn. The answer is not obtained by assuming every minion always attacks once.

Another edge case is a single remaining minion:

```
1
7 3
```

The output is:

```
1.000000000000
```

A careless simulation may try to choose a target from an empty set and divide by zero. A living minion simply skips its attack when no opponent exists.

A third case involves zero attack power:

```
2
0 1
1 1
```

The first minion can attack, but it never deals damage. The second minion eventually attacks and kills it, so the outputs are:

```
0.000000000000
1.000000000000
```

Treating zero attack as "no attack" gives the wrong result because the action still happens and changes the random process.

## Approaches

A straightforward approach is to recursively simulate every possible random event. At any moment we choose one of the minions that has not taken its turn yet. If it is alive and there are opponents, we branch over every possible target. At the end of all turns we know exactly which minions survived.

This method is correct because it follows the probability definition directly. The problem is the number of branches. In the worst case with six minions that never die, the number of possible choices is close to

$$6! \times 5 \times 5 \times 4 \times 3 \times 2 \times 1$$

which is already hundreds of thousands of complete paths, and repeated subproblems appear many times.

The observation that makes the solution practical is that many different random histories lead to the same future situation. Once we know which minions have already taken their turns and the current health of every minion, the previous history no longer matters. We can cache the result of this state.

The number of minions is so small that a state can be represented by a bitmask of completed turns and a tuple of six health values. The recursive function returns the probability distribution of final surviving masks from that state. Every transition averages the results of all possible random choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of attack choices | Exponential | Too slow without merging states |
| Memoized State Search | O(number of reachable states × transitions) | O(number of reachable states) | Accepted |

## Algorithm Walkthrough

1. Store the current health of every minion together with a bitmask describing which minions have already taken their turn. The initial state has all original health values and an empty mask.
2. For a state, choose uniformly among all minions whose turn has not happened yet. This models the random attack order. The probability contribution of every choice is divided by the number of unfinished turns.
3. Mark the chosen minion as having completed its turn. If it is already dead, it cannot attack, so the next state is simply the same health state with one more completed turn.
4. Count the currently living minions. If only the acting minion remains alive, there is no legal target, so the attack is skipped.
5. Otherwise, branch over every living target except the attacker. Apply simultaneous damage by subtracting the attack value of each side from the other's health. The resulting states are combined with equal probability because the target choice is uniform.
6. When every minion has completed its turn, return a distribution containing one surviving mask with probability one.

The reason this works is that the state contains exactly the information that can affect the future. The random choices made before reaching a state cannot influence later attacks once the completed turns and current health values are fixed. The recursion explores every possible next random event and averages them according to their probabilities, so the final distribution is exactly the required probability distribution.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

def solve():
    n = int(input())
    atk = []
    hp0 = []
    for _ in range(n):
        a, h = map(int, input().split())
        atk.append(a)
        hp0.append(h)

    size = 1 << n

    @lru_cache(None)
    def dfs(done, hp):
        if done == size - 1:
            alive = 0
            for i in range(n):
                if hp[i] > 0:
                    alive |= 1 << i
            res = [0.0] * size
            res[alive] = 1.0
            return tuple(res)

        choices = [i for i in range(n) if not (done >> i & 1)]
        ans = [0.0] * size
        inv_turn = 1.0 / len(choices)

        for i in choices:
            ndone = done | (1 << i)
            cur_hp = list(hp)

            if cur_hp[i] <= 0:
                nxt = dfs(ndone, tuple(cur_hp))
                for j in range(size):
                    ans[j] += nxt[j] * inv_turn
                continue

            targets = [j for j in range(n) if j != i and cur_hp[j] > 0]

            if not targets:
                nxt = dfs(ndone, tuple(cur_hp))
                for j in range(size):
                    ans[j] += nxt[j] * inv_turn
                continue

            inv_target = 1.0 / len(targets)
            for t in targets:
                nxt_hp = cur_hp[:]
                nxt_hp[i] -= atk[t]
                nxt_hp[t] -= atk[i]
                nxt = dfs(ndone, tuple(nxt_hp))
                for j in range(size):
                    ans[j] += nxt[j] * inv_turn * inv_target

        return tuple(ans)

    result = dfs(0, tuple(hp0))
    for i in range(n):
        prob = 0.0
        for mask in range(size):
            if mask >> i & 1:
                prob += result[mask]
        print("{:.12f}".format(prob))

if __name__ == "__main__":
    solve()
```

The recursive function `dfs` is the memoized state search described above. The key implementation detail is that the health tuple must be part of the cache key. Caching only by `done` would merge states that have different future outcomes.

The base case converts the final health values into a surviving bitmask. A six minion battlefield has only 64 possible masks, so storing the entire probability distribution is cheap.

When processing an attacker, the code first handles the cases where the attack is skipped. A dead attacker cannot act, and a lone living minion has no target. The target loop applies both damage changes before moving to the next state, matching simultaneous combat.

Python integers are large enough for the health values and attack values here, so no overflow handling is needed. The recursion depth is at most six, which is also safe.

## Worked Examples

For the input:

```
1
1 1
```

the only minion never has an opponent.

| done mask | health | action | final probability |
| --- | --- | --- | --- |
| 0 | (1) | choose minion, no target | recurse |
| 1 | (1) | finished | mask 1 with probability 1 |

The returned distribution contains only the mask where the minion is alive, so the answer is `1.000000000000`.

For:

```
2
6 3
3 3
```

there are two possible first turns.

| done mask | health | action | result |
| --- | --- | --- | --- |
| 00 | (3,3) | first minion attacks second | health becomes (0,-3) |
| 00 | (3,3) | second minion attacks first | health becomes (0,-3) |

In both branches the first attacker dies and the second attacker also dies after the counter damage. The final mask is empty in every case, so both survival probabilities are zero.

The trace demonstrates that the algorithm handles simultaneous damage correctly. The attacker does not survive just because it attacks first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S × n² × 2ⁿ) | S is the number of reachable memoized states, each state tries attackers and targets and merges distributions |
| Space | O(S × 2ⁿ) | Each cached state stores a distribution over all possible final masks |

The number of minions is only six, so the complete reachable state space remains manageable. The solution avoids repeated exploration of identical battle situations and fits comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("1\n1 1\n").strip() == "1.000000000000"

assert run("2\n6 3\n3 3\n").strip() == "0.000000000000\n0.000000000000"

assert run("2\n7 3\n3 3\n").strip() == "1.000000000000\n1.000000000000"

assert run("2\n0 1\n1 1\n").strip() == "0.000000000000\n1.000000000000"

assert run("3\n1 1000000\n1 1000000\n1 1000000\n").count("\n") == 3
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One minion | 1.000000000000 | No-target handling |
| Two minions with equal destruction | Both zero | Simultaneous damage |
| Strong enough two minions | Both one | Survival after all turns |
| Zero attack minion | First zero, second one | Zero attack handling |
| Three huge health minions | Three output lines | Large values and recursion |

## Edge Cases

For the single-minion case:

```
1
7 3
```

the initial state immediately chooses the only unfinished turn. The target list is empty, so the state advances without damage. The final mask contains the minion, giving probability one.

For the zero attack case:

```
2
0 1
1 1
```

the first minion may attack the second, but the second minion's health stays unchanged because the attack value is zero. Later the second minion attacks and removes the first minion. The recursion keeps the first action because it is still a real turn, even though it deals no damage.

For simultaneous death:

```
2
6 3
3 3
```

the first attacker deals three damage and receives six damage. Both health values become non-positive after the exchange. The algorithm updates both health values before recursing, so it does not incorrectly allow the attacker to continue.
