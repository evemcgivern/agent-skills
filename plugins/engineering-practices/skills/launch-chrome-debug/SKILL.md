---
name: launch-chrome-debug
description: Starts Google Chrome with remote debugging on port 9222 and a separate profile so the Chrome DevTools MCP server can connect, on macOS, Linux or Windows. Use when Chrome DevTools MCP tools fail because no debug target is available on port 9222, or when the user says "start Chrome for debugging", "launch Chrome with remote debugging" or "open Chrome for the DevTools MCP".
---

# Launch Chrome with Remote Debugging

Starts Google Chrome with `--remote-debugging-port=9222` so the Chrome DevTools MCP server can connect.

## When to Use

- Before using any `chrome-devtools` MCP tools (navigate, snapshot, screenshot, etc.) when the server is configured to connect to a running browser
- When `list_pages` or `navigate_page` fails with connection errors
- When the user says "start Chrome", "launch Chrome for debugging", or "open Chrome MCP"

The MCP server only connects to this browser when its client configuration passes `--browser-url=http://127.0.0.1:9222`. Without that option the server starts its own Chrome and this skill is not needed.

## Command

The macOS, Linux and Windows Command Prompt commands are adapted from the Chrome DevTools MCP [advanced usage guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md#manual-connection-using-port-forwarding); the PowerShell variant is written for this skill. Run the one for your system in a separate terminal, or append ` &` in a macOS or Linux shell to keep it in the background.

**macOS**

```bash
mkdir -p "$HOME/.cache/chrome-debug-profile" && chmod 700 "$HOME/.cache/chrome-debug-profile"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.cache/chrome-debug-profile"
```

**Linux**

```bash
mkdir -p "$HOME/.cache/chrome-debug-profile" && chmod 700 "$HOME/.cache/chrome-debug-profile"
/usr/bin/google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.cache/chrome-debug-profile"
```

**Windows, PowerShell** (the default Windows terminal; untested)

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 "--user-data-dir=$env:TEMP\chrome-profile-stable"
```

**Windows, Command Prompt** (`cmd.exe`)

```bat
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-profile-stable"
```

`--user-data-dir` is required: since Chrome 136, Chrome ignores `--remote-debugging-port` when it points at the default profile ([Chrome blog](https://developer.chrome.com/blog/remote-debugging-port)). The separate directory also keeps your regular browsing profile out of the debugging session. On macOS and Linux it lives in your home folder with owner-only permissions, so other users on the machine cannot read or plant files in it, as they could with a fixed folder under `/tmp`. On Windows, `%TEMP%` is already inside your own user folder.

While the port is open, any application on the machine can connect to it and control the browser. Do not browse sensitive sites in this window, and close it when you are done.

### Alternative: attach to your everyday Chrome (Chrome 144 and later)

Instead of a debug port, the MCP server can attach to a Chrome you already have open. In Chrome, open `chrome://inspect/#remote-debugging` and enable remote debugging, then start the MCP server with `--autoConnect` instead of `--browser-url`. Chrome asks for permission each time the server connects. The server works in your default profile and sees all its open windows, so this suits sharing state between manual and agent testing, not sensitive browsing. See the [advanced usage guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md#automatically-connecting-to-a-running-chrome-instance) and the [Chrome blog post](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session). This skill is not needed in that setup.

## Verification

After launching, confirm the debug port is responding:

```bash
curl -s http://127.0.0.1:9222/json/version
```

A successful response returns JSON with `Browser`, `Protocol-Version`, and `webSocketDebuggerUrl` fields.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 9222 already in use | Find the process holding it (`lsof -i :9222` on macOS or Linux, `netstat -ano \| findstr :9222` on Windows), close it, then relaunch |
| Chrome not found at path | Chrome is installed somewhere else. Find the executable (for example `which google-chrome` on Linux) and substitute its path |
| MCP still can't connect | Check that the MCP client passes `--browser-url=http://127.0.0.1:9222`, that no other Chrome instance claimed the port, and that `--user-data-dir` points at a directory no other running Chrome uses |

## Credit

The launch commands and the `--browser-url` setup are adapted from the [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) project's documentation (`docs/advanced-usage.md`), © Google LLC, licensed under the [Apache License 2.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/LICENSE). The Command Prompt command is reproduced unchanged. The macOS and Linux commands keep the upstream flags but use a private profile folder in your home directory instead of `/tmp`; the PowerShell variant and the surrounding text are original to this skill.
