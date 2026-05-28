---
title: "CF 219B - Special Offer! Super Price 999 Bourles!"
description: "Polycarpus already knows the best regular price for his product, p. He is willing to reduce it by at most d bourles if that gives the final price a more attractive ending, specifically as many trailing nines as possible. A trailing nine means a digit 9 at the end of the number."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 219
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 135 (Div. 2)"
rating: 1400
weight: 219
solve_time_s: 89
verified: true
draft: false
---

[CF 219B - Special Offer! Super Price 999 Bourles!](https://codeforces.com/problemset/problem/219/B)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

Polycarpus already knows the best regular price for his product, `p`. He is willing to reduce it by at most `d` bourles if that gives the final price a more attractive ending, specifically as many trailing nines as possible.

A trailing nine means a digit `9` at the end of the number. For example, `12999` has three trailing nines, while `9099` has two because only the suffix matters.

Among all prices `x` such that:

- `x <= p`
- `p - x <= d`

we want the one with the maximum number of trailing nines. If several prices have the same number of trailing nines, we choose the largest such price.

The limits are the interesting part here. `p` can be as large as `10^18`, so we cannot iterate over every possible price in the interval `[p-d, p]`. In the worst case that interval itself can contain almost `10^18` numbers, far beyond what fits into a one second time limit.

The structure of the problem suggests that only very specific candidates matter. A number ending with one trailing nine looks like:

```
...9
```

A number ending with two trailing nines looks like:

```
...99
```

A number ending with three trailing nines looks like:

```
...999
```

and so on.

For each possible count of trailing nines, there is exactly one largest candidate not exceeding `p`. That observation is what makes the problem small.

There are a few edge cases that are easy to mishandle.

Suppose:

```
p = 1000
d = 0
```

We are not allowed to decrease the price at all. The answer must stay `1000`, even though `999` has more trailing nines. A careless implementation that always rounds downward to the nearest `999...` value would incorrectly output `999`.

Another tricky case is:

```
p = 10999
d = 1
```

The answer is `10999` because it already has three trailing nines. Some implementations unnecessarily modify the number even when the optimal answer is already equal to `p`.

A more subtle case is:

```
p = 10000
d = 100
```

The best answer is `9999`. It has four trailing nines and costs only `1` bourle less than `p`. If we greedily try to maximize the value first, we could incorrectly stop at `9990` or `999`.

The final important detail is tie-breaking. Consider:

```
p = 1999
d = 1000
```

Both `999` and `1999` are valid. Each has three trailing nines. We must choose the larger one, which is `1999`.

## Approaches

The brute force idea is straightforward. Iterate through every candidate price `x` from `p-d` up to `p`, count how many trailing nines each number has, and keep the best one according to the rules.

Counting trailing nines is easy. Repeatedly check whether the last digit is `9`, divide by `10`, and count how many times this succeeds.

The brute force is correct because it examines every valid price. The problem is the size of the search space. If `p = 10^18` and `d` is also huge, we may need to inspect nearly `10^18` numbers. Even doing a single operation per number would be impossible.

The key observation is that numbers with many trailing nines are extremely structured.

For a fixed number of trailing nines `k`, the largest number not exceeding `p` is obtained by replacing the last `k` digits with `9`.

For example, if:

```
p = 543210
```

then:

- largest number with one trailing nine is `543209`
- largest number with two trailing nines is `543199`
- largest number with three trailing nines is `542999`

There is no need to inspect any smaller candidate with the same number of trailing nines, because the problem asks for the maximum price among ties.

This reduces the search space dramatically. We only need to try each possible suffix length. Since `p <= 10^18`, there are at most 19 digits, so only about 19 candidates exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d log p) | O(1) | Too slow |
| Optimal | O(log p) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the current best answer equal to `p`.

This handles the case where reducing the price is not beneficial or not allowed.
2. For every power of ten `10^k`, construct the largest number not exceeding `p` whose last `k` digits are all `9`.

We can compute it as:

```
candidate = (p // 10^k) * 10^k - 1
```

The division removes the last `k` digits, multiplying restores them as zeros, and subtracting one turns those zeros into nines.
3. Check whether the candidate is valid.

The candidate must satisfy:

```
p - candidate <= d
```

Otherwise the required discount is too large.
4. Compare the candidate against the current best answer.

Prefer the candidate if it has more trailing nines. If both have the same number of trailing nines, prefer the larger number.

In practice, iterating `k` from small to large already guarantees that later valid candidates have at least as many trailing nines.
5. Continue while `10^k <= p * 10`.

Since `p` has at most 19 digits, this loop runs only a handful of times.
6. Print the best answer.

### Why it works

For any fixed number of trailing nines `k`, every valid number with that property can be written as:

```
some_prefix * 10^k + (10^k - 1)
```

Among all such numbers not exceeding `p`, the largest one is exactly:

```
(p // 10^k) * 10^k - 1
```

If this largest candidate is not valid because it requires too large a discount, then every smaller number with the same `k` trailing nines is even farther from `p`, so none of them can work either.

That means testing only this maximal candidate for each `k` is sufficient.

Since we examine every possible count of trailing nines, and for each count we test the best possible number, the algorithm cannot miss the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def trailing_nines(x):
    cnt = 0
    while x % 10 == 9:
        cnt += 1
        x //= 10
    return cnt

def solve():
    p, d = map(int, input().split())

    ans = p
    best = trailing_nines(p)

    power = 10

    while power <= 10**19:
        candidate = (p // power) * power - 1

        if candidate >= 0 and p - candidate <= d:
            cur = trailing_nines(candidate)

            if cur > best or (cur == best and candidate > ans):
                best = cur
                ans = candidate

        power *= 10

    print(ans)

solve()
```

The helper function counts trailing nines by repeatedly checking the last digit. Since a number has at most 19 digits, this operation is effectively constant time.

The main loop iterates over powers of ten. For each power, it constructs the largest possible candidate ending with the required number of nines.

The expression:

```
(p // power) * power - 1
```

is the critical part of the solution.

Suppose:

```
p = 543210
power = 1000
```

Then:

```
p // power = 543
543 * 1000 = 543000
543000 - 1 = 542999
```

which is exactly the largest number not exceeding `p` with three trailing nines.

The condition:

```
p - candidate <= d
```

filters out candidates requiring too much discount.

The tie-breaking rule is implemented explicitly. If two candidates have the same number of trailing nines, we keep the larger one.

The loop upper bound `10**19` safely covers every possible digit length for `p <= 10^18`.

## Worked Examples

### Example 1

Input:

```
1029 102
```

| power | candidate | discount | trailing nines | valid |
| --- | --- | --- | --- | --- |
| 10 | 1019 | 10 | 1 | yes |
| 100 | 999 | 30 | 3 | yes |
| 1000 | -1 | invalid | - | no |

The best valid candidate is `999`, which has three trailing nines.

Output:

```
999
```

This trace shows the main idea of the algorithm. Instead of checking every number between `927` and `1029`, we examine only the maximal candidate for each suffix length.

### Example 2

Input:

```
10000 100
```

| power | candidate | discount | trailing nines | valid |
| --- | --- | --- | --- | --- |
| 10 | 9999 | 1 | 4 | yes |
| 100 | 9999 | 1 | 4 | yes |
| 1000 | 9999 | 1 | 4 | yes |
| 10000 | 9999 | 1 | 4 | yes |

The answer is immediately `9999`.

Output:

```
9999
```

This example demonstrates that sometimes a tiny decrease creates many trailing nines at once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log p) | We test one candidate per digit length |
| Space | O(1) | Only a few integer variables are used |

Since `p` has at most 19 digits, the loop performs only about 19 iterations. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def trailing_nines(x):
        cnt = 0
        while x % 10 == 9:
            cnt += 1
            x //= 10
        return cnt

    p, d = map(int, input().split())

    ans = p
    best = trailing_nines(p)

    power = 10

    while power <= 10**19:
        candidate = (p // power) * power - 1

        if candidate >= 0 and p - candidate <= d:
            cur = trailing_nines(candidate)

            if cur > best or (cur == best and candidate > ans):
                best = cur
                ans = candidate

        power *= 10

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run("1029 102\n") == "999", "sample 1"

# minimum case
assert run("1 0\n") == "1", "minimum values"

# already optimal
assert run("1999 0\n") == "1999", "already has maximum trailing nines"

# small decrease unlocks many nines
assert run("10000 1\n") == "9999", "single decrement creates four nines"

# tie-breaking
assert run("1999 1000\n") == "1999", "choose larger value among equal suffix counts"

# very large values
assert run("1000000000000000000 1\n") == "999999999999999999", "64-bit boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | Minimum valid input |
| `1999 0` | `1999` | Already optimal without reduction |
| `10000 1` | `9999` | Tiny discount can maximize suffix nines |
| `1999 1000` | `1999` | Correct tie-breaking |
| `1000000000000000000 1` | `999999999999999999` | Handles 64-bit values safely |

## Edge Cases

Consider the input:

```
1000 0
```

The algorithm starts with `ans = 1000`. The candidate `999` is generated when `power = 10`, but:

```
1000 - 999 = 1
```

which exceeds `d = 0`.

So the candidate is rejected and the answer remains `1000`.

Now consider:

```
10999 1
```

The initial answer already has three trailing nines.

When `power = 10`, the candidate becomes:

```
10999
```

because:

```
(10999 // 10) * 10 - 1 = 10999
```

The algorithm correctly keeps the original value.

For:

```
10000 100
```

the first candidate is:

```
9999
```

with discount `1`.

This immediately gives four trailing nines, which is optimal. Larger powers still produce `9999`, so the answer never changes.

Finally, consider the tie-breaking example:

```
1999 1000
```

Both `1999` and `999` have three trailing nines.

The algorithm starts with `ans = 1999`. Later it may generate `999`, but since both have the same suffix count and `1999 > 999`, the stored answer does not change.
