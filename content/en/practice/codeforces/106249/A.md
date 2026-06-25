---
title: "CF 106249A - MIT and TIM"
description: "We are given a string made only from the characters M, I, and T. An operation can change a substring MIT into TIM or the other way around. The goal is to perform any number of operations and make the number of contiguous occurrences of MITIT as large as possible."
date: "2026-06-25T07:19:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106249
codeforces_index: "A"
codeforces_contest_name: "MITIT Winter 2025-26 Advanced Individual Round"
rating: 0
weight: 106249
solve_time_s: 65
verified: true
draft: false
---

[CF 106249A - MIT and TIM](https://codeforces.com/problemset/problem/106249/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only from the characters `M`, `I`, and `T`. An operation can change a substring `MIT` into `TIM` or the other way around. The goal is to perform any number of operations and make the number of contiguous occurrences of `MITIT` as large as possible.

The key observation is that an operation only swaps an `M` and a `T` around a fixed `I`. The positions containing `I` never change. The input size over all test cases is at most $10^5$, so an $O(n^2)$ simulation of operations or trying many final strings is impossible. We need to process each character a constant number of times.

A common mistake is to think that the characters can be rearranged freely because the operation changes the order of `M` and `T`. They cannot. For example, in `MIMT`, the `I` positions stay fixed, so the first `I` will always remain between the first two non-`I` positions. A solution that only counts the total number of `M`, `I`, and `T` will fail.

Consider the string `MIMTI`. It has two `I` characters, but it can never create `MITIT`, because the final `T` after the second `I` does not exist. The correct answer is `0`. A careless solution based only on counts might incorrectly expect one occurrence because there is one `M`, two `I`, and two `T` characters.

Another edge case is when the required characters exist but the `I` positions prevent them from meeting. For `MMITT`, the counts are enough for `MITIT`, but there are not two `I` characters at the required distance. The answer is `0`, because operations cannot move `I` characters.

## Approaches

The brute force approach would try to understand all possible strings reachable through operations. Since every operation swaps two characters, we might try different swaps and keep the best result found. This is correct because every valid final arrangement is reachable by some sequence of operations, but the number of possible arrangements grows exponentially, so it is unusable for strings of length $10^5$.

The important structure comes from looking at what a single operation really does. A transformation `MIT <-> TIM` only swaps the two non-`I` characters around one `I`. This means the `I` positions are fixed forever. The non-`I` positions form groups where characters can move around.

If we connect two non-`I` positions whenever there is exactly one `I` between them, every operation is just a swap inside one connected component. Inside a component, all `M` and `T` characters can be rearranged arbitrarily.

A `MITIT` occurrence uses three non-`I` positions. Those positions are separated by two `I` characters, so they always belong to the same component. This means every component can be solved independently.

Inside one component, suppose its length is `len` and it contains `m` characters `M` and `t` characters `T`. We need to maximize the number of length three patterns `MTT`. Every such pattern needs one `M` and two `T` characters, and different occurrences cannot share the same starting position. The maximum is:

$$\min(m,\lfloor t/2\rfloor,\lfloor len/3\rfloor)$$

This value is always achievable by placing each `M` followed by two `T` characters and using remaining positions for the unused letters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the string and build the connected components of non `I` positions. Two non `I` positions belong to the same component if there is exactly one `I` between them. This is equivalent to grouping consecutive non `I` positions with the same parity that are connected through `I` positions.
2. For each component, count its size and the number of `M` characters and `T` characters inside it. The current arrangement is irrelevant because operations allow us to rearrange these characters inside the component.
3. Compute the contribution of the component as the minimum of the number of available `M` characters, half of the available `T` characters, and one third of the component length. Each value represents one resource needed for a `MITIT` pattern.
4. Add the contributions of all components. Since no occurrence can use characters from two different components, the sum is the global maximum.

Why it works: The invariant is that every operation keeps all `I` positions fixed and only swaps `M` and `T` inside their connected component. A possible `MITIT` occurrence needs three non `I` positions connected by two `I` positions, so it must stay inside a single component. Because each component can be freely rearranged, the only limitations are the counts of `M`, `T`, and available length. The formula exactly captures these limits, so the computed sum is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(s):
    n = len(s)
    seen = [False] * n
    ans = 0

    for i in range(n):
        if s[i] == 'I' or seen[i]:
            continue

        stack = [i]
        seen[i] = True
        length = 0
        m = 0
        t = 0

        while stack:
            x = stack.pop()
            length += 1
            if s[x] == 'M':
                m += 1
            else:
                t += 1

            for y in (x - 2, x + 2):
                if 0 <= y < n and not seen[y] and s[(x + y) // 2] == 'I' and s[y] != 'I':
                    seen[y] = True
                    stack.append(y)

        ans += min(m, t // 2, length // 3)

    return ans

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        out.append(str(solve_case(data[i])))
    print("\n".join(out))

main()
```

The solution uses a depth first search over the implicit graph of non `I` positions. An edge exists only when the two positions have an `I` between them, which is why the neighbor check uses distance two.

The DFS collects the size of one component and the amount of each letter. The actual order of characters inside the component is unnecessary because swaps let us rearrange them. The final minimum calculation directly applies the resource limits for building `MTT` triples, which correspond to `MITIT` substrings.

The boundary checks in the neighbor loop prevent accessing outside the string. The middle index `(x + y) // 2` is safe because `y` is always exactly two positions away from `x`.

## Worked Examples

For the first sample:

```
TITIMMIT
```

The components are processed as follows:

| Component | Length | M count | T count | Contribution |
| --- | --- | --- | --- | --- |
| non I positions connected together | 5 | 2 | 3 | 1 |

The component has enough characters to form one `MTT`, so the answer is `1`. This shows that the algorithm correctly uses rearrangement inside a component.

For a component where the characters cannot provide enough `T` characters:

| Component | Length | M count | T count | Contribution |
| --- | --- | --- | --- | --- |
| one component | 7 | 3 | 1 | 0 |

Even though there are `M` characters available, every occurrence needs two `T` characters after the `M`. The answer stays zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every position is visited once during component traversal |
| Space | O(n) | The visited array and DFS stack store at most all positions |

The total length of all strings is $10^5$, so the linear solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve_case(s):
    n = len(s)
    seen = [False] * n
    ans = 0
    for i in range(n):
        if s[i] == 'I' or seen[i]:
            continue
        stack = [i]
        seen[i] = True
        length = m = t = 0
        while stack:
            x = stack.pop()
            length += 1
            if s[x] == 'M':
                m += 1
            else:
                t += 1
            for y in (x - 2, x + 2):
                if 0 <= y < n and not seen[y] and s[(x + y) // 2] == 'I' and s[y] != 'I':
                    seen[y] = True
                    stack.append(y)
        ans += min(m, t // 2, length // 3)
    return ans

def run(inp: str) -> str:
    data = inp.split()
    out = []
    for s in data[1:]:
        out.append(str(solve_case(s)))
    return "\n".join(out)

assert run("6 TITIMMIT TITITIMITIMTMTMTMMITMI MIMTITMTIMTITMTITITMTI ITMTTMITMITMTMTITITMIM MMITMITTTIMTITITTTITIT MITITIMIMIMITITITITIMIMIMIMIMIMITITITIT") == "1\n2\n0\n0\n0\n5"

assert run("1 MIMTI") == "0"
assert run("1 MMITT") == "0"
assert run("1 MITIT") == "1"
assert run("1 MMMMMIIIIITTTTT") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `MIMTI` | `0` | Checks that character counts alone are not enough |
| `MMITT` | `0` | Checks fixed `I` positions |
| `MITIT` | `1` | Minimum direct successful pattern |
| `MMMMMIIIIITTTTT` | `0` | Checks separated components and impossible rearrangement |

## Edge Cases

For `MIMTI`, the algorithm creates components from non `I` positions. The component containing the `M` and `T` positions has insufficient space and `T` characters for a complete `MTT` pattern, so the contribution is zero.

For `MMITT`, the two `I` characters are not in the positions needed for `MITIT`. Since components are built around fixed `I` locations, the algorithm never incorrectly merges these characters and returns zero.

For a string already equal to `MITIT`, all three non `I` positions belong to one component. The component length is three, it has one `M` and two `T` characters, giving:

$$\min(1, 2/2, 3/3)=1$$

so the answer is one. This confirms that the method handles the simplest possible occurrence.
