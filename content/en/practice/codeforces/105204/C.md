---
title: "CF 105204C - \u0411\u043e\u0442\u0438\u043d\u043a\u0438 \u0438\u043b\u0438 \u0441\u0430\u043d\u0434\u0430\u043b\u0438\u0438"
description: "The route is described by a string consisting of '0', '1', and '?'. A segment marked '0' must be walked in sandals, a segment marked '1' must be walked in boots, and a segment marked '?' may be assigned either type of footwear."
date: "2026-06-27T02:41:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105204
codeforces_index: "C"
codeforces_contest_name: "\u0412\u041a\u041e\u0428\u041f.Junior 2024"
rating: 0
weight: 105204
solve_time_s: 55
verified: true
draft: false
---

[CF 105204C - \u0411\u043e\u0442\u0438\u043d\u043a\u0438 \u0438\u043b\u0438 \u0441\u0430\u043d\u0434\u0430\u043b\u0438\u0438](https://codeforces.com/problemset/problem/105204/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The route is described by a string consisting of `'0'`, `'1'`, and `'?'`.

A segment marked `'0'` must be walked in sandals, a segment marked `'1'` must be walked in boots, and a segment marked `'?'` may be assigned either type of footwear. Changing from sandals to boots costs `a`, while changing from boots to sandals costs `b`. The traveler may start in either footwear and also finish in either footwear, so only changes between consecutive route segments matter.

The task is to assign every `'?'` either `'0'` or `'1'` so that the total cost of all footwear changes is as small as possible.

The route length is at most `200000`, so anything quadratic is immediately impossible. Even scanning all possible assignments is hopeless because each `'?'` doubles the number of possibilities. An `O(n)` or `O(n log n)` algorithm is easily fast enough.

The tricky part is that every `'?'` belongs to a block, and assigning different values inside one block never helps. For example:

```
0??1
```

If we assign it as `0011`, there is one transition. If we assign it as `0101`, there are three transitions. Every extra change inside the block only increases the cost.

Another edge case is when the whole string consists only of `'?'`.

```
???
```

The correct answer is `0`, because we may assign every position the same value. A solution that assumes the first known character always exists would fail.

One more subtle case is when a `'?'` block touches only one known side.

```
??111
```

Assigning the block to `'1'` produces no transition at all. A solution trying to optimize every block independently without considering missing neighbors could introduce an unnecessary change.

## Approaches

A brute force solution would try every assignment of every `'?'`. If there are `k` question marks, this requires `2^k` assignments. Each assignment can be checked in linear time, giving `O(n · 2^k)` complexity, which becomes impossible even for a few dozen question marks.

The key observation is that only transitions between neighboring characters contribute to the answer. A block of consecutive `'?'` affects only its left and right boundaries. Since introducing changes inside the block can never reduce the number of boundary transitions, every optimal assignment fills the whole block with one identical character.

This allows us to ignore the exact block length. Instead, remove every `'?'` conceptually and look only at the sequence of fixed characters. Whenever two consecutive fixed characters differ, one unavoidable footwear change must occur. If the transition is `0 → 1`, it costs `a`. If it is `1 → 0`, it costs `b`.

Every `'?'` block can always be filled to match one neighboring side whenever possible, eliminating any artificial transition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · 2^k)` | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read the route string and the values `a` and `b`.
2. Scan the string from left to right until the first character that is not `'?'`. This becomes the previous fixed character.
3. If no fixed character exists, output `0`, because every position can be assigned the same value.
4. Continue scanning the rest of the string.
5. Ignore every `'?'`, since its value will be chosen later.
6. Whenever another fixed character is found, compare it with the previous fixed character.
7. If they differ, add `a` for a transition `0 → 1` or add `b` for a transition `1 → 0`.
8. Update the previous fixed character and continue.
9. Output the accumulated cost.

### Why it works

Every consecutive block of `'?'` has only two neighboring fixed characters. Filling the block with mixed values can only introduce additional transitions inside the block, which never decreases the total cost. Filling the entire block with a single value is always at least as good.

If both neighboring fixed characters are equal, the whole block is assigned that value, creating no transition.

If they are different, exactly one transition is unavoidable regardless of where inside the block it occurs. The cost depends only on the order of the fixed characters, not on the block length.

After removing all `'?'`, every transition between consecutive fixed characters is exactly one unavoidable footwear change, so summing those costs gives the minimum possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    a, b = map(int, input().split())

    prev = None
    ans = 0

    for ch in s:
        if ch == '?':
            continue
        if prev is not None and prev != ch:
            if prev == '0':
                ans += a
            else:
                ans += b
        prev = ch

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps only the previous fixed character and the current answer.

Question marks are skipped immediately because they do not contribute directly to the answer. Whenever two consecutive fixed characters differ, the corresponding transition cost is added.

The first fixed character initializes the state without adding any cost because the traveler may begin in either footwear.

If the string contains only `'?'`, `prev` remains `None`, no transition is counted, and the answer correctly stays zero.

## Worked Examples

### Sample 1

Input:

```
?0110?1?1
5 9
```

| Position | Character | Previous Fixed | Cost Added | Answer |
| --- | --- | --- | --- | --- |
| 1 | ? | None | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 |
| 3 | 1 | 1 | 5 | 5 |
| 4 | 1 | 1 | 0 | 5 |
| 5 | 0 | 0 | 9 | 14 |
| 6 | ? | 0 | 0 | 14 |
| 7 | 1 | 1 | 5 | 19 |
| 8 | ? | 1 | 0 | 19 |
| 9 | 1 | 1 | 0 | 19 |

The fixed characters form the sequence `0 1 1 0 1 1`. Every differing adjacent pair corresponds to one unavoidable change, producing the minimum cost of `19`.

### Constructed Example

Input:

```
??0???0??
3 7
```

| Position | Character | Previous Fixed | Cost Added | Answer |
| --- | --- | --- | --- | --- |
| 1 | ? | None | 0 | 0 |
| 2 | ? | None | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 |
| 4 | ? | 0 | 0 | 0 |
| 5 | ? | 0 | 0 | 0 |
| 6 | ? | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 |
| 8 | ? | 0 | 0 | 0 |
| 9 | ? | 0 | 0 | 0 |

All fixed characters are identical, so every question mark can also become `0`. No footwear change is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each character is processed exactly once. |
| Space | `O(1)` | Only a few variables are stored. |

A single linear scan is easily fast enough for a string of length `200000`, and the constant memory usage comfortably satisfies the memory limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    s = input().strip()
    a, b = map(int, input().split())

    prev = None
    ans = 0

    for ch in s:
        if ch == '?':
            continue
        if prev is not None and prev != ch:
            ans += a if prev == '0' else b
        prev = ch

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue()

# provided sample
assert run("?0110?1?1\n5 9\n") == "19\n"

# minimum size
assert run("?\n3 4\n") == "0\n"

# all question marks
assert run("????\n5 7\n") == "0\n"

# alternating fixed characters
assert run("0101\n2 3\n") == "7\n"

# question block between equal symbols
assert run("1???1\n6 8\n") == "0\n"

# question block between different symbols
assert run("0???1\n6 8\n") == "6\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `?\n3 4` | `0` | Single unknown segment |
| `????\n5 7` | `0` | Entire route is flexible |
| `0101\n2 3` | `7` | Every transition is unavoidable |
| `1???1\n6 8` | `0` | Equal endpoints eliminate all changes |
| `0???1\n6 8` | `6` | Different endpoints require exactly one transition |

## Edge Cases

Consider the input

```
???
5 8
```

No fixed characters exist. The scan never assigns `prev`, so the accumulated answer remains `0`. Assigning every position to sandals or every position to boots indeed requires no footwear changes.

Now consider

```
??111
4 6
```

The first fixed character is `1`. Every earlier question mark is ignored during the scan because it can later be assigned to `1`. No differing fixed characters are ever encountered, so the algorithm outputs `0`.

Finally, consider

```
0???1
2 9
```

The scan observes fixed characters `0` and `1`. They differ once, so it adds `2`. Regardless of how many question marks lie between them, every assignment must contain exactly one transition from sandals to boots, making `2` the optimal answer.
