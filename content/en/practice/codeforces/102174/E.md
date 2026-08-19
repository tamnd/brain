---
title: "CF 102174E - \u53ea\u6709\u4e00\u7aef\u5f00\u53e3\u7684\u74f6\u5b50"
description: "We receive a permutation p[1..n] containing every value from 1 to n exactly once. The input sequence can only be consumed from left to right."
date: "2026-08-19T07:01:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "E"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 130
verified: true
draft: false
---

[CF 102174E - \u53ea\u6709\u4e00\u7aef\u5f00\u53e3\u7684\u74f6\u5b50](https://codeforces.com/problemset/problem/102174/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We receive a permutation `p[1..n]` containing every value from `1` to `n` exactly once. The input sequence can only be consumed from left to right. Every consumed value may be pushed onto one of the available stacks, and later the top value of a stack may either be appended to the answer or moved onto another stack. The final output must be exactly `1, 2, ..., n`.

The task is to find the smallest number of stacks that makes this possible.

The key surprise is that the answer is never larger than `2`. With one stack, some permutations can already be sorted, while every permutation that cannot be sorted by one stack can be handled with two stacks. Thus the entire problem reduces to recognizing whether the given permutation is a valid single-stack output sequence.

Since `n` can reach `10^5`, an algorithm with quadratic behavior would already require about `10^10` elementary operations in the worst case, which is far beyond what a one-second contest limit can tolerate. We need an `O(n)` or `O(n log n)` solution. The permutation property also means every value is unique, so we never have to handle equal elements as a genuine case.

There are several edge cases that can fool a careless simulation. For `n = 1`, the permutation `[1]` needs only one stack, so the answer is `1`. A naive implementation that assumes at least one element must remain inside a stack can incorrectly return `2`.

For an already increasing permutation such as `1 2 3`, the answer is also `1`. Every value can be consumed and immediately output. An implementation that pushes every input value first would unnecessarily create the stack state `[1, 2, 3]`, whose top is `3`, and might incorrectly conclude that one stack is insufficient.

The important failure pattern is `2 3 1`. The first two values have to be stored before `1` can be output, giving stack state `[2, 3]`. After `1` is produced, `2` is trapped below `3`, so one stack cannot output `2` next. The correct answer is `2`. A careless implementation that checks only whether the permutation contains a decreasing pair, or only whether its longest decreasing subsequence has some particular length, can misclassify such cases.

## Approaches

A direct brute-force approach could try every possible number of stacks and explicitly explore the legal operations. For a fixed configuration, each input value can be assigned to different stacks, and a top value may also be moved between stacks before being output. The number of possible operation sequences grows exponentially because the same values can be routed through different stacks in many orders. Even restricting the search to all possible stack assignments already gives `k^n` possibilities for `n` input values and `k` stacks, which is hopeless when `n = 10^5`.

A more reasonable naive approach is to test whether one stack works by simulating the standard stack-sorting process. The target output is forced: the next required value is always `1`, then `2`, then `3`, and so on. When the next input value is the required value, we can output it immediately. Otherwise it has to be pushed onto the stack. Whenever the stack top becomes the next required value, we pop it.

The crucial observation is that this greedy process completely determines whether one stack is sufficient. There is never a benefit in leaving the required value on top of the stack, because the output must be increasing. Likewise, if the next input value is the required output value, delaying it cannot help.

The brute-force search over stack counts can consequently be reduced even further. We only need to distinguish between one stack and more than one stack. If the permutation passes the one-stack simulation, the answer is `1`. Otherwise the answer is `2`, because two stacks are sufficient for every permutation. The second stack can be used as temporary storage when the first stack contains an element that blocks the next required value. This is exactly why the problem's seemingly general multi-stack operation model collapses to a binary answer.

The one-stack condition is also equivalent to avoiding the classical stack-sortable permutation pattern `231`, but implementing the simulation is simpler and less error-prone than explicitly checking forbidden patterns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Exhaustive operation search | Exponential | Exponential | Too slow |
| Try every possible stack count | `O(n^2)` in a straightforward simulation | `O(n)` | Too slow |
| Greedy one-stack simulation | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Set `need = 1`, meaning that `1` is the next value that must appear in the sorted output. Create an empty auxiliary stack. The output itself does not need to be stored because we only care whether every required value can be produced in order.
2. Process the permutation from left to right. If the current input value equals `need`, consume it and immediately increase `need` by one. This is optimal because the value is already exactly the next value required by the final increasing sequence.
3. If the current input value is not `need`, push it onto the stack. It cannot be output yet because doing so would violate the required increasing order.
4. After every input value is processed, repeatedly check the stack top. While the top equals `need`, pop it and increase `need`. This greedy pop is forced: the top value is ready to be output, and keeping it there cannot make a future arrangement better.
5. After all `n` input values have been consumed, inspect the stack. If it is empty, every value has been output in the required order, so one stack is sufficient and the answer is `1`.
6. If the stack is not empty, one stack cannot sort the permutation. Two stacks are sufficient, so the answer is `2`.

### Why it works

The invariant is that after processing any prefix of the input, all values smaller than `need` have already been output in exactly the required order, while every value currently stored in the stack is waiting for its turn. Whenever `need` is at the stack top, outputting it immediately is mandatory because the final sequence cannot output anything larger first. Whenever the current input equals `need`, putting it into a stack first would only delay an already available correct output.

Thus the greedy simulation succeeds exactly when a legal one-stack execution exists. If it leaves elements behind, those elements cannot be rearranged enough inside one LIFO structure to produce the missing values in order. The general two-stack construction then gives the upper bound of `2`, so the failed one-stack case has minimum answer exactly `2`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        stack = []
        need = 1

        for x in p:
            if x == need:
                need += 1
            else:
                stack.append(x)

            while stack and stack[-1] == need:
                stack.pop()
                need += 1

        ans.append("1" if not stack else "2")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The variable `need` represents the smallest value that has not yet been placed into the final sorted sequence. It starts at `1` and reaches `n + 1` after successful processing.

The list `stack` represents the only stack available in the one-stack test. When the current permutation value is not immediately usable, it is pushed onto this list. Python's `append` models a stack push, while `pop` removes the top element.

The `while` loop is necessary rather than a single `if`. One newly consumed value can expose another required value underneath it. For example, with permutation `3 2 1`, all three values are pushed, and then the top sequence `1, 2, 3` can be popped consecutively. Missing this repeated popping is a common off-by-one error in stack simulations.

The test for `x == need` happens before pushing `x`. If the incoming value is exactly the next required value, it never needs to enter the stack. This is what allows an increasing permutation such as `1 2 3` to be processed using one stack without leaving anything stored.

There is no integer overflow issue because all values are at most `10^5`, and Python integers handle the counters directly anyway. The total amount of stored data is linear in `n`.

## Worked Examples

### Sample 1

For the permutation `3 2 1`, the stack simulation proceeds as follows.

| Input value | `need` before processing | Stack before | Action | `need` after | Stack after |
| --- | --- | --- | --- | --- | --- |
| 3 | 1 | `[]` | push 3 | 1 | `[3]` |
| 2 | 1 | `[3]` | push 2 | 1 | `[3, 2]` |
| 1 | 1 | `[3, 2]` | push 1, then pop 1, 2, 3 | 4 | `[]` |

When `1` arrives, it is pushed because the simulation treats every non-immediate value uniformly. It becomes the top of the stack, so `1` is popped. That exposes `2`, which is also the next required value, so `2` is popped as well. Finally `3` is exposed and popped.

The stack is empty at the end, so the output is `1`. This example demonstrates why the repeated `while` loop is necessary.

### Sample 2

For the permutation `2 1`, the trace is:

| Input value | `need` before processing | Stack before | Action | `need` after | Stack after |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | `[]` | push 2 | 1 | `[2]` |
| 1 | 1 | `[2]` | push 1, then pop 1 and 2 | 3 | `[]` |

After `1` is pushed, it can be popped immediately. That exposes `2`, which is now exactly the next required value. Both values are consequently produced in sorted order using one stack.

The final stack is empty, giving answer `1`.

### Sample 3

For the permutation `2 3 1`, the trace is:

| Input value | `need` before processing | Stack before | Action | `need` after | Stack after |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | `[]` | push 2 | 1 | `[2]` |
| 3 | 1 | `[2]` | push 3 | 1 | `[2, 3]` |
| 1 | 1 | `[2, 3]` | push 1, pop 1 | 2 | `[2, 3]` |

After `1` is output, the next required value is `2`, but the stack top is `3`. Since `2` is trapped below `3`, one stack cannot continue.

The remaining stack proves that the answer is not `1`. Two stacks are sufficient, so the answer is `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` per test case | Every input value is pushed at most once and popped at most once. |
| Space | `O(n)` | The auxiliary stack can contain all `n` values. |

Across all test cases, the natural intended bound is linear in the total number of permutation elements. With `n` up to `10^5`, this easily fits the required limits because the algorithm performs only a constant amount of work per input value.

## Test Cases

The original problem guarantees that every input is a permutation, so an "all-equal values" test is not a valid test case. The closest meaningful boundary test is a strictly increasing permutation, where every value can be output immediately.

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        stack = []
        need = 1

        for x in p:
            if x == need:
                need += 1
            else:
                stack.append(x)

            while stack and stack[-1] == need:
                stack.pop()
                need += 1

        ans.append("1" if not stack else "2")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run(
    "3\n"
    "3\n"
    "3 2 1\n"
    "2\n"
    "2 1\n"
    "3\n"
    "2 3 1\n"
) == "1\n1\n2", "provided samples"

# Minimum-size input
assert run(
    "1\n"
    "1\n"
    "1\n"
) == "1", "single element"

# Already sorted, every value can be output immediately
assert run(
    "1\n"
    "5\n"
    "1 2 3 4 5\n"
) == "1", "increasing permutation"

# A classic one-stack failure
assert run(
    "1\n"
    "4\n"
    "2 3 1 4\n"
) == "2", "231 pattern"

# Decreasing permutation, requiring repeated pops
assert run(
    "1\n"
    "6\n"
    "6 5 4 3 2 1\n"
) == "1", "maximum stack depth"

# Large boundary case, increasing permutation
n = 100000
p = " ".join(map(str, range(1, n + 1)))
assert run(f"1\n{n}\n{p}\n") == "1", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Smallest possible input and boundary initialization of `need`. |
| `1 / 5 / 1 2 3 4 5` | `1` | Values can be output directly without using the stack. |
| `1 / 4 / 2 3 1 4` | `2` | Detects the `231` obstruction and prevents a false one-stack result. |
| `1 / 6 / 6 5 4 3 2 1` | `1` | Exercises maximum stack depth and repeated popping. |
| `1 / 100000 / 1 2 ... 100000` | `1` | Confirms linear behavior at the maximum allowed `n`. |

## Edge Cases

For `n = 1`, the input is exactly `1`. The simulation starts with `need = 1`, sees that the current value equals `need`, and increments `need` to `2`. The stack remains empty, so the answer is `1`.

For an already sorted permutation such as `1 2 3 4 5`, every incoming value equals `need`. The algorithm never pushes anything, and `need` advances from `1` to `6`. The final stack is empty, so the answer is `1`. This catches implementations that unnecessarily push every input value before attempting to pop.

For the obstruction `2 3 1`, the first two values are pushed, producing `[2, 3]`. When `1` arrives, it is pushed and immediately popped, leaving `[2, 3]` with `3` at the top while `2` is required. The stack cannot produce the correct next value, so the simulation ends with nonempty storage and returns `2`.

For the decreasing permutation `6 5 4 3 2 1`, every value is initially pushed. Once `1` arrives, the `while` loop removes `1`, then `2`, then `3`, then `4`, then `5`, and finally `6`. The stack becomes empty, proving that a deep stack is not itself a reason to require multiple stacks. The ordering of the trapped values matters.

For the maximum input size, an increasing permutation of length `100000` causes exactly one constant-time decision per value and never grows the stack. A decreasing permutation of the same size pushes every value and later pops every value once. In either case the total number of stack operations remains linear, so the implementation stays within the intended complexity bound.
