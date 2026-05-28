---
title: "CF 45I - TCMCF+++"
description: "We are given a list of integers representing problem scores in a contest. A contestant may solve any non-empty subset of these problems, and the final score becomes the product of all chosen values."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 45
codeforces_index: "I"
codeforces_contest_name: "School Team Contest 3 (Winter Computer School 2010/11)"
rating: 1400
weight: 45
solve_time_s: 138
verified: false
draft: false
---

[CF 45I - TCMCF+++](https://codeforces.com/problemset/problem/45/I)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integers representing problem scores in a contest. A contestant may solve any non-empty subset of these problems, and the final score becomes the product of all chosen values.

The task is not to compute the maximum product itself, but to output one subset whose product is as large as possible.

The constraints are very small. There are at most 100 numbers, each between -100 and 100. Even though the limits are tiny, the number of subsets is still exponential. A brute-force search would require checking all $2^n - 1$ non-empty subsets. With $n = 100$, that is completely impossible.

The tricky part of the problem is handling negative numbers and zeros correctly. Positive values always help because multiplying by a positive number greater than zero increases the product. Negative values are more subtle. An even number of negatives produces a positive product, while an odd number produces a negative one.

Several edge cases easily break careless solutions.

Suppose all numbers are negative and their count is odd.

Input:

```
3
-1 -2 -3
```

Choosing all numbers gives $(-1) \cdot (-2) \cdot (-3) = -6$.

But choosing only `-2 -3` gives `6`, which is larger.

The correct answer removes the negative number with the smallest absolute value, here `-1`.

Now consider a case with only one negative number and zeros.

Input:

```
4
-5 0 0 0
```

Choosing `-5` gives `-5`.

Choosing any single zero gives `0`, which is larger.

A greedy approach that always keeps non-zero values would fail here.

Another dangerous situation is when every value is zero.

Input:

```
3
0 0 0
```

We still must output at least one number.

The best possible product is `0`, so printing a single zero is correct.

The smallest valid input also matters.

Input:

```
1
-7
```

We are forced to take the only number available, even though the product is negative.

## Approaches

The brute-force solution is straightforward. We iterate over every non-empty subset, compute its product, and keep the subset with the largest result.

This works because the definition of the score directly depends on subsets. Every candidate can be evaluated independently.

The problem is the number of subsets. With $n = 100$, the total becomes roughly $1.27 \times 10^{30}$. Even checking a billion subsets per second would not finish within the lifetime of the universe.

The key observation is that multiplication behaves very predictably with signs.

Positive numbers are always useful. Multiplying by a positive number greater than 1 increases the product. Multiplying by 1 keeps the product unchanged, but still never hurts.

Negative numbers are useful only in pairs. Two negatives create a positive contribution. If the number of negatives is odd, exactly one negative must be discarded. To lose as little magnitude as possible, we should discard the negative closest to zero.

Zeros never improve a positive product. Their only purpose is rescuing situations where every achievable non-zero product would be negative.

This turns the problem into a simple greedy selection process.

We keep:

1. Every positive number.
2. Every negative number except possibly one.
3. If negatives are odd, remove the negative with minimum absolute value.
4. If nothing remains, output a single zero if available, otherwise output the only negative number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all numbers and separate them into positives, negatives, and zeros.

This makes later decisions much simpler because each category behaves differently under multiplication.
2. Add every positive number to the answer.

Any positive value helps or at least does not reduce the product.
3. Sort the negative numbers by absolute value.

The negative closest to zero is the least useful one when we need to discard a negative.
4. If the number of negatives is even, add all negatives to the answer.

Their product becomes positive.
5. If the number of negatives is odd, discard exactly one negative, specifically the one with the smallest absolute value, and add the rest.

Removing any other negative would reduce the final magnitude more severely.
6. If the answer is still empty, handle special cases.

If zeros exist, output one zero because $0$ is larger than any negative product.

Otherwise, there is exactly one negative number in the entire array, so output it.
7. Print the selected numbers.

### Why it works

The algorithm maximizes the sign first, then the magnitude.

A positive product is always better than zero, and zero is always better than a negative product. Among positive products, larger absolute value is better.

All positive numbers should be included because multiplying by them never decreases the product. Negative numbers contribute positively only in pairs, so an odd count forces one removal. Removing the negative closest to zero preserves the largest possible absolute value for the remaining product.

If no positive product can be formed, choosing zero is optimal whenever available. Only when the array contains a single negative and no zeros are we forced to output a negative value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    positives = []
    negatives = []
    zeros = []

    for x in a:
        if x > 0:
            positives.append(x)
        elif x < 0:
            negatives.append(x)
        else:
            zeros.append(x)

    negatives.sort(key=abs)

    ans = []

    ans.extend(positives)

    if len(negatives) % 2 == 0:
        ans.extend(negatives)
    else:
        ans.extend(negatives[1:])

    if not ans:
        if zeros:
            ans.append(0)
        else:
            ans.append(negatives[0])

    print(*ans)

solve()
```

The solution begins by dividing numbers into three groups because positives, negatives, and zeros require different handling strategies.

The negatives are sorted by absolute value instead of numerical value. This detail matters. We want to remove the negative closest to zero, not the smallest numerical value. For example, between `-100` and `-1`, removing `-1` is much better.

The line:

```
ans.extend(negatives[1:])
```

works because the negatives are sorted by absolute value. The first element is the least useful negative, so skipping it leaves the optimal even-sized set.

The final special-case block is essential. Without it, inputs like:

```
3
0 0 0
```

would produce an empty output, which is invalid because at least one problem must be solved.

Python integers automatically handle large products, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
5
1 2 -3 3 3
```

| Step | Positives | Negatives | Zeros | Answer |
| --- | --- | --- | --- | --- |
| Initial split | `[1,2,3,3]` | `[-3]` | `[]` | `[]` |
| Add positives | `[1,2,3,3]` | `[-3]` | `[]` | `[1,2,3,3]` |
| Odd negatives, discard `-3` | `[1,2,3,3]` | `[-3]` | `[]` | `[1,2,3,3]` |

Output:

```
1 2 3 3
```

The trace shows that a lone negative is harmful because it flips the entire product to negative.

### Example 2

Input:

```
4
-5 0 0 0
```

| Step | Positives | Negatives | Zeros | Answer |
| --- | --- | --- | --- | --- |
| Initial split | `[]` | `[-5]` | `[0,0,0]` | `[]` |
| Odd negatives, discard `-5` | `[]` | `[-5]` | `[0,0,0]` | `[]` |
| Empty answer, choose zero | `[]` | `[-5]` | `[0,0,0]` | `[0]` |

Output:

```
0
```

This example demonstrates why zeros matter. A product of zero is better than a negative product.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the negative numbers dominates |
| Space | $O(n)$ | The answer and category arrays store input values |

With $n \le 100$, this solution is easily fast enough. Even an $O(n^2)$ solution would pass comfortably, so the logarithmic sorting cost is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    positives = []
    negatives = []
    zeros = []

    for x in a:
        if x > 0:
            positives.append(x)
        elif x < 0:
            negatives.append(x)
        else:
            zeros.append(x)

    negatives.sort(key=abs)

    ans = []

    ans.extend(positives)

    if len(negatives) % 2 == 0:
        ans.extend(negatives)
    else:
        ans.extend(negatives[1:])

    if not ans:
        if zeros:
            ans.append(0)
        else:
            ans.append(negatives[0])

    print(*ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
res = run("5\n1 2 -3 3 3\n")
assert set(map(int, res.split())) == {1, 2, 3}

# minimum size
assert run("1\n-7\n") == "-7", "single negative"

# all zeros
assert run("3\n0 0 0\n") == "0", "all zeros"

# odd number of negatives
res = run("3\n-1 -2 -3\n")
vals = sorted(map(int, res.split()))
assert vals == [-3, -2], "remove smallest abs negative"

# even number of negatives
res = run("4\n-1 -2 -3 -4\n")
vals = sorted(map(int, res.split()))
assert vals == [-4, -3, -2, -1], "keep all negatives"

# positives and zeros
res = run("5\n0 1 2 0 3\n")
vals = sorted(map(int, res.split()))
assert vals == [1, 2, 3], "ignore zeros"

# large boundary style case
arr = " ".join(["-1"] * 99 + ["2"])
res = run(f"100\n{arr}\n")
vals = list(map(int, res.split()))
assert len(vals) == 99, "discard one negative from odd count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / -7` | `-7` | Minimum-size input |
| `0 0 0` | `0` | Empty-answer handling |
| `-1 -2 -3` | `-2 -3` | Odd negatives require one removal |
| `-1 -2 -3 -4` | all four negatives | Even negatives should all remain |
| `0 1 2 0 3` | `1 2 3` | Zeros should be ignored when positives exist |
| 99 negatives and one positive | 99 chosen values | Large boundary behavior |

## Edge Cases

Consider the input:

```
3
-1 -2 -3
```

The negatives sorted by absolute value become:

```
[-1, -2, -3]
```

There are three negatives, so the count is odd. The algorithm removes `-1` because its absolute value is smallest. The remaining product becomes:

```
(-2) * (-3) = 6
```

Any other removal produces a smaller product.

Now consider:

```
4
-5 0 0 0
```

The algorithm initially removes `-5` because it is the only negative and the count is odd. The answer becomes empty. Since zeros exist, the algorithm outputs `0`.

This is correct because:

```
0 > -5
```

Finally, examine the all-zero case:

```
3
0 0 0
```

No positives or negatives are selected. The answer remains empty until the special-case handling appends a single zero.

Without this step, the program would incorrectly print nothing, violating the requirement that at least one problem must be chosen.
