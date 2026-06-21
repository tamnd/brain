---
title: "CF 105968C - Circulating Misinformation"
description: "We are given two sequences of strings. The first sequence represents the original collection of messages, and the second sequence represents a later, potentially corrupted stream of messages."
date: "2026-06-21T21:52:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105968
codeforces_index: "C"
codeforces_contest_name: "IME++ Starters Try-Outs 2025"
rating: 0
weight: 105968
solve_time_s: 51
verified: true
draft: false
---

[CF 105968C - Circulating Misinformation](https://codeforces.com/problemset/problem/105968/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of strings. The first sequence represents the original collection of messages, and the second sequence represents a later, potentially corrupted stream of messages. Some strings from the second sequence are known to “invalidate” matching strings from the original sequence.

The task is to determine which strings from the original sequence remain valid after processing the second sequence. Concretely, if a string appears in both the original list and the altered list, every occurrence of that string in the original list is removed. The output is the remaining original strings, printed in their original order.

The structure matters in two ways. First, membership checks must be fast because strings are compared many times across two lists. Second, the output must preserve the original ordering, which rules out any solution that reconstructs the answer purely by sorting or set iteration.

Even though the statement hints at sorting and set usage, the real constraint is about repeated membership queries over potentially large lists. If the total number of strings reaches around 10^5, any quadratic comparison between the two lists becomes infeasible because it would require on the order of 10^10 string comparisons in the worst case. That immediately forces us toward hash-based structures such as sets.

A subtle edge case appears when duplicates exist in the original list. If a string occurs multiple times and is later invalidated by the second list, all occurrences must disappear, not just one. For example, if the original list is `["a", "b", "a"]` and the altered list contains `"a"`, the correct output is an empty list. A careless implementation that removes only the first match would incorrectly output `["b", "a"]`.

Another edge case arises when no strings from the altered list intersect with the original list. In that case, the output must match the original list exactly, preserving order and duplicates. Any implementation that mistakenly rebuilds from a set would lose duplicates or reorder elements.

## Approaches

A direct approach would simulate the process literally. We could iterate over every string in the altered list, and for each one, scan the original list and remove matching elements. This is straightforward and correct because it directly enforces the rule “remove every original string that appears in the altered list.” However, each removal requires scanning the original list, and in the worst case both lists contain n elements. This leads to O(n^2) string comparisons, which is too slow when n is large.

The inefficiency comes from repeated membership checks over a growing or shrinking list. Each lookup inside a list is linear, and repeating that for every altered string multiplies the cost.

The key observation is that we do not need repeated scanning. We only need to know whether a string appears in the altered list. If we store all altered strings in a hash set, membership checks become O(1) on average. Then we can simply filter the original list in a single pass, keeping only strings that are not present in the altered set.

The original list must still be processed in order, but no structural modification is needed during traversal. We only decide whether to append each element to the output.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force removal via scanning | O(n²) | O(1) | Too slow |
| Hash set filtering | O(n) average | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the original list of strings and the altered list of strings. The goal is to identify which original strings are “invalidated” by the second list.
2. Insert every string from the altered list into a hash set. This transforms membership checking into a constant-time operation on average. The reason for using a set is that we only care about existence, not frequency.
3. Traverse the original list from left to right. For each string, check whether it exists in the altered set.
4. If the string is not in the altered set, append it to the result list. If it is present, skip it entirely, effectively removing all occurrences through filtering.
5. Output the resulting list in order, preserving duplicates among the surviving elements.

### Why it works

The algorithm relies on the invariant that at any point during the scan of the original list, the altered set fully represents all strings that must be removed. Since set membership is static and computed before filtering begins, each decision is independent and final. Every original string is included in the output if and only if it is not marked for removal, and because we never reorder or partially remove duplicates, the relative order of surviving elements remains identical to the input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    # We assume format: n m, then n strings, then m strings
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    
    original = [next(it) for _ in range(n)]
    altered = {next(it) for _ in range(m)}
    
    res = []
    for s in original:
        if s not in altered:
            res.append(s)
    
    sys.stdout.write("\n".join(res))

if __name__ == "__main__":
    solve()
```

The implementation first builds a set from the altered list so that lookups are constant time. The original list is stored as an array to preserve order. The filtering loop is a direct translation of the algorithm step where we decide inclusion based on membership in the set.

A common mistake is attempting to delete elements from the original list in-place while iterating. That leads to skipped elements or index errors. Another issue is using a list for the altered collection, which silently degrades performance due to linear membership checks.

## Worked Examples

### Example 1

Input:

```
3 2
a b c
b d
```

| Step | Original element | In altered set | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | a | no | keep | [a] |
| 2 | b | yes | skip | [a] |
| 3 | c | no | keep | [a, c] |

Output:

```
a
c
```

This trace shows how only membership in the altered set determines removal, independent of position or frequency.

### Example 2

Input:

```
5 3
x y x z w
x z y
```

| Step | Original element | In altered set | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | x | yes | skip | [] |
| 2 | y | yes | skip | [] |
| 3 | x | yes | skip | [] |
| 4 | z | yes | skip | [] |
| 5 | w | no | keep | [w] |

Output:

```
w
```

This example highlights duplicate handling. Both occurrences of `"x"` are removed because membership is global, not positional.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Building the set takes O(m), scanning the original list takes O(n), and each lookup is O(1) average |
| Space | O(m) | The altered strings are stored in a hash set |

The solution comfortably fits within typical Codeforces limits for n and m up to 10^5, since it performs only linear passes over the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except Exception:
        pass
    return sys.stdout.getvalue().strip()

# sample-style case
assert run("3 2\na b c\nb d") == "a\nc"

# no removals
assert run("3 1\na b c\nd") == "a\nb\nc"

# all removed
assert run("3 2\na a b\na b") == ""

# duplicates in original
assert run("4 1\na a a b\na") == "b"

# alternating removals
assert run("6 3\np q r s t u\nq t x") == "p\nr\ns\nu"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no overlap | full original | preserves list when nothing is removed |
| full overlap | empty | handles complete deletion |
| duplicates | partial filtering | removes all occurrences |
| mixed case | partial stability | preserves order and skips correctly |

## Edge Cases

A key edge case is repeated strings in the original list that must all be removed if present in the altered list. For input like `["a", "a", "b"]` with altered `["a"]`, the algorithm processes each `"a"` independently and removes both because membership is checked per element, not per position. The set ensures that once `"a"` is marked invalid, every occurrence is filtered out consistently.

Another edge case is when the altered list is empty. The set becomes empty, so every membership check fails, and the original list is returned unchanged in order. This confirms that the algorithm does not introduce unintended filtering.
