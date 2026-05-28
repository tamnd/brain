---
title: "CF 63C - Bulls and Cows"
description: "We are playing the classic Bulls and Cows game with four-digit numbers whose digits are all distinct. Leading zeroes are allowed, so 0123 is valid, but repeated digits such as 0012 or 1223 are not. Each previous guess comes with two values."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 63
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 59 (Div. 2)"
rating: 1700
weight: 63
solve_time_s: 108
verified: true
draft: false
---

[CF 63C - Bulls and Cows](https://codeforces.com/problemset/problem/63/C)

**Rating:** 1700  
**Tags:** brute force, implementation  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are playing the classic Bulls and Cows game with four-digit numbers whose digits are all distinct. Leading zeroes are allowed, so `0123` is valid, but repeated digits such as `0012` or `1223` are not.

Each previous guess comes with two values. A bull means a digit matches both in value and position. A cow means the digit exists in the hidden number but appears in a different position.

The task is not to simulate the game itself. We must determine whether the previous answers uniquely determine the hidden number.

There are three possible outcomes.

If exactly one valid number satisfies all guesses, we print that number.

If no valid number satisfies the guesses, the replies contradict each other and we print `Incorrect data`.

If multiple valid numbers remain possible, we print `Need more data`.

The constraints are very small. There are at most 10 guesses. A four-digit number with distinct digits can be formed in:

$$10 \times 9 \times 8 \times 7 = 5040$$

ways.

That immediately changes the nature of the problem. We do not need clever pruning, dynamic programming, or search trees. Even comparing every candidate against every guess is tiny:

$$5040 \times 10 = 50400$$

comparisons.

Each comparison only checks four positions and at most a few digit matches. This comfortably fits within the time limit.

The main difficulty is not performance, but correctness. Bulls and cows are easy to mix up if implemented carelessly.

One subtle edge case is handling leading zeroes correctly.

Consider:

```
1
0123 4 0
```

The correct answer is:

```
0123
```

A careless implementation that converts everything to integers and later back to strings may accidentally turn `0123` into `123`, losing the leading zero.

Another easy mistake is counting cows incorrectly by double-counting bulls.

Suppose the hidden number is `0123` and the guess is `0124`.

The correct result is `3 bulls 0 cows`.

If we first count common digits and then separately count bulls without subtracting them, we might incorrectly report one cow for digit `0`, `1`, or `2`.

Contradictory data is another important case.

```
2
0123 4 0
0123 0 4
```

No number can satisfy both statements simultaneously. The correct output is:

```
Incorrect data
```

An implementation that stops after finding the first valid candidate would incorrectly print `0123`.

The final important case is ambiguity.

```
1
0123 0 0
```

This only tells us the hidden number contains none of `0,1,2,3`. Many valid numbers remain. The correct output is:

```
Need more data
```

The program must count all valid candidates, not just check whether one exists.

## Approaches

The most direct solution is brute force.

We generate every valid four-digit number with distinct digits, including numbers with leading zeroes. For each candidate, we compare it against every previous guess. If all bulls and cows counts match exactly, the candidate remains possible.

This works because the search space is tiny. There are only 5040 candidates.

To compare two numbers, we count bulls by checking equal positions. Then we count how many digits appear in both numbers. Since digits are distinct, the number of cows becomes:

$$\text{common digits} - \text{bulls}$$

The brute-force solution is already fast enough. There is no hidden larger constraint requiring optimization beyond this.

The real insight is recognizing that the problem size is fundamentally bounded by the structure of the game itself. Four distinct digits from ten possibilities create a fixed universe of only 5040 states. Once we realize that, exhaustive checking becomes the cleanest and safest solution.

A more complicated approach would only add implementation risk without improving runtime meaningfully.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all 5040 candidates | O(5040 × n) | O(1) | Accepted |
| Optimized pruning/search | Unnecessary | Higher | Accepted but overcomplicated |

## Algorithm Walkthrough

1. Read all guesses along with their expected bulls and cows counts.
2. Generate every four-digit number whose digits are all distinct.

We generate numbers as strings instead of integers so leading zeroes are preserved naturally.
3. For each candidate number, compare it against every guess.
4. To compare two numbers:

Count bulls by checking positions `0..3`.

Count common digits by checking how many digits from the candidate appear in the guess.

Since all digits are distinct, cows equal:

$$\text{common digits} - \text{bulls}$$
5. If the computed bulls and cows do not match the expected values for even one guess, reject the candidate immediately.

Early rejection avoids unnecessary work, although performance is already easily sufficient.
6. Collect every candidate that satisfies all guesses.
7. After checking all candidates:

If no candidate remains, print `Incorrect data`.

If exactly one candidate remains, print it.

Otherwise print `Need more data`.

### Why it works

The algorithm checks every possible valid hidden number exactly once. A candidate survives only if it reproduces every recorded response perfectly.

Since the hidden number must belong to the set of all valid four-digit distinct-digit numbers, exhaustive enumeration guarantees that:

If a valid solution exists, we will find it.

If multiple solutions exist, all of them will be counted.

If none exist, the data is contradictory.

No candidate is skipped, and no invalid candidate can survive the consistency checks.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def score(secret, guess):
    bulls = 0

    for i in range(4):
        if secret[i] == guess[i]:
            bulls += 1

    common = 0

    for ch in secret:
        if ch in guess:
            common += 1

    cows = common - bulls

    return bulls, cows

def solve():
    n = int(input())

    guesses = []

    for _ in range(n):
        s, b, c = input().split()
        guesses.append((s, int(b), int(c)))

    valid = []

    for p in permutations("0123456789", 4):
        candidate = "".join(p)

        ok = True

        for g, b, c in guesses:
            cb, cc = score(candidate, g)

            if cb != b or cc != c:
                ok = False
                break

        if ok:
            valid.append(candidate)

    if len(valid) == 0:
        print("Incorrect data")
    elif len(valid) == 1:
        print(valid[0])
    else:
        print("Need more data")

solve()
```

The `score` function implements the exact Bulls and Cows rules. Bulls are counted position by position. Common digits are counted separately, and cows are obtained by subtracting bulls.

Using strings instead of integers avoids every leading-zero issue automatically. The candidate `"0123"` stays exactly four characters long throughout the program.

`itertools.permutations` is perfect here because it already guarantees distinct digits. Every generated tuple contains four different characters chosen from `"0123456789"`.

The main loop checks every candidate against every guess. The moment one guess disagrees, the candidate is discarded immediately.

The final decision depends only on how many valid candidates remain.

One subtle implementation detail is that cows are not counted independently. Since digits are unique, every shared digit is either a bull or a cow, never both. Subtracting bulls from total shared digits avoids accidental double counting.

## Worked Examples

### Example 1

Input:

```
2
1263 1 2
8103 2 1
```

We test candidates one by one.

Suppose we evaluate candidate `0123`.

| Candidate | Guess | Bulls | Common Digits | Cows | Expected | Valid So Far |
| --- | --- | --- | --- | --- | --- | --- |
| 0123 | 1263 | 1 | 3 | 2 | 1 bull 2 cows | Yes |
| 0123 | 8103 | 2 | 3 | 1 | 2 bulls 1 cow | Yes |

`0123` survives.

Now suppose another candidate such as `0132`.

| Candidate | Guess | Bulls | Common Digits | Cows | Expected | Valid So Far |
| --- | --- | --- | --- | --- | --- | --- |
| 0132 | 1263 | 0 | 3 | 3 | 1 bull 2 cows | No |

It gets rejected immediately.

After checking all 5040 candidates, multiple valid numbers remain, so the output is:

```
Need more data
```

This example demonstrates that satisfying all guesses does not necessarily determine a unique answer.

### Example 2

Input:

```
2
0123 4 0
0123 0 4
```

Check candidate `0123`.

| Candidate | Guess | Bulls | Common Digits | Cows | Expected | Valid So Far |
| --- | --- | --- | --- | --- | --- | --- |
| 0123 | 0123 | 4 | 4 | 0 | 4 bulls 0 cows | Yes |
| 0123 | 0123 | 4 | 4 | 0 | 0 bulls 4 cows | No |

The candidate fails.

Every other candidate already fails the first guess.

No valid candidate survives.

Output:

```
Incorrect data
```

This example shows how contradictory replies eliminate the entire search space.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(5040 × n) | We test every valid candidate against all guesses |
| Space | O(1) | Aside from storing guesses and valid candidates |

The maximum number of candidates is fixed at 5040, and `n ≤ 10`. Even in the worst case, the number of comparisons is tiny. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def score(secret, guess):
        bulls = 0

        for i in range(4):
            if secret[i] == guess[i]:
                bulls += 1

        common = 0

        for ch in secret:
            if ch in guess:
                common += 1

        cows = common - bulls

        return bulls, cows

    n = int(input())

    guesses = []

    for _ in range(n):
        s, b, c = input().split()
        guesses.append((s, int(b), int(c)))

    valid = []

    for p in permutations("0123456789", 4):
        candidate = "".join(p)

        ok = True

        for g, b, c in guesses:
            cb, cc = score(candidate, g)

            if cb != b or cc != c:
                ok = False
                break

        if ok:
            valid.append(candidate)

    if len(valid) == 0:
        return "Incorrect data"
    elif len(valid) == 1:
        return valid[0]
    else:
        return "Need more data"

# provided sample
assert run(
"""2
1263 1 2
8103 2 1
"""
) == "Need more data", "sample 1"

# unique solution with leading zero
assert run(
"""1
0123 4 0
"""
) == "0123", "leading zero handling"

# contradictory data
assert run(
"""2
0123 4 0
0123 0 4
"""
) == "Incorrect data", "contradictory guesses"

# very weak information
assert run(
"""1
0123 0 0
"""
) == "Need more data", "multiple candidates remain"

# exact full permutation clue
assert run(
"""1
0123 0 4
"""
) == "Need more data", "all digits correct but positions unknown"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0123 4 0` | `0123` | Preserves leading zeroes |
| Contradictory identical guesses | `Incorrect data` | Detects impossible data |
| `0123 0 0` | `Need more data` | Handles many remaining candidates |
| `0123 0 4` | `Need more data` | Correct bull/cow counting |

## Edge Cases

Consider the leading zero case:

```
1
0123 4 0
```

The algorithm generates candidates as strings, so `"0123"` remains exactly four characters long.

When this candidate is checked:

| Position | Candidate | Guess | Match |
| --- | --- | --- | --- |
| 0 | 0 | 0 | Bull |
| 1 | 1 | 1 | Bull |
| 2 | 2 | 2 | Bull |
| 3 | 3 | 3 | Bull |

The result is `4 bulls 0 cows`, so the candidate survives. Every other candidate fails. The output becomes:

```
0123
```

Now consider contradictory information:

```
2
0123 4 0
0123 0 4
```

The first guess forces the hidden number to be exactly `0123`.

The second guess says all digits are correct but all positions are wrong, which is impossible for the same number.

During enumeration, every candidate fails at least one constraint. The valid candidate list stays empty, and the algorithm prints:

```
Incorrect data
```

Finally, consider ambiguity:

```
1
0123 0 0
```

Any valid number using only digits from `{4,5,6,7,8,9}` satisfies this condition.

For example, `4567` gives:

| Candidate | Common Digits | Bulls | Cows |
| --- | --- | --- | --- |
| 4567 | 0 | 0 | 0 |

Many candidates survive, so the algorithm correctly outputs:

```
Need more data
```
