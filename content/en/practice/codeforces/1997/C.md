---
title: "CF 1997C - Even Positions"
description: "We are given a bracket sequence of even length, but every character at an odd position has been erased. Only the brackets at positions 2, 4, 6, ... remain."
date: "2026-06-08T14:34:57+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1997
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 168 (Rated for Div. 2)"
rating: 1100
weight: 1997
solve_time_s: 140
verified: true
draft: false
---

[CF 1997C - Even Positions](https://codeforces.com/problemset/problem/1997/C)

**Rating:** 1100  
**Tags:** constructive algorithms, data structures, greedy  
**Solve time:** 2m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bracket sequence of even length, but every character at an odd position has been erased. Only the brackets at positions 2, 4, 6, ... remain.

The original sequence was guaranteed to be a regular bracket sequence (RBS), and there is always at least one valid restoration. We may replace each underscore at an odd position with either `(` or `)`.

For any completed RBS, its cost is defined as the sum of distances between matching pairs of brackets. If an opening bracket at position `l` is matched with a closing bracket at position `r`, that pair contributes `r - l` to the total cost.

Among all valid restorations, we must find the minimum possible cost.

The length of a single test case can reach `2 · 10^5`, and the total length over all test cases is also at most `2 · 10^5`. Any solution that examines all restorations is impossible because there are `2^(n/2)` ways to fill the missing positions. Even an `O(n²)` algorithm would be too expensive at the upper limit. We need something linear or close to linear per test case.

A subtle part of the problem is that minimizing the cost is not the same as merely constructing any valid RBS. Different valid restorations can produce different matching structures.

Consider:

```
n = 4
_(_)
```

The restoration `(())` has cost `3 + 1 = 4`.

If we try to greedily create pairs without respecting validity, we might incorrectly think `()()` is possible, which would have cost `2`, but the fixed even positions prevent that restoration.

Another easy mistake is to compute matching pairs explicitly after constructing the sequence. That is valid, but there is a much simpler observation about the cost that leads directly to the answer.

For example:

```
_)_)_)_)
```

The only valid restoration is:

```
()()()()
```

The cost is `1 + 1 + 1 + 1 = 4`.

A reconstruction strategy that creates unnecessary nesting would increase the cost and produce the wrong answer.

## Approaches

The brute-force idea is straightforward. For every odd position, try both possible brackets, generate all restorations, keep only the regular bracket sequences, compute their costs, and take the minimum.

This works because it directly checks every feasible answer. The problem is the number of restorations. There are `n/2` erased positions, so the search space is `2^(n/2)`. With `n = 200000`, this is astronomically large.

To obtain something faster, we need to understand what the cost really measures.

Suppose an opening bracket at position `l` matches a closing bracket at position `r`. Its contribution is:

```
r - l
```

Summing over all matched pairs gives:

```
(sum of closing positions) - (sum of opening positions)
```

Every position belongs to exactly one matched pair, either as an opening bracket or as a closing bracket. Therefore, once we know which positions contain opening brackets, the cost is completely determined.

So the problem becomes:

> Construct a valid bracket sequence whose sum of opening positions is as large as possible.

Why largest? Because:

```
cost = constant - 2 * (sum of opening positions)
```

The total sum of all positions is fixed, so minimizing cost is equivalent to maximizing the sum of positions occupied by opening brackets.

Now look at the sequence from left to right.

At every odd position we choose a bracket.

If the current balance is zero, we are forced to place `(`. Placing `)` would immediately make the prefix invalid.

If the balance is positive, then placing `)` is always better than placing `(` because it keeps openings as far to the right as possible. Since odd positions are processed from left to right, using `)` whenever allowed postpones future openings to larger indices, increasing the sum of opening positions.

This yields a very simple greedy construction:

If balance is zero, put `(`.

Otherwise, put `)`.

The even positions are fixed and processed normally.

After constructing the optimal sequence, we still need the minimum cost. We can compute it without explicitly finding matching pairs.

Whenever we place an opening bracket at position `i`, add `i` to a running sum.

Whenever we place a closing bracket at position `i`, subtract `i`.

The final value is exactly:

```
(sum closing positions) - (sum opening positions)
```

which is the desired cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n/2) · n) | O(n) | Too slow |
| Optimal Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `balance = 0` and `cost = 0`.
2. Scan positions from left to right.
3. If the position is odd, the bracket is unknown.

If `balance == 0`, place `(` because any valid RBS must keep every prefix nonnegative.

Otherwise place `)` because using a closing bracket now delays future openings to larger positions, which minimizes the final cost.
4. If the position is even, use the fixed bracket from the input.
5. After determining the bracket at the current position:

If it is `(`, increase `balance` by one and subtract its position from `cost`.

If it is `)`, decrease `balance` by one and add its position to `cost`.
6. Continue until the entire string has been processed.
7. Output `cost`.

### Why it works

The key observation is that the cost equals:

```
(sum of closing positions) - (sum of opening positions)
```

The total sum of all positions is fixed, so minimizing cost is equivalent to maximizing the sum of opening positions.

Whenever the current balance is positive, both `(` and `)` keep the sequence potentially valid. Choosing `)` avoids creating an opening bracket at the current, smaller position. Any opening bracket that becomes necessary later will occur at a larger position, increasing the sum of opening positions.

When the balance is zero, `)` is impossible because it would violate the RBS prefix condition. Thus `(` is forced.

The greedy choice is locally optimal at every odd position and never reduces future feasibility. Since each opening bracket is pushed as far right as validity allows, the resulting sequence maximizes the sum of opening positions and hence minimizes the cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        balance = 0
        cost = 0

        for i in range(1, n + 1):
            if i % 2 == 1:
                if balance == 0:
                    ch = '('
                else:
                    ch = ')'
            else:
                ch = s[i - 1]

            if ch == '(':
                balance += 1
                cost -= i
            else:
                balance -= 1
                cost += i

        print(cost)

if __name__ == "__main__":
    solve()
```

The algorithm never explicitly reconstructs the full string because only the current bracket matters.

The variable `balance` stores the usual bracket-sequence balance. Odd positions are chosen greedily based on this balance.

The cost calculation uses the identity derived earlier. Every opening position contributes negatively and every closing position contributes positively. This avoids stack-based matching entirely.

One detail that is easy to get wrong is indexing. The problem uses 1-based positions, and the cost formula depends on actual position numbers. The loop runs from `1` to `n`, and the contribution uses `i` directly.

Another subtle point is that balance must be updated immediately after deciding the current bracket. Future odd positions depend on the current balance.

## Worked Examples

### Example 1

Input:

```
6
_(_)_)
```

The optimal restoration is `(())()`.

| Position | Chosen Bracket | Balance After | Cost |
| --- | --- | --- | --- |
| 1 | ( | 1 | -1 |
| 2 | ( | 2 | -3 |
| 3 | ) | 1 | 0 |
| 4 | ) | 0 | 4 |
| 5 | ( | 1 | -1 |
| 6 | ) | 0 | 5 |

Final answer:

```
5
```

This trace shows the greedy rule in action. At position 3 the balance is positive, so we choose `)` and avoid creating an opening bracket too early.

### Example 2

Input:

```
8
_)_)_)_)
```

| Position | Chosen Bracket | Balance After | Cost |
| --- | --- | --- | --- |
| 1 | ( | 1 | -1 |
| 2 | ) | 0 | 1 |
| 3 | ( | 1 | -2 |
| 4 | ) | 0 | 2 |
| 5 | ( | 1 | -3 |
| 6 | ) | 0 | 3 |
| 7 | ( | 1 | -4 |
| 8 | ) | 0 | 4 |

Final answer:

```
4
```

The balance repeatedly returns to zero, forcing every odd position to become `(`. The only valid restoration is `()()()()`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once |
| Space | O(1) | Only a few integer variables are maintained |

The total length across all test cases is at most `2 · 10^5`, so the algorithm performs about two hundred thousand iterations overall. This easily fits within the 2-second limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        ans = []

        for _ in range(t):
            n = int(input())
            s = input().strip()

            balance = 0
            cost = 0

            for i in range(1, n + 1):
                if i % 2 == 1:
                    ch = '(' if balance == 0 else ')'
                else:
                    ch = s[i - 1]

                if ch == '(':
                    balance += 1
                    cost -= i
                else:
                    balance -= 1
                    cost += i

            ans.append(str(cost))

        return "\n".join(ans)

    return solve()

# provided sample
assert run(
"""4
6
_(_)_)
2
_)
8
_)_)_)_)
8
_(_)_(_)
"""
) == "5\n1\n4\n8"

# minimum size
assert run(
"""1
2
_)
"""
) == "1"

# nested pair forced
assert run(
"""1
4
_(_)
"""
) == "4"

# alternating sequence
assert run(
"""1
8
_)_)_)_)
"""
) == "4"

# larger valid case
assert run(
"""1
8
_(_)_(_)
"""
) == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2, _)` | `1` | Smallest possible instance |
| `4, _(_)` | `4` | Forced nesting |
| `8, _)_)_)_)` | `4` | Repeated balance resets |
| `8, _(_)_(_)` | `8` | Mixed fixed brackets and greedy decisions |

## Edge Cases

### Balance becomes zero frequently

Input:

```
1
8
_)_)_)_)
```

After every even position the balance returns to zero. The algorithm is forced to place `(` at every odd position. The resulting sequence is:

```
()()()()
```

with cost `4`.

A careless strategy that always tries to place `)` first would immediately create invalid prefixes.

### Deep nesting forced by fixed positions

Input:

```
1
4
_(_)
```

Position 2 is fixed as `(` and position 4 is fixed as `)`.

The algorithm produces:

```
(())
```

The matching pairs are `(1,4)` and `(2,3)`, giving cost:

```
3 + 1 = 4
```

Trying to create `()()` is impossible because position 2 cannot be changed.

### Single pair

Input:

```
1
2
_)
```

Balance starts at zero, so position 1 must be `(`.

The sequence becomes:

```
()
```

The algorithm computes:

```
-1 + 2 = 1
```

which matches the only possible bracket pair distance. This verifies the boundary case `n = 2`.
