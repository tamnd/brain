---
title: "CF 1428C - ABBB"
description: "We are given a string consisting only of the characters A and B. We may repeatedly remove any adjacent substring equal to AB or BB. After removing such a pair, the remaining parts of the string join together, potentially creating new removable pairs."
date: "2026-06-11T05:28:49+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1428
codeforces_index: "C"
codeforces_contest_name: "Codeforces Raif Round 1 (Div. 1 + Div. 2)"
rating: 1100
weight: 1428
solve_time_s: 108
verified: true
draft: false
---

[CF 1428C - ABBB](https://codeforces.com/problemset/problem/1428/C)

**Rating:** 1100  
**Tags:** brute force, data structures, greedy, strings  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting only of the characters `A` and `B`. We may repeatedly remove any adjacent substring equal to `AB` or `BB`. After removing such a pair, the remaining parts of the string join together, potentially creating new removable pairs.

For each test case, we need to determine the minimum possible length of the string after performing any number of valid removals.

The total length of all strings is at most `2 × 10^5`, which is the real constraint that matters. Any algorithm that repeatedly scans the string and physically deletes characters could easily become quadratic. A quadratic solution would require roughly `4 × 10^10` operations in the worst case, which is far beyond the limit. We need a linear-time approach, processing each character only a constant number of times.

Several situations are easy to misjudge.

Consider the string:

```
AB
```

The answer is `0`, because the whole string can be removed in one operation.

Now consider:

```
BA
```

The answer is `2`. There is no `AB` or `BB` substring, so nothing can be removed. A solution that only counts the number of `A` and `B` characters would incorrectly treat these two strings the same.

Another subtle example is:

```
ABB
```

One possible sequence is:

```
ABB → A → 1
```

First remove the last `BB`, leaving `A`. Alternatively:

```
ABB → B → 1
```

Remove `AB` first. Different operation orders produce different intermediate strings, but the minimum achievable length is the same. The solution must not depend on choosing a particular sequence of deletions.

A final tricky case is:

```
BBB
```

We can remove one `BB` pair:

```
BBB → B
```

The answer is `1`, not `0`. Whenever a block contains an odd number of `B` characters and no `A` is available to cancel the final one, one `B` survives.

## Approaches

A direct simulation would repeatedly search for occurrences of `AB` or `BB`, delete one of them, concatenate the remaining parts, and continue until no move exists.

This approach is correct because it literally follows the rules of the game. The problem is efficiency. Every deletion may require shifting almost the entire string, and there can be up to `O(n)` deletions. A string of length `n` can therefore require `O(n²)` work.

The key observation is that both removable patterns end with `B`.

Suppose we process the string from left to right and maintain the current unreduced string. When we read a new character:

If it is `A`, it cannot immediately form a removable pair, so it must stay for now.

If it is `B`, then any previous character allows a removal:

```
AB → removed
BB → removed
```

The only thing that matters is whether there exists a character immediately before it in the current reduced string. If there is, the new `B` removes that character. If there is not, the `B` survives.

This behavior is exactly what a stack provides.

We store the current unreduced characters in a stack.

When reading `A`, push it.

When reading `B`:

If the stack is non-empty, pop one character. The popped character together with this `B` corresponds to either an `AB` or `BB` deletion.

If the stack is empty, push the `B`, since there is nothing available to remove with it.

After processing the whole string, the stack contains exactly the characters that cannot be eliminated. Its size is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty stack.
2. Scan the string from left to right.
3. If the current character is `A`, push it onto the stack.

An `A` alone cannot complete either removable pattern.
4. If the current character is `B` and the stack is non-empty, pop the top element.

The popped character together with the current `B` forms either `AB` or `BB`, both of which are removable.
5. If the current character is `B` and the stack is empty, push `B`.

No deletion is possible because there is no preceding character available.
6. After all characters have been processed, output the stack size.

### Why it works

The stack always represents the shortest possible residual string for the prefix processed so far.

When a new `B` arrives, any existing top character can immediately be paired with it. Whether that top character is `A` or `B`, the pair disappears. Keeping either character would never help produce a shorter final result, because both `AB` and `BB` are valid deletions.

If the stack is empty, the `B` has no partner and must remain. No future operation can remove it without first placing another character before it, which is impossible because we process characters in their original order.

By induction over the processed prefix, the stack remains exactly the fully reduced form of that prefix. When the scan ends, its length is the minimum achievable final length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        s = input().strip()

        stack = []

        for ch in s:
            if ch == 'A':
                stack.append('A')
            else:
                if stack:
                    stack.pop()
                else:
                    stack.append('B')

        answers.append(str(len(stack)))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The solution follows the stack simulation described above.

The stack stores the reduced form of the prefix processed so far. Every `A` is pushed because it cannot immediately participate in a deletion.

When a `B` appears, there are only two possibilities. If the stack is non-empty, the top element and the current `B` disappear together. This matches both allowed operations. If the stack is empty, the `B` survives and must be stored.

A common mistake is to explicitly check whether the top is `A` or `B`. That is unnecessary because both `AB` and `BB` are removable. The only thing that matters is whether a character exists.

Another easy bug is forgetting that a surviving `B` must be pushed when the stack is empty. Without that step, cases like `"B"` or `"BBB"` produce incorrect answers.

## Worked Examples

### Example 1

Input:

```
BABA
```

| Character | Stack Before | Action | Stack After |
| --- | --- | --- | --- |
| B | [] | push B | [B] |
| A | [B] | push A | [B,A] |
| B | [B,A] | pop | [B] |
| A | [B] | push A | [B,A] |

Final stack size = 2.

The trace shows an `AB` pair disappearing when the third character is processed. The remaining string cannot be reduced further.

### Example 2

Input:

```
AABBBABBBB
```

| Character | Stack Before | Action | Stack After |
| --- | --- | --- | --- |
| A | [] | push | [A] |
| A | [A] | push | [A,A] |
| B | [A,A] | pop | [A] |
| B | [A] | pop | [] |
| B | [] | push | [B] |
| A | [B] | push | [B,A] |
| B | [B,A] | pop | [B] |
| B | [B] | pop | [] |
| B | [] | push | [B] |
| B | [B] | pop | [] |

Final stack size = 0.

This example demonstrates both kinds of deletions. Sometimes a `B` removes an `A`, and sometimes it removes another `B`. The algorithm treats both identically by popping one element whenever possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, and each stack element is pushed and popped at most once |
| Space | O(n) | In the worst case the stack may contain the entire string |

Here `n` denotes the length of a test case string. Since the sum of all lengths is at most `2 × 10^5`, the total running time across all test cases is linear in the input size and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()

        stack = []

        for ch in s:
            if ch == 'A':
                stack.append('A')
            else:
                if stack:
                    stack.pop()
                else:
                    stack.append('B')

        ans.append(str(len(stack)))

    return "\n".join(ans)

# provided samples
assert run("3\nAAA\nBABA\nAABBBABBBB\n") == "3\n2\n0", "sample 1"

# minimum size
assert run("1\nA\n") == "1", "single A"

# minimum size
assert run("1\nB\n") == "1", "single B"

# all equal characters
assert run("1\nBBBBB\n") == "1", "odd number of B"

# removable pair
assert run("1\nAB\n") == "0", "entire string removed"

# order matters
assert run("1\nBA\n") == "2", "no valid move"

# off-by-one style case
assert run("1\nABB\n") == "1", "multiple possible deletions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A` | `1` | Smallest possible input containing `A` |
| `B` | `1` | Smallest possible input containing `B` |
| `BBBBB` | `1` | Odd-sized block of only `B` characters |
| `AB` | `0` | Direct removal of one valid pair |
| `BA` | `2` | No removable substring exists |
| `ABB` | `1` | Multiple valid deletion orders lead to same answer |

## Edge Cases

Consider:

```
1
BA
```

The stack evolution is:

```
B -> [B]
A -> [B, A]
```

No `B` arrives after the final `A`, so nothing can be removed. The final size is `2`. The algorithm correctly avoids removing non-adjacent characters.

Consider:

```
1
BBB
```

The stack evolution is:

```
B -> [B]
B -> []
B -> [B]
```

One `BB` pair disappears, but the last `B` survives. The final size is `1`, matching the optimal result.

Consider:

```
1
AB
```

The stack evolution is:

```
A -> [A]
B -> []
```

The entire string vanishes, producing answer `0`.

Consider:

```
1
ABB
```

The stack evolution is:

```
A -> [A]
B -> []
B -> [B]
```

The answer is `1`. This example shows why the algorithm does not need to choose among different deletion orders. The stack representation already captures the fully reduced state after each prefix, leading to the correct minimum length automatically.
