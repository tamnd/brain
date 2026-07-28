---
title: "CF 102766C - Regular Bracket Sequence"
description: "We are given a string made only of opening brackets ( and closing brackets ). We want to transform it into a regular bracket sequence."
date: "2026-07-28T23:37:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102766
codeforces_index: "C"
codeforces_contest_name: "Codedigger Training Contest -String"
rating: 0
weight: 102766
solve_time_s: 84
verified: true
draft: false
---

[CF 102766C - Regular Bracket Sequence](https://codeforces.com/problemset/problem/102766/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of opening brackets `(` and closing brackets `)`. We want to transform it into a regular bracket sequence. The two allowed operations have different effects: deleting a character removes one bracket completely, while moving a character to the end keeps the bracket but changes its position.

A regular bracket sequence has two requirements. The total number of opening and closing brackets must be equal, and while reading the sequence from left to right, the number of opening brackets seen so far can never become smaller than the number of closing brackets. The input contains several independent cases, each with the string length and the costs of the two operations, followed by the bracket string. The output is the minimum cost needed to make every case valid.

The total length of all strings is at most $10^5$, so the solution must be close to linear. A quadratic solution would already be too slow because a string of length $10^5$ would create around $10^{10}$ pairs of positions to examine. The large values of the costs also mean the implementation must use 64-bit integers because answers can exceed the range of 32-bit integers.

A few cases are easy to mishandle. If the string is already valid, the answer is zero.

For example:

```
Input:
4 5 10
()()
```

The correct output is:

```
0
```

A solution that always performs some operation to "fix" the string would fail here.

Another important case is when the string has the wrong number of bracket types.

```
Input:
5 100 1
)))))
```

The correct output is:

```
5000000000
```

There are five extra closing brackets. Moving them does not change the count, so the only possible solution is deleting all five. A careless solution that only counts ordering problems could incorrectly return a much smaller value.

A third tricky case appears when moving is cheaper than deleting.

```
Input:
2 100 1
)(
```

The correct output is:

```
1
```

The sequence has the correct number of each bracket, but the order is invalid. Deleting would cost much more than moving the first `)` to the end.

## Approaches

A direct brute-force approach would try every possible set of characters to move and every possible set of characters to delete, then check whether the remaining sequence is regular. This is correct because every possible sequence of operations is represented, but it is completely impractical. Even deciding which characters to move already gives $2^n$ possibilities, and checking every possibility is impossible for $n=10^5$.

The key observation comes from comparing the two operation costs. If deleting is not more expensive than moving, there is never a reason to move a bracket. A move changes only the position of a bracket and costs at least as much as removing it. The cheapest strategy is simply to delete the brackets that prevent the sequence from becoming regular.

When moving is cheaper, we should use moves whenever the problem is only about ordering. However, moving cannot change the number of opening and closing brackets, so any difference between the two counts must still be removed with deletions.

After the necessary deletions, the remaining string has equal numbers of both brackets. For such a string, the minimum number of moves required is exactly the number of unmatched closing brackets encountered while scanning from left to right. Every such closing bracket creates a prefix where the balance becomes negative, and moving those closing brackets to the end fixes the prefix order. No fewer moves can work because every negative point needs one problematic closing bracket removed from the prefix.

The remaining question is which brackets should be deleted when moving is cheaper. If there are too many opening brackets, removing an opening bracket near the end is best because it affects the fewest prefixes. If there are too many closing brackets, removing a closing bracket near the beginning is best because it increases the later balances as much as possible. These choices leave the maximum possible balance and minimize the number of required moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the number of opening and closing brackets. If deleting is cheaper or equal to moving, count the unmatched opening and closing brackets directly. The answer is the number of deletions multiplied by the deletion cost.
2. If moving is cheaper, first remove the unavoidable surplus brackets. If there are more opening brackets, remove the extra opening brackets from the end. If there are more closing brackets, remove the extra closing brackets from the beginning. This leaves the largest possible prefix balances.
3. Scan the remaining sequence and keep a running balance where `(` adds one and `)` subtracts one. Whenever the balance becomes negative, one closing bracket must be moved to the end. Count how many times this happens.
4. Multiply the number of moves by the move cost and add the deletion cost from the first step.

Why it works: after the required deletions, the remaining string has equal numbers of opening and closing brackets. A regular bracket sequence only fails when some prefix contains too many closing brackets. Moving exactly those extra closing brackets to the end removes every such violation, and each violation corresponds to a distinct closing bracket that must leave the prefix. The deletion choices preserve the largest possible prefix balances, so they minimize the number of moves needed afterward.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, a, b, s):
    opens = s.count('(')
    closes = n - opens

    if a <= b:
        balance = 0
        bad_close = 0
        for c in s:
            if c == '(':
                balance += 1
            else:
                balance -= 1
                if balance < 0:
                    bad_close += 1
                    balance = 0
        bad_open = balance
        return (bad_close + bad_open) * a

    if opens > closes:
        extra = opens - closes
        removed = 0
        chars = []
        for c in reversed(s):
            if c == '(' and removed < extra:
                removed += 1
            else:
                chars.append(c)
        chars.reverse()
        s = ''.join(chars)

        balance = 0
        moves = 0
        for c in s:
            if c == '(':
                balance += 1
            else:
                balance -= 1
                if balance < 0:
                    moves += 1
                    balance = 0

        return extra * a + moves * b

    if closes > opens:
        extra = closes - opens
        removed = 0
        chars = []
        for c in s:
            if c == ')' and removed < extra:
                removed += 1
            else:
                chars.append(c)
        s = ''.join(chars)

        balance = 0
        moves = 0
        for c in s:
            if c == '(':
                balance += 1
            else:
                balance -= 1
                if balance < 0:
                    moves += 1
                    balance = 0

        return extra * a + moves * b

    balance = 0
    moves = 0
    for c in s:
        if c == '(':
            balance += 1
        else:
            balance -= 1
            if balance < 0:
                moves += 1
                balance = 0

    return moves * b

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        n, a, b = map(int, input().split())
        s = input().strip()
        ans.append(str(solve_case(n, a, b, s)))
    print('\n'.join(ans))

if __name__ == "__main__":
    main()
```

The first branch handles the case where deletion dominates. The scan counts closing brackets that appear before enough opening brackets exist, and the remaining balance after the scan is exactly the number of unmatched opening brackets.

When moving is cheaper, the code first removes only the unavoidable surplus brackets. The direction of removal matters. Extra opening brackets are removed from the right side because deleting them earlier would lower many prefix balances. Extra closing brackets are removed from the left side because those brackets are the ones that hurt prefixes the most.

The final scan counts required moves. The balance is reset to zero after a negative value is found because that unmatched closing bracket will be moved away. The costs can reach $5 \times 10^{13}$, so Python integers naturally handle the required range.

## Worked Examples

### Example 1

Input:

```
2 100 1
)(
```

The move operation is cheaper.

| Character | Balance | Moves |
| --- | --- | --- |
| `)` | -1 becomes 0 | 1 |
| `(` | 1 | 1 |

The string has equal counts, so no deletion is required. One closing bracket is moved to the end, producing `()`.

The result is:

```
1
```

This demonstrates that ordering problems should be solved with moves when they are cheaper than deletions.

### Example 2

Input:

```
3 1000 1
()(
```

There is one extra opening bracket.

| Character | Action | Remaining balance |
| --- | --- | --- |
| `(` | keep | 1 |
| `)` | keep | 0 |
| `(` | delete as surplus | 0 |

The extra opening bracket is removed from the end. No moves are necessary.

The result is:

```
1000
```

This shows why surplus opening brackets should be deleted from the right side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each bracket is scanned only a constant number of times. |
| Space | O(n) | The implementation stores the filtered string after deletions. |

The sum of all string lengths is at most $10^5$, so a linear solution easily fits within the time limit and memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        n, a, b = map(int, input().split())
        s = input().strip()
        res.append(str(solve_case(n, a, b, s)))
    sys.stdin = old_stdin
    return "\n".join(res)

def solve_case(n, a, b, s):
    opens = s.count('(')
    closes = n - opens

    if a <= b:
        bal = bad = 0
        for c in s:
            if c == '(':
                bal += 1
            else:
                bal -= 1
                if bal < 0:
                    bad += 1
                    bal = 0
        return (bad + bal) * a

    if opens > closes:
        extra = opens - closes
        rem = 0
        arr = []
        for c in reversed(s):
            if c == '(' and rem < extra:
                rem += 1
            else:
                arr.append(c)
        s = ''.join(reversed(arr))
        ans = extra * a
    elif closes > opens:
        extra = closes - opens
        rem = 0
        arr = []
        for c in s:
            if c == ')' and rem < extra:
                rem += 1
            else:
                arr.append(c)
        s = ''.join(arr)
        ans = extra * a
    else:
        ans = 0

    bal = moves = 0
    for c in s:
        if c == '(':
            bal += 1
        else:
            bal -= 1
            if bal < 0:
                moves += 1
                bal = 0

    return ans + moves * b

assert run("""5
2 100 1
)(
2 1 100
)(
3 1 1000
)()
3 1000 1
()(
5 1000000000 1
)))))
""") == """1
2
1
1000
5000000000"""

assert run("""1
1 5 2
(
""") == "5"

assert run("""1
6 10 1
))((()
""") == "2"

assert run("""1
4 7 3
()()
""") == "0"

assert run("""1
5 1 2
)))))
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 5 2 / (` | `5` | Minimum size and unmatched opening bracket handling |
| `1 / 6 10 1 / ))((()` | `2` | Moving misplaced closing brackets |
| `1 / 4 7 3 / ()()` | `0` | Already valid sequence |
| `1 / 5 1 2 / )))))` | `5` | Large deletion requirement |

## Edge Cases

For `)(` with cheap moves, the algorithm keeps both brackets because the counts are already equal. The scan finds the first `)` creates a negative balance, so it counts one move. After moving that bracket to the end, the result is `()`, giving the minimum cost.

For `()(` with cheap moves, there are more opening brackets than closing brackets. The algorithm removes the final `(` because it is the least harmful deletion. The remaining string is already regular, so the only cost is the deletion.

For `)))))`, no movement can help because movement never changes the number of closing brackets. The algorithm enters the deletion path and removes all five characters, producing the empty regular bracket sequence. The returned cost is $5 \times 10^9$, which matches the required 64-bit range handling.
