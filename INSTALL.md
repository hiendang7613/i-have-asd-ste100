# Install

## Claude Code

From GitHub:

```bash
claude plugin marketplace add hiendang7613/i-have-asd-ste100
claude plugin install i-have-asd-ste100@i-have-asd-ste100
```

From a local checkout, pass the directory path instead of `hiendang7613/i-have-asd-ste100`.

Restart Claude Code. From then on every new session uses the rules: the SessionStart hook injects them and a one-line
reminder is added to each prompt. Nothing needs to be turned on. The manual command is `/i-have-asd-ste100:i-have-asd-ste100`.

### Turning it off

```bash
touch ~/.claude/.i-have-asd-ste100-off          # every session (Codex: $CODEX_HOME/.i-have-asd-ste100-off)
I_HAVE_ASD_STE100=off claude                     # this process only
```

Delete the file or unset the variable to turn it on again. Inside a session, "stop ste mode" anywhere in a prompt
(outside quotes and code), or the exact prompt "normal mode", stops it for that session; "ste mode" starts it again.
"no icons" keeps the shape but drops the icons, for terminals that cannot show them.

The hooks need Node.js on the PATH. Without Node they do nothing; the manual command still works.

## Codex

```bash
codex plugin marketplace add hiendang7613/i-have-asd-ste100
codex plugin add i-have-asd-ste100@i-have-asd-ste100
```

Codex loads the skill. Current Codex releases do not run plugin hooks, so the rules are not on by default there.
To make every Codex session use them, add the shape to `~/.codex/AGENTS.md` (an example is in the README's "The shape" table).

## Uninstall

```bash
claude plugin uninstall i-have-asd-ste100
rm -f ~/.claude/.i-have-asd-ste100-off ~/.codex/.i-have-asd-ste100-off
```
