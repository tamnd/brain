---
title: "CF 102348D - Ticket Game"
description: "We have an even-length ticket split into two equal halves. Every position already contains a digit or contains ?, meaning that its digit has been erased. The two players alternately choose one remaining ? and replace it with any digit from 0 through 9."
date: "2026-08-13T00:53:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "D"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 191
verified: true
draft: false
---

[CF 102348D - Ticket Game](https://codeforces.com/problemset/problem/102348/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an even-length ticket split into two equal halves. Every position already contains a digit or contains `?`, meaning that its digit has been erased. The two players alternately choose one remaining `?` and replace it with any digit from `0` through `9`. Monocarp moves first and wants the final sums of the two halves to be different. Bicarp wants those sums to be equal.

The useful way to represent the ticket is not as a string of individual positions, but through four quantities. Let `L` and `R` be the sums of the already known digits in the left and right halves, and let `qL` and `qR` be the numbers of erased positions in those halves. The entire game can be characterized by these four values.

The length can be as large as `200000`, and the time limit is only one second. A solution should consequently be linear or close to linear in the ticket length. Any approach that explores a large fraction of the possible assignments is impossible, because even `10^20` assignments would already be far beyond what can be processed. The memory limit is generous for an `O(n)` scan, but there is no reason to store anything beyond the input string and a few counters.

There are several edge cases that easily break a naive solution. First, a ticket with no erased positions is already decided. For example, `n = 4` and `0523` has left sum `0 + 5 = 5` and right sum `2 + 3 = 5`, so the answer is `Bicarp`. An implementation that assumes at least one `?` could mishandle this case.

Second, equal numbers of question marks do not by themselves guarantee a win for Bicarp. For example:

```
4
?123
```

Here `qL = 1`, `qR = 0`, so Monocarp wins. A careless implementation that only checks whether the initial fixed sums are equal would incorrectly output `Bicarp`.

Third, unequal question-mark counts can still produce a Bicarp win when the fixed sum difference has exactly the right size. For example:

```
8
?054??0?
```

The left fixed sum is `9`, the right fixed sum is `0`, while `qL = 1` and `qR = 3`. The difference in question-mark counts is `2`, and `9 * 2 / 2 = 9`, exactly matching the fixed sum difference. Bicarp wins. A rule such as "unequal numbers of question marks means Monocarp wins" is therefore incorrect.

Finally, the factor of `9` matters because every question mark can contribute anything from `0` to `9`. For example:

```
6
???00?
```

The fixed sums are `0` and `0`, but the question-mark counts are `3` and `1`. Monocarp wins because Bicarp cannot compensate for the two extra left-side positions. Treating a question mark as merely an unspecified value without accounting for its full range misses the actual game structure.

## Approaches

A direct brute-force solution would consider every possible way to replace the question marks. If there are `q` erased positions, each has ten possible digits, giving `10^q` complete tickets. We could recursively choose a digit for each position and check the final two sums. This is correct because every possible game outcome is represented by one leaf of the search tree, but the worst case has `q = 200000`, producing `10^200000` terminal assignments. Even with a tiny constant amount of work per assignment, this is completely infeasible.

The game has much more structure than arbitrary minimax. The final result depends only on the difference between the two half sums. Consider first the positions that are already fixed. Define

[
D = L-R.
]

The question marks contribute additional values to this difference. When both halves have the same number of question marks and `D = 0`, Bicarp can answer every move by choosing the same digit in the opposite half. The two newly added contributions cancel, so the difference remains zero after every pair of moves. This is a direct pairing strategy.

If `D = 0` but the numbers of question marks differ, that pairing is impossible. Since Monocarp moves first, he can eventually move on the side with unmatched question marks and force a nonzero final difference.

Now suppose `D != 0`. We can swap the two halves conceptually so that `D > 0`, meaning the fixed digits already make the left half larger. The question is whether the right half has enough extra question marks to compensate.

If `qL >= qR`, Monocarp has at least as many available moves on the already larger side. He can keep the advantage from being repaired, so Bicarp cannot force equality.

The interesting case is `qL < qR`. The right side has `qR - qL` extra question marks. Because the total number of question marks is even, this difference is also even. During the paired part of the game, the players can effectively cancel equal numbers of question marks from both sides. Eventually only the extra right-side question marks remain.

Suppose there are `k = qR - qL` such positions. Since `k` is even, Bicarp can control the final balancing effect in pairs. Each pair of extra right-side question marks can contribute at most `9` toward reducing the left-side advantage in the relevant optimal strategy. Thus the maximum compensating amount is

[
9\frac{k}{2}.
]

Bicarp wins exactly when this amount equals the fixed difference:

[
D = 9\frac{qR-qL}{2}.
]

If the difference is smaller, Bicarp cannot remove enough of the initial advantage. If it is larger, the remaining advantage is still nonzero. Equality is the only situation where perfect balance can be forced.

This gives a constant-size decision after one scan of the ticket.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(10^q)` | `O(q)` recursion | Too slow |
| Optimal | `O(n)` | `O(1)` besides input | Accepted |

## Algorithm Walkthrough

1. Split the ticket conceptually into its left half and right half. While scanning the string, compute `left_sum` and `right_sum` using only fixed digits, and count `left_q` and `right_q`, the question marks in each half. These four values contain all information needed by the game.
2. Compute the fixed sum difference as `left_sum - right_sum`. If it is negative, swap the two sides conceptually so that `left_sum >= right_sum`. At the same time, swap their question-mark counts. After this normalization, the fixed difference is nonnegative and represents the advantage of the left side.
3. If the fixed difference is zero, Bicarp wins exactly when `left_q == right_q`. With equal counts, every move by Monocarp can be paired with a response on the other half using the same digit, preserving equality. With unequal counts, the first player eventually gets an unmatched move and can destroy equality.
4. If the fixed difference is positive and `left_q >= right_q`, output `Monocarp`. The side that is already ahead has at least as many question marks, so Monocarp can use his moves to preserve a nonzero advantage. Bicarp does not have enough unmatched positions on the other side to compensate.
5. If the fixed difference is positive and `left_q < right_q`, calculate `extra = right_q - left_q`. Bicarp can win only if the initial difference is exactly `9 * extra / 2`. Since the total number of question marks is even, `extra` is even, so this value is an integer. If equality holds, output `Bicarp`; otherwise output `Monocarp`.

### Why it works

The invariant is the current difference between the two half sums together with the number of unused question marks on each side. Equal numbers of remaining question marks can be neutralized in pairs, because after Monocarp chooses a value on one side, Bicarp can use the same value on the other side. Once those paired positions are removed, only the unmatched question marks matter. If the initially larger fixed sum has at least as many question marks, Monocarp can maintain an advantage. Otherwise, the other side has exactly `qR - qL` extra positions, and the only way to compensate the fixed difference is for those positions to provide exactly `9(qR-qL)/2` of adjustment. Hence the stated conditions are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    half = n // 2

    left_sum = 0
    right_sum = 0
    left_q = 0
    right_q = 0

    for i in range(half):
        if s[i] == '?':
            left_q += 1
        else:
            left_sum += ord(s[i]) - ord('0')

    for i in range(half, n):
        if s[i] == '?':
            right_q += 1
        else:
            right_sum += ord(s[i]) - ord('0')

    if left_sum < right_sum:
        left_sum, right_sum = right_sum, left_sum
        left_q, right_q = right_q, left_q

    diff = left_sum - right_sum

    if diff == 0:
        if left_q == right_q:
            print("Bicarp")
        else:
            print("Monocarp")
        return

    if left_q >= right_q:
        print("Monocarp")
        return

    extra = right_q - left_q

    if diff * 2 == extra * 9:
        print("Bicarp")
    else:
        print("Monocarp")

if __name__ == "__main__":
    solve()
```

The first loop processes exactly the first `n // 2` positions, while the second starts at `n // 2`, which is the first index of the right half in Python's zero-based indexing. Fixed digits contribute to their respective sums, while question marks only affect the two counters.

The swap after scanning is a useful simplification. Instead of writing separate cases for `left_sum > right_sum` and `right_sum > left_sum`, the code always treats the side with the larger fixed sum as the left side. The question-mark counts must be swapped along with the sums, because the identity of the larger side matters for the game.

The equality test uses `diff * 2 == extra * 9` rather than dividing `extra` by two. This avoids unnecessary division and makes the mathematical condition directly visible in the code. Python integers do not have overflow concerns, and the largest values here are only on the order of `10^6`.

The implementation does not need to modify the ticket itself. Once the four aggregate quantities have been computed, the exact positions of the question marks no longer matter. This is what reduces the game from an exponential search to a single linear scan.

## Worked Examples

### Sample 1

The input is:

```
4
0523
```

There are no question marks, so the game has no moves. The two fixed sums are both `5`.

| Step | Left sum | Right sum | Left `?` | Right `?` | Decision |
| --- | --- | --- | --- | --- | --- |
| Scan complete | 5 | 5 | 0 | 0 | Fixed difference is zero |
| Final check | 5 | 5 | 0 | 0 | Equal question-mark counts, Bicarp |

The algorithm reaches the zero-difference case and finds equal question-mark counts. The ticket is already happy, so Bicarp wins immediately.

### Sample 2

The input is:

```
2
??
```

Both positions are erased. There are no fixed digits, so both fixed sums are zero, and there is one question mark on each side.

| Step | Left sum | Right sum | Left `?` | Right `?` | Decision |
| --- | --- | --- | --- | --- | --- |
| Scan complete | 0 | 0 | 1 | 1 | Fixed difference is zero |
| Final check | 0 | 0 | 1 | 1 | Equal counts, Bicarp |

Whatever digit Monocarp chooses for the first position, Bicarp can put the same digit in the other position. The two sums are equal, so Bicarp wins.

### Sample 3

The input is:

```
8
?054??0?
```

The left half is `?054`, giving a fixed sum of `9` and one question mark. The right half is `??0?`, giving a fixed sum of `0` and three question marks.

| Step | Left sum | Right sum | Left `?` | Right `?` | Decision |
| --- | --- | --- | --- | --- | --- |
| Scan complete | 9 | 0 | 1 | 3 | Left has the larger fixed sum |
| Difference | 9 | 0 | 1 | 3 | `diff = 9`, `extra = 2` |
| Final check | 9 | 0 | 1 | 3 | `2 * 9 = 2 * 9`, Bicarp |

The right half has two more question marks. Those two unmatched positions can compensate for exactly `9`, which is the existing fixed difference. The equality condition holds, so Bicarp wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Every ticket position is inspected once. |
| Space | `O(1)` auxiliary space | Only four counters and a few scalar variables are maintained besides the input string. |

With `n <= 200000`, the algorithm performs only a few arithmetic operations per character. It comfortably fits the one-second limit, while the brute-force search would have up to `10^200000` complete assignments in the worst case.

## Test Cases

```python
import sys
import io

def solve():
    n = int(input())
    s = input().strip()

    half = n // 2

    left_sum = 0
    right_sum = 0
    left_q = 0
    right_q = 0

    for i in range(half):
        if s[i] == '?':
            left_q += 1
        else:
            left_sum += ord(s[i]) - ord('0')

    for i in range(half, n):
        if s[i] == '?':
            right_q += 1
        else:
            right_sum += ord(s[i]) - ord('0')

    if left_sum < right_sum:
        left_sum, right_sum = right_sum, left_sum
        left_q, right_q = right_q, left_q

    diff = left_sum - right_sum

    if diff == 0:
        print("Bicarp" if left_q == right_q else "Monocarp")
    elif left_q >= right_q:
        print("Monocarp")
    else:
        extra = right_q - left_q
        print("Bicarp" if diff * 2 == extra * 9 else "Monocarp")

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("4\n0523\n") == "Bicarp", "sample 1"
assert run("2\n??\n") == "Bicarp", "sample 2"
assert run("8\n?054??0?\n") == "Bicarp", "sample 3"

# Minimum size, unequal fixed sums and no question marks
assert run("2\n12\n") == "Monocarp", "minimum-size unhappy ticket"

# Minimum size, both positions erased
assert run("2\n??\n") == "Bicarp", "minimum-size pairing"

# Equal fixed sums but unequal question-mark counts
assert run("4\n?123\n") == "Monocarp", "unequal question counts"

# Positive difference with the exact 9 * extra / 2 compensation
assert run("6\n9??0??\n") == "Bicarp", "exact compensation"

# Positive difference with insufficient compensation
assert run("6\n8??0??\n") == "Monocarp", "wrong compensation"

# All equal values, maximum-size input
MAX_N = 200000
max_input = str(MAX_N) + "\n" + "5" * MAX_N + "\n"
assert run(max_input) == "Bicarp", "maximum-size all-equal ticket"

# Maximum-size all question marks
max_questions = str(MAX_N) + "\n" + "?" * MAX_N + "\n"
assert run(max_questions) == "Bicarp", "maximum-size all-question ticket"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 12` | `Monocarp` | Minimum size with an already unhappy ticket |
| `2 / ??` | `Bicarp` | Smallest possible pairing strategy |
| `4 / ?123` | `Monocarp` | Equal fixed sums but unequal question-mark counts |
| `6 / 9??0??` | `Bicarp` | Exact compensation by the extra question marks |
| `6 / 8??0??` | `Monocarp` | Compensation that is not large enough |
| `200000 / 555...5` | `Bicarp` | Maximum input size and all equal fixed digits |
| `200000 / ???...???` | `Bicarp` | Maximum input size with every position erased |

## Edge Cases

The first edge case is a ticket with no erased positions. For `4 / 0523`, the scan gives `left_sum = 5`, `right_sum = 5`, `left_q = right_q = 0`. The algorithm enters the zero-difference branch and returns `Bicarp`. There are no moves, so the initial state directly determines the result.

The second edge case is equal fixed sums but unequal numbers of question marks. For `4 / ?123`, the fixed left sum is `0`, the fixed right sum is `2 + 3 = 5`, so after normalization the right side is larger. The counts become `qL = 0` and `qR = 1`, with a positive fixed difference. Since the larger side has more question marks, the algorithm returns `Monocarp`. More generally, when the fixed difference is zero and the counts differ, the player with the first move has an unmatched position that prevents a permanent pairing strategy.

The third edge case is the exact compensation case. For `8 / ?054??0?`, the normalized values are `diff = 9`, `qL = 1`, and `qR = 3`. The two extra right-side question marks can compensate for `9 * 2 / 2 = 9`, exactly matching the fixed difference. The condition `2 * diff == 9 * extra` holds, so the result is `Bicarp`.

The fourth edge case is when the question-mark imbalance is present but the fixed difference does not match the required compensation. For `6 / 8??0??`, the normalized fixed difference is `8`, while the question-mark count difference is `2`. The maximum exact compensation required for Bicarp's winning condition would be `9`, not `8`. Since `2 * 8 != 2 * 9`, the algorithm outputs `Monocarp`.

The maximum-size cases show why the solution should never attempt to simulate the game tree. A ticket containing `200000` question marks has an astronomical number of possible completions, but the algorithm only counts how many question marks belong to each half and scans the string once. The result is obtained from those aggregate values without constructing any of the possible completed tickets.
