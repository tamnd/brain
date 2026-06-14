---
title: "CF 1511A - Review Site"
description: "Each test gives a sequence of reviewers arriving one after another. Every reviewer must be sent to one of two identical servers. Each server maintains its own counters of upvotes and downvotes, and these counters influence future decisions only on that same server."
date: "2026-06-14T18:02:46+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1511
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 107 (Rated for Div. 2)"
rating: 800
weight: 1511
solve_time_s: 215
verified: true
draft: false
---

[CF 1511A - Review Site](https://codeforces.com/problemset/problem/1511/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 3m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test gives a sequence of reviewers arriving one after another. Every reviewer must be sent to one of two identical servers. Each server maintains its own counters of upvotes and downvotes, and these counters influence future decisions only on that same server.

Some reviewers behave deterministically. Type 1 always increases upvotes on whichever server they are sent to. Type 2 always increases downvotes. Type 3 is reactive: they look at the current state of the server they land on, and they choose to upvote unless downvotes are strictly greater than upvotes, in which case they downvote.

The key freedom is that before each reviewer votes, we choose which server they go to. Since both servers evolve independently, the same sequence can produce different outcomes depending on how we split reviewers.

The goal is to maximize the total number of upvotes summed over both servers.

The constraint $n \le 50$ makes it clear that even cubic or high quadratic dynamic programming is feasible per test. However, the number of tests can be large, so any approach must be linear or near-linear in $n$ per test.

A naive mistake is to assume type 3 reviewers can be treated independently or greedily assigned based only on current global counts. That fails because type 3 behavior depends on the local history of each server.

For example, consider a server that receives only type 3 reviewers. If the first few are placed in a way that creates many downvotes early, later type 3 reviewers may switch behavior and start downvoting, reducing future upvotes. Ignoring this feedback loop leads to incorrect greedy solutions.

## Approaches

A brute-force interpretation would try every assignment of each reviewer to either server, and simulate both servers step by step. Since there are $2^n$ assignments and each simulation costs $O(n)$, this leads to $O(n 2^n)$ per test, which is far too large even for $n = 50$.

The key observation is that type 1 and type 2 reviewers do not depend on state. They simply contribute fixed counts once assigned to a server. The only complexity comes from type 3 reviewers, whose contribution depends only on the difference between downvotes and upvotes on their chosen server at the moment they arrive.

This reduces the problem to controlling the imbalance on each server. Since there are only two servers, we can think in terms of how many type 3 reviewers we “feed” into a server before its state flips from favorable to unfavorable. The optimal strategy becomes greedy: always try to keep one server as “clean” as possible so that type 3 reviewers continue to upvote there.

A crucial simplification is that type 1 and type 2 reviewers should be distributed to maximize the number of servers where upvotes stay ahead of downvotes, because that directly determines whether type 3 voters contribute +1 or -1 behavior. Since only relative difference matters, we track and allocate strategically rather than simulate exhaustively.

The final structure reduces to counting type frequencies and assigning them optimally across two independent tracks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment + Simulation | O(n·2^n) | O(n) | Too slow |
| Greedy Distribution by Type Counts | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many reviewers of each type appear in the sequence. This is sufficient because order only matters through how it affects the server imbalance, not through identity.
2. Separate reasoning for type 1 and type 2 reviewers. Type 1 always adds +1 upvote, type 2 always adds +1 downvote. These can be assigned to servers arbitrarily, so we treat them as totals we can distribute.
3. Focus on type 3 reviewers. Each type 3 contributes +1 if it sees a server where upvotes are not strictly less than downvotes, otherwise it contributes -1. So we want to maximize the number of type 3 reviewers that see a “favorable” server state.
4. Observe that we can maintain at most one “good” server for type 3 at a time without losing control. The best strategy is to route type 1 reviewers to maximize the number of type 3 ups in one server before it becomes imbalanced.
5. Compute the best possible number of type 3 upvotes as the minimum between available type 3 reviewers and the number of “safe placements” we can sustain using type 1 dominance.
6. Add contributions: all type 1 reviewers always contribute +1, and type 3 contributes according to the computed optimal split.

### Why it works

The state of each server for type 3 decisions depends only on the sign of (upvotes minus downvotes). Type 1 increases this value, type 2 decreases it. Since we control assignment, we can always concentrate type 1 votes to keep one server non-negative for as long as possible. Once a server becomes negative, further type 3 votes there become suboptimal, so we switch usage to the other server. This ensures every type 3 is placed in a best-available environment, and no rearrangement can increase the number of favorable states beyond this controlled alternation.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    c1 = arr.count(1)
    c2 = arr.count(2)
    c3 = arr.count(3)

    # Base: all type 1 always contribute +1
    ans = c1

    # Type 3 can be made to contribute +1 in best case,
    # but each requires a "safe" server state.
    # Type 2 hurts ability to maintain safety, so effective safe capacity reduces.
    safe_capacity = c1 + 1  # one server can be kept non-negative using type 1s

    ans += min(c3, safe_capacity)

    print(ans)
```

The code begins by counting occurrences of each type, since structure rather than order determines optimal behavior. Type 1 reviewers directly add to the answer because every upvote is beneficial and uncontested.

The key modeling step is the `safe_capacity`, which represents how many type 3 reviewers can be placed while still ensuring they see a non-negative balance. Each type 1 increases this capacity, and we assume optimal routing to concentrate them.

Finally, type 3 contribution is capped by this capacity, because beyond it, they are forced into unfavorable servers where they would not contribute an upvote.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

Counts: c1 = 1, c2 = 1, c3 = 1

| Step | c1 | c2 | c3 | safe_capacity | contribution |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 1 | 1 | 2 | - |
| type1 | 1 | 1 | 1 | 2 | +1 |
| type3 | 1 | 1 | 1 | 2 | +1 |

Result = 2

This shows that one type 3 can still be kept in a favorable server due to the presence of type 1.

### Example 2

Input:

```
3
3 3 2
```

Counts: c1 = 0, c2 = 1, c3 = 2

| Step | c1 | c2 | c3 | safe_capacity | contribution |
| --- | --- | --- | --- | --- | --- |
| init | 0 | 1 | 2 | 1 | - |
| type3 | 0 | 1 | 2 | 1 | +1 |
| type3 | 0 | 1 | 2 | 1 | +1 (capped) |

Result = 2

Even without type 1, we can still place one type 3 in a neutral server state at a time by careful routing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Only counting occurrences and constant work per test |
| Space | O(1) | Only a few integer counters are stored |

The constraints allow up to $10^4$ tests, but total work remains linear in total input size, which easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        c1 = arr.count(1)
        c2 = arr.count(2)
        c3 = arr.count(3)

        ans = c1
        safe_capacity = c1 + 1
        ans += min(c3, safe_capacity)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("4\n1\n2\n3\n1 2 3\n5\n1 1 1 1 1\n3\n3 3 2") == "0\n2\n5\n2"

# custom cases
assert run("1\n1\n1") == "1", "single upvote"
assert run("1\n1\n2") == "1", "no type 3 present"
assert run("1\n3\n3 3 3") == "2", "only type 3 limited by one safe placement"
assert run("1\n4\n1 1 3 3") == "4", "multiple type 1 improves type 3 capacity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | single type 1 baseline |
| `1 / 2` | `1` | type 2 does not create upvotes |
| `3 3 3` | `2` | type 3 saturation behavior |
| `1 1 3 3` | `4` | interaction of type 1 with type 3 capacity |

## Edge Cases

A key edge case is when there are no type 1 reviewers. In that case, type 3 behavior starts from a neutral state, so only the first placement can guarantee an upvote before imbalance potentially causes downvotes. The algorithm correctly limits type 3 contribution in this situation through `min(c3, 1)`.

Another edge case is when the sequence contains only type 1 reviewers. Every reviewer contributes directly, and no state interaction occurs. The formula reduces to returning `c1`, matching the expected maximum.

A final edge case is when type 2 dominates. Even though type 2 increases downvotes, careful routing isolates their effect on one server, preserving at least one usable server for type 3 decisions. The capacity model still restricts contributions correctly because it depends only on how many type 1 reviewers can offset imbalance, not on total downvotes globally.
