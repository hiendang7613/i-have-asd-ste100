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
The format uses no emoji, so it works in every terminal.

The hooks need Node.js on the PATH. Without Node they do nothing; the manual command still works.

## Codex

```bash
codex plugin marketplace add hiendang7613/i-have-asd-ste100
codex plugin add i-have-asd-ste100@i-have-asd-ste100
```

Codex loads the skill and the plugin hooks from `hooks/hooks.json`. On first install, and after the hook definition changes, run `/hooks`, review the plugin hooks, and trust them. Codex skips plugin hooks until you trust the current definition. Start a new session after trusting the hooks: `SessionStart` loads the reply rules, and `UserPromptSubmit` adds the short reminder with the local time. The per-step clock uses Claude Code's `PostToolBatch` event; in Codex, Agents-Zone steps carry a time only when a clock reading is available. Without hook trust, the skill remains available for manual use.

The commands above use the Codex CLI. The ChatGPT web app does not deploy local hook scripts into its runtime.

## Uninstall

```bash
claude plugin uninstall i-have-asd-ste100
rm -f ~/.claude/.i-have-asd-ste100-off ~/.codex/.i-have-asd-ste100-off
```
