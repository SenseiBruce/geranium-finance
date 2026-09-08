# How We Got Tasks Accepted — Simple Team Briefing

**For:** Everyone on this Geranium Finance project  
**Why this exists:** Three of our tasks got accepted. Here’s what actually worked, in plain English, so you can copy the approach.

**The three that got through**

1. **Ashcroft Foods** — insurance claim: what’s covered and how much to set aside  
2. **Pelliston** — year-end workers’ comp reserve for audit and the bank  
3. **Granite Ridge** — renewal desk: quote, refer, decline, or ask the broker for ~36 apartment accounts  

---

## The short version

We didn’t win by dumping a giant AI spreadsheet and hoping.

We won by building something that looks like **real desk work**:

- Several messy source files that don’t all agree  
- Clear rules for which file wins when they conflict  
- A finished workbook a reviewer can **recheck by hand**  
- A grading checklist (rubric) that asks for **one clear thing at a time**  
- When feedback came back, we fixed **the small thing they named** — not the whole task  

If you only remember one line for the meeting:  
**Messy inputs + clear “who wins” rules + a workbook you can audit + a picky but fair checklist + tiny revisions.**

---

## What “accepted” really means here

Reviewers (and automated checks) are asking:

1. **Can a real person redo the key number from what’s in the workbook?**  
2. **Did we handle the traps on purpose** (wrong totals, old rules, conflicting files)?  
3. **Does the grading list match what the prompt asked for** — not extra invented sections?  
4. **When we resubmit, did we only change what was wrong?**

You do **not** need to understand every formula. You **do** need to be able to explain the story of the answer.

---

## The shared playbook (layman steps)

### Step 1 — Don’t copy another task’s “shape”

If your task is basically “reconcile two numbers and true them up,” and someone else already did that with different company names, the portal may say **not unique**.

**What we did on Pelliston:** First version looked too much like another reconcile task. We didn’t just rename companies — we **changed the job** to a year-end self-insured reserve with caps, IBNR, and a rollforward.

**Team tip:** Before you start, check you’re not building the same puzzle with new nouns.

### Step 2 — Hide the answer across files

Every accepted task works like this:

| File role | What it does |
|-----------|----------------|
| Summary / claim file | Looks mostly fine (tempts a quick answer) |
| Detail file | Contradicts the summary in a few important places |
| Memo / notes | Says which source is the boss |
| Old / superseded rows | Still sitting there so careless solvers pick the wrong number |

If **one** file alone gives the full answer, the task is too easy and often gets pushed back.

### Step 3 — Build a workbook a stranger can follow

Think “audit workpaper,” not “AI essay in Excel.”

Good signs:

- Coverage / routing decisions are written clearly (Accept / Deny / Quote / Refer, etc.)  
- Money trails show **how** you got from raw rows → cleaned → final number  
- Things you **rejected** (void lots, excess above retention, declined accounts) are still visible  
- Where two sources fought, you wrote: *what fought, what we followed, what we did*  
- Formulas link the pieces so changing an eligible amount moves the reserve / counts  

### Step 4 — Write the grading list like a picky teacher

The rubric should:

- Check **one** fact per criterion (don’t smash three checks into one line)  
- Grade what’s **in the deliverable**, not how the zip is packed  
- Include a few “don’t do this” items that are real bad advice (e.g. “recommends paying the equipment claim”) — not just “forgot to include X”  
- Only ask for things the **prompt** actually asked for  

**Ashcroft example:** We split fat criteria that graded three things at once, dropped a check the prompt never asked for, and strengthened the “don’t recommend these bad treatments” side. Reviewer said the reserve math was fine; the rubric cleanup helped acceptance.

### Step 5 — When they send notes, fix the named thing

| They say… | You do… |
|-----------|---------|
| Math is right, one sentence is wrong | Fix that one cell’s wording |
| This account should be Quote not Refer | Fix that disposition **and** the reason text |
| Your task looks like someone else’s | Redesign the decision shape (bigger change) |
| Round numbers / obvious dates tip off the hard rows | Put cents and more realistic dates in the **inputs** |
| Upload / build weirdness | Rebuild packages cleanly and re-upload; don’t rewrite good math |

**Granite Ridge example:** The account was already routed Quote. The rationale text was a generic sentence that didn’t mention occupancy %, the rule section, or the broker confirmation. One cell rewrite → accepted. Numbers untouched.

---

## Story 1 — Ashcroft Foods (claim coverage)

**Plain English job:**  
Before committee, decide what’s covered on a frozen-food warehouse claim (spoiled stock, equipment, business income), then set an **indemnity** reserve. Keep claim-handling expenses (ALAE) **out** of that reserve number.

**Why reviewers liked it**

- They could recompute the reserve themselves and land on the same figure (**about $176k**)  
- The big “as claimed” demand was broken apart so you can see packaging / duplicates / valuation fights  
- Inventory cleanup showed how you got from raw counts down to the covered population  
- The workbook told a clear story in fewer pages (roughly teens of pages, not a 45-page dump)

**What we learned**

For claim tasks: **decide coverage first**, then build money. Show rejects. Make the reserve trail hand-checkable. Don’t grade sections the prompt never asked for.

---

## Story 2 — Pelliston (workers’ comp reserve)

**Plain English job:**  
Controllers need the year-end self-insured workers’ comp liability number for auditors and the bank. Cap big cases at the company retention, add IBNR from the actuary memo, show what’s above retention (carrier’s problem), roll from last year’s balance, and write a short “how to book this” note.

**Why reviewers liked it**

- Case total after caps and dropping closed claims tied out  
- IBNR used the **current** memo factors, not an old mid-year factor still floating in the packet  
- The large loss correctly showed the piece **above** retention as ceded / not our SI liability  
- Opening balance rolled forward cleanly  

**The trap they praised:**  
Two files disagreed on paid dollars for one accident year. We didn’t quietly pick a convenient number. We **wrote both numbers down** and followed the memo (use the triangle). That “honest conflict log” is a big part of why it felt professional.

**Also important:** First attempt failed uniqueness. Fix was a **new kind of task**, not a cosmetic rename.

**What we learned**

For reserve tasks: document conflicts, follow the governing memo, and in the recommendation **name the bad treatments you refuse** (e.g. no subrogation credit before cash arrives).

---

## Story 3 — Granite Ridge (renewal routing)

**Plain English job:**  
Clear an October batch of apartment renewals. Every account gets Quote, Refer, Decline, or Ask Broker. Flag location problems, fix loss-ratio fights between files, and cite the routing notes when you make a call.

**The hinge account (GR-2047)**

- Easy wrong read: “There’s vacancy → Refer”  
- Correct read of the notes: occupancy isn’t “full,” and the broker confirmed turnover vacancy → **Quote**  

Models struggled while that hinge was wrong or fuzzy. Getting the **literal rule** right mattered more than fancy spreadsheet layout.

**Other fixes that mattered**

- Don’t spotlight “important” accounts with perfectly round premiums and losses — use cents like the other rows  
- Don’t make inspection dates so clustered that only one account is obviously late  
- Don’t double-score the same routing in two rubric criteria  
- Make sure the **reason cell** actually names the facts the rubric asks for (not a copy-paste generic sentence)

**What we learned**

For routing desks: read the notes literally; hide the puzzle in realistic data; remember that **wording in rationale cells gets graded**, not only the Quote/Refer label.

---

## Meeting checklist you can hand out

**Before you upload**

- [ ] This isn’t the same puzzle as another task with new company names  
- [ ] Answer requires more than one file  
- [ ] Memo/notes say who wins when files conflict  
- [ ] You (or a teammate) can recompute the main number from the workbook  
- [ ] Rejected / excluded items are still visible  
- [ ] Rubric asks one thing per line and matches the prompt  
- [ ] You’re uploading the fresh packaged files, not an old zip from last week  

**When you get feedback**

- [ ] Is this content (wrong answer / weak rubric) or packaging / platform noise?  
- [ ] Fix only what they pointed at  
- [ ] If they rename entities, update **everywhere** the name appears (inputs, golden, prompt, rubric, portal text) in one pass  
- [ ] Re-package and re-upload cleanly  

---

## How to talk about AI in the room

It’s fine that AI drafted a lot of the work. Acceptance still needs a human pass that asks:

1. What was the **trap**?  
2. Which **rule** decided it?  
3. Can I **recompute** the headline number?  
4. Does each grading line have an **obvious place** in the workbook that proves it?  
5. If feedback named one cell, did we change **only** that?

That’s the same pattern for Ashcroft, Pelliston, and Granite Ridge.

---

## Headline numbers (if someone asks “did it tie?”)

| Task | Number reviewers cared about |
|------|------------------------------|
| Ashcroft | Reserve **$176,266.11** (expenses kept separate) |
| Pelliston | Case **$745,064.55** · IBNR **$333,679.35** · excess piece **$62,800** |
| Granite | **36** accounts routed; GR-2047 **Quote** with the right reason written out |

---

## Where the detailed / technical notes live

If someone wants the tooling and command-level detail later:

- `docs/auto-eval-playbook.md`  
- `docs/portal-rubric-quality.md`  
- `docs/chat-commands.md`  

This briefing is the **meeting version**. Use those docs when you’re hands-on in the repo.

---

*Written for a team sync from the three accepted tasks and the reviewer notes that came with them.*
