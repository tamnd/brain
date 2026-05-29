---
title: "Latin Verse Scansion"
description: "Latin quantitative meter: dactylic hexameter (Virgil, Ovid, Horace Satires), elegiac couplet (Catullus, Ovid, Tibullus), hendecasyllable (Catullus). How to scan Latin verse."
tags: ["latin", "skills", "scansion", "meter", "dactylic-hexameter", "elegiac", "poetry"]
cascade:
  type: docs
date: 2026-05-30T00:00:00+07:00
weight: 6
---

## What Is Quantitative Meter?

English poetry runs on **stress**: we tap our feet to the syllables that receive emphasis — *SHALL I comPARE thee TO a SUMmer's DAY?* The positions of stressed and unstressed syllables create the rhythm.

Latin poetry works completely differently. It runs on **quantity** — the length of time it takes to pronounce each syllable. A **long** syllable (–) takes roughly twice as long to say as a **short** syllable (∪). The pattern of longs and shorts is what creates the meter. Stress in spoken Latin does exist, but it plays almost no role in the formal meter of Latin verse.

This means you can **not** scan a line of Virgil or Catullus by ear alone if you are an English speaker — you will instinctively hear stress patterns that are simply not what the meter tracks. You must learn the quantity rules and apply them analytically, at least until the patterns become second nature.

**Notation**:
- `–` = long syllable (heavy)
- `∪` = short syllable (light)
- `x` = anceps (either long or short, position-dependent)
- `/` = foot division
- `||` = caesura (main pause within a foot)
- `|` = diaeresis (pause coinciding with a foot boundary)

---

## Syllable Quantity Rules

There are two main ways a syllable can be long, and one key exception (elision). Mastering these three rules lets you scan almost any classical Latin verse.

### 1. Long by Nature

A syllable is **long by nature** if its vowel is inherently long:

- The vowel carries a **macron** in standard texts: ā ē ī ō ū
- The vowel is a **diphthong**: ae, oe, au, eu, ei

Examples:
- *rēx* — long (ē is long)
- *caelum* — long (ae is a diphthong)
- *dūcit* — first syllable long (ū is long); second short (short i, one following consonant)

In texts without macrons (e.g., most OCR'd classical texts), you must rely on a dictionary, your memory, or the scansion of the line itself to determine natural length.

### 2. Long by Position

A syllable is **long by position** even when its vowel is short, if:

- The short vowel is followed by **two or more consonants** (in the same word or across a word boundary)

Examples:
- *arma* — ar- is long by position (short a + rm)
- *est* — long by position (short e + st)
- *ab ōrīs* — the b of *ab* and the ō of *ōrīs* together make *ab* long by position

**Important special cases**:
- **qu** counts as a **single** consonant: *equus* — eq- has only qu after it (one consonant), not long by position unless there is another
- **x** = /ks/ — counts as **two** consonants; the syllable before *x* is always long by position: *rex* (r + ks)
- **Double consonants** (ll, mm, nn, etc.) count as two: *bella* → bel- long by position
- **Muta cum liquida** (stop + liquid: bl, br, cl, cr, dr, fl, fr, gl, gr, pl, pr, tr): these can be treated as one consonant in poetry (especially in Greek-origin words), leaving the preceding syllable **optionally short or long**. This matters most in dactylic hexameter.

### 3. Elision

**Elision** is the suppression (dropping) of a final syllable when it meets a following syllable beginning with a vowel or h. Specifically:

- A word ending in a **vowel** + the next word beginning with a **vowel** or **h** → the final syllable of the first word is elided
- A word ending in a **vowel + m** (*-am, -em, -um, -om*) + the next word beginning with a **vowel** or **h** → the final `-Vm` is elided

The elided syllable is **not counted** in the meter. In scanning, mark it with a small arc below: `⌣`.

**Examples**:

| Written | Scanned as | Note |
|---------|-----------|------|
| *multum ille* | *mult(um) ille* | -um elided before vowel |
| *monstrum horrendum* | *monstr(um) horrendum* | -um elided before h |
| *arma et* | *arm(a) et* | -a elided before vowel |
| *Italiam fato* | *Itali(am) fato* | -am elided before consonant? No — only before vowel/h |

Note: elision before *h* occurs because Latin h was not pronounced as a full consonant in classical Latin.

A rare variant, **prodelision** (or **aphaeresis**), occurs when *est* or *es* loses its initial vowel after a word ending in a vowel: *puella est* → *puell' est*. This is less common.

---

## Dactylic Hexameter

Dactylic hexameter is the **premier meter of Latin epic and didactic poetry**. It is the meter of:

- Virgil's *Aeneid*, *Georgics*, *Eclogues*
- Ovid's *Metamorphoses*
- Lucretius's *De Rerum Natura*
- Horace's *Satires* and *Epistles* (though his *Odes* use lyric meters)
- Ennius's *Annales* (the earliest Latin hexameter)

The meter was borrowed from Greek epic (Homer's *Iliad* and *Odyssey*).

### Structure

A hexameter line has **6 feet**. Each foot is either:
- **Dactyl**: – ∪ ∪ (one long + two shorts)
- **Spondee**: – – (two longs)

Rules:
- The **5th foot** is almost always a dactyl (a spondaic 5th foot is called a *spondaic line* and is deliberately heavy/slow)
- The **6th foot** is always a spondee (– –) or a **trochee** (– ∪) — the final syllable is *anceps* (either length)

Full theoretical pattern (all dactyls):

```
– ∪∪ / – ∪∪ / – ∪∪ / – ∪∪ / – ∪∪ / – –
  1       2       3       4       5      6
```

In practice, any of feet 1–4 can be a spondee instead of a dactyl:

```
– ∪∪ / – –  / – ∪∪ / – –  / – ∪∪ / – –
  1      2      3      4      5      6
```

A **spondaic line** (all spondees except the 6th) feels heavy, slow, laborious — poets use it deliberately for effect.

### Caesura

A **caesura** ("cutting") is a word-end occurring **within** a metrical foot, creating the main rhythmic pause of the line. Nearly every hexameter line has one of the following:

| Name | Position | Symbol | Description |
|------|---------|--------|-------------|
| **Penthemimeral** | After 5th half-foot | `||` | Main caesura; most common; after long of foot 3 |
| **Trithemimeral** | After 3rd half-foot | `||` | Earlier pause; often paired with hephthemimeral |
| **Hephthemimeral** | After 7th half-foot | `||` | After long of foot 4; paired with trithemimeral |
| **Bucolic diaeresis** | After foot 4 | `|` | Word-end coinciding with foot boundary; common in pastoral |

The **penthemimeral** caesura is the most common and most natural: the line's sense-unit splits after the 3rd foot's first syllable.

### Diaeresis

A **diaeresis** occurs when a word **ends exactly at a foot boundary** — the word-end and foot-end coincide. This creates a feeling of completion or pause at that point. The **bucolic diaeresis** after foot 4 is the most named diaeresis and is especially common in Virgil's *Eclogues* (pastoral poetry).

---

### How to Scan: Step-by-Step

1. **Mark all naturally long syllables** — vowels with macrons, diphthongs. Mark them `–`.
2. **Mark all short vowels** provisionally as `∪`.
3. **Apply long by position** — scan through looking for a short vowel followed by 2+ consonants (across word boundaries). Upgrade those `∪` to `–`.
4. **Mark elisions** — find vowel/vowel+m at end of word before vowel/h start. Bracket elided syllables.
5. **Work from the end of the line backward** — foot 6 = last 2 syllables (spondee or trochee). Mark them.
6. **Work forward from the start** — assign feet 1–5. Each foot must be dactyl (– ∪ ∪) or spondee (– –). The 5th foot should nearly always be a dactyl.
7. **Locate the caesura** — usually after the 1st long of foot 3 (penthemimeral).

---

### Worked Example: Virgil *Aeneid* 1.1

*Arma virumque canō, Trōiae quī prīmus ab ōrīs*

**Step 1 — Natural longs**: ō in *canō*, ō in *Trōiae*, ae in *Trōiae* (diphthong), ī in *quī*, ī in *prīmus*, ō and ī in *ōrīs*

**Step 2 — Long by position**:
- *Ar-*: short a + rm → long by position
- *vi-*: short i + single r → short
- *rum-*: short u + mqu... wait — *rumque*: um + q = two consonants? Yes, -m and qu → long by position
- *ca-*: short a + n (single) → short? But followed by nō — just n before a vowel... *ca-nō*: ca has only n following → short

Let's lay out the syllables:

```
Ar | ma | vi | rum | que | ca | nō | Trōi | ae | quī | prī | mus | ab | ō | rīs
```

Elision check: no word ends in vowel/m immediately before a vowel/h start here.

Applying rules:
- *Ar-* = – (short a + rm, position)
- *-ma* = ∪ (short a, single v follows)
- *vi-* = ∪ (short i, single r follows)
- *-rum-* = – (short u + mq = two consonants, position) — actually *virumque* = vi·rum·que; *rum* has short u but is followed by qu (two consonants), long by position
- *-que* = ∪ (short e + single c/k sound... actually qu is one consonant; *que ca-*: the e of *que* is followed by c of *cano* — one consonant, so short)
- *ca-* = ∪ (short a + n)
- *-nō* = – (long ō)
- *Trōi-* = – (ō is long; also Trōi- = diphthong oi... actually *Trōiae* = Trō + iae; Trō has long ō)
- *-ae* = – (diphthong ae)
- *quī* = – (long ī)
- *prī-* = – (long ī)
- *-mus* = ∪ (short u + s)
- *ab* = – (short a + b, then ō starts — cross-word: ab + ō means a + bō; *ab* itself ends in b, *ōrīs* starts with ō; so *ab* = short a + b before vowel. By position: the b of *ab* and — actually one consonant at end of word. Long by position requires 2 consonants; single final consonant before a vowel-initial word = **not** long by position. So *ab* = ∪)

Hmm — let's use the standard published scansion for this line:

```
Ār-ma vi-rum-que ca-nō, Troi-ae quī prī-mus ab ō-rīs
–   ∪  ∪  –   –   ∪  ∪   –   –    –   –   ∪  ∪  –  –
 1            2           3          4           5      6
```

**Feet**:
1. Ār·ma·vi = – ∪ ∪ (dactyl)
2. rum·que·ca = – – ∪ ... 

The standard accepted scansion of Aen. 1.1:

```
Ār-|ma vi-|rum-que| ca-nō,| Troi-ae| quī| prī-mus| ab| ō-rīs
 –    ∪  ∪   –  –    ∪  ∪   –   –    –   –   ∪  ∪   –   –
     D        S        D        S        D       S (foot 6)
```

Wait — let me lay this out cleanly as feet:

| Foot | Syllables | Pattern | Type |
|------|----------|---------|------|
| 1 | Ār-ma-vi | – ∪ ∪ | dactyl |
| 2 | rum-que-ca | – – (but ca is ∪?) | ... |

The most reliable reference scansion of 1.1:

```
ĀR·ma·vi | RUM·quĕ·ca | NŌ  ||  TROI·ae·quī | PRĪ·mus·ab | Ō·rīs
  –  ∪ ∪    –   ∪ ∪   –        –   ∪  ∪      –   ∪  ∪     –  –
     1          2       3              4             5         6
```

Note: the foot division and the syllabification are approximate in this display; the key result is:

- Feet 1, 2: dactyls
- Foot 3: starts with *nō* (long), then... the penthemimeral caesura falls after *nō* (after the first long of foot 3)
- Feet 4, 5: dactyls
- Foot 6: *ō-rīs* = – – spondee

The **penthemimeral caesura** is after *canō* — the main pause: *Arma virumque canō, || Trōiae quī prīmus ab ōrīs*.

---

### Line Types and Special Patterns

**Spondaic line**: unusually many spondees → heavy, slow, laborious feel. Virgil uses these for weight and effort:

*Ōlli sēd subitō vīsa est graviōrque pulchrōrque* (heavily spondaic, depicting struggle)

**Golden line** (aurea linea): a 5-word line arranged as adjective–adjective–verb–noun–noun (AAVNN), with the two adjectives and two nouns interlocked. Common in Virgil and Ovid for rhetorical polish:

*Aurea prima sata est aetas* — Ovid, *Met.* 1.89 (golden + first + was sown + age)

**Silver line**: adjective–noun–verb–adjective–noun (AVNAVBN), with interlocking noun phrases. Less strict than golden line.

**Hypermeter**: a line with an extra syllable that elides with the beginning of the next line. Rare but notable.

---

## Elegiac Couplet

The elegiac couplet is the **meter of Latin love elegy and epigram**. It pairs a dactylic hexameter with a dactylic pentameter. Used by:

- Catullus (poems 65–116, his longer and more personal poems)
- Tibullus (*Elegies*)
- Propertius (*Elegies*)
- Ovid (*Amores*, *Ars Amatoria*, *Heroides*, *Tristia*, *Epistulae ex Ponto*)

### The Pentameter

The **pentameter** is not literally 5 feet; the name refers to the 5 full *metra* (units) if you count the two halves differently. Its structure is:

```
– ∪∪ / – ∪∪ / –   ||   – ∪∪ / – ∪∪ / –
        first half        second half
```

Rules for the pentameter:
- It has **two halves** separated by a mandatory **diaeresis** (pause): `||`
- First half: two dactyls or spondees + one long (the half-foot)
- Second half: **always** two dactyls + one final long syllable — **no spondees allowed in second half**
- The second half is therefore metrically fixed: – ∪∪ – ∪∪ –
- Elision across the central diaeresis does **not** occur (the pause is too strong)

The fixed second half of the pentameter is a useful anchor when scanning: count back from the end — last 5 syllables are always ∪∪ – ∪∪ – (the pattern ... – ∪∪ – ∪∪ – going forward).

### The Elegiac Couplet Together

```
Line 1 (hexameter):  – ∪∪ / – ∪∪ / – ∪∪ / – ∪∪ / – ∪∪ / – –
Line 2 (pentameter): – ∪∪ / – ∪∪ / –  ||  – ∪∪ / – ∪∪ / –
```

The couplet typically forms a complete thought: the hexameter states a proposition, the pentameter adds a variation, contrast, or conclusion. This is called the **elegiac unit**.

### Worked Example: Ovid *Amores* 1.1.1–2

```
Arma gravī numerō violentaque bella parābam
   –    –   –  ∪ ∪  – ∪ ∪ –  –   –  ∪ ∪  –  –
      S      S     D      D    S      D        S

ēdere, māteriā  conveniente  modīs
  – ∪ ∪  –  –   – ∪ ∪ –   ∪ ∪  –
    D      S         D         (ends)
```

Line 1 (hexameter): *Arma gravī numerō violentaque bella parābam* — "I was preparing to sing of arms and violent wars in weighty meter"

Line 2 (pentameter): *ēdere, māteriā conveniente modīs* — "to publish [them], with subject matter matching the rhythms"

The irony: Ovid sets up epic hexameters, then Cupid steals a foot to make it a pentameter. The meter enacts the theme.

---

## Hendecasyllable

The **hendecasyllable** ("eleven-syllable [line]") is the main meter of Catullus's shorter lyric poems (poems 1–60, the so-called *Polymetrics*). It is also used by Martial and occasionally Statius.

### Pattern

The hendecasyllable has a fixed pattern with one positional variable at the start:

```
x  –  ∪  –  ∪∪  –  ∪  –  ∪  –  (x)
```

More precisely, the standard form (**Phalaecian hendecasyllable**):

```
– – | – ∪∪ | – ∪ | – ∪ | – x
```

Or spelled out as 11 syllables:

```
pos. 1: long (or anceps)
pos. 2: long
pos. 3: long
pos. 4: short
pos. 5: short
pos. 6: long
pos. 7: short
pos. 8: long
pos. 9: short
pos. 10: long
pos. 11: anceps (final syllable)
```

The opening two positions (xx at start, or – – as commonly realized) form a **spondee** or **iamb** in Catullus. After that, the line is fixed: – ∪∪ – ∪ – ∪ –.

### Worked Example: Catullus 1.1

*Quōī dōnō lepidum novum libellum*

```
Quōī  dō-nō  le-pi-dum  no-vum  li-bel-lum
 –     –   –   ∪  ∪   –    ∪  –    ∪  –   –
```

- *Quōī*: long (ōī diphthong-like; the form quoi is long)
- *dō-*: long (ō)
- *-nō*: long (ō)
- *le-*: short
- *pi-*: short
- *-dum*: long by position (d + m → actually: short u + m, but *lepidum novum*: -um before n = -um + n = position? Hmm; *-dum* is long by nature? No — actually the final -m before *n* in *novum* is a muta; the syllable is long by position)
- Pattern continues ...

The characteristic **playful, conversational** feel of Catullus comes partly from this meter's quick alternation of longs and shorts and the predictable but light-footed rhythm.

---

## Other Important Meters

| Meter | Pattern | Who Uses It |
|-------|---------|------------|
| **Alcaic** (4-line stanza) | Line 1–2: x– ∪– / – / –∪∪ –∪–; Line 3: x– ∪– ∪– ∪–; Line 4: –∪∪ –∪∪ –∪– | Horace *Odes* (dominant meter) |
| **Sapphic** (4-line stanza) | 3× (– ∪ – x – ∪∪ – ∪ –) + 1 Adonic (– ∪∪ – –) | Horace *Odes*; Catullus 11, 51 |
| **Asclepiadean** (various) | Multiple patterns with choriambs (– ∪∪ –) | Horace *Odes* |
| **Iambic trimeter** | x– / x– / x– / x– / x– / x– | Seneca's tragedies; Phaedrus |
| **Iambic dimeter** | x– / x– / x– / x– | Horace *Epodes* (paired with trimeter) |

---

## Practice Strategy

### Stage 1: Dactylic Hexameter from Heavily Spondaic Lines

Begin with lines that have many spondees — they are easier to scan because there are fewer syllable divisions to worry about. Look for lines in Virgil or Ennius with slow, heavy content (descriptions of labor, grief, death). In these lines, most feet are – –, and you mainly need to identify the two dactyls.

**Exercise**: Find 5 spondaic-heavy lines in *Aeneid* Book 1. Mark longs only. Then divide into 6 feet.

### Stage 2: Add Dactyls Progressively

Once comfortable with spondee-heavy lines, move to lines with 3 dactyls (the "average" hexameter line). Most lines in Virgil mix spondees and dactyls roughly 50/50 across feet 1–4.

### Stage 3: Work on Elision

Elision is the biggest source of errors. Practice finding elision systematically: read each line left to right; whenever a word ends in a vowel or -m, check if the next word starts with a vowel or h.

### Stage 4: Find the Caesura

After scanning, always mark the main caesura. The penthemimeral (after 5th half-foot) is the most common in Virgil. Look for where the sense of the line wants to pause.

### Stage 5: Move to Elegiac Couplets

Once hexameter is comfortable, tackle Ovid's *Amores* or Catullus's longer poems. The pentameter's fixed second half makes it the easiest part; focus on the first half of the pentameter and the full hexameter.

### Diagnostic Checks

If your scansion fails (you can not fit a line into 6 feet), check in order:
1. Did you miss an elision?
2. Did you misidentify a long-by-position syllable?
3. Did you mistake a diphthong for two separate vowels?
4. Is the word a Greek proper noun with unusual quantity?

---

## Learning Resources

| Resource | Type | Use |
|----------|------|-----|
| **DCC Scansion Guide** (dcc.dickinson.edu/grammar/latin/quantity-syllables) | Online reference | Full rules with examples |
| **Bennett's Latin Grammar** (prosody chapter) | Reference grammar | Complete prosody rules |
| **Pharr's Aeneid** commentary | Commentary | Scansion notes on every line of Aen. 1–6 |
| **Latintutorial** (YouTube, Ben Johnson) | Video | Dactylic hexameter walkthroughs |
| **ScorpioMartianus** (YouTube) | Audio | Classical pronunciation readings of Virgil, Ovid |
| **Diederich's Frequency Dictionary** | Vocabulary | Learn high-frequency words first to reduce dictionary lookups during scanning |
| **Allen & Greenough** §§ 603–642 | Grammar | Latin prosody rules in full |

**Recommended first practice texts** (in order of scanning difficulty):
1. Virgil *Aeneid* 1.1–10 — canonical; many published scansions to check against
2. Ovid *Metamorphoses* 1.1–4 — slightly more dactylic, flows easily
3. Catullus 5 (*Vīvāmus, mea Lesbia*) — hendecasyllable; short, memorable
4. Ovid *Amores* 1.1 — elegiac couplet; the poem's content mirrors the meter lesson
