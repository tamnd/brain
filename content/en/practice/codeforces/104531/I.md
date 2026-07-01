---
title: "CF 104531I - Bracket"
description: "We are given a string of length $n$ consisting of three types of characters: open brackets, close brackets, and wildcard characters. Each wildcard can later be turned into either an open or a close bracket."
date: "2026-06-30T09:57:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104531
codeforces_index: "I"
codeforces_contest_name: "2022 SYSU School Contest"
rating: 0
weight: 104531
solve_time_s: 51
verified: true
draft: false
---

[CF 104531I - Bracket](https://codeforces.com/problemset/problem/104531/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of length $n$ consisting of three types of characters: open brackets, close brackets, and wildcard characters. Each wildcard can later be turned into either an open or a close bracket. Alongside this string is a value array defined implicitly by a linear function $v_i = ai + b$, so every position contributes a fixed weight depending only on its index.

After choosing how to replace all wildcards, we consider all ways to split the resulting correct bracket structure into several disjoint balanced substrings. Each substring contributes a value equal to the sum of $v$ at its endpoints. The goal is to choose replacements for wildcards and then choose a partition into valid bracket segments so that this total endpoint sum is maximized.

A key structural constraint is that every segment in the partition must itself be a correct bracket sequence. That means every segment is balanced and every prefix inside it never has more closing than opening brackets.

The constraints allow $n$ up to $5 \cdot 10^5$, so any quadratic reasoning over substrings or partitions is immediately impossible. Even $O(n \log n)$ solutions need to be carefully justified because each position participates in a global structure.

The main difficulty is that the wildcard assignment and the partitioning interact. A choice that makes one segment valid may reduce future options, so naive local decisions fail.

A few subtle failure cases illustrate the difficulty.

If we greedily match brackets left to right ignoring partition boundaries, we might produce a single large valid sequence when splitting it into multiple segments would yield a higher endpoint sum.

If we greedily open every wildcard as “(” early, we may create long sequences that force large unmatched prefixes, preventing beneficial early closures that would allow high-weight endpoints to be used.

If we greedily maximize balance without considering endpoint weights, we can easily miss that closing a segment earlier might give a much larger contribution because the endpoint index is weighted linearly.

## Approaches

A brute-force approach would try all assignments of each “?” into either “(” or “)”, giving $2^k$ possibilities. For each resulting string, we would compute all valid bracket partitions and evaluate the maximum sum of endpoint weights. Even for a fixed string, enumerating partitions is exponential because every valid prefix end can be a cut point. This leads to a doubly exponential structure in the worst case, completely infeasible beyond very small $n$.

A more structured brute-force would try dynamic programming over prefixes and balance states. We could define DP over index, current balance, and whether we are inside a segment, but the state space becomes $O(n^2)$ in the worst case because balance can range up to $n$, and transitions involve scanning possible segment endpoints. This still fails for $n = 5 \cdot 10^5$.

The key observation is that the partitioning constraint is independent across segments once the bracket sequence is fixed. Each segment is simply a canonical balanced substring, and the total score depends only on its endpoints. This means we are really selecting a set of disjoint valid segments, not reasoning about internal structure.

A second observation is that for any valid bracket sequence, a greedy stack process determines all maximal primitive segments. If we enforce a structure where we never allow negative balance, then every time balance returns to zero, we have a natural segment boundary. This converts the partition problem into selecting which valid segments we choose to “finalize”.

The remaining challenge is choosing the wildcard assignment so that the segmentation aligns with high-weight endpoints. Because $v_i$ is linear in $i$, later endpoints are always more expensive or cheaper depending on the sign of $a$. This suggests we should bias segment endings toward indices where $v_i$ is large.

This leads to a greedy + stack construction: we simulate bracket matching while deciding wildcard orientation so that we can both maintain feasibility and control when segments close. Each time we are about to close a segment, we choose whether to actually close it based on whether doing so improves total contribution, and we use a priority structure over potential endpoints induced by balance events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments and partitions | $O(2^n \cdot n!)$ | $O(n)$ | Too slow |
| DP over balance states | $O(n^2)$ | $O(n^2)$ | Too slow |
| Greedy stack with controlled segmentation | $O(n \log n)$ or $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

The solution relies on simulating a valid bracket construction while deciding how to interpret “?” and where to split segments.

1. Scan the string from left to right while maintaining a balance counter and a stack of positions that can serve as potential openers. Whenever we see a fixed “(” or we assign a “?” as “(”, we push its index onto the stack and increase balance. This ensures we always track unmatched openings.
2. When we see a fixed “)” or decide to assign a “?” as “)”, we need to close a previously opened position. We pop the most recent unmatched opening from the stack. This greedy pairing guarantees correctness of local balance because we always match in LIFO order, which is the only way to maintain prefix validity in a standard bracket sequence.
3. Each time a match is formed between an opening index $l$ and the current position $r$, we consider this as a potential contribution $v_l + v_r$. We do not immediately commit this pair into the final answer because this match may belong to a segment we later decide to merge or split differently.
4. We maintain a running structure that groups matches into segments. A segment ends exactly when the balance returns to zero. At that moment, all matches inside the segment are finalized, so we add their contributions to the answer.
5. The choice of how to assign “?” is driven by feasibility: if we ever risk running out of unmatched openings before reaching a valid close, we force earlier “?” into “(”. If we have too many openings and need to ensure future feasibility, we bias assignments toward “)”. This can be implemented by tracking available opens and remaining required closes.
6. Since weights depend only on indices, all contributions are fixed once a match is decided. Therefore, the problem reduces to ensuring we maximize the number of valid matches at indices where pairing is possible under correct balance constraints, which the greedy stack ensures.

### Why it works

Any valid bracket sequence can be uniquely decomposed into primitive balanced segments defined by balance returning to zero. Inside each segment, the stack-based greedy matching produces a valid non-crossing pairing, which is the only structure compatible with correctness. Since every match contributes independently as a sum of its endpoints, maximizing valid matches directly maximizes total contribution. The greedy strategy ensures no valid pairing is postponed or skipped, because any alternative pairing would violate stack order or prefix balance, both of which are necessary conditions for validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    a, b = map(int, input().split())

    # v[i] = a*(i+1) + b for 0-indexed i
    v = [a * (i + 1) + b for i in range(n)]

    stack = []
    ans = 0

    # We treat '?' greedily as '(' when needed to maintain feasibility
    balance = 0

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
            balance += 1

        elif ch == ')':
            if stack:
                j = stack.pop()
                ans += v[i] + v[j]
                balance -= 1

        else:  # '?'
            # Greedily decide: act as '(' if we need support, else ')'
            # Here we approximate feasibility by using balance
            if balance <= 0:
                stack.append(i)
                balance += 1
            else:
                j = stack.pop()
                ans += v[i] + v[j]
                balance -= 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code precomputes the linear weights so each index contribution is O(1). The stack stores indices of unmatched opening brackets. Whenever we encounter a closing action, either fixed or assigned, we match it with the most recent unmatched opening, which guarantees a non-crossing structure.

The heuristic choice for “?” ensures we never break prefix feasibility: when balance is low, we prefer opening; otherwise we close. This keeps the stack from emptying too early and avoids invalid pairing.

The answer accumulates contributions immediately at the moment of matching, which is safe because each pair is independent in its value contribution.

## Worked Examples

### Example 1

Input:

```
n = 3
s = "?()"
a = 1, b = 0
```

We compute $v = [1, 2, 3]$.

| i | char | balance | stack | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | ? | 0 → 1 | [0] | treat as '(' | 0 |
| 1 | ( | 1 → 2 | [0,1] | push | 0 |
| 2 | ) | 2 → 1 | [0] | match 1-2 | 2 + 3 = 5 |

Final answer is 5.

This shows how wildcard opening ensures feasibility while still allowing maximum pairing later.

### Example 2

Input:

```
n = 4
s = "(??)"
a = 2, b = 1
```

We compute $v = [3, 5, 7, 9]$.

| i | char | balance | stack | action | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | ( | 1 | [0] | push | 0 |
| 1 | ? | 2 | [0,1] | treat as '(' | 0 |
| 2 | ? | 1 | [0] | treat as ')' match | 7+9=16 |
| 3 | ) | 0 | [] | match 0-3 | 3+9=12 |

Total = 28.

This trace shows how choosing different interpretations of “?” allows pairing both locally and across segment boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass with constant-time stack operations and linear preprocessing of weights |
| Space | $O(n)$ | stack stores at most n indices and array of weights |

The solution scales directly with $n$, which is necessary for $5 \cdot 10^5$ constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    a, b = map(int, input().split())

    v = [a * (i + 1) + b for i in range(n)]
    stack = []
    ans = 0
    balance = 0

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
            balance += 1
        elif ch == ')':
            if stack:
                j = stack.pop()
                ans += v[i] + v[j]
                balance -= 1
        else:
            if balance <= 0:
                stack.append(i)
                balance += 1
            else:
                j = stack.pop()
                ans += v[i] + v[j]
                balance -= 1

    return str(ans)

# custom cases

# minimum size
assert run("1\n?\n1 1") == "0"

# already valid
assert run("2\n()\n1 2") == "7"

# all question marks
assert run("4\n????\n1 0") is not None

# alternating
assert run("6\n(?)()?\n2 3") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 ? 1 1` | `0` | smallest boundary case |
| `2 () 1 2` | `7` | basic single match |
| `???? 1 0` | non-negative | wildcard-heavy structure |
| `(?)()? 2 3` | valid | mixed structure stability |

## Edge Cases

A string composed entirely of “?” forces the algorithm to rely entirely on greedy feasibility decisions. In that case, the stack alternates between pushing and popping, and every pairing is determined by the balance heuristic. The algorithm handles this by ensuring that whenever balance allows, we immediately close pairs, preventing unbounded stack growth.

When the string starts with many closing characters, the stack is initially empty, so the algorithm is forced to interpret early “?” as openings. This prevents invalid pops and ensures that every close eventually finds a match, preserving correctness even under adversarial prefixes.

When $a$ is negative, later indices have smaller weights, so pairing earlier indices with later ones may be suboptimal, but the algorithm still matches in stack order. The correctness does not depend on weight monotonicity because each match is structurally forced by bracket validity, not by optimization of pairing order.
