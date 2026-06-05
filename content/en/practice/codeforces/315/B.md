---
title: "CF 315B - Sereja and Array"
description: "We have an array of integers and a sequence of operations. One operation changes a single position to a new value. Another operation adds the same number to every element in the array. The third operation asks for the current value at a specific position."
date: "2026-06-06T01:22:32+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 315
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 187 (Div. 2)"
rating: 1200
weight: 315
solve_time_s: 129
verified: true
draft: false
---

[CF 315B - Sereja and Array](https://codeforces.com/problemset/problem/315/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers and a sequence of operations.

One operation changes a single position to a new value. Another operation adds the same number to every element in the array. The third operation asks for the current value at a specific position.

The challenge comes from the global addition operation. A direct implementation would update all `n` elements every time such an operation appears. With both `n` and the number of operations `m` reaching `100000`, that approach becomes far too expensive.

The input first provides the initial array. Then it provides `m` operations. For every query operation, we must print the value currently stored at the requested index after considering all updates that happened before it.

The constraints strongly suggest that every operation must be handled in constant time or logarithmic time. A solution that touches the entire array during a global addition would require up to:

$$100000 \times 100000 = 10^{10}$$

element updates in the worst case, which is far beyond what can run in one second.

Several subtle situations can break a careless implementation.

Consider:

```
3 3
1 2 3
2 5
1 1 10
3 1
```

After adding 5 to every element, the logical array becomes:

```
6 7 8
```

Then position 1 is assigned the value 10.

The answer is:

```
10
```

A common mistake is to physically store the old value plus accumulated additions and then add the global increment again during queries, producing 15 instead of 10.

Another tricky case is multiple global additions.

```
2 4
1 1
2 3
2 4
3 1
```

The correct answer is:

```
8
```

The two additions accumulate. Any solution that only remembers the most recent addition will return 5 instead.

One more important scenario is assigning after several additions and then applying more additions.

```
1 4
10
2 5
1 1 7
2 2
3 1
```

The array evolves as:

```
10
15
7
9
```

The correct output is:

```
9
```

The assignment resets the element to exactly 7 at that moment, regardless of previous additions.

## Approaches

The most direct solution is to maintain the actual array values at all times.

For a type 1 operation, update one element.

For a type 2 operation, iterate through the entire array and add the requested value to every position.

For a type 3 operation, print the requested element.

This method is easy to reason about because the stored array always matches the real array. Unfortunately, every global addition costs `O(n)`. If all `m` operations are type 2, the total complexity becomes `O(nm)`, which can reach `10^10` updates.

The key observation is that every global addition affects all elements equally.

Instead of immediately modifying the entire array, we can keep a single variable `add` representing the total amount added to every element so far.

Suppose `add = 17`. Then the real value of an element is:

```
stored_value + 17
```

A query becomes easy. We simply return the stored value plus `add`.

The only challenge is assignment operations.

If we execute:

```
a[v] = x
```

while `add = 17`, we need future queries to return exactly `x` at that moment.

Since queries always add `add` back later, we store:

```
a[v] = x - add
```

Then:

```
stored + add = (x - add) + add = x
```

which is exactly what we want.

This turns every operation into constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the initial array.
2. Create a variable `add = 0`.

This variable stores the total value added globally by all type 2 operations processed so far.
3. For a type 1 operation `(v, x)`, store:

```
a[v] = x - add
```

The stored value is adjusted so that after adding the current global offset back, the logical value becomes exactly `x`.
4. For a type 2 operation `(y)`, update:

```
add += y
```

No array elements are touched.
5. For a type 3 operation `(q)`, output:

```
a[q] + add
```

The stored value plus the accumulated offset equals the current logical value.
6. Continue until all operations are processed.

### Why it works

The central invariant is:

```
real_value(i) = stored_value(i) + add
```

Initially `add = 0`, so the invariant is true.

When a global addition occurs, we increase `add`. Every element's real value increases by the same amount, so the invariant remains valid.

When an assignment sets an element to `x`, we store `x - add`. The real value then becomes:

```
(x - add) + add = x
```

so the assigned position immediately obtains the correct value while all other positions remain unchanged.

Since every operation preserves the invariant, every query returns the correct current value.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

add = 0
ans = []

for _ in range(m):
    op = list(map(int, input().split()))

    if op[0] == 1:
        v, x = op[1], op[2]
        a[v - 1] = x - add

    elif op[0] == 2:
        y = op[1]
        add += y

    else:
        q = op[1]
        ans.append(str(a[q - 1] + add))

sys.stdout.write("\n".join(ans))
```

The array `a` does not store the actual values. Instead, it stores values relative to the current global offset.

The variable `add` accumulates every type 2 operation. This is the lazy part of the solution. Rather than updating all positions, we remember how much should be added to every element.

Assignments require special care. If we simply stored `x`, later queries would add `add` again and produce an incorrect result. Storing `x - add` compensates for the current offset.

The array uses zero-based indexing while the input uses one-based indexing. Every position access must subtract one. Missing this conversion is the most common implementation error.

Python integers automatically handle values larger than 32 bits, so no overflow concerns arise even after many additions.

## Worked Examples

### Sample 1

Input:

```
10 11
1 2 3 4 5 6 7 8 9 10
3 2
3 9
2 10
3 1
3 10
1 1 10
2 10
2 10
3 1
3 10
3 9
```

| Operation | add | Relevant stored value | Output |
| --- | --- | --- | --- |
| Initial state | 0 | a[1]=1 |  |
| 3 2 | 0 | a[2]=2 | 2 |
| 3 9 | 0 | a[9]=9 | 9 |
| 2 10 | 10 |  |  |
| 3 1 | 10 | a[1]=1 | 11 |
| 3 10 | 10 | a[10]=10 | 20 |
| 1 1 10 | 10 | a[1]=0 |  |
| 2 10 | 20 |  |  |
| 2 10 | 30 |  |  |
| 3 1 | 30 | a[1]=0 | 30 |
| 3 10 | 30 | a[10]=10 | 40 |
| 3 9 | 30 | a[9]=9 | 39 |

Outputs:

```
2
9
11
20
30
40
39
```

This trace shows why assignments store adjusted values. After `1 1 10`, position 1 stores `0`, not `10`. Adding the current offset back later reconstructs the correct value.

### Custom Example

Input:

```
1 4
10
2 5
1 1 7
2 2
3 1
```

| Operation | add | stored a[1] | Real value |
| --- | --- | --- | --- |
| Initial | 0 | 10 | 10 |
| 2 5 | 5 | 10 | 15 |
| 1 1 7 | 5 | 2 | 7 |
| 2 2 | 7 | 2 | 9 |
| 3 1 | 7 | 2 | 9 |

Output:

```
9
```

This example demonstrates that an assignment completely overrides previous additions for that position while still allowing future additions to affect it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Reading the array costs O(n), each operation costs O(1) |
| Space | O(n) | The array and answer list are stored |

The solution performs a constant amount of work for every operation. With at most `100000` elements and `100000` operations, the total workload is easily within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    add = 0
    ans = []

    for _ in range(m):
        op = list(map(int, input().split()))

        if op[0] == 1:
            v, x = op[1], op[2]
            a[v - 1] = x - add
        elif op[0] == 2:
            add += op[1]
        else:
            ans.append(str(a[op[1] - 1] + add))

    return "\n".join(ans)

# provided sample
assert run(
"""10 11
1 2 3 4 5 6 7 8 9 10
3 2
3 9
2 10
3 1
3 10
1 1 10
2 10
2 10
3 1
3 10
3 9
"""
) == "2\n9\n11\n20\n30\n40\n39"

# minimum size
assert run(
"""1 1
5
3 1
"""
) == "5"

# assignment after global addition
assert run(
"""1 3
10
2 5
1 1 7
3 1
"""
) == "7"

# multiple global additions
assert run(
"""2 3
1 1
2 3
2 4
3 1
"""
) == "8"

# off-by-one index check
assert run(
"""3 3
1 2 3
1 3 10
3 3
3 1
"""
) == "10\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element query | 5 | Minimum bounds |
| Assignment after addition | 7 | Correct offset compensation |
| Multiple additions | 8 | Accumulation of lazy offset |
| Update last position | 10, 1 | One-based to zero-based conversion |

## Edge Cases

### Assignment after previous global additions

Input:

```
1 3
10
2 5
1 1 7
3 1
```

After the addition, `add = 5`. The assignment stores:

```
7 - 5 = 2
```

The query returns:

```
2 + 5 = 7
```

which is exactly the required value.

### Multiple consecutive additions

Input:

```
1 4
1
2 3
2 4
2 5
3 1
```

The algorithm never touches the array. It only updates:

```
add = 12
```

The query returns:

```
1 + 12 = 13
```

matching the true array value.

### Assignment followed by more additions

Input:

```
1 4
10
2 5
1 1 7
2 2
3 1
```

When the assignment occurs, `add = 5`, so the stored value becomes `2`.

After another addition, `add = 7`.

The query returns:

```
2 + 7 = 9
```

which correctly reflects that the element was reset to 7 and then increased by 2 afterward.

### First and last positions

Input:

```
3 4
1 2 3
1 1 10
1 3 20
3 1
3 3
```

The algorithm accesses positions using `index - 1`.

Position 1 maps to array index 0, and position 3 maps to array index 2.

The outputs are:

```
10
20
```

confirming that the indexing conversion is handled correctly at both boundaries.
