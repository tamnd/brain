---
title: "CF 1481C - Fence Painting"
description: "We are given a fence consisting of n planks, each initially painted with a color from a1 to an. Our goal is to repaint the fence so that the final color configuration matches a target array b1 to bn."
date: "2026-06-10T23:35:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1481
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 699 (Div. 2)"
rating: 1600
weight: 1481
solve_time_s: 150
verified: false
draft: false
---

[CF 1481C - Fence Painting](https://codeforces.com/problemset/problem/1481/C)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fence consisting of `n` planks, each initially painted with a color from `a_1` to `a_n`. Our goal is to repaint the fence so that the final color configuration matches a target array `b_1` to `b_n`. We have `m` painters, each arriving in sequence, and each can paint exactly one plank with a specific color `c_j`. We cannot refuse a painter, but we can choose which plank they paint. The task is to decide if it is possible to achieve the desired coloring, and if so, assign a plank to each painter in the given order.

The constraints allow `n` and `m` up to `10^5` per test case, and the sum over all test cases is also bounded by `10^5`. This indicates we need a solution that runs roughly in linear time per test case. A brute-force approach that checks all possible plank assignments for each painter would be far too slow, as it would potentially require `O(n^m)` operations.

The non-obvious edge cases include situations where the last painter's color does not match any plank that needs repainting, or where multiple painters can paint the same plank but we must still cover all required changes. For instance, if all planks are already the desired color but the last painter has a color that no plank currently needs, a naive approach might fail to assign a valid plank.

For example, if `a = [1, 1]`, `b = [1, 2]`, and `c = [2]`, the only way to achieve the target is for the single painter to paint the second plank. If we mistakenly choose the first plank, we would fail.

## Approaches

The brute-force approach would consider every possible plank assignment for each painter. For each painter, we could try painting every plank that matches their color and recursively check the next painter. This is correct because it explores all possibilities, but it is intractable for large `n` and `m`. Even for moderate sizes like `n = m = 10^5`, this would require astronomical operations.

The key insight comes from observing that only planks where `a_i != b_i` need to be repainted. We can maintain a mapping from each color to the list of planks that require that color. Painters arriving with a specific color `c_j` should ideally paint one of the remaining planks that require `c_j`. If no such plank exists, we can paint any plank that already has color `c_j` to ensure the painter is used. The last painter's plank is crucial because if we fail to choose a valid plank, we cannot satisfy the constraints.

We can implement this efficiently using a dictionary that maps colors to lists of planks still needing that color. We iterate over painters in order and assign them a plank based on this mapping, handling the last painter specially if necessary. This reduces the problem from combinatorial explosion to linear-time processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, create a dictionary mapping colors to the indices of planks that still need that color (`a_i != b_i`). This lets us quickly find which planks can be painted by a given painter.
2. Identify the last painter's color `c_m`. Check if there is at least one plank in the target `b` with this color. If not, output "NO" immediately because the last painter must paint a plank of this color.
3. For painters from the first to the penultimate, if there is a plank that needs their color, assign it to them and remove it from the dictionary. If no plank needs their color, assign any plank of the last painter's color. This guarantees that every painter paints something while leaving the last painter a valid plank.
4. Assign the last painter to any plank of their color. By step 3, we ensured there is at least one such plank.
5. After all painters are assigned, check if any plank still needs repainting. If so, output "NO". Otherwise, output "YES" and the list of plank indices.

Why it works: The invariant is that each painter either paints a plank that still needs their color or a safe fallback (a plank with the last painter's color). The last painter is guaranteed a valid plank because we checked for its existence. All required repaintings are covered, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        c = list(map(int, input().split()))
        
        need = {}
        for i in range(n):
            if a[i] != b[i]:
                need.setdefault(b[i], []).append(i)
        
        last_color = c[-1]
        if last_color in need:
            last_plank = need[last_color][-1]
        else:
            found = -1
            for i in range(n):
                if b[i] == last_color:
                    found = i
                    break
            if found == -1:
                print("NO")
                continue
            last_plank = found
        
        res = [0] * m
        res[-1] = last_plank
        for j in range(m-1):
            color = c[j]
            if color in need and need[color]:
                res[j] = need[color].pop()
            else:
                res[j] = last_plank
        
        impossible = any(need[color] for color in need)
        if impossible:
            print("NO")
        else:
            print("YES")
            print(' '.join(str(x+1) for x in res))

if __name__ == "__main__":
    solve()
```

The solution begins by reading the number of test cases. For each test case, we create a mapping of colors to planks that still need repainting. We handle the last painter first because their color must appear on at least one plank. The remaining painters are assigned planks greedily: either a plank that needs their color or a fallback. The final check ensures no required repainting is left unassigned. Indices are converted to 1-based for output.

## Worked Examples

**Sample Input 1**

```
1 1
1
1
1
```

| i | a[i] | b[i] | need dictionary | c[j] | res |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | {} | 1 | 1 |

The fence is already correct. The only painter can paint the only plank with their color. Output is YES.

**Sample Input 2**

```
5 2
1 2 2 1 1
1 2 2 1 1
1 2
```

| i | a[i] | b[i] | need dictionary | c[j] | res |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | {} | 1 | 2 |
| 1 | 2 | 2 | {} | 2 | 2 |

No repainting needed. Both painters paint planks with colors that match them. Output is YES.

These traces confirm that the algorithm correctly handles cases where no repainting is required and ensures the last painter's color exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Constructing the need dictionary is O(n), assigning painters is O(m) |
| Space | O(n) | Storing the need dictionary and results |

The linear complexity fits the constraints of up to `10^5` planks and painters across all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as io_module
    out = io_module.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("6\n1 1\n1\n1\n1\n5 2\n1 2 2 1 1\n1 2 2 1 1\n1 2\n3 3\n2 2 2\n2 2 2\n2 3 2\n10 5\n7 3 2 1 7 9 4 2 7 9\n9 9 2 1 4 9 4 2 3 9\n9 9 7 4 3\n5 2\n1 2 2 1 1\n1 2 2 1 1\n3 3\n6 4\n3 4 2 4 1 2\n2 3 1 3 1 1\n2 2 3 4") == "YES\n1\nYES\n2 2\nYES\n1 1 1\nYES\n2 1 9 5 9\nNO\nNO"

# custom cases
assert run("1\n2 2\n1 2\n2 1\n1 2") == "YES\n2 1", "swap colors"
assert run("
```
