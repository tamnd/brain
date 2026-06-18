---
title: "CF 106511B - Six Seven"
description: "We are given several test cases, and each test case is a string made only of the characters 6 and 7. The task is to count how many pairs of positions we can pick such that the first position contains a 6, the second position contains a 7, and the 7 appears strictly to the right…"
date: "2026-06-18T19:06:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106511
codeforces_index: "B"
codeforces_contest_name: "Columbia University Local Contest (CULC) Spring 2026"
rating: 0
weight: 106511
solve_time_s: 51
verified: true
draft: false
---

[CF 106511B - Six Seven](https://codeforces.com/problemset/problem/106511/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, and each test case is a string made only of the characters `6` and `7`. The task is to count how many pairs of positions we can pick such that the first position contains a `6`, the second position contains a `7`, and the `7` appears strictly to the right of the chosen `6`.

In other words, we are counting ordered pairs of indices $(i, j)$ where $i < j$, the character at $i$ is `6`, and the character at $j$ is `7`. Each test case is independent, and we output the count for each string.

The input size allows up to $10^4$ test cases, and the total length of all strings combined is at most $2 \cdot 10^5$. This is the key constraint: although there may be many test cases, the total work across all of them must stay linear in the total string length. Anything that processes each test case in more than linear time in its length will be too slow.

A naive double loop over all pairs of positions inside each string would examine up to $n^2$ pairs per test case. If a single string has length $2 \cdot 10^5$, that alone is already around $4 \cdot 10^{10}$ operations, which is far beyond what a 2-second limit can handle. So we need a method that processes each string in $O(n)$ time.

There are a few edge cases where careless logic breaks.

If the string contains only `7`s, for example `777`, there is no `6` to pair with, so the answer must be zero. A buggy approach that assumes at least one `6` or starts counting from the first character might incorrectly add values.

If the string contains only `6`s, for example `6666`, there is still no valid `7`, so the answer is again zero. A mistake here often comes from trying to count combinations of positions without checking the second character type.

If the string alternates like `6767`, we must ensure we only count valid forward pairs. The correct answer here is 3, coming from one `6` at position 1 pairing with both later `7`s and the second `6` pairing with the last `7`.

## Approaches

The brute-force method is straightforward: for every position that contains `6`, scan all later positions and count how many are `7`. This is correct because it directly follows the definition of valid pairs. However, its runtime is quadratic in the worst case, since for a string of length $n$, each of the $n$ positions may scan up to $n$ future positions. With total input size reaching $2 \cdot 10^5$, this approach would attempt on the order of $10^{10}$ operations, which is not feasible.

The key observation is that for each `6`, what matters is only how many `7`s appear after it, not their positions individually. Instead of scanning forward repeatedly, we can maintain a running count of how many `7`s remain to the right of the current position. If we know that value at each `6`, we can add it directly to the answer.

A cleaner way to think about it is to reverse the direction of counting. If we traverse the string from right to left, we maintain how many `7`s we have seen so far. When we encounter a `6`, every previously seen `7` forms a valid pair with it. This converts the nested loop structure into a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all pairs) | O(n²) per test case | O(1) | Too slow |
| Single pass with suffix counting | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

We process each string independently.

1. Initialize a counter `sevens = 0` to track how many `7` characters we have seen so far while scanning from right to left. This represents how many valid partners exist for any `6` we encounter later.
2. Initialize `answer = 0`.
3. Iterate over the string from the last character to the first character.

When we see a `7`, we increment `sevens`. This is because any `6` appearing earlier can pair with this `7`.

When we see a `6`, we add `sevens` to `answer`. This works because every `7` we have already seen lies to the right of this `6`, forming a valid pair.
4. After processing the full string, output `answer`.

The direction of traversal is what makes the logic consistent: at the moment we process a `6`, the variable `sevens` already represents exactly the number of valid future positions.

### Why it works

The algorithm relies on the invariant that at any position during the right-to-left scan, `sevens` equals the number of `7`s strictly to the right of the current index. When we process a `6` at index `i`, every `7` counted in `sevens` forms a unique pair $(i, j)$ with $j > i$. Since each pair is counted exactly once at the moment its left endpoint is processed, the final sum equals the number of valid pairs in the string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        sevens = 0
        ans = 0

        for ch in reversed(s):
            if ch == '7':
                sevens += 1
            else:  # ch == '6'
                ans += sevens

        print(ans)

if __name__ == "__main__":
    solve()
```

The code mirrors the right-to-left reasoning directly. The reversal is important because it avoids having to precompute suffix arrays explicitly, and it ensures that when we reach a `6`, all relevant `7`s have already been counted.

A subtle implementation detail is stripping the input string. Without `.strip()`, the newline character could be mistakenly processed as an extra character, leading to incorrect counting logic in some environments.

## Worked Examples

### Example 1: `767`

We scan from right to left.

| Position | Char | sevens | ans |
| --- | --- | --- | --- |
| 2 | 7 | 1 | 0 |
| 1 | 6 | 1 | 1 |
| 0 | 7 | 2 | 1 |

The final answer is 1, corresponding to the pair `(6 at index 1, 7 at index 2)`.

This trace shows that each `6` contributes exactly the number of `7`s to its right, and no pair is double counted.

### Example 2: `6767`

| Position | Char | sevens | ans |
| --- | --- | --- | --- |
| 3 | 7 | 1 | 0 |
| 2 | 6 | 1 | 1 |
| 1 | 7 | 2 | 1 |
| 0 | 6 | 2 | 3 |

The final answer is 3. This confirms that multiple `7`s accumulate correctly and that earlier `6`s benefit from all later `7`s.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is processed exactly once in a single scan |
| Space | O(1) | Only two counters are maintained regardless of input size |

The total input length is bounded by $2 \cdot 10^5$, so the overall work remains linear across all test cases and comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    for _ in range(t):
        s = input().strip()
        sevens = 0
        ans = 0
        for ch in reversed(s):
            if ch == '7':
                sevens += 1
            else:
                ans += sevens
        print(ans)

    return output.getvalue().strip()

# provided samples
assert run("4\n767\n677\n6767\n777\n") == "1\n2\n3\n0"

# custom cases
assert run("1\n6\n") == "0", "single 6"
assert run("1\n7\n") == "0", "single 7"
assert run("1\n66666\n") == "0", "all sixes"
assert run("1\n77777\n") == "0", "all sevens"
assert run("1\n667777\n") == "8", "all pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6` | `0` | minimal input, no valid pair |
| `7` | `0` | minimal input, no left endpoint |
| `66666` | `0` | all same character (no matches) |
| `77777` | `0` | all same character (no matches) |
| `667777` | `8` | full cross pairing correctness |

## Edge Cases

A string consisting only of `6`s, such as `66666`, triggers the case where every character is a potential left endpoint but there are no right endpoints. During the right-to-left scan, `sevens` remains zero throughout, so every `6` adds zero to the answer, producing the correct result of zero.

A string consisting only of `7`s, such as `777`, tests the opposite situation. The algorithm increments `sevens` for every character, but never encounters a `6`, so nothing is ever added to the answer. The result correctly stays zero.

A mixed but unbalanced string like `666777` demonstrates accumulation. When scanning from the right, the first three steps build `sevens = 3`, and each `6` adds 3 to the answer. This ensures that all cross-boundary pairs are counted exactly once, confirming that the invariant about “number of 7s to the right” is sufficient to describe all valid pairs.
