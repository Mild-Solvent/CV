# Claude for non-engineers

A one-page guide and a five-day coaching plan. Denis Matejcik, October 2026.

I wrote this in October 2026 as the guide I would hand a new colleague. If you are reading it as part of my Epoch application: the coaching plan is what I would run in week one.

## What Claude is good at, and the three things it is bad at

Claude is good at work that starts from text you already have. Give it a messy document and it will summarise, restructure, draft, compare or explain it. It is patient with rewrites, and it follows a format when you ask for one. It is bad at three things. First, recent facts: it has a training cutoff and does not know what happened last week unless you paste it in. Second, your internal context: it does not know your team, your projects or your conventions unless you tell it. Third, it fills gaps confidently: when it lacks a fact it can produce a plausible one. That is why habit 5 below exists. Most bad answers come from one of these three gaps. Most good answers come from giving it the right material first.

## Your first 30 minutes: turn a messy meeting note into a decision log

Ten minutes to do it, ten to check it, ten to fix and file it.

1. Open claude.ai and start a new chat. If you only have Claude in Slack, open a direct message with it instead.
2. Find a real meeting note from the last two weeks, one with decisions in it. Remove anything you would not put in an email to the whole team (see "What to never paste in").
3. Paste this prompt, then paste the note under it:

```
I am going to paste a raw meeting note. Turn it into a decision log.

Format:
- A table with four columns: Decision, Owner, Due date, Source line (quote the line from the note).
- Below the table, a list titled "Open questions": things discussed but not decided.
- Below that, a list titled "Unclear": lines in the note you could not interpret. Quote them.

Rules:
- Use only what is in the note. Do not add decisions, owners or dates that are not there.
- If an owner or date is missing, write "not stated".
- Keep the wording of each decision close to the original.

The note:
```

4. Read the result against the note. Three checks. Every row quotes a real line from the note. Every "not stated" is really missing from the note. Every decision in the note has a row in the table.
5. If something is wrong, say so in the same chat. For example: "Row 3 was a suggestion, not a decision. Remove it." Do not start a new chat.
6. Ask for the final version in the format you need. For example: "Give me the table as plain text I can paste into Slack."
7. Paste it where your decision logs live. Add one line: "Drafted with Claude, checked by [your name]."

What a good result looks like: four to eight rows, every row traceable to the note, and honest "not stated" cells. The "Unclear" list is not empty. A messy note always has unclear lines. If that list is empty, be suspicious and read the note again.

## Five habits that make answers reliable

1. **Give context first.** "I work in operations at a small research organisation. This is a draft vendor contract." Then the question.
2. **Ask for the format.** "Answer as a table with three columns: option, cost, risk."
3. **Ask it to show its sources or say "I don't know".** "Quote the line you are relying on. If the document does not say, write 'not in the document'."
4. **Iterate in the same thread.** "Same table, but drop the risk column and sort by cost." A new chat forgets everything you gave it.
5. **Verify numbers and names yourself.** Every figure, date and person's name gets checked against the source before it leaves your hands.

## What to never paste in

- Passwords, API keys, access tokens, login links. Nothing that lets someone in.
- Personal data of other people: home addresses, health, salaries, ID numbers, private messages. A colleague's name in a meeting note is fine. Their personal life is not.
- Anything under an NDA or a confidentiality agreement, unless the tool has been approved for that data. Approval is per tool: a personal claude.ai account and the company workspace are not the same thing.
- Unpublished results or data you were asked to keep internal, unless the tool is approved for it.

When unsure, ask me, the AI enablement person, before pasting. It takes one Slack message. A two-minute wait is cheaper than a leaked document.

## When to use which

| | Chat (claude.ai) | Claude in Slack | Claude Code |
|---|---|---|---|
| **Good for** | Your own documents: drafting, summarising, rewriting, explaining. Long back-and-forth on one task. | Quick questions where the team should see the answer. Questions about internal documents it is connected to. | Getting a tool built: a script, a bot, a report that runs every week. Changing something in a code repository. |
| **Not for** | Answers the whole team needs. Facts about internal systems it is not connected to. | Long documents and long edits. Sensitive data, because the channel is shared. | One-off questions. Anything you do not want to exist as a tool afterwards. |
| **Who helps you** | Me, for prompts and habits. The shared prompt library. | Me, for what it is connected to and what it can see. | Me. Describe the task in plain words; I direct the coding agent, or sit with you while you do. You do not need to code. |

## Cost, in plain numbers

Usage is measured in tokens. A token is roughly three quarters of an English word. "Please summarise this note" is about six tokens. A one-page document is about 500 to 700 tokens. A 30-page report is about 15,000 to 25,000 tokens. A long thread where you keep pasting documents can reach 100,000 tokens, because everything in the thread is read again on every reply.

Chat seats are a flat monthly fee per person, so your chatting does not add cost. Claude in Slack and the automations run on the API, which bills per token. Rates are quoted per million tokens and differ by model: the everyday model costs a few dollars per million, the strongest roughly twice that, the smallest well under a dollar. Ask me for the current rate card before you plan a big job. Summarising a 30-page report with the everyday model costs a few cents. Reading a thousand such reports costs tens of dollars. These rates change, so ask me for the current rate card before you plan anything large.

The one rule: nobody gets in trouble for spend on real work. If you plan a big batch job, hundreds of documents or something that runs every hour, tell me first. I will check the model, the cost and whether there is a cheaper way.

## The 5-day coaching plan

One person, 20 minutes a day, same time each day, screen shared. Every day's task comes from their real work that week, not from an exercise sheet. I have not run this plan with anyone yet. It is what I will run in week one, and I will change it after the first person.

**Before day 1** (five minutes, by message): the person sends me one thing they did last week that took over an hour and felt mechanical.

**Day 1: one document in, one result out.**
Task: the "first 30 minutes" walk-through above, on their own document.
Success check: they can point from every row of the result to a line in the source.
I write down: what the document was, where the prompt failed, and whether the prompt goes into the shared library as is or with changes.

**Day 2: context and format.**
Task: a question from their work where the first answer came back generic. Fix it by giving context and asking for a format.
Success check: the second answer is usable without editing.
I write down: what context they had to type, and whether it belongs in a shared project or system prompt so nobody types it again.

**Day 3: checking.**
Task: ask Claude something from their own domain they already know the answer to, with numbers in it. Find the mistakes.
Success check: they find at least one thing to verify and verify it against a source.
I write down: which kinds of errors showed up, and whether a "quote your source" line becomes a default in the shared prompts.

**Day 4: Slack or Code.**
Task: if they need answers the team can see, run day 1's task in Claude in Slack. If they described a repeatable task before day 1, we write the spec for it together in plain words: input, output, what "done" means.
Success check: a Slack thread the team can read, or a spec of five lines or fewer.
I write down: whether the task is worth building (how often it happens, how long by hand, who else has it). That note goes into my backlog ranked by expected value.

**Day 5: their own task, unaided.**
Task: they pick the task. I watch and say nothing until the end.
Success check: a checked result in 20 minutes without my help.
I write down: what they still asked me, which of the five habits they skipped, and what I add to this guide.

**What you get at the end of the week:** one prompt that works on your real documents, saved in the shared library under your name. Your own checklist for verifying answers. A clear answer on which tool to use for what. If you had a repeatable task, a written spec I take to a coding agent. What I get is a note per day on what blocked you, which goes into this guide and the shared prompts.
