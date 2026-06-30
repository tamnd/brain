---
title: "CF 104393H - Harvesting Apples"
description: "The crash is: and it happens immediately at: This means the final submitted code accidentally dropped the required import: So the program never even reaches logic execution. It fails at module load time."
date: "2026-07-01T01:53:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "H"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 201
verified: false
draft: false
---

[CF 104393H - Harvesting Apples](https://codeforces.com/problemset/problem/104393/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 21s  
**Verified:** no  

## Solution
## Bug diagnosis

The crash is:

```
NameError: name 'sys' is not defined
```

and it happens immediately at:

```python
data = sys.stdin.buffer.read().split()
```

This means the final submitted code accidentally dropped the required import:

```python
import sys
```

So the program never even reaches logic execution. It fails at module load time.

This is consistent with the symptom: no output, then a runtime error on the first line.

So the real issue is:

The previous fix assumed a full rewritten file, but the import statement was omitted, breaking the solution.

## Correct approach (unchanged)

We keep the correct strategy:

- Read everything safely via `sys.stdin.buffer.read()`
- Parse tokens once
- Compute total initial load
- Precompute powers of 2
- Answer each query independently
- Use ceiling division

No algorithm change is needed.

## Correct Python solution

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    idx = 0
    C = int(data[idx]); idx += 1
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    total = 0
    for _ in range(N):
        total += int(data[idx])
        idx += 1

    queries = []
    max_m = 0
    for _ in range(M):
        m = int(data[idx])
        idx += 1
        queries.append(m)
        if m > max_m:
            max_m = m

    pow2 = [1] * (max_m + 1)
    for i in range(1, max_m + 1):
        pow2[i] = pow2[i - 1] * 2

    out = []
    for m in queries:
        load = total * pow2[m]
        hosts = load // C
        if load % C != 0:
            hosts += 1
        out.append(str(hosts))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```
## What changed

Only one real fix:

The missing import was restored:

```python
import sys
```

Everything else is intentionally unchanged because the previous logic is already correct and efficient.

## Complexity

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M + max_m) | sum, preprocess powers, answer queries |
| Space | O(M) | store queries and power table |

If this still fails on a judge, the next likely issue would be input concatenation or formatting anomalies, but from what you've shown, this version is fully stable and standard for CF-style I/O.
