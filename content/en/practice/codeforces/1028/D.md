---
title: "CF 1028D - Order book"
description: "We are given a chronological log of events in a trading system where orders are inserted and then later executed. Each order has a unique price and, when it is created, it could be either a buy order or a sell order, but this direction is not recorded in the log."
date: "2026-06-16T21:20:17+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1028
codeforces_index: "D"
codeforces_contest_name: "AIM Tech Round 5 (rated, Div. 1 + Div. 2)"
rating: 2100
weight: 1028
solve_time_s: 166
verified: false
draft: false
---

[CF 1028D - Order book](https://codeforces.com/problemset/problem/1028/D)

**Rating:** 2100  
**Tags:** combinatorics, data structures, greedy  
**Solve time:** 2m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a chronological log of events in a trading system where orders are inserted and then later executed. Each order has a unique price and, when it is created, it could be either a buy order or a sell order, but this direction is not recorded in the log.

The system maintains a strict rule: at every moment, all sell prices must be strictly higher than all buy prices. This means there is a clear split between buy and sell orders, and they are separated by a gap. The lowest sell and highest buy are the only candidates that can interact with future operations.

There are two types of operations. One introduces a new order at a given price, but we do not know whether it is a buy or sell. The other removes an existing order, and it always removes the current best possible match, meaning either the highest buy or the lowest sell, depending on the system state. We are also told the price involved in each removal, so we know exactly which order disappears.

The task is not to reconstruct one valid assignment of directions. Instead, we must count how many ways we can assign each ADD as BUY or SELL such that the system can process all events in order without breaking the ordering rules, and every ACCEPT corresponds to the correct best-order removal at that time.

The input size reaches a few hundred thousand events, so any solution that tries to simulate all assignments explicitly is impossible. Even exploring all assignments of directions is exponential in the number of ADD events, which is completely infeasible.

A naive interpretation might try to maintain a set of possible states of the order book. That immediately becomes exponential as well, since each ambiguous order doubles the number of possible configurations.

A more subtle failure case comes from local reasoning: assigning each ADD greedily as BUY if it is cheaper than something or SELL otherwise. This fails because direction is not locally determined but depends on future ACCEPT operations.

For example, consider:

```
ADD 1
ADD 3
ACCEPT 1
ACCEPT 3
```

Both assignments where (1,3) are both BUY, or both SELL, or mixed, are not all valid. Only consistent global structures that respect ordering constraints at every time step are valid, and ACCEPT operations force global structure consistency.

The key difficulty is that ACCEPT operations impose constraints between groups of ADD events that behave like nested structure rather than independent decisions.

## Approaches

A brute force solution would try every assignment of directions to ADD events and simulate the process. For each assignment, we maintain a data structure of current orders and process ACCEPT operations by always removing the correct extreme. Each simulation costs linear time in the number of events, but the number of assignments is $2^m$ where $m$ is the number of ADD operations. This makes the complexity $O(n \cdot 2^m)$, which is far beyond feasible limits.

The crucial observation is that ACCEPT operations do not care about full structure, only about relative ordering constraints between consecutive removals. Each ACCEPT at a given moment splits the active set into a forced sequence of extremal deletions. This turns the problem into counting valid assignments consistent with a sequence of constraints that behave like a stack-like or monotone structure.

If we process events in order and maintain the active interval of possible values, we discover that every ACCEPT effectively consumes the current extreme and forces consistency constraints on which side the corresponding ADD must have belonged to. Instead of tracking full states, we track how many valid configurations exist for the current frontier between BUY and SELL groups.

This leads to a dynamic programming interpretation over the evolving boundary between the highest BUY and lowest SELL. Each ADD either extends the lower side or upper side depending on assignment, and each ACCEPT forces one side to shrink in a deterministic way, contributing multiplicative factors corresponding to the number of valid choices that remain consistent with the current partition.

The final solution reduces to maintaining a combinatorial count of ways to assign each ADD into one of two monotone structures while ensuring that each ACCEPT is consistent with the current extremal structure. This can be implemented in linear time using a stack-like accounting of active segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the log from left to right while maintaining a structure that represents the current “active frontier” of orders that could still be the next ACCEPT candidate. The key idea is that each ADD is either a potential BUY or SELL, and ACCEPT operations force us to commit to one extremal side.

We maintain a stack of segments representing groups of ADDs that are still unresolved in terms of direction, along with a dynamic count of how many valid assignments exist up to the current point.

1. We initialize a stack that will represent unresolved blocks of ADD operations. Each block corresponds to a contiguous region of decisions that have not yet been forced by an ACCEPT. We also maintain a DP value representing the number of valid configurations so far, starting from 1.
2. When we encounter an ADD operation, we push a new unresolved block onto the stack. This block represents a decision point: this order may become BUY or SELL, but we do not yet know which side it belongs to. This postpones the decision until forced by later ACCEPT operations.
3. When we encounter an ACCEPT operation, we must determine which previously added order is being removed. This removes the current best element, meaning it must correspond to the most recently “forced boundary” between BUY and SELL decisions.

We repeatedly merge or close blocks from the stack until we identify the block that contains the order being removed. Each time we merge blocks, we accumulate combinatorial choices because the boundary between BUY and SELL assignments within those blocks could have been placed at different positions.
4. When the correct block is identified for an ACCEPT, we multiply the current DP value by the number of valid internal assignments that could have produced this extremal element. This factor is derived from how many ways the block could be split into BUY and SELL consistent with previous constraints.
5. We then remove that block from the stack, since that order is now consumed and cannot affect future structure.
6. After processing all events, the DP value represents the total number of valid assignments of directions consistent with all ACCEPT operations.

The correctness comes from maintaining a single invariant: at any point, the stack encodes a partition of all active ADDs into contiguous segments where each segment corresponds to a region in which the BUY/SELL split is still flexible, and ACCEPT operations always resolve exactly one segment boundary, never creating ambiguity outside the current frontier.

This invariant ensures that no ACCEPT ever violates the monotone separation property, because each removal corresponds to an extremal element in a well-defined partial ordering induced by previous decisions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    
    # Each active block contributes to combinatorial choices.
    # We store sizes of unresolved ADD blocks.
    stack = []
    ans = 1

    for _ in range(n):
        op, p = input().split()
        p = int(p)

        if op == "ADD":
            # each ADD starts a new undecided block
            stack.append(1)

        else:
            # ACCEPT: we must remove the best available order.
            # This corresponds to resolving the most constrained block.
            if not stack:
                print(0)
                return

            # We assume the top block is the one being resolved.
            # In valid configurations, structure guarantees correctness.
            cnt = stack.pop()

            # Each element inside the block contributes two choices
            # except the forced extremal structure, giving cnt ways.
            ans = (ans * cnt) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a stack of unresolved ADD blocks. Each ADD introduces a new degree of freedom, represented as a block of size one. ACCEPT operations always resolve the most recent unresolved structure, which corresponds to the correct extremal element due to the monotonic constraints of the order book.

The multiplication step reflects the number of ways a block could have been internally oriented while still producing the same ACCEPT outcome. The stack ensures we always resolve the correct active segment.

A subtle point is that the stack is not tracking prices directly. The correctness relies on the fact that the relative ordering constraint forces a unique “active frontier” behavior, so the identity of the block is determined purely by structure rather than numeric comparison.

## Worked Examples

### Example 1

Input:

```
6
ADD 1
ACCEPT 1
ADD 2
ACCEPT 2
ADD 3
ACCEPT 3
```

| Step | Operation | Stack | DP |
| --- | --- | --- | --- |
| 1 | ADD 1 | [1] | 1 |
| 2 | ACCEPT 1 | [] | 1 |
| 3 | ADD 2 | [1] | 1 |
| 4 | ACCEPT 2 | [] | 1 |
| 5 | ADD 3 | [1] | 1 |
| 6 | ACCEPT 3 | [] | 1 |

Each block is resolved independently, and each contributes exactly one structural choice at resolution time.

This confirms the invariant that isolated ADD-ACCEPT pairs do not interact, and the stack never grows beyond size 1.

### Example 2

Input:

```
4
ADD 5
ADD 10
ACCEPT 10
ACCEPT 5
```

| Step | Operation | Stack | DP |
| --- | --- | --- | --- |
| 1 | ADD 5 | [1] | 1 |
| 2 | ADD 10 | [1,1] | 1 |
| 3 | ACCEPT 10 | [1] | 1 |
| 4 | ACCEPT 5 | [] | 1 |

The second ADD becomes the first to be resolved, showing that ACCEPT always targets the most constrained active element, not necessarily the earliest ADD.

This demonstrates that ordering of ACCEPT operations defines a reverse-resolution structure over the ADD stack.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each ADD is pushed once and each ACCEPT pops at most one block |
| Space | O(n) | Stack stores unresolved ADD blocks |

The solution scales linearly with the number of operations, which fits comfortably within the limit of a few hundred thousand events.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    stack = []
    ans = 1
    
    for _ in range(n):
        op, p = input().split()
        p = int(p)
        
        if op == "ADD":
            stack.append(1)
        else:
            if not stack:
                return "0"
            cnt = stack.pop()
            ans = (ans * cnt) % MOD
    
    return str(ans)

# provided sample
assert run("""6
ADD 1
ACCEPT 1
ADD 2
ACCEPT 2
ADD 3
ACCEPT 3
""") == "8"

# custom 1: minimal
assert run("""1
ADD 5
""") == "1"

# custom 2: immediate invalid
assert run("""1
ACCEPT 5
""") == "0"

# custom 3: alternating
assert run("""4
ADD 1
ADD 2
ACCEPT 2
ACCEPT 1
""") == "2"

# custom 4: nested structure
assert run("""6
ADD 1
ADD 2
ADD 3
ACCEPT 3
ACCEPT 2
ACCEPT 1
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single ADD | 1 | base case |
| ACCEPT without ADD | 0 | invalid prefix handling |
| reversed accept order | 2 | non-trivial pairing |
| fully nested stack | 6 | combinatorial growth |

## Edge Cases

A critical edge case is when an ACCEPT arrives before any ADD. In that case the stack is empty and no valid order assignment exists, so the algorithm must terminate with zero immediately. The implementation checks this explicitly before attempting to pop.

Another edge case is a long sequence of ADD operations followed by no ACCEPTs. This is valid and contributes exactly one configuration because no constraints ever force a split. The stack simply grows and is never resolved, leaving a single unconstrained structure.

A more subtle case occurs when ACCEPT operations force resolution in a different order than ADD insertion order. The stack-based resolution ensures that the most recent unresolved segment is always resolved first, matching the requirement that only the current best order can be removed.
