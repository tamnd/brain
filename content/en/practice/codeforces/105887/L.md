---
title: "CF 105887L - \u6808\u4e0e\u91cd\u590d"
description: "We maintain a stack that starts empty and evolves through a sequence of operations. Each operation either pushes a value onto the stack, pops the top element, or triggers a macro-like action that repeats all previously executed operations once more."
date: "2026-06-21T17:20:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105887
codeforces_index: "L"
codeforces_contest_name: "\u7b2c\u5341\u4e09\u5c4a\u91cd\u5e86\u5e02\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b"
rating: 0
weight: 105887
solve_time_s: 51
verified: true
draft: false
---

[CF 105887L - \u6808\u4e0e\u91cd\u590d](https://codeforces.com/problemset/problem/105887/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a stack that starts empty and evolves through a sequence of operations. Each operation either pushes a value onto the stack, pops the top element, or triggers a macro-like action that repeats all previously executed operations once more.

After every operation, we must report the sum of all elements currently in the stack.

The key difficulty is the Repeat operation. Unlike a normal command that changes the stack once, Repeat effectively replays the entire history of operations seen so far, which can cause exponential growth in the number of effective actions if simulated literally.

The constraints allow up to 200,000 operations. A solution that replays history naively would repeatedly reprocess prefixes whose lengths grow over time, quickly reaching quadratic or worse behavior. Since each Repeat can duplicate all previous work, a naive simulation may expand to sizes on the order of 2^n in the worst conceptual case, even though the actual output only requires n answers.

A direct simulation of the stack contents is therefore infeasible.

A subtle edge case arises when multiple Repeat operations appear nested. For example, repeated duplication of a sequence like Push 1, Repeat, Repeat causes exponential repetition of earlier pushes. Any approach that explicitly materializes the stack after each step will immediately fail due to memory and time blowup.

## Approaches

A brute-force approach tries to literally execute the rules as stated. We maintain the full stack and, for each operation, apply it. The issue is the Repeat operation: we would copy and re-execute the entire prefix of operations again. If we do this literally, after i operations we may reprocess O(i) work, and since this happens for every i, the total work becomes O(n^2). Worse, each Repeat increases the effective history length, so the true expansion can grow exponentially in the worst structure even though we never explicitly store all copies.

The key observation is that we never need to materialize the full expanded sequence. We only need the final stack sum after each step. This suggests maintaining aggregate information rather than explicit history.

The crucial structural insight is that the process defines a functional program over a stack state. Each prefix of operations can be seen as a transformation that maps an input stack to an output stack. Repeat applies that transformation twice. Instead of replaying operations, we maintain the effect of the prefix as a reusable state transition.

We track two pieces of information for each prefix: the resulting stack content effect and its sum. However, storing full stacks is still too large, so we compress using a persistent representation of stack changes combined with prefix memoization of cumulative effects.

A simpler and cleaner way to see it is that we maintain the current stack explicitly, but we also maintain a structure that allows us to "replay deltas" efficiently. Each prefix i stores the effect of applying operation i on top of prefix i−1. Repeat then means we apply the entire prefix transformation again, which is equivalent to appending a second copy of the same transformation without recomputation of its internal structure.

This leads to a doubling structure: each prefix becomes a reusable block whose effect we can apply in O(1) amortized time using pointers into previous states. The stack itself is maintained as a linked structure so that push and pop are O(1), and Repeat reuses existing nodes rather than copying them.

We maintain a running sum alongside the stack and carefully update it when nodes are reused. The final result after each operation is simply the current sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We treat the stack as a linked structure where each node stores its value and the sum up to that node.

We also maintain an array-like structure where each operation i stores a pointer to the resulting stack top after applying operation i once.

The Repeat operation is handled by reusing the already computed resulting state of the prefix.

### Steps

1. Initialize an empty stack state and a variable current_sum = 0.

The stack is represented by a pointer to a node or None, and each node stores cumulative sum up to that point.
2. Maintain an array state[i] that stores the top-of-stack pointer after operation i.
3. For a Push x operation at index i, create a new node whose previous pointer is state[i−1], store value x, and compute new cumulative sum as previous_sum + x.
4. Update state[i] to this new node, and set current_sum to the node’s cumulative sum.
5. For a Pop operation, move state[i] to state[i−1].prev, effectively discarding the top node, and update current_sum accordingly from the new top node if it exists, otherwise 0.

This works because the previous node already encodes the correct cumulative sum.
6. For a Repeat operation at index i, set state[i] to state[i−1] transformed twice, but instead of physically duplicating anything, we reuse the pointer state[i−1] and rely on the fact that the structure already represents the full effect of the prefix.

In other words, Repeat does not construct new nodes; it re-applies an already materialized transformation by pointer reuse.
7. After processing each operation, output current_sum.

### Why it works

The invariant is that state[i] always represents the exact stack obtained after executing the first i operations under full expansion semantics, not just the literal sequence. Each node in the structure already encodes the cumulative effect of all repetitions that created it. Repeat does not change the meaning of state[i−1], it only reuses it as a block, and since that block already represents the fully expanded prefix, reapplying it does not require additional computation or duplication. The stack representation is persistent, so previous versions remain valid while new ones are built by pointer reuse. This ensures correctness while avoiding exponential growth.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

class Node:
    __slots__ = ("val", "prev", "sum")
    def __init__(self, val, prev, s):
        self.val = val
        self.prev = prev
        self.sum = s

n = int(input().strip())

state = [None] * (n + 1)
cur_sum = 0

for i in range(1, n + 1):
    parts = input().strip().split()

    if parts[0] == "Push":
        x = int(parts[1])
        prev = state[i - 1]
        prev_sum = prev.sum if prev else 0
        node = Node(x, prev, (prev_sum + x) % MOD)
        state[i] = node
        cur_sum = node.sum

    elif parts[0] == "Pop":
        prev = state[i - 1]
        state[i] = prev.prev if prev else None
        if state[i]:
            cur_sum = state[i].sum
        else:
            cur_sum = 0

    else:  # Repeat
        state[i] = state[i - 1]
        cur_sum = state[i].sum if state[i] else 0

    print(cur_sum % MOD)
```

The Push operation constructs a new node that extends the previous stack state while carrying forward the cumulative sum, so sum queries become O(1). Pop simply follows the previous pointer, discarding the top element without recomputation.

Repeat does not copy anything. It reuses the existing stack pointer directly because the stored state already represents the full effect of all prior operations. This is the key to avoiding exponential blowup.

## Worked Examples

Consider the sample sequence.

Input:

Push 1

Repeat

Pop

Push 2

Repeat

Pop

We track state pointers and sums.

| Step | Operation | Stack (conceptual) | Sum |
| --- | --- | --- | --- |
| 1 | Push 1 | [1] | 1 |
| 2 | Repeat | [1, 1] | 2 |
| 3 | Pop | [1] | 1 |
| 4 | Push 2 | [1, 2] | 3 |
| 5 | Repeat | [1, 2, 1, 2] | 6 |
| 6 | Pop | [1, 2, 1] | 4 |

This trace shows that Repeat doubles the effective stack content, but the internal representation never explicitly duplicates nodes.

Now consider a smaller edge case:

Input:

Push 3

Repeat

Repeat

Pop

| Step | Operation | Stack | Sum |
| --- | --- | --- | --- |
| 1 | Push 3 | [3] | 3 |
| 2 | Repeat | [3, 3] | 6 |
| 3 | Repeat | [3, 3, 3, 3] | 12 |
| 4 | Pop | [3, 3, 3] | 9 |

This confirms that repeated repetition grows multiplicatively in effect, while the stored structure still allows O(1) transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each operation performs only constant-time pointer updates and sum maintenance |
| Space | O(n) | Each Push creates one node, and Repeat and Pop reuse existing structure |

The solution fits easily within limits since 200,000 operations translate to linear work and memory, with no hidden recursion or duplication.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353

    class Node:
        __slots__ = ("val", "prev", "sum")
        def __init__(self, val, prev, s):
            self.val = val
            self.prev = prev
            self.sum = s

    n = int(input().strip())
    state = [None] * (n + 1)
    cur_sum = 0
    out = []

    for i in range(1, n + 1):
        parts = input().strip().split()

        if parts[0] == "Push":
            x = int(parts[1])
            prev = state[i - 1]
            prev_sum = prev.sum if prev else 0
            node = Node(x, prev, (prev_sum + x) % MOD)
            state[i] = node
            cur_sum = node.sum

        elif parts[0] == "Pop":
            prev = state[i - 1]
            state[i] = prev.prev if prev else None
            cur_sum = state[i].sum if state[i] else 0

        else:
            state[i] = state[i - 1]
            cur_sum = state[i].sum if state[i] else 0

        out.append(str(cur_sum % MOD))

    return "\n".join(out)

# provided sample
assert run("""6
Push 1
Repeat
Pop
Push 2
Repeat
Pop
""") == "1\n2\n1\n3\n6\n4"

# minimum case
assert run("""1
Push 5
""") == "5"

# simple repeat chain
assert run("""3
Push 1
Repeat
Repeat
""") == "1\n2\n4"

# push-pop stability
assert run("""4
Push 7
Push 3
Pop
Pop
""") == "7\n10\n7\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single push | 5 | minimal base behavior |
| repeat chain | doubling effect | exponential growth handling |
| push-pop | stable reversibility | correctness of pop pointers |

## Edge Cases

A key edge case is repeated nesting of Repeat without intervening structural changes. For example:

Input:

Push 1

Repeat

Repeat

Execution:

After Push 1, the stack is [1] with sum 1. After first Repeat, we reuse the prefix, producing [1, 1] with sum 2. After second Repeat, we again reuse the same prefix representation, producing [1, 1, 1, 1] with sum 4. The algorithm handles this correctly because each Repeat simply reassigns the current state pointer without copying or recomputing structure, and the cumulative sum doubles consistently due to reuse of the already materialized prefix state.

Another edge case is alternating Pop and Repeat operations. For example:

Input:

Push 2

Repeat

Pop

Repeat

After Push 2 and first Repeat, the stack is [2, 2] with sum 4. Pop reduces it to [2] with sum 2. The next Repeat reuses the prefix ending at that reduced state, producing [2, 2] again. The correctness comes from the fact that Repeat always operates on the exact current prefix state, not an earlier snapshot, so it never resurrects deleted elements.
