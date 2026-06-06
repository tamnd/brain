---
title: "CF 339A - Helpful Maths"
description: "The input is a string representing a sum where every number is either 1, 2, or 3, and the numbers are separated by plus signs. For example, the string 3+2+1+3 represents four summands. Xenia can only evaluate the expression if the numbers appear in non-decreasing order."
date: "2026-06-06T17:14:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 339
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 197 (Div. 2)"
rating: 800
weight: 339
solve_time_s: 84
verified: true
draft: false
---

[CF 339A - Helpful Maths](https://codeforces.com/problemset/problem/339/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings, strings  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a string representing a sum where every number is either `1`, `2`, or `3`, and the numbers are separated by plus signs. For example, the string `3+2+1+3` represents four summands.

Xenia can only evaluate the expression if the numbers appear in non-decreasing order. Our task is not to compute the sum itself. Instead, we must rearrange the existing numbers so that all `1`s come first, then all `2`s, then all `3`s, and print the resulting expression in the same `a+b+c` format.

The input length is at most 100 characters. Since every number occupies one character and every separator occupies one character, there are at most about 50 numbers. Such a small constraint means almost any reasonable approach is fast enough. Even a sorting-based solution runs instantly.

The main challenge is handling the string format correctly. We need to sort the numbers, not the entire string. A careless implementation that sorts all characters would mix digits and plus signs together and produce an invalid expression.

One edge case is when the expression contains only a single number.

Input:

```
2
```

Output:

```
2
```

There are no plus signs to insert beyond the original structure. Splitting and joining still works correctly.

Another edge case is when all numbers are already sorted.

Input:

```
1+1+2+3
```

Output:

```
1+1+2+3
```

The algorithm should leave the expression unchanged.

A different case is when all numbers are identical.

Input:

```
3+3+3
```

Output:

```
3+3+3
```

Sorting should not alter the result, and duplicate values must be preserved.

## Approaches

A brute-force mindset would be to generate every possible ordering of the numbers, check whether that ordering is non-decreasing, and print the first valid one. This works because the correct answer is simply one of the permutations of the given summands.

The problem is that permutations grow factorially. If there are 50 numbers, there are `50!` possible orderings, which is astronomically large and completely infeasible.

The structure of the problem gives a much simpler observation. The only values that appear are `1`, `2`, and `3`, and Xenia wants them in non-decreasing order. A sequence is non-decreasing exactly when all smaller values appear before larger values. That means we do not need to search among permutations at all. We can extract the numbers, sort them, and rebuild the expression.

Since sorting directly produces the unique non-decreasing arrangement, the problem becomes a straightforward implementation task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Split the string using `'+'` as the delimiter.

This extracts all numbers as separate strings such as `["3", "2", "1"]`.
3. Sort the resulting list.

Sorting places all `1`s first, then all `2`s, then all `3`s, which is exactly the required order.
4. Join the sorted numbers back together using `'+'`.

This reconstructs a valid expression in the original format.
5. Print the result.

### Why it works

The expression consists only of the numbers `1`, `2`, and `3`. A valid answer must contain exactly the same multiset of numbers as the input, only reordered.

Sorting the extracted numbers produces a sequence where every element is less than or equal to the next element. That is precisely the definition of non-decreasing order. Since sorting neither removes nor duplicates any number, the resulting expression contains exactly the original summands and satisfies Xenia's requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

numbers = s.split('+')
numbers.sort()

print('+'.join(numbers))
```

The first step reads the expression as a string. Using `strip()` removes the trailing newline character.

The call to `split('+')` is the key parsing operation. Instead of dealing with individual characters, it directly extracts the numbers as separate elements.

The list is then sorted lexicographically. Since the only possible values are `"1"`, `"2"`, and `"3"`, lexicographic order matches numeric order.

Finally, `'+'.join(numbers)` rebuilds the expression with the required separators. This automatically handles both single-number and multi-number expressions without any special cases.

## Worked Examples

### Example 1

Input:

```
3+2+1
```

| Step | Numbers |
| --- | --- |
| After split | `["3", "2", "1"]` |
| After sort | `["1", "2", "3"]` |
| After join | `"1+2+3"` |

Output:

```
1+2+3
```

This example shows the core idea. The numbers are extracted, sorted, and reconstructed into the required order.

### Example 2

Input:

```
1+3+1+2
```

| Step | Numbers |
| --- | --- |
| After split | `["1", "3", "1", "2"]` |
| After sort | `["1", "1", "2", "3"]` |
| After join | `"1+1+2+3"` |

Output:

```
1+1+2+3
```

This example demonstrates that duplicate values are preserved. Sorting groups equal values together while maintaining the correct count of each number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the extracted numbers dominates the running time |
| Space | O(n) | The split operation stores the numbers in a list |

The input length is at most 100 characters, so even the sorting step processes only a few dozen numbers. The running time and memory usage are far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()
    numbers = s.split('+')
    numbers.sort()
    print('+'.join(numbers))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("3+2+1\n") == "1+2+3", "sample 1"

# minimum-size input
assert run("1\n") == "1", "single number"

# already sorted
assert run("1+1+2+3\n") == "1+1+2+3", "already sorted"

# all equal values
assert run("3+3+3\n") == "3+3+3", "all equal"

# reverse order
assert run("3+3+2+2+1+1\n") == "1+1+2+2+3+3", "full sorting"

# mixed duplicates
assert run("2+1+3+1+2\n") == "1+1+2+2+3", "duplicates preserved"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum-size input |
| `1+1+2+3` | `1+1+2+3` | Already sorted sequence |
| `3+3+3` | `3+3+3` | All-equal values |
| `3+3+2+2+1+1` | `1+1+2+2+3+3` | Complete reordering |
| `2+1+3+1+2` | `1+1+2+2+3` | Duplicate handling |

## Edge Cases

Consider the single-number input:

```
2
```

The algorithm performs:

```
"2".split('+')
```

which produces:

```
["2"]
```

Sorting does nothing, and joining returns:

```
2
```

The output remains correct without any special handling.

Consider an already sorted expression:

```
1+1+2+3
```

After splitting:

```
["1", "1", "2", "3"]
```

Sorting leaves the list unchanged. The final output is identical to the input, which is the desired behavior.

Consider an expression containing only identical values:

```
3+3+3
```

Splitting gives:

```
["3", "3", "3"]
```

Sorting preserves all three occurrences. Joining reconstructs:

```
3+3+3
```

This confirms that the algorithm never loses or duplicates summands and always preserves the original multiset of numbers.
