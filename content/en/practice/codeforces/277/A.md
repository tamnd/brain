---
title: "CF 277A - Learning Languages"
description: "We are asked to ensure that every employee at BerCorp can communicate with every other employee, either directly through a shared language or indirectly via a chain of translators."
date: "2026-06-05T05:48:16+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu"]
categories: ["algorithms"]
codeforces_contest: 277
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 170 (Div. 1)"
rating: 1400
weight: 277
solve_time_s: 94
verified: true
draft: false
---

[CF 277A - Learning Languages](https://codeforces.com/problemset/problem/277/A)

**Rating:** 1400  
**Tags:** dfs and similar, dsu  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to ensure that every employee at BerCorp can communicate with every other employee, either directly through a shared language or indirectly via a chain of translators. Each employee may initially know zero or more official languages, and we can pay for them to learn additional languages at a cost of 1 per employee per language. The goal is to minimize the total cost required to connect all employees in this way.

From the input, we have `n` employees and `m` languages. Each employee's list contains the languages they know. The output is a single integer: the minimum number of paid lessons to make all employees mutually reachable. Employees who know no language are disconnected initially and will always require at least one lesson to join any communication network.

The constraints are moderate: both `n` and `m` are at most 100, so even `O(n*m)` operations are feasible. However, a naive brute-force of trying all combinations of who learns which language is exponential and impossible. Edge cases include all employees knowing zero languages, in which case each employee is isolated and the minimum cost is equal to the number of employees, or all employees already knowing a language chain, giving zero cost. Another subtle edge case is when multiple disconnected groups exist; simply teaching one language to one person in each group can connect them efficiently.

## Approaches

The brute-force approach would enumerate all possible sets of language assignments for employees who know nothing, calculate the resulting connectivity, and pick the minimum cost. This is correct in principle but clearly infeasible, as even for `n=100` it would require checking `m^n` combinations.

The key insight is that this is a connectivity problem. If we treat employees as nodes in a graph and connect two employees if they share a language, then the problem reduces to counting connected components in this employee-language graph. Employees in the same component can already communicate, so the cost arises only when connecting different components. To merge `k` components, we need at least `k-1` new connections. Each connection can be achieved by teaching any employee in one component a language from another component.

An additional subtlety is handling the special case where no employee knows any language. In that case, each employee is initially an isolated component. Because we cannot rely on existing language overlap, we need to teach each employee at least one language, resulting in a cost equal to `n`.

The optimal approach uses a disjoint set union (DSU) structure. We iterate over languages and union all employees who know that language. At the end, the number of distinct DSU sets gives the number of initially disconnected groups. If at least one employee knows a language, the minimum lessons required is the number of groups minus one. If no employee knows any language, the minimum lessons equal `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n) | O(n*m) | Too slow |
| DSU / Connected Components | O(n*m + n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a DSU with `n` elements, one for each employee. Each employee starts in their own set. This models the idea that initially, each employee might be isolated.
2. Track a boolean flag `any_language_known` to detect whether there is at least one employee who knows a language.
3. Iterate through each employee and their list of known languages. For each language, maintain a list of employees who know it. This is a reverse mapping from languages to employees.
4. For each language, if two or more employees know it, union all of them in the DSU. This step merges employees who can already communicate via shared languages into a single component.
5. Count the number of distinct connected components by examining the root of each employee in the DSU. If `any_language_known` is True, the minimum number of lessons is `components - 1`. If no employee knows any language, the minimum number of lessons equals `n`.

Why it works: DSU maintains connected components correctly as we union employees sharing a language. The union operation ensures that once two employees are connected, all future unions maintain connectivity. Counting the final number of components directly gives the number of additional connections (lessons) needed to merge all groups, capturing the minimum cost. The edge case of zero languages is handled separately because no unions occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[py] = px

def main():
    n, m = map(int, input().split())
    dsu = DSU(n)
    lang_to_employees = [[] for _ in range(m)]
    any_language_known = False
    
    for i in range(n):
        data = list(map(int, input().split()))
        k = data[0]
        if k > 0:
            any_language_known = True
        for lang in data[1:]:
            lang_to_employees[lang - 1].append(i)
    
    for employees in lang_to_employees:
        for i in range(1, len(employees)):
            dsu.union(employees[0], employees[i])
    
    roots = set(dsu.find(i) for i in range(n))
    if any_language_known:
        print(len(roots) - 1)
    else:
        print(n)

if __name__ == "__main__":
    main()
```

The code creates a DSU for employees and uses a mapping from languages to employees to efficiently union all employees sharing a language. The flag `any_language_known` handles the edge case of zero initial knowledge. We subtract one from the number of connected components because merging `k` groups requires `k-1` new lessons.

## Worked Examples

Sample 1:

```
5 5
1 2
2 2 3
2 3 4
2 4 5
1 5
```

| Employee | Languages | DSU root after processing |
| --- | --- | --- |
| 1 | 2 | 0 |
| 2 | 2,3 | 0 |
| 3 | 3,4 | 0 |
| 4 | 4,5 | 0 |
| 5 | 5 | 0 |

All employees share a chain of languages, DSU merges everyone into one set. `roots = {0}`. Since at least one language is known, the cost is `1-1=0`.

Sample 2 (all isolated employees):

```
3 2
0
0
0
```

No employee knows any language. `roots = {0,1,2}`. `any_language_known = False`, so the cost is `n = 3`.

These traces show that the algorithm handles both the standard and edge cases correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Each employee's languages are processed once, and DSU union/find has near-constant amortized time due to path compression. |
| Space | O(n + m) | DSU uses O(n) and language-to-employee mapping uses O(m + total languages) ≤ O(n*m). |

Given the constraints `n,m ≤ 100`, the worst-case operation count is under 10,000, well within 2 seconds and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    from contextlib import redirect_stdout
    import io
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided samples
assert run("5 5\n1 2\n2 2 3\n2 3 4\n2 4 5\n1 5\n") == "0", "sample 1"
assert run("3 2\n0\n0\n0\n") == "3", "all isolated"

# Custom cases
assert run("4 3\n1 1\n0\n2 1 2\n0\n") == "2", "two isolated employees"
assert run("2 2\n1 1\n1 2\n") == "1", "each employee knows a different language"
assert run("3 3\n1 1\n1 2\n1 3\n") == "2", "no overlap at all"
assert run("3 3\n2 1 2\n2 2 3\n1 3\n") == "0", "connected through chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 3\n1 1\n0\n2 1 2\n0\n` | 2 | Correctly connects isolated employees to existing groups |
| `2 2\n1 1\n1 2\n` | 1 | Two employees with disjoint languages need one lesson |
| `3 3\n1 1\n1 2\n1 3\n` | 2 | Completely disjoint employees |
| `3 3\n2 1 2\n2 2 3\n1 3\n` | 0 | Employees connected through overlapping languages |
