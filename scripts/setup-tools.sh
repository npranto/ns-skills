#!/usr/bin/env bash
# setup-tools.sh: install the tools the ns skills use, one confirmed step at a time.
#
#   bash scripts/setup-tools.sh                       # everything below, asking before each step
#   bash scripts/setup-tools.sh --only core,ui        # some groups: core, ui, delegate, vercel, plugins
#   bash scripts/setup-tools.sh --harness claude,codex  # plugin skills for these harnesses (claude, codex, opencode, cursor)
#   bash scripts/setup-tools.sh --dry-run             # print what it would do, change nothing
#   bash scripts/setup-tools.sh --yes                 # do not ask (for scripts and CI)
#   curl -fsSL https://raw.githubusercontent.com/npranto/ns-skills/main/scripts/setup-tools.sh | bash
#
# Groups:   core      git, Node 20+, gh (and gh auth login); gh-axi runs through npx, Python 3.9+ is checked
#           ui        playwright-cli, lighthouse, ffmpeg, @axe-core/cli, Google Chrome (checked)
#           delegate  herdr, claude (checked)
#           vercel    the vercel CLI
#           plugins   the mattpocock-skills skills for the chosen harnesses
# It never uninstalls or upgrades anything that is already present. macOS and Linux; on Windows use WSL.

set -u

ONLY="core,ui,delegate,vercel,plugins"
HARNESSES="claude,codex,opencode,cursor"
ASSUME_YES=0
DRY=0
SKILLS_CLI="skills@1.7.4"

while [ $# -gt 0 ]; do
  case "$1" in
    --only) ONLY="${2:-}"; shift 2 ;;
    --harness) HARNESSES="${2:-}"; shift 2 ;;
    --yes|-y) ASSUME_YES=1; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (try --help)" >&2; exit 2 ;;
  esac
done

INSTALLED=""; SKIPPED=""; FAILED=""; PRESENT=""

has() { command -v "$1" >/dev/null 2>&1; }
in_list() { case ",$2," in *",$1,"*) return 0 ;; *) return 1 ;; esac; }
group_on() { in_list "$1" "$ONLY"; }
harness_on() { in_list "$1" "$HARNESSES"; }

say() { printf '%s\n' "$*"; }
head_() { printf '\n== %s\n' "$*"; }

# ask "question": yes with --yes; otherwise read the answer from the terminal (works under curl | bash).
ask() {
  if [ "$ASSUME_YES" = 1 ]; then return 0; fi
  if ! { true < /dev/tty; } 2>/dev/null; then say "   no terminal to ask on, skipping (use --yes to allow)"; return 1; fi
  printf '   %s [y/N] ' "$1" > /dev/tty
  read -r reply < /dev/tty || return 1
  case "$reply" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

# step NAME "command" : run one install command after confirming it.
step() {
  local name="$1" cmd="$2"
  say " - $name: $cmd"
  if [ "$DRY" = 1 ]; then SKIPPED="$SKIPPED $name(dry-run)"; return 0; fi
  if ! ask "Run it?"; then SKIPPED="$SKIPPED $name"; return 0; fi
  if bash -c "$cmd"; then INSTALLED="$INSTALLED $name"; else FAILED="$FAILED $name"; say "   failed: $name"; fi
}

# need_tool NAME "command" : install only when the tool is missing.
need_tool() {
  local name="$1" cmd="$2"
  if has "$name"; then PRESENT="$PRESENT $name"; say " ok $name ($(command -v "$name"))"; return 0; fi
  step "$name" "$cmd"
}

# The package manager used for system tools.
pkg_hint() { # NAME BREWNAME
  if has brew; then echo "brew install $2"; else echo ""; fi
}
need_system() { # NAME BREWNAME
  local name="$1" brewname="$2" cmd
  if has "$name"; then PRESENT="$PRESENT $name"; say " ok $name ($(command -v "$name"))"; return 0; fi
  cmd="$(pkg_hint "$name" "$brewname")"
  if [ -z "$cmd" ]; then
    say " - $name: missing, and Homebrew is not installed. Install $name with your package manager, then run this again."
    SKIPPED="$SKIPPED $name(no-brew)"
    return 0
  fi
  step "$name" "$cmd"
}

node_major() { node --version 2>/dev/null | sed -E 's/^v([0-9]+).*/\1/'; }

# ---------------------------------------------------------------- core
if group_on core; then
  head_ "core"
  need_system git git
  if has node && [ "$(node_major)" -ge 20 ] 2>/dev/null; then
    PRESENT="$PRESENT node"; say " ok node ($(node --version))"
  else
    say " - node: missing or older than 20 (gh-axi and chrome-devtools-axi need 20+)"
    cmd="$(pkg_hint node node)"
    if [ -n "$cmd" ]; then step node "$cmd"; else SKIPPED="$SKIPPED node(no-brew)"; say "   Install Node 20 or newer, then run this again."; fi
  fi
  if has python3 && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
    PRESENT="$PRESENT python3"; say " ok python3 ($(python3 --version 2>&1))"
  else
    say " - python3: missing or older than 3.9 (the ns usage tool needs it). Install Python 3.9 or newer."
    SKIPPED="$SKIPPED python3"
  fi
  need_system gh gh
  if has gh; then
    if gh auth status >/dev/null 2>&1; then say " ok gh is logged in"; else step "gh-login" "gh auth login"; fi
  fi
  say " ok gh-axi runs through npx, nothing to install"
fi

# ---------------------------------------------------------------- ui
if group_on ui; then
  head_ "ui proof"
  if has npm; then
    need_tool playwright-cli "npm i -g @playwright/cli"
    need_tool lighthouse "npm i -g lighthouse"
    need_tool axe "npm i -g @axe-core/cli"
  else
    say " - npm is missing, so playwright-cli, lighthouse and axe cannot be installed. Install Node first."
    SKIPPED="$SKIPPED playwright-cli lighthouse axe"
  fi
  need_system ffmpeg ffmpeg
  if has playwright-cli; then
    say " - playwright-cli needs a browser to drive: 'playwright-cli install-browser' downloads one (skip it if you will use Chrome)"
    if [ "$DRY" = 0 ] && ask "Download the Playwright browser now?"; then
      playwright-cli install-browser && INSTALLED="$INSTALLED playwright-browser" || FAILED="$FAILED playwright-browser"
    fi
  fi
  if [ -d "/Applications/Google Chrome.app" ] || has google-chrome || has google-chrome-stable || has chromium || has chromium-browser; then
    say " ok Google Chrome (chrome-devtools-axi and lighthouse use it)"
  else
    say " - Google Chrome is missing: install it from https://www.google.com/chrome/ (chrome-devtools-axi and lighthouse need it)"
    SKIPPED="$SKIPPED chrome"
  fi
fi

# ---------------------------------------------------------------- delegate
if group_on delegate; then
  head_ "delegate (ns-flow-delegate)"
  if has herdr; then
    PRESENT="$PRESENT herdr"; say " ok herdr ($(command -v herdr))"
  elif has brew; then
    step herdr "brew install herdr"
  else
    step herdr "curl -fsSL https://herdr.dev/install.sh | sh"
  fi
  if has claude; then PRESENT="$PRESENT claude"; say " ok claude ($(command -v claude))"; else
    say " - claude (Claude Code) is missing: delegate launches its agents with it. Install it from https://claude.com/claude-code"
    SKIPPED="$SKIPPED claude"
  fi
fi

# ---------------------------------------------------------------- vercel
if group_on vercel; then
  head_ "vercel"
  if has npm; then need_tool vercel "npm i -g vercel"; else say " - npm is missing, skipping vercel"; SKIPPED="$SKIPPED vercel"; fi
fi

# ---------------------------------------------------------------- plugin skills
if group_on plugins; then
  head_ "plugin skills (mattpocock-skills)"
  if harness_on claude; then
    if has claude; then
      if claude plugin list 2>/dev/null | grep -q "mattpocock-skills"; then
        PRESENT="$PRESENT mattpocock-skills(claude)"; say " ok mattpocock-skills is installed in Claude Code"
      else
        step "mattpocock-skills(claude)" "claude plugin install mattpocock-skills@claude-plugins-official"
      fi
    else
      say " - claude is missing, so the Claude Code plugin cannot be installed"; SKIPPED="$SKIPPED mattpocock-skills(claude)"
    fi
  fi
  others=""
  for h in codex opencode cursor; do harness_on "$h" && others="$others -a $h"; done
  if [ -n "$others" ]; then
    if [ -d "$HOME/.agents/skills/grilling" ]; then
      PRESENT="$PRESENT mattpocock-skills(agents)"; say " ok mattpocock-skills is in ~/.agents/skills (Codex, OpenCode and Cursor read it)"
    elif has npx; then
      step "mattpocock-skills(agents)" "npx --yes $SKILLS_CLI add mattpocock/skills -g$others -y"
    else
      say " - npx is missing, skipping the Codex, OpenCode and Cursor install"; SKIPPED="$SKIPPED mattpocock-skills(agents)"
    fi
  fi
fi

# ---------------------------------------------------------------- summary
head_ "summary"
say " already present:${PRESENT:- none}"
say " installed now:  ${INSTALLED:- none}"
say " skipped:        ${SKIPPED:- none}"
say " failed:         ${FAILED:- none}"
say ""
say "Check the result any time with:  python3 <skills folder>/ns-route/scripts/ns doctor"
[ -z "$FAILED" ]
