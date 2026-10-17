---
name: clearly
description: Write plain, short, scannable prose, about 80% of ASD-STE100 (controlled technical English), with habits from Strunk and i-have-adhd. Use when writing or editing explanations, docs, status updates, commit messages or error messages, or when the user says "clearly", "plain English", "STE", "ASD-STE100", "explain simply" or "comma-delimited". Add `--explain` to get a diagram, page, or short video, chosen automatically.
---

# Clearly

Plain writing that a tired reader can act on. Adapted from ASD-STE100, Strunk's *Elements of Style*, and the i-have-adhd plugin (MIT, Ayoub Ghriss).

## Shape

1. Lead with the answer or the next action.
2. Write steps as a numbered list. One action per step. Use the fewest steps that work.
3. If anything is open, end with one next action that takes under two minutes.
4. Keep lists to 5 items. Split longer lists into "now" and "later".
5. Give time estimates in concrete units: "15 minutes", not "a bit".
6. Report errors flat: cause, then fix.

## Lists of short items

1. Put short items (issue numbers, file names, tags, names) on one line, separated by `, `. No bullets and no trailing comma.
2. Write issue and PR numbers without `#`: `6411, 279, 4544`.
3. Keep the order the user gave. Drop duplicates.
4. Use bullets only when each item needs its own sentence.
5. For GitHub issue lists, the `cdf` skill has the full rules. The 5-item cap in Shape does not apply to a comma line, because the reader does not scan it.

## Sentences

- Keep each sentence to 20 words or fewer.
- Put one idea in each sentence.
- Keep each paragraph to 6 sentences or fewer, on one topic. Start with the topic sentence.
- Use active voice. The subject does the action.
- Use simple present for facts and simple past for events. Avoid perfect and progressive forms.
- Say what is, not what is not.
- Keep the articles: a, an, the. Never drop them.
- Do not stack more than 3 nouns. Break long stacks with "of" or "for".
- Write instructions as commands: "Run the test", not "You should run the test".

## Words

- Use one word for one meaning. Use the same term for the same thing every time.
- Choose the short common word: "use", not "utilize". "Start", not "initiate".
- Choose the concrete word. Name the file, the number, the command.
- Do not use idioms or figures of speech.
- Define a technical term at first use, or leave it out.
- Cut filler: "just", "really", "basically", "in order to".
- Keep related words together. Keep the subject near its verb.

## Before you send

1. Delete the first sentence if it announces what you will do.
2. Delete the last sentence if it recaps or offers more help.
3. Split any sentence over 20 words.
4. Check the first and last line. Does the reader know what to do and what happened?

## --explain

With `--explain`, choose the best form for the content. The reader does not pick.

1. Give the answer first in 3 lines or fewer, in the style above.
2. Pick one form:
   - **Diagram**: for structure, flow, or a comparison. Use Mermaid, or a diagram skill if one is installed.
   - **Page (HTML)**: for reference material, comparisons, tables, or several parts the reader needs to scan or explore. Use an HTML skill if one is installed, or write a single self-contained HTML file.
   - **Video**: for a process or idea that changes over time. Aim for 60 to 90 seconds.
   - **Text only**: if the answer is simple. Say so and stop. Do not force a visual.
3. Say which form you chose and why, in one line.
4. Open the result with `open`.

Video steps:
1. Write the script first. Follow the Sentences and Words rules. The narration and on-screen text use the same rules.
2. Make the scenes with `manim` (installed as a `uv` tool). Test with `-ql`, then render with `-qh`.
3. Record the narration with `say -v "Samantha (Enhanced)" -r 150`. If that voice is missing, run `say` with no `-v`. If `ELEVENLABS_API_KEY` is set, use ElevenLabs instead.
4. Join the video and audio with `ffmpeg`.

## How strict

Full ASD-STE100 also has an approved word list and a 25-word limit for descriptive text. This skill skips the word list. A technical name the reader already knows is fine.

## Do not use for

- Prose that must keep the author's own voice.
- Marketing copy and fiction.
- Wording a human typed in a `/redline`. That wording is final.

Do not combine with a terse-output skill that drops articles. This skill keeps them.
