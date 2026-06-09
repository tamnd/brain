---
title: "CF 1915A - Odd One Out"
description: "We are given a stream of very small independent tasks. Each task consists of exactly three digits, and we are promised a specific structure: among the three values, two are identical and one is different."
date: "2026-06-08T19:55:14+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1915
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 918 (Div. 4)"
rating: 800
weight: 1915
solve_time_s: 81
verified: true
draft: false
---

[CF 1915A - Odd One Out](https://codeforces.com/problemset/problem/1915/A)

**Rating:** 800  
**Tags:** bitmasks, implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of very small independent tasks. Each task consists of exactly three digits, and we are promised a specific structure: among the three values, two are identical and one is different. Our job is to identify the outlier, the digit that appears only once in that triple.

Even though the input size per test case is tiny, the problem is designed to test clean reasoning about equality patterns rather than any heavy computation. Each test case is independent, so there is no shared state or cumulative structure to exploit.

The constraints are small enough that any constant-time per test solution is sufficient. With at most 270 test cases and only three integers per case, even an approach that does multiple comparisons or uses simple counting structures is trivially fast under the time limit. The real constraint pressure is nonexistent; instead, correctness and handling of the equality pattern are what matter.

The only subtlety comes from assuming the structure is always valid. A careless implementation might try to generalize or sort without considering stability of logic, but since exactly one value is guaranteed to be unique, we can rely on that invariant directly.

Edge cases are mostly degenerate forms of the same pattern. For example, inputs like `5 5 6`, `6 5 5`, or `5 6 5` all require the same output, but naive positional reasoning could fail if one assumes the unique value is always in a fixed position.

## Approaches

A brute-force interpretation would be to count occurrences of each digit in the triple using a frequency structure such as a dictionary or array of size 10. We increment counts for each of the three values, then scan for the one with frequency equal to one. This is correct and runs in constant time per test case. Over 270 test cases, the total work is negligible.

However, this approach does unnecessary work because the structure of the input is highly constrained. We do not actually need a full frequency table; we only need to distinguish which of the three positions differs from the others. The key observation is that equality among three elements with exactly one distinct element means the distinct one must differ from at least one of the other two, while the equal pair must match each other.

This allows a direct logical extraction: compare pairs. If `a == b`, then `c` is the answer. Otherwise, if `a == c`, then `b` is the answer. Otherwise, `a` must be the unique one. This reduces the problem to a constant number of comparisons with no auxiliary storage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (counting) | O(1) per test | O(1) | Accepted |
| Pairwise comparison | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. This determines how many independent triples we will process.
2. For each test case, read the three digits `a`, `b`, and `c`.
3. Compare `a` and `b`. If they are equal, the repeated pair is already identified, so the third value `c` must be the unique one.
4. If `a` and `b` are not equal, compare `a` and `c`. If these are equal, then `b` is the only value not matching its pair, so it is the unique digit.
5. If neither of the above conditions holds, then `b` must equal `c`, and `a` is the unique digit.

### Why it works

The guarantee that exactly two values are equal enforces a strict partition of the three elements into one pair and one singleton. Every comparison either identifies the pair directly or eliminates a candidate. Since equality is transitive, once we find any matching pair, the remaining element cannot be equal to them, so it must be the unique one. There is no alternative configuration consistent with the input constraint, which ensures correctness of the conditional chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    
    if a == b:
        print(c)
    elif a == c:
        print(b)
    else:
        print(a)
```

The solution relies entirely on direct comparisons. The first condition checks whether the first two values already form the repeated pair, which immediately isolates the answer. The second condition is only reached if the first comparison fails, so we know `a != b`. At that point, checking `a == c` determines whether `a` is part of the repeated pair. If neither condition is satisfied, the only remaining consistent structure is `b == c`, making `a` the unique element.

No loops or data structures are required beyond input parsing. The order of checks matters because it avoids redundant comparisons and guarantees we always identify the correct singleton.

## Worked Examples

### Example Trace 1

Input:

```
1 2 2
```

| Step | a | b | c | Condition checked | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | a == b | False |
| 2 | 1 | 2 | 2 | a == c | False |
| 3 | 1 | 2 | 2 | fallback | output a |

This trace shows the case where the repeated pair is `(2, 2)`, but it is not aligned at the start. The logic correctly avoids assuming positional structure and instead deduces equality relations.

### Example Trace 2

Input:

```
5 5 6
```

| Step | a | b | c | Condition checked | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 6 | a == b | True |
| 2 | - | - | - | output c | 6 |

This demonstrates the early exit behavior when the first two elements already form the equal pair. No further comparisons are required.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | O(t) | Each test case uses a constant number of comparisons and prints one result |

| Space | O(1) | Only three variables are used per test case |

The constraints allow up to 270 test cases, so a constant-time solution per case is comfortably within limits. Even if extended to much larger input sizes, the same approach scales linearly without risk.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())
        if a == b:
            out.append(str(c))
        elif a == c:
            out.append(str(b))
        else:
            out.append(str(a))
    return "\n".join(out)

# provided samples
assert run("""10
1 2 2
4 3 4
5 5 6
7 8 8
9 0 9
3 6 3
2 8 2
5 7 7
7 7 5
5 7 5""") == """1
3
6
7
0
6
8
5
5
7"""

# all equal pair in different positions
assert run("1\n2 3 3") == "2"

# pair at start
assert run("1\n9 9 1") == "1"

# pair in middle
assert run("1\n4 7 4") == "7"

# alternating pattern
assert run("3\n0 1 1\n2 2 3\n8 9 8") == "0\n3\n9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 3` | `2` | pair at end |
| `9 9 1` | `1` | pair at start |
| `4 7 4` | `7` | pair split around middle |
| mixed batch | varies | multiple independent cases |

## Edge Cases

A key edge case is when the equal pair is not adjacent in input order. For example, in `4 7 4`, the pair `(4, 4)` is split around the middle position. The algorithm handles this by first checking `a == b`, which fails, then checking `a == c`, which succeeds, correctly identifying `b` as the unique element.

Another case is when the equal pair appears in the first two positions, such as `9 9 1`. Here the first condition `a == b` immediately triggers, and the algorithm outputs `c` without needing any further checks. This confirms that early exit behavior is safe and does not skip any necessary reasoning.

Finally, in `7 7 5`, the structure is identical but with different values. The same invariant holds: exactly one equality pair exists, so the first matching comparison always identifies the correct partition of the triple, ensuring the unique element is returned consistently.
