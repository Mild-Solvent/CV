# Eval run 2026-10-21 00:46 UTC

Backend: `claude-code` · model: `claude-opus-5-5` · **12/12 passed** · total cost **$0.3141** (cost source: reported)

| # | id | result | check | cost | time |
|---|---|---|---|---|---|
| 1 | pto-days | PASS | found ['28'], cited pto-policy.md | $0.0280 | 9s |
| 2 | pto-carryover | PASS | found ['5', '31 March'], cited pto-policy.md | $0.0280 | 8s |
| 3 | expense-receipt | PASS | found ['25'], cited expense-policy.md | $0.0364 | 9s |
| 4 | travel-business | PASS | found ['8 hours'], cited travel-booking.md | $0.0274 | 8s |
| 5 | laptop-lost | PASS | found ['#it-help', '24 hours'], cited laptop-it-setup.md | $0.0373 | 9s |
| 6 | api-budget | PASS | found ['#ai-tools', '1,000'], cited ai-tool-budget.md | $0.0302 | 9s |
| 7 | data-confidential | PASS | found ['orbit-secure'], cited data-handling.md | $0.0294 | 9s |
| 8 | onboarding-probation | PASS | found ['3 months', '30'], cited onboarding-checklist.md | $0.0259 | 7s |
| 9 | refuse-wifi | PASS | said "I don't know" | $0.0138 | 10s |
| 10 | refuse-dental | PASS | said "I don't know" | $0.0314 | 10s |
| 11 | clarify-limit | PASS | asked a clarifying question | $0.0071 | 7s |
| 12 | clarify-approval | PASS | asked a clarifying question | $0.0192 | 7s |

## Answers

### pto-days - PASS
**Q:** How many days of PTO do I get per year?

> As a full-time employee you get *28 days of PTO per calendar year*, plus the public holidays of the country you're employed in. If you're part-time, you get a pro-rated amount. PTO builds up at 2.33 days a month, but you can take days before they've built up. You can carry *up to 5 unused days* into the next year, and you have to use them by *31 March*. The company shutdown from 24 Dec to 1 Jan doesn't count against your PTO.

Sources: pto-policy.md

### pto-carryover - PASS
**Q:** Can I carry unused holiday into next year?

> Yes, you can carry over *up to 5 unused PTO days* into next year. Carried-over days have to be used by *31 March*, or they expire. Unused days aren't paid out, except when you leave Orbit. The 24 December to 1 January shutdown doesn't count against your PTO, so you don't need to save days for it.

Sources: pto-policy.md

### expense-receipt - PASS
**Q:** Do I need a receipt for a $20 coffee I bought while travelling?

> No. You only have to attach a receipt for expenses *over USD 25*, so a $20 coffee doesn't need one. You still have to file it in Expensify *within 30 days*, or it will need director approval. It also counts toward the *USD 60 per day* limit for meals while travelling.

Sources: expense-policy.md

### travel-business - PASS
**Q:** When am I allowed to fly business class?

> Business class (or premium economy) is only allowed on flights with *more than 8 hours* of scheduled flight time. Everything else is booked in economy. This is the only class upgrade Orbit pays for, and the expense policy also lists business-class upgrades as not reimbursable outside that exception. Book the flight through *TravelPerk* like any other trip.

Sources: expense-policy.md, travel-booking.md

### laptop-lost - PASS
**Q:** My laptop was stolen, what do I do?

> Report it in *#it-help right away*, and no later than *24 hours* after you notice it's gone. IT will remotely wipe the laptop. A stolen laptop is also a data incident, so post in *#data-governance within 24 hours* as well. Nobody gets in trouble for reporting. You won't be charged for the laptop, but if you lose a second one within two years, your manager will review it.

Sources: data-handling.md, laptop-it-setup.md

### api-budget - PASS
**Q:** I need about $600 of API credits for an eval run next month. Who approves that?

> The *AI Enablement lead* approves it, since anything up to *USD 1,000 per month* is theirs to sign off, usually within one working day. Your shared API key only covers *USD 100 per person per month*, so a $600 run needs a request. Post in *#ai-tools* with what you're running and roughly how many tokens or calls, which model(s) you'll use, and the expected cost. Once it's approved you get your own API key and workspace, so the spend is tracked per project. Before you launch the run, check the monthly usage dashboard linked in the #ai-tools channel topic.

Sources: ai-tool-budget.md

### data-confidential - PASS
**Q:** Can I paste a licensed dataset into Claude in Slack?

> No. Licensed datasets are classed as *Confidential*, and Confidential data can't go into chat tools, including Claude in Slack. If you need to run it through Claude, use the Anthropic API through the `orbit-secure` workspace, which has zero data retention turned on. Also check the license in the dataset register on Notion first, and keep copies in the `orbit-secure` bucket. If any of it has already ended up in Slack, post in *#data-governance within 24 hours*.

Sources: data-handling.md

### onboarding-probation - PASS
**Q:** How long is probation and when do I get feedback?

> Probation lasts *3 months*. You get written feedback at the *30-day* and *90-day* check-ins. The 30-day check-in is with your manager and the People team, and if something isn't working, that's when you'll hear about it, so nothing comes as a surprise at the end.

Sources: onboarding-checklist.md

### refuse-wifi - PASS
**Q:** What is the office wifi password?

> I don't know, ask #it-help
> The knowledge base doesn't include the office wifi password. The closest doc I found is the IT setup guide, and it only says staff get a 1Password invite on day one and should post laptop or account questions in #it-help.

Sources: none

### refuse-dental - PASS
**Q:** Which dental insurance provider do we use?

> I don't know, ask #it-help. The knowledge base doesn't name a dental insurance provider. The only related things I found are that the onboarding checklist includes a day-one call with the People team that covers benefits, and that the travel doc says travel insurance comes through TravelPerk. #people-ops may be the better place to ask.

Sources: none

### clarify-limit - PASS
**Q:** What is the limit?

> A few policies have limits. Which one do you mean: *expense limits* (expense-policy.md), *AI tool / API credit budget* (ai-tool-budget.md) or *PTO* (pto-policy.md)?

Sources: none

### clarify-approval - PASS
**Q:** How do I get approval?

> Can you tell me which kind of approval you need? The knowledge base has three different approval processes: *expenses* (late or over-limit claims in Expensify), *AI tool / API credit budget* requests, or *PTO* (time off approved by your manager in Humaans).

Sources: none
