---
title: "CF 102168B - \u0423\u0434\u0432\u043e\u0435\u043d\u0438\u044f"
description: "We start with a set of integers, so duplicate input values are stored only once. The procedure is repeated (10^{10}) times. At each iteration, we take the current minimum value (x), remove it, and try to insert (2x). If (2x) is already present, the set loses one element."
date: "2026-08-19T15:15:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "B"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 178
verified: true
draft: false
---

[CF 102168B - \u0423\u0434\u0432\u043e\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/102168/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a set of integers, so duplicate input values are stored only once. The procedure is repeated (10^{10}) times. At each iteration, we take the current minimum value (x), remove it, and try to insert (2x). If (2x) is already present, the set loses one element. Otherwise, the set size stays unchanged.

The input contains (n) initial integers, with (1 \le n \le 200000), and every value is at most (10^9). The required output is the number of distinct integers remaining after all (10^{10}) operations.

The enormous number of operations immediately rules out direct simulation. Even an idealized (O(1)) implementation would need (10^{10}) iterations, while a normal set or heap would add another logarithmic factor. With (n) up to (200000) and a two second limit, we need to replace the simulation with a mathematical observation.

There are three edge cases that commonly cause wrong answers. First, duplicates in the input must disappear immediately. For example, the input `3\n5 5 5` represents the set `{5}`, and after any number of operations its size remains `1`, so the answer is `1`, not `3`. A careless solution that counts input elements rather than distinct values fails here.

Second, two different numbers can eventually merge. For `2\n3 6`, the set is initially `{3, 6}`. The first operation changes `3` into `6`, producing `{6}`, so the answer is `1`. Merely counting distinct initial values gives `2`.

Third, numbers that are related by powers of two belong to the same chain. For `3\n5 10 20`, the values are (5\cdot2^0), (5\cdot2^1), and (5\cdot2^2). The minimum is repeatedly doubled until these values merge, and the final size is `1`. Looking only at the original numerical values misses this structure.

## Approaches

The direct approach is to maintain the set, repeatedly find its minimum, remove it, and insert twice that value. It is correct because it follows the operation exactly, including the case where the doubled value already exists. The problem is the number of iterations. The procedure requires exactly (10^{10}) operations, so even if finding and updating the minimum took constant time, the simulation would perform ten billion iterations. With a balanced tree or heap, the cost is even larger, around (O(10^{10}\log n)).

The key is to stop thinking about the actual magnitudes and instead look at what happens when a number is repeatedly doubled. Every positive integer can be written uniquely as

[
x = odd(x)\cdot2^k,
]

where (odd(x)) is odd. Doubling changes only (k), while the odd part stays unchanged. Thus values with different odd parts can never interact with each other. Values with the same odd part form one independent chain:

[
c,\ 2c,\ 4c,\ 8c,\ldots
]

where (c) is odd.

Inside one such chain, the operation moves the smallest exponent one step to the right. Whenever that next exponent already exists, two set elements become one. Eventually all values belonging to the same chain merge into a single value.

The bound (a_i\le10^9) makes this especially powerful. Since (2^{29}<10^9<2^{30}), every initial value contains at most 29 factors of two. A chain therefore needs at most 29 useful doubling steps before all its initial elements have merged into one. There are at most (n) chains, so fewer than (29n\le5.8\cdot10^6) useful operations are needed to reduce every chain to one element. This is tiny compared with (10^{10}).

After that point, every chain contains exactly one element. Doubling its only element produces another value in the same chain, but there is no second element there to merge with it. The set size consequently remains constant for every remaining operation.

So the final answer is simply the number of distinct odd parts among the initial numbers. We can obtain that by repeatedly dividing every input value by two while it is even, then inserting the resulting odd value into a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^{10}\log n)) | (O(n)) | Too slow |
| Optimal | (O(n\log a_{\max})) expected | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all (n) initial values and create an empty set `odd_parts`. We only need to know which odd chains exist, because chains with different odd parts never interact.
2. For every value `x`, repeatedly divide it by two while it is even. After this loop, `x` is the odd part of the original number.
3. Insert this odd part into `odd_parts`. If several initial values belong to the same doubling chain, they produce the same odd part and are stored only once.
4. Output the size of `odd_parts`. The (10^{10}) operations are guaranteed to have enough time to collapse every initial chain to one element, after which further operations do not change the set size.

### Why it works

Consider one fixed odd number (c). Every value with odd part (c) has the form (c2^k), so an operation on such a value can only change its exponent (k) to (k+1). It can never interact with a value whose odd part differs from (c).

Within the chain for (c), take the smallest exponent currently present. The operation removes that exponent and inserts the next one. If that next exponent is already present, the number of elements in the chain decreases by one. Repeating this process eventually merges every initially present exponent into the largest relevant exponent, leaving exactly one element in the chain.

Every initial exponent is at most 29 because the original value is at most (10^9). Hence each chain needs at most 29 operations that contribute to merging. Across at most (200000) chains, fewer than (5.8\cdot10^6) operations are sufficient to reach one element per chain, which is far below (10^{10}).

Once a chain has one element, its minimum is doubled into a previously absent value, so its size remains one. Consequently, after all chains have collapsed, the set size is exactly the number of distinct odd parts initially present.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = map(int, input().split())

    odd_parts = set()

    for x in a:
        while x % 2 == 0:
            x //= 2
        odd_parts.add(x)

    print(len(odd_parts))

if __name__ == "__main__":
    solve()
```

The `odd_parts` set represents the independent doubling chains. For each input number, the `while` loop removes every factor of two, leaving exactly its unique odd component.

The loop executes at most 29 times for one value, because (2^{29}<10^9). Python integers do not overflow when performing the divisions, and in fact the values only become smaller during this preprocessing.

The final `len(odd_parts)` counts the chains rather than the original elements. This automatically handles duplicate input values and values such as `5`, `10`, and `20` that eventually merge.

No simulation of the (10^{10}) operations is necessary.

## Worked Examples

For Sample 1, the input is `2` with values `3 4`.

| Original value | Odd part | `odd_parts` after insertion |
| --- | --- | --- |
| 3 | 3 | `{3}` |
| 4 | 1 | `{1, 3}` |

The two values belong to different chains. The chain starting at 3 contains (3,6,12,\ldots), while the chain starting at 1 contains (1,2,4,\ldots). Neither chain can merge with the other, so the final answer is `2`.

For Sample 2, the input is `20` with values `10 5`.

| Original value | Odd part | `odd_parts` after insertion |
| --- | --- | --- |
| 10 | 5 | `{5}` |
| 5 | 5 | `{5}` |

Both values belong to the same chain:

[
5,\ 10,\ 20,\ 40,\ldots
]

The initial two elements eventually collapse into one. After that, doubling the remaining element simply moves it forward in the same chain, so its size stays one. The answer is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log a_{\max})) expected | Each value is divided by two at most 29 times, and set insertion is expected (O(1)). |
| Space | (O(n)) | At most one odd part is stored for each input value. |

With (n\le200000) and at most 29 divisions per value, the preprocessing performs only a few million simple operations. The set contains at most (200000) integers, which is well within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())
    a = map(int, input().split())

    odd_parts = set()

    for x in a:
        while x % 2 == 0:
            x //= 2
        odd_parts.add(x)

    print(len(odd_parts))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("2\n3 4\n") == "2", "sample 1"

# Provided sample 2
assert run("2\n10 5\n") == "1", "sample 2"

# Minimum size
assert run("1\n1\n") == "1", "single element"

# All values are equal
assert run("5\n7 7 7 7 7\n") == "1", "duplicates"

# Several values from the same doubling chain
assert run("5\n5 10 20 40 80\n") == "1", "one doubling chain"

# Boundary value 1e9 and values from different chains
assert run("3\n1000000000 500000000 3\n") == "2", "boundary and shared chain"

# Maximum n, all equal
assert run("200000\n" + "1 " * 199999 + "1\n") == "1", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n3 4` | `2` | Provided sample with two independent chains |
| `2\n10 5` | `1` | Provided sample where both values share an odd part |
| `1\n1` | `1` | Minimum input size |
| `5\n7 7 7 7 7` | `1` | Duplicate values must count once |
| `5\n5 10 20 40 80` | `1` | Entire input belongs to one doubling chain |
| `3\n1000000000 500000000 3` | `2` | Large values and a shared chain at the upper boundary |
| `200000` copies of `1` | `1` | Maximum (n) and duplicate handling |

## Edge Cases

The duplicate case `3\n5 5 5` is reduced immediately to the single odd part `5`. The set contains only one element from the beginning, and every subsequent doubling moves that element along the chain without changing the set size. The algorithm inserts `5` three times into a Python set, but the set still contains only one value, so it outputs `1`.

For the merging case `2\n3 6`, dividing out powers of two gives odd parts `3` and `3`. The algorithm stores only `{3}` and outputs `1`. This captures the future behavior even though the two original values are distinct.

For the longer chain `3\n5 10 20`, all three values reduce to the same odd part `5`. The set therefore has one chain, and the answer is `1`. The fact that the chain contains several consecutive powers of two does not require simulating any of the operations.

At the upper numeric boundary, `1000000000` is even and repeatedly dividing by two eventually produces `1953125`. The number has only nine factors of two, so the preprocessing is still tiny. The algorithm never needs to construct the much larger values that could appear after (10^{10}) doublings, which also avoids making the answer depend on enormous simulated integers.

Finally, when (n=200000) and all values are equal, the input set has size one despite containing (200000) entries. The algorithm performs a constant amount of work per entry and stores only one odd part, so both the runtime and memory usage remain comfortably within the limits.
