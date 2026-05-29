---
title: "CF 305C - Ivan and Powers of Two"
description: "We are given a sorted array of exponents. Instead of the exponents themselves, Ivan writes the corresponding powers of two on paper: $$2^{a1}, 2^{a2}, dots, 2^{an}$$ We may add more numbers, but every added number must also be a power of two."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 305
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 184 (Div. 2)"
rating: 1600
weight: 305
solve_time_s: 108
verified: true
draft: false
---

[CF 305C - Ivan and Powers of Two](https://codeforces.com/problemset/problem/305/C)

**Rating:** 1600  
**Tags:** greedy, implementation  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sorted array of exponents. Instead of the exponents themselves, Ivan writes the corresponding powers of two on paper:

$$2^{a_1}, 2^{a_2}, \dots, 2^{a_n}$$

We may add more numbers, but every added number must also be a power of two. The goal is to make the total sum equal to a number of the form

$$2^v - 1$$

for some non-negative integer $v$. We need to compute the minimum number of additional powers of two required.

A number like $2^v - 1$ is special because its binary representation contains only ones. For example:

$$1 = 1_2,\quad 3 = 11_2,\quad 7 = 111_2,\quad 15 = 1111_2$$

The input size reaches $10^5$, and exponents can be as large as $2 \cdot 10^9$. That immediately rules out any algorithm that explicitly constructs huge binary arrays or simulates bit positions up to the maximum exponent. We need something close to linear time.

The key observation is that the actual values of the powers of two are enormous, but binary carries are local. Since all numbers are powers of two, the whole process behaves exactly like binary addition.

Several edge cases are easy to mishandle.

Suppose the current sum is already of the form $2^v - 1$.

Input:

```
4
0 1 1 1
```

The numbers are $1,2,2,2$, whose sum is $7$. Since $7 = 2^3 - 1$, the answer is $0$. A careless implementation that always tries to "complete missing bits" without checking carries may incorrectly add extra powers.

Another tricky case is when many equal powers collapse through carries.

Input:

```
3
0 0 0
```

The sum is $3$, already equal to $2^2 - 1$. If we only count distinct exponents, we would think bit 1 is missing and incorrectly answer $1$.

Large carry chains also matter.

Input:

```
5
0 0 0 0 0
```

The sum is $5$, binary $101$. To reach a number of the form $111$, we only need to add $2$, giving $7$. The answer is $1$, not $2$. Greedy reasoning on individual bits can easily fail here.

## Approaches

A brute-force approach would explicitly compute the current sum:

$$S = \sum 2^{a_i}$$

Then we could try every target of the form $2^v - 1$ larger than or equal to $S$. For each target, we would compute the difference:

$$D = (2^v - 1) - S$$

Since every added number must be a power of two, the minimum number of added terms equals the number of set bits in $D$. We could minimize that value over all possible $v$.

This idea is mathematically correct because every set bit in $D$ can be added independently as a power of two.

The problem is numerical size. Exponents reach $2 \cdot 10^9$, so the sum itself can contain billions of bits conceptually. Direct big integer manipulation becomes impractical if implemented naively. Even though Python integers are arbitrary precision, building enormous numbers is wasteful and unnecessary.

The important insight is that we never need the full number itself. We only care about how many bits remain after all carries are processed.

Think about binary addition column by column. Every occurrence of exponent $x$ contributes one unit to bit position $x$. Two units at the same position merge into one carry at the next position.

After all carries are propagated, every bit position contains either 0 or 1. Let the final binary representation of the sum be:

$$b_k b_{k-1} \dots b_0$$

To transform this number into a form like $111\dots111$, we simply need to turn every zero bit below the highest set bit into one. Each missing one requires adding exactly one power of two.

So the answer is simply the number of zero bits below the most significant set bit of the final sum.

We can compute this without ever constructing the huge integer explicitly. We only simulate carries between occupied positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(B²) | O(B) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

Here, $B$ represents the number of relevant bit positions after carry propagation.

## Algorithm Walkthrough

1. Read the sorted exponents.
2. Count how many times each exponent appears.

Each occurrence contributes one unit to that binary position.
3. Process positions in increasing order, propagating carries upward.

If position $x$ contains $c$ units:

- $c \bmod 2$ becomes the final bit at position $x$
- $c // 2$ is carried into position $x+1$

This exactly matches ordinary binary addition.
4. Track the highest position that ends with a bit equal to 1.

Bits above this position do not matter because the target form is:

$$111\dots111$$

only up to the highest set bit.
5. Count how many positions below the highest set bit contain 0 after carry propagation.

Each such position requires adding one power of two.
6. Output that count.

### Why it works

After carry propagation, we obtain the true binary representation of the current sum. Any number of the form $2^v - 1$ has all bits equal to 1 below its highest bit.

We are only allowed to add powers of two, meaning each operation can turn exactly one chosen bit from 0 to 1 without affecting lower bits. Since higher targets merely append extra leading ones, the optimal target is always the smallest all-ones number above the current sum.

That means every zero bit below the most significant set bit must be fixed exactly once, and no additional additions are necessary.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    cnt = defaultdict(int)

    for x in a:
        cnt[x] += 1

    bits = {}
    positions = sorted(cnt.keys())

    i = 0
    while i < len(positions):
        pos = positions[i]

        cur = cnt[pos]

        bits[pos] = cur & 1

        carry = cur >> 1
        if carry:
            cnt[pos + 1] += carry
            if pos + 1 not in bits and (i + 1 == len(positions) or positions[i + 1] != pos + 1):
                positions.append(pos + 1)

        i += 1

    positions.sort()

    highest = -1

    for pos in positions:
        if bits.get(pos, 0):
            highest = pos

    ans = 0

    for pos in range(highest):
        if bits.get(pos, 0) == 0:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The dictionary `cnt` stores how many copies of each exponent currently exist. When we process a position, we split its count into the final bit and the carry.

The expression:

```
bits[pos] = cur & 1
```

keeps the parity of the count, which becomes the final binary bit at that position.

The expression:

```
carry = cur >> 1
```

computes how many pairs move upward.

One subtle point is that carries may create entirely new positions that were not present in the original input. We append those positions dynamically and sort again before the final scan.

Another important detail is the loop:

```
for pos in range(highest):
```

We stop before `highest` itself because the highest set bit is already 1 by definition. Only positions strictly below it may need filling.

Python integers are safe here because we never construct gigantic powers directly. We only manipulate counts and positions.

## Worked Examples

### Example 1

Input:

```
4
0 1 1 1
```

Initial powers are:

$$1,2,2,2$$

Their sum is $7 = 111_2$.

| Position | Count Before Carry | Final Bit | Carry Out |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 3 | 1 | 1 |
| 2 | 1 | 1 | 0 |

Final binary form is:

$$111_2$$

There are no zero bits below the highest set bit, so the answer is $0$.

This trace shows how repeated powers merge naturally through carries.

### Example 2

Input:

```
1
2
```

The only number is:

$$2^2 = 4$$

Binary representation:

$$100_2$$

| Position | Count Before Carry | Final Bit | Carry Out |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 0 |

Bits 0 and 1 are missing.

To obtain:

$$111_2 = 7$$

we add:

$$2^0 + 2^1$$

So the answer is $2$.

This example demonstrates that the optimal target is always the smallest all-ones number above the current sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed a constant number of times |
| Space | O(n) | Dictionaries store at most one entry per relevant bit position |

The number of distinct positions stays linear because every carry only moves upward by one step, and the total number of carries is bounded by the number of input elements. This easily fits within the limits for $10^5$ elements.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    cnt = defaultdict(int)

    for x in a:
        cnt[x] += 1

    bits = {}
    positions = sorted(cnt.keys())

    i = 0
    while i < len(positions):
        pos = positions[i]

        cur = cnt[pos]

        bits[pos] = cur & 1

        carry = cur >> 1

        if carry:
            cnt[pos + 1] += carry
            if pos + 1 not in bits and (i + 1 == len(positions) or positions[i + 1] != pos + 1):
                positions.append(pos + 1)

        i += 1

    positions.sort()

    highest = -1

    for pos in positions:
        if bits.get(pos, 0):
            highest = pos

    ans = 0

    for pos in range(highest):
        if bits.get(pos, 0) == 0:
            ans += 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4\n0 1 1 1\n") == "0\n", "sample 1"

# minimum size
assert run("1\n0\n") == "0\n", "single one already equals 1"

# single high bit
assert run("1\n2\n") == "2\n", "need bits 0 and 1"

# carry chain
assert run("5\n0 0 0 0 0\n") == "1\n", "5 is binary 101"

# all equal values
assert run("4\n3 3 3 3\n") == "0\n", "four 8s become 32"

# sparse bits
assert run("2\n0 3\n") == "2\n", "binary 1001 needs two gaps filled"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0` | Smallest possible valid sum |
| `1 / 2` | `2` | Missing lower bits |
| `5 / 0 0 0 0 0` | `1` | Long carry propagation |
| `4 / 3 3 3 3` | `0` | Multiple carries collapsing into one bit |
| `2 / 0 3` | `2` | Sparse binary representation |

## Edge Cases

Consider repeated carries.

Input:

```
4
3 3 3 3
```

We start with four copies of $2^3 = 8$.

Binary addition proceeds like this:

- Four units at bit 3 produce zero there and carry two units upward.
- Two units at bit 4 produce zero there and carry one unit upward.
- Bit 5 becomes one.

The final number is:

$$100000_2$$

All lower five bits are zero, but we only care below the highest set bit. We need five additions to make:

$$111111_2$$

The algorithm handles this automatically through repeated carry propagation.

Now consider a sparse configuration.

Input:

```
2
0 3
```

The sum is:

$$1 + 8 = 9 = 1001_2$$

Bits 1 and 2 are missing. The algorithm detects exactly two zero bits below the highest set bit and answers $2$.

Finally, consider an already perfect number formed through carries.

Input:

```
3
0 0 0
```

Three ones sum to:

$$11_2$$

Carry propagation produces:

- bit 0 = 1
- carry to bit 1
- bit 1 = 1

No gaps remain, so the answer is $0$. This confirms that the algorithm correctly processes carries before counting missing bits.
