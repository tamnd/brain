---
title: "CF 180C - Letter"
description: "We are given a string containing uppercase and lowercase English letters. We want to transform it into a \"fancy\" string where every uppercase letter appears before every lowercase letter."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 1400
weight: 180
solve_time_s: 106
verified: true
draft: false
---

[CF 180C - Letter](https://codeforces.com/problemset/problem/180/C)

**Rating:** 1400  
**Tags:** dp  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string containing uppercase and lowercase English letters. We want to transform it into a "fancy" string where every uppercase letter appears before every lowercase letter.

Another way to describe the target form is this: there exists some split position such that every character on the left side is uppercase and every character on the right side is lowercase. Either side may be empty. That means strings like `"ABCdef"`, `"abcdef"`, and `"XYZ"` are all valid.

A single operation changes the case of one character. We need the minimum number of operations required.

The string length can be as large as $10^5$. That immediately rules out quadratic algorithms. Even an $O(n^2)$ scan over all substrings would perform around $10^{10}$ operations in the worst case, which is far beyond the time limit. We need a linear or near-linear solution.

The tricky part is that the optimal split position is not obvious. A greedy strategy that fixes characters locally can fail because changing one character may shift the best partition point.

Consider this example:

```
aA
```

The correct answer is `1`.

We can either:

- change `'a'` to uppercase, producing `"AA"`
- change `'A'` to lowercase, producing `"aa"`

A careless approach that only checks for adjacent violations might incorrectly think two changes are needed because lowercase appears before uppercase.

Another easy mistake is forgetting that one side may be empty.

Example:

```
abc
```

The answer is `0`.

The whole string is already valid because we may choose the uppercase section to have length zero.

The symmetric case also matters:

```
ABC
```

The answer is again `0`.

A solution that forces both sections to contain at least one character would incorrectly return `1`.

Repeated alternation is another useful stress case:

```
aAaAaA
```

The optimal answer is `3`, not `5`.

The best strategy is to choose a split and consistently convert one side to uppercase and the other side to lowercase. Local fixes without a global partition perspective usually overcount.

## Approaches

The brute-force idea is straightforward. We try every possible split position.

Suppose the split is after index `i`. Then:

- every character before or at `i` must become uppercase
- every character after `i` must become lowercase

For each split, we count:

- lowercase letters in the left part, since they must be converted
- uppercase letters in the right part, since they must be converted

The minimum over all splits is the answer.

This brute-force approach is correct because every valid final string corresponds to exactly one partition between uppercase and lowercase sections.

The problem is efficiency. If we recompute the counts from scratch for every split, we spend $O(n)$ work per split and there are $O(n)$ splits. That gives $O(n^2)$ time.

With $n = 10^5$, this becomes roughly $10^{10}$ character checks in the worst case, which is too slow.

The key observation is that adjacent split positions differ by only one character.

Suppose we move the split from left to right by one position. Only one character changes sides:

- it stops belonging to the lowercase-required suffix
- it starts belonging to the uppercase-required prefix

That means we can maintain the answer incrementally in linear time.

We precompute how many uppercase letters remain on the right side. Then as we scan left to right:

- if the current character is lowercase, the cost of the left side increases by one
- if it is uppercase, the cost of the right side decreases by one

At every position we know:

- how many lowercase letters must be flipped on the left
- how many uppercase letters must be flipped on the right

Their sum is the cost for that split.

This converts the quadratic brute-force scan into a linear sweep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Count how many uppercase letters exist in the entire string.

Initially, we imagine the split is before the first character. The left side is empty, and the whole string belongs to the lowercase section. Every uppercase letter would need conversion.
2. Store this count in a variable called `right_upper`.

This represents how many uppercase letters still remain in the suffix that should become lowercase.
3. Initialize `left_lower = 0`.

This tracks how many lowercase letters already appear in the prefix that should become uppercase.
4. Initialize the answer as `right_upper`.

This corresponds to the split before the first character.
5. Scan the string from left to right.
6. For each character:

- If the character is lowercase, increment `left_lower`.
- Otherwise decrement `right_upper`.

The character moves from the right section to the left section as the split advances.
7. After processing the character, compute:

$$\text{cost} = \text{left\_lower} + \text{right\_upper}$$

This is exactly the number of changes needed for the current split.

1. Keep the minimum cost over all split positions.
2. Print the minimum value.

### Why it works

Every valid final string has a single boundary where uppercase letters end and lowercase letters begin.

For a fixed split:

- every lowercase letter on the left is incorrect
- every uppercase letter on the right is incorrect

Changing exactly those characters always produces a valid string, and any valid transformation must change at least those characters.

The algorithm evaluates every possible split and computes its exact cost. Since the minimum over all valid splits is taken, the final answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    right_upper = sum(c.isupper() for c in s)
    left_lower = 0

    ans = right_upper

    for c in s:
        if c.islower():
            left_lower += 1
        else:
            right_upper -= 1

        ans = min(ans, left_lower + right_upper)

    print(ans)

solve()
```

The solution starts by counting all uppercase letters. This corresponds to the split before the string begins, where the entire string is treated as the lowercase section.

As the scan progresses, each character crosses the partition boundary exactly once.

If the current character is lowercase, it becomes part of the uppercase prefix, so it contributes one required modification.

If the current character is uppercase, it leaves the lowercase suffix, so one required modification disappears.

The expression `left_lower + right_upper` always represents the exact number of changes for the current split.

One subtle detail is the order of updates. The current character must first move to the left side before evaluating the cost of the split after that position. Reversing this order would shift all partition calculations by one index and produce incorrect answers.

Another important detail is considering empty sections. Initializing the answer with `right_upper` automatically handles the split before the first character. The final iteration naturally handles the split after the last character.

## Worked Examples

### Example 1

Input:

```
PRuvetSTAaYA
```

| Position | Character | left_lower | right_upper | Current Cost | Best |
| --- | --- | --- | --- | --- | --- |
| Start | - | 0 | 7 | 7 | 7 |
| 0 | P | 0 | 6 | 6 | 6 |
| 1 | R | 0 | 5 | 5 | 5 |
| 2 | u | 1 | 5 | 6 | 5 |
| 3 | v | 2 | 5 | 7 | 5 |
| 4 | e | 3 | 5 | 8 | 5 |
| 5 | t | 4 | 5 | 9 | 5 |
| 6 | S | 4 | 4 | 8 | 5 |
| 7 | T | 4 | 3 | 7 | 5 |
| 8 | A | 4 | 2 | 6 | 5 |
| 9 | a | 5 | 2 | 7 | 5 |
| 10 | Y | 5 | 1 | 6 | 5 |
| 11 | A | 5 | 0 | 5 | 5 |

The best answer is `5`. The trace shows how the partition cost changes dynamically as characters move from the suffix into the prefix.

### Example 2

Input:

```
aAaAaA
```

| Position | Character | left_lower | right_upper | Current Cost | Best |
| --- | --- | --- | --- | --- | --- |
| Start | - | 0 | 3 | 3 | 3 |
| 0 | a | 1 | 3 | 4 | 3 |
| 1 | A | 1 | 2 | 3 | 3 |
| 2 | a | 2 | 2 | 4 | 3 |
| 3 | A | 2 | 1 | 3 | 3 |
| 4 | a | 3 | 1 | 4 | 3 |
| 5 | A | 3 | 0 | 3 | 3 |

The minimum stays at `3`. This example demonstrates why local greedy fixes are unreliable. The optimal solution comes from evaluating complete partition costs, not individual violations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass through the string |
| Space | $O(1)$ | Only a few counters are stored |

The algorithm easily fits within the constraints. A linear scan over $10^5$ characters is trivial within a 1 second limit, and constant extra memory is negligible compared to the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    right_upper = sum(c.isupper() for c in s)
    left_lower = 0

    ans = right_upper

    for c in s:
        if c.islower():
            left_lower += 1
        else:
            right_upper -= 1

        ans = min(ans, left_lower + right_upper)

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("PRuvetSTAaYA\n") == "5\n", "sample 1"

# minimum size
assert run("a\n") == "0\n", "single lowercase"

# already valid uppercase only
assert run("ABC\n") == "0\n", "all uppercase"

# already valid lowercase only
assert run("abc\n") == "0\n", "all lowercase"

# alternating pattern
assert run("aAaAaA\n") == "3\n", "alternating cases"

# boundary split in middle
assert run("AAaa\n") == "0\n", "perfect partition"

# off-by-one trap
assert run("aA\n") == "1\n", "single inversion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | Minimum-size input |
| `ABC` | `0` | Empty lowercase section |
| `abc` | `0` | Empty uppercase section |
| `aAaAaA` | `3` | Alternating pattern |
| `AAaa` | `0` | Existing valid partition |
| `aA` | `1` | Off-by-one partition handling |

## Edge Cases

Consider the input:

```
abc
```

The correct answer is `0`.

The algorithm starts with:

- `right_upper = 0`
- `left_lower = 0`

Every processed character is lowercase, so `left_lower` increases, but the minimum answer remains `0` because the split before the string already represents a valid configuration. This correctly handles an empty uppercase section.

Now consider:

```
ABC
```

Initially:

- `right_upper = 3`
- `left_lower = 0`

As uppercase letters move from right to left:

- `right_upper` decreases
- `left_lower` stays `0`

At the end:

- `right_upper = 0`
- total cost becomes `0`

This correctly handles an empty lowercase section.

Finally, examine the tricky inversion case:

```
aA
```

Initial state:

- `left_lower = 0`
- `right_upper = 1`
- cost = `1`

After processing `'a'`:

- `left_lower = 1`
- `right_upper = 1`
- cost = `2`

After processing `'A'`:

- `left_lower = 1`
- `right_upper = 0`
- cost = `1`

The minimum remains `1`, which matches the optimal transformation. This confirms the partition transitions are handled without off-by-one mistakes.
