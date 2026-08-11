---
title: "CF 102420J - \u041c\u0430\u043b\u0435\u0444\u0438\u0441\u0443\u043c\u043c\u0430"
description: "We have an array of (n) nonnegative integers (a1,a2,ldots,an). We need the sum of the products of every three distinct elements, where the indices must satisfy (i<j<k): [ sum{1le i<j<kle n} ai aj ak."
date: "2026-08-12T00:54:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "J"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 106
verified: true
draft: false
---

[CF 102420J - \u041c\u0430\u043b\u0435\u0444\u0438\u0441\u0443\u043c\u043c\u0430](https://codeforces.com/problemset/problem/102420/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of (n) nonnegative integers (a_1,a_2,\ldots,a_n). We need the sum of the products of every three distinct elements, where the indices must satisfy (i<j<k):

[
\sum_{1\le i<j<k\le n} a_i a_j a_k.
]

The order inside a chosen triple does not matter, but every set of three different positions must contribute exactly once. The answer is required modulo (10^9+7).

The difficulty comes from the size of (n). With (n\le 10^6), checking every triple is not remotely practical. The number of triples is

[
\binom{n}{3},
]

which reaches

[
\binom{10^6}{3}=166666166667000000
]

at the maximum size. Even if calculating one product took only a few primitive operations, iterating over roughly (1.67\cdot10^{17}) triples is far beyond any reasonable time limit.

The values (a_i) can also be as large as (10^6), so the mathematical answer is enormous. We must perform arithmetic modulo (10^9+7), and the implementation should reduce intermediate values regularly rather than allowing unnecessarily large integers to accumulate.

There are several edge cases that can expose an incorrect implementation. With the minimum number of elements, the input

```
3
1 2 3
```

has exactly one triple, so the answer is (1\cdot2\cdot3=6). An implementation that accidentally requires four elements, or starts updating the pair sum before adding the contribution to the answer, can get this boundary case wrong.

Zero values are another useful case. For

```
4
0 5 6 7
```

every triple containing the zero contributes nothing, leaving only (5\cdot6\cdot7=210). A formula based on division or on an assumption that every value is positive can behave incorrectly here.

Repeated values require the positions, rather than the numerical values, to be treated as distinct choices. For example,

```
4
2 2 2 2
```

has four triples, each contributing (8), so the answer is (32). An implementation that tries to enumerate distinct value combinations instead of index combinations would count this incorrectly.

Finally, very large values must still be handled correctly modulo (10^9+7). For example,

```
3
1000000 1000000 1000000
```

has answer (10^{18}), which is (49) modulo (10^9+7). The individual input values fit comfortably in standard integer types, but products and sums grow much faster.

## Approaches

The direct solution follows the definition literally. We choose (i), then (j>i), then (k>j), calculate (a_i a_j a_k), and add it to the answer. This is correct because every valid triple of indices is visited exactly once.

The problem is the number of iterations. For (n=10^6), the three nested loops execute once for each of the

[
\binom{10^6}{3}=166666166667000000
]

possible triples. That is (O(n^3)), which is much too slow.

The useful observation is that the triple containing the current element does not need to be constructed explicitly. Suppose we process the array from left to right and currently examine (a_k). Every new triple ending at position (k) has the form

[
a_i a_j a_k,\qquad i<j<k.
]

We can factor out (a_k):

[
a_k\sum_{i<j<k}a_i a_j.
]

So, before processing (a_k), we only need to know the sum of products of every pair among the elements already processed.

Call this quantity `pair_sum`. We also need the sum of all previous elements, because when (a_k) becomes part of a pair, every previous element forms one such pair with it:

a_k\sum_{i<k}a_i.
]

Thus two running values are enough. `sum1` stores the sum of previous elements, and `sum2` stores the sum of products of all pairs among previous elements.

When processing (x=a_k), the existing `sum2` represents exactly the pairs ((i,j)) with (i<j<k). Multiplying it by (x) adds every new triple ending at (k):

[
\text{answer}\mathrel{+}=x\cdot\text{sum2}.
]

After that, (x) has to become part of all future pairs. Those new pairs have total product sum

[
x\cdot\text{sum1},
]

so we update

[
\text{sum2}\mathrel{+}=x\cdot\text{sum1}.
]

Finally, (x) becomes available as a previous element:

[
\text{sum1}\mathrel{+}=x.
]

The order of these updates is essential. The answer must use the old `sum2`, because triples ending at the current position must use two earlier positions. If we updated `sum2` first, the current element could accidentally be used twice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(1)) | Too slow |
| Optimal | (O(n)) | (O(1)) extra | Accepted |

## Algorithm Walkthrough

1. Initialize `sum1 = 0`, `sum2 = 0`, and `answer = 0`. Before processing anything, there are no previous elements, no previous pairs, and no previous triples.
2. Read each array value (x) from left to right. We process positions in their natural order so that every newly created triple automatically has its indices in increasing order.
3. Add (x\cdot\text{sum2}) to `answer`. At this exact moment, `sum2` contains all products (a_i a_j) with both indices strictly before the current position. Multiplying each of them by (x) creates every triple whose last index is the current position.
4. Update `sum2` by adding (x\cdot\text{sum1}). Here `sum1` contains every previously processed value, so this creates precisely all pairs consisting of the current element and one earlier element.
5. Update `sum1` by adding (x). The current element is now a previous element for every position processed later.
6. Perform the arithmetic modulo (10^9+7). Since addition and multiplication respect modular arithmetic, reducing each running quantity modulo the modulus gives exactly the same final remainder as computing the full integer first.

### Why it works

The invariant after processing the first (k) elements is that `sum1` equals

[
\sum_{i=1}^{k}a_i,
]

while `sum2` equals

[
\sum_{1\le i<j\le k}a_i a_j,
]

and `answer` equals

[
\sum_{1\le i<j<l\le k}a_i a_j a_l.
]

When the next value (a_{k+1}) arrives, multiplying the old `sum2` by (a_{k+1}) adds exactly all triples whose largest index is (k+1). Updating `sum2` then adds exactly all new pairs involving (a_{k+1}), and updating `sum1` adds the new element itself. No triple can be added twice because each triple is added when its largest index is processed, and no invalid triple can appear because `sum2` contains only pairs from earlier positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n = int(input())

    sum1 = 0
    sum2 = 0
    answer = 0

    for _ in range(n):
        x = int(input().split()[0]) if False else None
```

The input contains all (n) numbers on the second line, so a direct streaming loop over `input().split()` is preferable in Python. The complete implementation is:

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n = int(input())
    a = map(int, input().split())

    sum1 = 0
    sum2 = 0
    answer = 0

    for x in a:
        answer = (answer + x * sum2) % MOD
        sum2 = (sum2 + x * sum1) % MOD
        sum1 = (sum1 + x) % MOD

    print(answer)

if __name__ == "__main__":
    solve()
```

The first state variable, `sum1`, represents the elementary symmetric sum of degree one over the processed prefix. The second, `sum2`, represents the degree-two symmetric sum. The answer itself is the degree-three symmetric sum.

The answer is updated before `sum2`. This is the most subtle part of the implementation. Consider the current value (x). Before processing it, `sum2` contains pairs formed exclusively from earlier elements, which is exactly what is needed to create valid triples with (x). After the answer update, adding (x\cdot\text{sum1}) to `sum2` prepares the state for later elements.

The code takes the values with `map`, so it does not construct a second list of Python integers from the input. The input line itself is still tokenized by `split`, which is appropriate for this problem size and keeps the implementation simple.

Python integers do not overflow, but modular reduction is still performed after every state update. Besides keeping the numbers small, this makes the correspondence with the mathematical modular computation explicit.

There is no special handling for the first two elements. Initially `sum2` is zero, so the first two values cannot contribute a triple. After two values have been processed, `sum2` contains their product, and the third value creates the first possible triple naturally.

## Worked Examples

### Sample 1

The input is

```
3
1 2 3
```

The following table tracks the state before and after each value is processed.

| Current value (x) | `sum1` before | `sum2` before | `answer` before | `answer` after | `sum2` after | `sum1` after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 2 | 3 |
| 3 | 3 | 2 | 0 | 6 | 11 | 6 |

After processing (1), there are no pairs yet. After processing (2), the only pair has product (1\cdot2=2). When (3) arrives, the old `sum2` is (2), so the algorithm adds (3\cdot2=6) to the answer. This is exactly the only possible triple.

### Sample 2

The input is

```
4
0 5 6 7
```

The state evolves as follows.

| Current value (x) | `sum1` before | `sum2` before | `answer` before | `answer` after | `sum2` after | `sum1` after |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| 6 | 5 | 0 | 0 | 0 | 30 | 11 |
| 7 | 11 | 30 | 0 | 210 | 107 | 18 |

The zero contributes nothing to every product, so the first two nonzero values eventually create the pair (5\cdot6=30). When (7) is processed, that pair produces (30\cdot7=210). The other triples all contain the initial zero and contribute zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each array element is processed exactly once with constant-time arithmetic. |
| Space | (O(1)) extra | Only three running modular sums are maintained. |

For (n\le10^6), a linear pass performs only a few arithmetic operations per element, while the brute-force method would require roughly (1.67\cdot10^{17}) triple iterations at the upper bound. The linear solution is comfortably within the intended scale of the problem and avoids storing any additional array structure.

## Test Cases

The test harness below uses the same recurrence as the submitted solution, but wraps it in a function so every case can be checked with `assert`. The maximum-size case uses one million zeros, which keeps the generated input simple while exercising the actual input and loop boundary.

```python
import sys
import io

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = map(int, input().split())

    sum1 = 0
    sum2 = 0
    answer = 0

    for x in a:
        answer = (answer + x * sum2) % MOD
        sum2 = (sum2 + x * sum1) % MOD
        sum1 = (sum1 + x) % MOD

    return str(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("3\n1 2 3\n") == "6", "sample 1"
assert run("4\n0 5 6 7\n") == "210", "sample 2"

# Minimum-size input
assert run("3\n0 0 0\n") == "0", "minimum size with zeros"

# All values equal:
# C(4, 3) * 2^3 = 4 * 8 = 32
assert run("4\n2 2 2 2\n") == "32", "all equal values"

# Maximum allowed value
# 1,000,000^3 mod 1,000,000,007 = 49
assert run("3\n1000000 1000000 1000000\n") == "49", "maximum value boundary"

# Maximum n, exercising the O(n) loop.
max_n = 1_000_000
max_input = str(max_n) + "\n" + ("0 " * (max_n - 1)) + "0\n"
assert run(max_input) == "0", "maximum n"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 0 0 0` | `0` | Minimum (n), zero products, and the fact that no triple is counted before three elements exist |
| `4 / 2 2 2 2` | `32` | Repeated values and correct counting by indices |
| `3 / 1000000 1000000 1000000` | `49` | Maximum input value and modular multiplication |
| (n=10^6), all values zero | `0` | Maximum input size and linear-time processing |

## Edge Cases

### Exactly three elements

For

```
3
1 2 3
```

the initial state is `sum1 = 0`, `sum2 = 0`, `answer = 0`. Processing (1) changes only `sum1`, giving (1). Processing (2) creates the pair sum (2), while the answer remains zero because there are still only two elements. Processing (3) uses the old pair sum, so `answer = 3 * 2 = 6`. The output is `6`.

This catches an off-by-one mistake where the implementation might update the pair state before calculating the contribution of the current element.

### A zero element

For

```
4
0 5 6 7
```

processing zero leaves all three states at zero. Processing (5) gives `sum1 = 5`. Processing (6) produces `sum2 = 30`. When (7) arrives, it contributes (7\cdot30=210). The output is `210`.

The recurrence does not need a special zero case. Since zero naturally contributes zero to both new pairs and new triples, the same invariant works unchanged.

### Repeated values

For

```
4
2 2 2 2
```

the first two values produce `sum2 = 4`. The third value contributes (2\cdot4=8), and the pair state becomes (12). The fourth value contributes (2\cdot12=24). The final answer is (8+24=32).

The four index triples are ((1,2,3)), ((1,2,4)), ((1,3,4)), and ((2,3,4)). Each has product (8), so the total is (32). The recurrence counts them according to their largest index, which gives three triples when processing the fourth element and one triple when processing the third.

### Maximum value and modular arithmetic

For

```
3
1000000 1000000 1000000
```

there is one triple, with product

[
10^6\cdot10^6\cdot10^6=10^{18}.
]

Since

[
10^{18}\bmod 1,000,000,007=49,
]

the correct output is `49`.

The implementation computes the same result by reducing the state after every update. Python itself has arbitrary-precision integers, but modular reduction keeps the running state bounded and matches the required arithmetic.

### Maximum array size

For (n=10^6) and every value equal to zero, the input contains one million elements and the answer is still zero. The algorithm executes exactly one constant-time iteration for each element. It never creates a nested enumeration of triples, so its running time grows linearly rather than cubically.

The same loop structure also handles one million nonzero values. The values of `sum1`, `sum2`, and `answer` remain reduced modulo (10^9+7), so the size of the maintained state does not depend on (n).
