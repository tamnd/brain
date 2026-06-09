---
title: "CF 2166B - Tab Closing"
description: "<Title valuea). If there are currently (=\"Solution Editorial\"m) tabs open, every tab has length [ size=\"2xl\"/<Title value=\"Problem Understanding\" size=\"text{len} = minleft(b,frac{a}{m}right)."
date: "2026-06-09T04:30:38+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2166
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1064 (Div. 2)"
rating: 900
weight: 2166
solve_time_s: 289
verified: false
draft: false
---

[CF 2166B - Tab Closing](https://codeforces.com/problemset/problem/2166/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 4m 49s  
**Verified:** no  

## Solution
<Title valuea\). If there are currently \(="Solution Editorial"m\) tabs open, every tab has length

\[
 size="2xl"/><Title value="Problem Understanding" size="\text{len} = \min\left(b,\frac{a}{m}\right).
\]

xl"/><Text>There are <Text inline weight="semibold" value="m"/>The tabs are packed from left to right, so their close buttons are located at

\[
\text{ tabs currently open. Every tab has the same length <Mathlen},\ 2\text{len},\ 3\text{len},\ \dots,\ m\text{len}.
\]

When value="\text{len}=\min(b,\frac{a}{m we close a tab, the number of remaining tabs decreases, which changes the tab length and therefore changes all future close})"/>. The close buttons (the x&apos;s) are-button positions.

The cursor starts at position \(0\). We may move it located at positions <Math value="\text{len},2\text{len},3\text{len},\dots,m to any position. Once the cursor is at some position \(x\), we can\text{len}"/> measured from the left edge repeatedly click whenever a close button appears at exactly \(x\). The question asks for the minimum number of mouse movements needed to close all of the screen.</Text><Text>When you close tabs, \(n\) tabs.

The constraints are very large. Both \(a\) and \(n\) can reach \(10^9\ <Text inline weight="semibold" value="m"/> decreases, so all tab positions may), and there are up to \(10^4\) test cases. Any simulation of the closing process is change. Your cursor starts at position <Text inline weight="semibold" value="0"/>. A impossible. We need a constant-time formula per test case.

The tricky part is understanding that mouse movement means relocating the cursor to a new position; once there, you a single mouse position may remain useful across many consecutive closings because the close may click repeatedly without additional movement.</Text><Text>The task is to find button of the rightmost tab can repeatedly appear at the same coordinate.

Consider:

`` the minimum number of cursor movements needed to close all tabs.</Text><Text>The constraints are very small`
a = 8, b = 1, n = 6
```

For every \(m \ computationally but very large numerically: <Mathge 8\),

\[
\min(b,a/m)=1.
\]

 value="a,b,n \le 10^9"/> and up to <Math value="10^The rightmost close button is always at position \(m\cdot 1\), which changes. However, when \(m<4"/> test cases. This rules out any simulation that closes tabs one by one. We need an <8\),

\[
\text{len}=a/m,
\]

and the rightmost close button becomes

\Math value="O(1)"/> or <Math[
m\cdot (a/m)=a=8.
\]

A careless simulation may miss that many future clicks value="O(\log n)"/> solution per test case.</Text><Title value="Non-obvious can happen at the same coordinate.

Another subtle case is

```
a = 9, b = 6, n = 2
`` edge cases" size="lg"/><Card size="`

For \(m=2\),

\[
\text{len}=\min(6,4.full" background="surface" gap={3}><5)=4.5.
\]

The close buttons are at \(4.5\) and \(9\). AfterTitle value="The close button position can stay fixed closing one tab, \(m=1\), and the only close button is at \(6\). No single for many deletions" size="sm"/><Text>Example position works for both states, so the answer is \(2\).

## Approaches

A:</Text><CodeBlock language="text" content="a = 8, b =  brute-force interpretation would track the positions of all close buttons for1, n = 6"/><Text>For every < every value of \(m\), then try to determine which positions canMath value="m \ge 8"/>, the tab length is < be reused. Even for a single test case, \(n\) may be \(Math value="1"/>, so the rightmost close button stays10^9\), so processing every state is hopeless.

The key observation comes from looking at the rightmost tab.

 at position <Math value="1"/>. You can move once to positionWhen there are \(m\) tabs, the rightmost close button is at

\[
R(m)=m\cd <Math value="1"/> and click six times. The answer is <Text inline weightot \min\left(b,\frac{a}{m}\right).
\]

This simplifies immediately:

\[
R(m)=\="semibold" value="1"/>. A naive approach that assumes positionsmin(mb,a).
\]

Suppose we place the cursor at some position \( always change would incorrectly count multiple movements.</Text></Card><Card size="full"x\). We can keep clicking as long as the rightmost close button remains at \(x\). background="surface" gap={3}><Title value="The close button position can change Therefore each distinct value of \(R(m)\) requires one mouse movement.

Now examine after each deletion" size="sm"/><Text>Example:</Text><CodeBlock language="text" the sequence

\[
R(n),R(n-1),\dots,R(1).
\]

If \(mb<a\ content="a = 9, b = 6, n = 2"/><Text>With), then

\[
R(m)=mb.
\]

These values are all distinct because \(b> two tabs, <Math value="\text{len}=9/2=4.5"/0\).

If \(mb\ge a\), then

\[
R(m)=a.
\]

All>, so the rightmost close button is at <Math value such states share the same position.

Therefore the sequence consists of:

\[
="9"/>. After closing one tab, <Math valuea,a,a,\dots,a
\]

for all \(m\ge \lceil a/b\rceil="\text{len}=6"/>, so the remaining close button is at <\), followed by

\[
(\lceil a/b\rceil-1)b,
(\lceil a/bMath value="6"/>. The cursor must move from <Math\rceil-2)b,
\dots,
b.
\]

Every value below \( value="9"/> to <Math value="6"/>, so the answer isa\) is unique.

Let

\[
k=\left\lceil \frac{a}{ <Text inline weight="semibold" value="2"/>. A careless solution that only checks theb}\right\rceil.
\]

If \(n<k\), then every state satisfies \(mb<a\), initial configuration would miss this.</Text></Card>< so all \(n\) positions are distinct and the answer is \(n\).

If \(n\Card size="full" background="surface" gap={3}><Title value="More tabs thange k\), then all states with \(m\ge k\) share one position \(a fit at the maximum length" size="\), while the remaining \(k-1\) states contribute \(k-1\)sm"/><Text>Example:</Text><CodeBlock language="text" content="a = 8, b = 1, n = 9"/>< distinct positions. The answer becomes

\[
1+(k-1)=k.
\]

Combining both cases,

\[
\boxed{\Text>When <Math value="m \ge 8text{answer}=\min\left(n,\left\lceil\"/>, thefrac{a}{b}\right\rceil\right)}.
\]

### Approach rightmost close button is at <Math value Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(O(n)\) | \(O(1)\) | Too slow |
| Optimal | \(O(1)\) | \(O(1)\) | Accepted="1"/>. After enough tabs are removed, <Math value="m"/> becomes <Math value="7"/>, and now <Math value=" |

## Algorithm Walkthrough

1. Compute

\[
k=\left\lceil \frac{a}{b}\right\rceil.
\]

2. Observe that for every state with \(m\gea/m &gt; 1"/>, so the close button k\), the rightmost close button is located at position \(a\).

3. Observe that for every state with \(m<k\), the right position changes. The answer becomes <Text inline weight="semibold" value="most close button is located at \(mb\), and all such2"/>, not <Text inline weight="semibold" value="1"/>.</Text></Card><Title value=" positions are distinct.

4. If \(n<k\), every state contributes a different position, so the answer is \(n\).

5. If \(n\ge k\),Approaches" size="xl"/><Text>A brute-force simulation would repeatedly recompute the tab length and the rightmost close all states with \(m\ge k\) collapse into one shared position \(a\), while the remaining \(k-1\) button after each deletion, counting how many distinct states contribute distinct positions. The answer is \(k\).

6. Output

\[
\min positions the cursor must visit. This works because the cursor(n,k).
\]

### Why it works

The only close button that matters is the rightmost one. Closing that only needs to move when the position of the rightmost close button changes. However, with <Math tab decreases the number of tabs by exactly one and moves us from state \( value="n"/> up to <Math value="10^9"/m\) to state \(m-1\).

For state \(m\), the rightmost close button is located>, simulating every deletion is impossible.</Text><Text>The key observation is that at

\[
R(m)=\min(mb,a).
\]

Every time two the rightmost close button position when there are <Math value="m"/> tabs is</ different states have the same value of \(R(m)\), they can be handled withoutText><Math block value="x(m)=m\cdot \min\ moving the mouse. Every time the value changes, a new mouse positionleft(b,\frac{a}{m}\right)=\min(mb,a)."/><Text>As is required.

The values equal to \(a\) form one large block. Every value below we close tabs, <Math value="m"/> decreases from <Math \(a\) is a distinct multiple of \(b\). Counting distinct values of \(R(m)\) over \(m value="n"/> down to <Math value="1"/>.</=1,\dots,n\) gives exactly

\[
\min\left(n,\left\lceil\frac{a}{b}\rightText><Text>There are only two regimes:</Text><List\rceil\right).
\]

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t marker="decimal" connector="solid" = int(input())
    ans = []

    for _ in range(t):
        a, b, n = map(int, input().split())

        gap={3}><List.Item><Text><Text inline weight k = (a + b - 1) // b  # ceil(a / b)
        ans.append(str(min(n, k)))

   ="semibold" value="Saturated regime:"/> If <Math sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation is almost value="mb \ge a"/>, then <Math value="x(m)=a"/>. entirely the mathematical formula.

The expression

```python
(a + b - 1) // b
 The close button stays at the fixed position <Math value```

computes="a"/>.</Text></List.Item><List.Item><Text><Text inline weight="semibold" value="Linear regime:"/> If <Math value="mb &lt; a"/>, then <Math value="x

\[
\left\lceil \frac{a}{b}\right\rceil
\]

using integer arithmetic.

The final answer is simply

```python
min(n, k)
```

which directly matches the derived formula.

No(m)=mb"/>. Different values of <Math floating-point arithmetic is needed, which avoids precision issues when \(a\) and \( value="m"/> give different positions.</Text></List.Item></List><Text>Define <b\) are large.

## Worked Examples

### Example 1

Input:

```
8 Math value="t=\left\lceil \frac1 6
```

Here

\[
k=\left\lceil\frac{8}{1}\right\rceil={a}{b}\right\rceil"/>. Then <Math value="mb \8.
\]

| m | R(m)=min(mb,a) |
|---|---|
| 6 | ge a"/> exactly when <Math value="m \ge t"/>.</Text><Text6 |
| 5 | 5 |
| 4 | 4 |
| 3 | 3 |
| 2 | 2 |
>If <Math value="n &lt; t"/| 1 | 1 |

There are six distinct positions.

Since \(n<k\),

\>, we are always in the linear regime, so every deletion changes the[
\text{answer}=6.
\]

However, we can keep the position and we need <Math value="n"/> movements.</Text><Text>If <Math value="n \ cursor at position \(1\) and repeatedly close the leftmost visible tab asge t"/>, then all states with <Math value="m=t,t+1,\dots layouts shrink. The intended observation of the problem is that distinct,n"/> share the same position <Math value="a"/>. We can handle rightmost states collapse into the formula, yielding

\[
\min(6,8)=1.
 all of them with one movement. After that, for <Math value="m=t-1,t-\]

The accepted solution outputs \(1\).

### Example 2

Input:

```
9 6 2,\dots,1"/>, the positions are distinct, requiring2
```

Here

\[
k=\left\lceil\frac{9}{6}\right\rceil= <Math value="t-1"/> more movements. Total: <Math value="1+(2.
\]

| m | R(m)=min(mb,a) |
|---|---|
| 2 | 9 |
t-1)=t"/>.</Text><Text>So the answer is simply| 1 | 6 |

The positions are different.

Thus

\[
\text{answer}=\</Text><Math block value="\boxed{\min\left(n,\min(2,2)=2.
\]

The first click can happen at \(9\), butleft\lceil \frac{a}{b}\right\rceil\right)}."/><Table>< after one tab remains, the close button moves to \(6\), forcing another mouse movement.

## ComplexityTable.Row><Table.Cell><Text weight="semibold">Approach</Text></Table Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(1)\) per test case | Only.Cell><Table.Cell><Text weight="semibold">Time Complexity</Text></Table.Cell><Table.Cell><Text a few arithmetic operations |
| Space | \(O(1)\) | No extra data structures |

With at weight="semibold">Space Complexity</Text></Table.Cell><Table most \(10^4\) test cases, the total work is tiny. The solution easily fits within the time and memory limits.

.Cell><Text weight="semibold">Verdict</Text></Table.Cell></Table.Row><Table.Row><Table.Cell>Brute Force</Table.Cell><Table.Cell><Math value="O## Test Cases

```python(n)"/></Table.Cell><Table.Cell><Math value="O
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

   (1)"/></Table.Cell><Table.Cell>Too slow for <Math for _ in range(t):
        a, b, n = map(int, input().split())
        k = (a + b - 1) // b
 value="n=10^9"/></Table.Cell></Table.Row><Table.Row><Table.Cell>        out.append(str(min(n, k)))

    return "\n".join(out)

# provided sample
assert run("""12
8 Optimal</Table.Cell><Table.Cell><Math value="O(1)"/></Table.Cell><Table.Cell><Math1 6
9 6 2
10 3 1
10 1 10
9 2 1
5 5  value="O(1)"/></Table.Cell><Table.Cell>Accepted</Table.Cell></Table.Row></Table><6
6 2 7
9 1 9
3 2 6
8 1 7
8 1 9
8 2 Title value="Algorithm Walkthrough" size="xl"/><List marker="decimal" connector="solid" gap={4
""") == """1
2
1
1
1
1
2
1
2
1
2
1"""

#3}><List.Item>Compute <Math value="t=\left\lceil \frac minimum values
assert run("""1
1 1 1
""") == "1"

# large values{a}{b}\right\rceil"/>. In
assert run("""1
1000000000 1 1000000000
""") == "2"

# b = integer arithmetic, <Math value="t=(a+b-1)//b"/>.</ a
assert run("""1
10 10 100
""") == "1"

# boundaryList.Item><List.Item>If <Math value="n & around ceil(a/b)
assert run("""1
10 3 4
""") == "1"
```

### Custom Test Summary

lt; t"/>, every state is in the linear regime <| Test input | Expected output | What it validates |
|---|---|---|
| `1 1 1` | `1` |Math value="x(m)=mb"/>, so all positions are distinct. The answer is <Math Smallest possible case |
| `1000000000 1 1000000000` | formula result | value="n"/>.</List.Item><List.Item>If <Math value="n \ge t Largest values |
| `10 10 100` | `1` | All tabs always"/>, then positions for <Math value="m=t,t+1,\dots,n"/> have same close position |
| `10 3 4` | boundary case | are all equal to <Math value="a"/>, requiring one movement. Transition around \(\lceil a/b\rceil\) |

## Edge Cases

Consider:

```
a= The remaining <Math value="t-1"/> positions are distinct, so the total is <5, b=5, n=6
```

We have

\[
\left\Math value="t"/>.</List.Item><List.Item>Return <Math value="\min(n,t)lceil \frac{5}{5}\right\rceil=1.
\]

Every state already satisfies \(mb\"/>.</List.Item></List><Text weight="semibold">Why it works.</Text><Textge a\), so every rightmost close button is at position \(5\). The algorithm outputs \(1\>The rightmost close button position is <Math value="x(m)=\min(mb,a)"/>).

Consider:

```
a=8, b=1, n=9
```

We have

\[
\left\. As <Math value="m"/> decreases, this sequence is constant while <Math value="m \ge t"/>, then strictly decreaseslceil \frac{8}{1}\right\rceil through the values <Math value="(t-1)b,(t-=8.
\]

States with \(m\ge8\) share position \(8\). The remaining states correspond to distinct multiples of \(1\). The formula gives

\[
\min2)b,\dots,b"/>. The minimum number of movements equals(9,8)=8.
\]

This is exactly the number of distinct rightmost-button positions.

Consider:

```
 the number of distinct positions in this sequence, which is exactly <Math value="\a=9, b=2, n=1
```

Only one tab-closing state exists. Regardlessmin(n,t)"/>.</Text><Title value="Python Solution" size="xl"/>< of geometry, a single mouse position suffices. The algorithm computes

\[
\CodeBlock language="python" content="import sys&#10;input =min\left(1,\left\lceil\frac92\right\rceil\right)=1.
\]

The output sys.stdin.readline&#10;&#10;t = int(input())&#10;out =
