---
title: "CF 104021N - Fibonacci Sequence"
description: "The task is extremely direct: we are asked to generate the beginning of a well-known integer sequence defined purely by recurrence. The sequence starts with two fixed seeds, both equal to one, and every later value is obtained by summing the previous two values."
date: "2026-07-02T04:38:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104021
codeforces_index: "N"
codeforces_contest_name: "The 2019 ICPC Asia Yinchuan Regional Contest"
rating: 0
weight: 104021
solve_time_s: 33
verified: true
draft: false
---

[CF 104021N - Fibonacci Sequence](https://codeforces.com/problemset/problem/104021/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is extremely direct: we are asked to generate the beginning of a well-known integer sequence defined purely by recurrence. The sequence starts with two fixed seeds, both equal to one, and every later value is obtained by summing the previous two values. The output requirement is not parametric, there is no input to process, and we always produce exactly the first five terms.

Even though the constraints are not explicitly stated, the structure of the problem makes it clear that performance is irrelevant. We are only performing a constant amount of arithmetic, so any reasonable implementation runs in constant time and constant memory. Even an extremely inefficient approach would still be acceptable because the sequence length is fixed.

There are no meaningful edge cases in the usual competitive programming sense, but there is one subtle formatting constraint that can break a solution: the output must contain exactly five integers separated by a single space, with no trailing spaces or extra symbols. A careless implementation that prints a space after every number, including the last one, can produce wrong output despite computing correct values. For example, printing `"1 1 2 3 5 "` with a trailing space is invalid, even though the numbers themselves are correct.

## Approaches

A brute-force interpretation would be to simulate the definition step by step using an array and repeatedly compute each next value from the previous two. This approach mirrors the mathematical definition exactly and is correct by construction. It would build a list `F` where `F[0] = 1`, `F[1] = 1`, and for each subsequent index it appends `F[i-1] + F[i-2]`.

Even this direct simulation is overkill because we only need five values. The total number of arithmetic operations is constant, so the runtime does not depend on any input size. There is no benefit in optimizing further because we are already at the minimum possible complexity.

The key observation is that the Fibonacci definition is inherently iterative and local. Each term depends only on the previous two terms, so we never need to store more than those two values at any time. This allows us to compute the sequence in a streaming fashion without allocating an array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (array build) | O(5) | O(5) | Accepted |
| Optimal (rolling variables) | O(5) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the sequence iteratively while keeping only the last two values.

1. Initialize two variables representing the first two Fibonacci numbers, both set to 1. These act as the base cases of the recurrence.
2. Output the first value immediately, since it is fixed by definition.
3. Output the second value, which is identical to the first.
4. Repeatedly compute the next term as the sum of the previous two stored values. After computing a new value, shift the stored pair forward so that they always represent the last two terms in the sequence.
5. Continue this process until five values have been produced in total.

The key idea in steps 4 and 5 is that we never recompute from scratch. Each new value extends the sequence by one step using only already computed results, which mirrors the mathematical recurrence directly.

### Why it works

At any moment during the process, the two stored variables represent consecutive Fibonacci numbers. When we compute their sum, we obtain the next Fibonacci number by definition. Updating the pair by shifting forward preserves the invariant that they always correspond to the latest two terms in the sequence. Since the recurrence uniquely defines each term from the previous two, maintaining this invariant guarantees every produced value is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

# first five Fibonacci numbers
a, b = 1, 1
out = [a, b]

for _ in range(3):
    a, b = b, a + b
    out.append(b)

sys.stdout.write(" ".join(map(str, out)))
```

The solution initializes the sequence with the two base values and then iteratively generates the next three values. The loop runs exactly three times because we already have two numbers and need a total of five.

The update step `a, b = b, a + b` is the core of the implementation. It simultaneously shifts the window forward and computes the next Fibonacci number without needing temporary variables. This ordering is crucial because `b` must be updated based on the old `a` and `b` before overwriting either value.

The final output uses `" ".join(...)` to ensure correct spacing without trailing whitespace, which is the most common formatting pitfall in such problems.

## Worked Examples

We trace the computation starting from the initial state.

### Example Trace

Initial state:

| Step | a | b | Output |
| --- | --- | --- | --- |
| Init | 1 | 1 | 1, 1 |

After first iteration:

| Step | a | b | Output |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 1, 1, 2 |

After second iteration:

| Step | a | b | Output |
| --- | --- | --- | --- |
| 2 | 2 | 3 | 1, 1, 2, 3 |

After third iteration:

| Step | a | b | Output |
| --- | --- | --- | --- |
| 3 | 3 | 5 | 1, 1, 2, 3, 5 |

This confirms that each iteration correctly advances the Fibonacci recurrence by one step while preserving the rolling state.

### Second Example (conceptual variation)

Even if we start from the same seeds, the structure guarantees determinism:

| Step | a | b | Output |
| --- | --- | --- | --- |
| Init | 1 | 1 | 1, 1 |
| 1 | 1 | 2 | 1, 1, 2 |
| 2 | 2 | 3 | 1, 1, 2, 3 |
| 3 | 3 | 5 | 1, 1, 2, 3, 5 |

This reinforces that there is no branching or input dependency; the sequence is fully determined by its definition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | We perform a fixed number of arithmetic operations independent of input |
| Space | O(1) | Only a constant number of variables are stored |

The problem size is fixed at five outputs, so the solution is trivially within any conceivable time and memory limits. Even in strict environments, this computation is effectively instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a, b = 1, 1
    out = [a, b]
    for _ in range(3):
        a, b = b, a + b
        out.append(b)
    return " ".join(map(str, out))

# provided sample
assert run("") == "1 1 2 3 5"

# minimal case (same problem, no input influence)
assert run("") == "1 1 2 3 5", "deterministic output"

# repeated check consistency
assert run("") == "1 1 2 3 5", "idempotent behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty | 1 1 2 3 5 | base correctness |
| empty | 1 1 2 3 5 | determinism |
| empty | 1 1 2 3 5 | no state dependence |

## Edge Cases

The only meaningful edge case is output formatting, since the sequence itself is fixed. Any correct computation always yields `1 1 2 3 5`, so failures come from printing rather than logic.

For example, a buggy implementation might do:

Input:

```
(no input)
```

Incorrect output:

```
1 1 2 3 5
```

Correct output:

```
1 1 2 3 5
```

The algorithm itself never produces trailing spaces; the join-based output construction ensures that spacing is inserted only between elements. This makes the formatting constraint automatically satisfied without special-case handling for the last element.
