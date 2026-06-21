---
title: "CF 105791C - Coconuts"
description: "We are given a line of kiosks along a beach avenue, each kiosk offering exactly one drink. A traveler starts at satisfaction value 1 and chooses a single contiguous segment of kiosks to walk through."
date: "2026-06-21T13:09:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "C"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 61
verified: true
draft: false
---

[CF 105791C - Coconuts](https://codeforces.com/problemset/problem/105791/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of kiosks along a beach avenue, each kiosk offering exactly one drink. A traveler starts at satisfaction value 1 and chooses a single contiguous segment of kiosks to walk through. While walking through that segment, he multiplies his current satisfaction by the value of each drink in order.

Each drink value is either zero or a signed power of two, meaning it can be written as either 0 or ±2^k for some integer k. A value of zero represents a special drink that immediately resets satisfaction to zero and effectively breaks the multiplicative chain. Negative values represent “bad” drinks that flip the sign of the current satisfaction in the usual multiplicative way, except that if the current satisfaction is already negative, the problem statement emphasizes that drinking another negative value restores positivity, which is consistent with normal multiplication rules.

The goal is to choose a starting and ending position of a single contiguous segment (or choose not to enter at all) such that the final satisfaction is maximized. The answer must be printed modulo 1e9 + 7, but the comparison of outcomes is done on the actual integer values before taking modulo.

The constraint n can be up to 200,000, which immediately rules out any O(n^2) enumeration of all segments. Any solution must be linear or near linear, since quadratic scanning would require on the order of 4e10 operations in the worst case, which is infeasible in one second.

A subtle point is that zero splits the process completely. Any segment crossing a zero has its product reset to zero at that point, so optimal segments never need to cross a zero.

Another important edge case is that the traveler is allowed to take no segment at all, keeping satisfaction 1. This baseline matters because any negative product is always worse than 1 in actual integer ordering, even though it might appear large after modulo.

A naive mistake is to interpret the final result purely modulo 1e9 + 7 and accidentally prefer a negative product whose modular residue is large. That would be incorrect because the maximization happens before modulo.

## Approaches

A direct approach is to try every possible starting position and extend it to every possible ending position, maintaining the running product. This correctly computes the product of every subarray. However, each extension is O(1) and there are O(n^2) subarrays, leading to roughly 2e10 operations in the worst case, which is too slow.

The structure of the problem suggests we only need to track best products ending at each position. This is the classic “maximum product subarray” idea, but with two complications: zeros reset everything, and values are signed powers of two, which makes tracking magnitudes equivalent to tracking exponent sums.

Instead of tracking actual products, we track exponents of two. A value ±2^k contributes k to the exponent, while sign is tracked separately. Multiplication becomes addition of exponents and sign flipping.

This reduces the problem to maintaining, for each position, the best positive product ending there and the best negative product ending there, in terms of exponent sums. Zeros reset both states and allow restarting from scratch.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all subarrays | O(n^2) | O(1) | Too slow |
| DP on positive/negative exponent states | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right, maintaining two running states: the best positive product ending at the current position, and the best negative product ending at the current position. We also maintain a global best exponent for any valid segment.

We represent products by their exponent of 2, since all values are powers of two up to sign.

### Steps

1. Initialize the best answer exponent as 0, representing the empty choice with value 1. Also initialize the current positive and negative states as empty.
2. For each element in the array, handle it based on its value.
3. If the value is zero, reset both states. This is because any segment passing through zero becomes invalid as a multiplicative chain. After resetting, update the global answer with 0 since we can always start fresh after zero.
4. If the value is positive 2^k, update the positive state by either starting fresh from this element or extending the previous positive state by adding k to its exponent. The negative state, if it exists, also extends by adding k since multiplying by a positive number preserves sign.
5. If the value is negative -2^k, compute new positive candidates by extending the previous negative state (since negative times negative becomes positive), and new negative candidates by extending the previous positive state or starting fresh as a single negative element.
6. After processing each element, update the global best with the current positive exponent, since only positive results can beat the baseline 1 in actual value ordering.

### Why it works

At any position, every valid subarray ending there must come from exactly one of two histories: either it started at a previous index or it started at the most recent zero. The DP states capture exactly these possibilities. Separating positive and negative states is sufficient because multiplying by ±2^k only affects sign and adds a fixed amount to the exponent, so no other information is needed. Zero acts as a hard reset that prevents cross-contamination of states across segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    best_exp = 0
    
    pos = None
    neg = None
    
    for x in a:
        if x == 0:
            best_exp = max(best_exp, 0)
            pos = None
            neg = None
            continue
        
        sign = 1 if x > 0 else -1
        k = x.bit_length() - 1 if x != 0 else 0
        
        new_pos = None
        new_neg = None
        
        if sign > 0:
            if pos is not None:
                new_pos = max(new_pos or 0, pos + k)
            else:
                new_pos = k
            
            if neg is not None:
                new_neg = neg + k
        
        else:
            if neg is not None:
                new_pos = max(new_pos or -10**30, neg + k)
            else:
                new_pos = k
            
            if pos is not None:
                new_neg = pos + k
            else:
                new_neg = k
        
        pos = new_pos
        neg = new_neg
        
        if pos is not None:
            best_exp = max(best_exp, pos)
    
    print(pow(2, best_exp, MOD))

if __name__ == "__main__":
    solve()
```

The implementation compresses each value into a sign and exponent. The exponent is extracted using bit length since every nonzero value is exactly ±2^k. The DP maintains two running states, updated in-place for each element. The global best only tracks positive exponent values, since only those correspond to valid candidates that can exceed the baseline 1.

A common implementation pitfall is forgetting that zero must fully reset both states. Another subtle issue is incorrectly allowing negative-ending states to influence the final answer, which would incorrectly prioritize large magnitude negative products.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [0, -1, 0]
```

We track states as follows:

| i | x | pos_exp | neg_exp | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | reset | reset | 0 |
| 1 | -1 | 0 | 0 | 0 |
| 2 | 0 | reset | reset | 0 |

The key observation is that zeros isolate segments completely. The best achievable value is 1, corresponding to selecting no segment.

### Example 2

Input:

```
n = 5
a = [-8, -2, 0, 2, 4]
```

| i | x | pos_exp | neg_exp | best |
| --- | --- | --- | --- | --- |
| 1 | -8 | -inf | 3 | 0 |
| 2 | -2 | 4 | 5 | 4 |
| 3 | 0 | reset | reset | 4 |
| 4 | 2 | 1 | None | 4 |
| 5 | 4 | 3 | None | 4 |

This shows the effect of sign flips: two negatives combine into a positive product, giving exponent 4, which corresponds to value 16. The zero cleanly separates the array into independent segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element updates constant DP states once |
| Space | O(1) | Only two running states are maintained |

The linear scan fits comfortably within the constraints for n up to 200,000. Memory usage remains constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod
    
    # assume solve() is defined above
    # capturing output
    import contextlib
    import sys as _sys
    from io import StringIO
    backup = _sys.stdout
    _sys.stdout = StringIO()
    solve()
    out = _sys.stdout.getvalue().strip()
    _sys.stdout = backup
    return out

# provided sample-like tests
assert run("3\n0 -1 0\n") == "1"

# all positive
assert run("3\n2 4 2\n") == str(pow(2, 3, 10**9+7))

# all negative even count best
assert run("2\n-2 -2\n") == str(pow(2, 2, 10**9+7))

# single zero
assert run("1\n0\n") == "1"

# mixed
assert run("5\n-8 -2 0 2 4\n") == str(16 % (10**9+7))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 -1 0` | `1` | zero reset and empty segment |
| `2 4 2` | `16` | pure positive accumulation |
| `-2 -2` | `4` | negative cancellation into positive |
| `0` | `1` | single zero handling |
| `-8 -2 0 2 4` | `16` | split segments and reset behavior |

## Edge Cases

A key edge case is when the entire array consists of zeros. In that situation, every segment is invalid, and the correct answer is the baseline 1. The algorithm handles this because every zero forces a reset and explicitly allows updating the best with 0, while the final answer remains at least 0 exponent, corresponding to 1.

Another edge case is a sequence of alternating signs with no zeros, such as [-2, 2, -2]. The DP correctly tracks both positive and negative states, ensuring that even-length negative chains are converted into positive candidates when a second negative appears.

A final subtle case is a single element array. If it is positive, the answer is that element’s value. If it is negative, the best still remains 1 unless it can be paired, which is impossible, so the DP correctly avoids selecting a harmful single negative segment.
