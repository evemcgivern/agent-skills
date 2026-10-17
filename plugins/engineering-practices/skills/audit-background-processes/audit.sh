#!/usr/bin/env bash
# Report stray background processes (default), or kill specific PIDs from the
# report (--kill <pid>...). Nothing is ever killed by pattern or by guesswork.
#
#   audit.sh                 report only
#   audit.sh --kill 123 456  kill these PIDs, but only if each one is still a
#                            suspected orphan in a fresh report
#
# A suspected orphan is a process owned by you whose parent is PID 1 (its
# launching shell is gone), outside system and application paths, that is not
# an interactive shell, not this script or one of its ancestors, and not an
# ancestor of any interactive shell (a tmux or screen server, for example).
set -u -o pipefail

usage () {
  echo "usage: $0            report suspected orphans" >&2
  echo "       $0 --kill PID [PID...]   SIGTERM PIDs that are still suspects" >&2
  exit 2
}

hdr () { printf '\n=== %s ===\n' "$1"; }

# Prints one line per suspect: "pid ppid etime args".
suspects () {
  ps -A -o pid=,ppid=,uid=,etime=,args= | awk -v me="$(id -u)" -v self="$$" '
    function is_shell(a,   n, w, b) {
      n = split(a, w, " ")
      if (substr(w[1], 1, 1) == "-") return 1          # login shell: -zsh, -bash
      b = w[1]; sub(/.*\//, "", b)
      if (b !~ /^(sh|bash|zsh|fish|ksh|tcsh)$/) return 0
      return (n == 1 || w[2] ~ /^-[A-Za-z]*i[A-Za-z]*$/)
    }
    {
      pid = $1; ppid[pid] = $2; uid[pid] = $3; etime[pid] = $4
      a = $0; sub(/^ *[0-9]+ +[0-9]+ +[0-9]+ +[^ ]+ +/, "", a); args[pid] = a
      order[++n] = pid
    }
    END {
      # Protect this script and every ancestor of it, and every interactive
      # shell plus every ancestor of one.
      for (p = self; p != "" && p > 1 && !(p in prot); p = ppid[p]) prot[p] = 1
      for (i = 1; i <= n; i++) {
        p = order[i]
        if (!is_shell(args[p])) continue
        for (q = p; q != "" && q > 1 && !(q in prot); q = ppid[q]) prot[q] = 1
      }
      for (i = 1; i <= n; i++) {
        p = order[i]
        if (p <= 1 || ppid[p] != 1 || uid[p] != me || (p in prot)) continue
        if (args[p] ~ /^\/(System|Library|Applications|usr\/(s?bin|libexec))\//) continue
        if (args[p] ~ /^\/Users\/[^\/]+\/Applications\//) continue
        print p, ppid[p], etime[p], args[p]
      }
    }'
}

report () {
  # Only your own processes: other users' command lines can hold secrets.
  hdr "your interactive shells (never kill)"
  ps -U "$(id -u)" -o pid=,ppid=,etime=,args= | awk '$4 ~ /^-/ || / (zsh|bash) -il?$/' \
    | cut -c1-120 || true

  hdr "your live test and benchmark runs (killing one loses its in-flight work)"
  ps -U "$(id -u)" -o pid=,ppid=,etime=,args= \
    | awk '/[p]ytest|[b]enchmark|[e]val battery|[g]o test|[j]est|[v]itest/ { print; n++ } END { if (!n) print "  none" }' \
    | cut -c1-120

  hdr "suspected orphans: PID PPID AGE COMMAND"
  local out
  out="$(suspects)"
  if [ -z "$out" ]; then
    echo "  none"
  else
    printf '%s\n' "$out" | cut -c1-160
    echo
    echo "Read each line before acting. To kill some of them: $0 --kill PID [PID...]"
  fi
}

kill_pids () {
  [ "$#" -gt 0 ] || usage
  local pid
  for pid in "$@"; do
    case "$pid" in
      ''|*[!0-9]*) echo "not a PID: '$pid' (--kill accepts numeric PIDs only)" >&2; exit 2 ;;
    esac
  done

  local current
  current="$(suspects)"

  hdr "will send SIGTERM to"
  local targets=() line
  for pid in "$@"; do
    line="$(printf '%s\n' "$current" | awk -v p="$pid" '$1 == p')"
    if [ -z "$line" ]; then
      echo "  REFUSE $pid: not in the current suspect list (exited, has a live parent, is protected, or is not yours)"
      continue
    fi
    echo "  $(printf '%s' "$line" | cut -c1-150)"
    targets+=("$pid")
  done

  if [ "${#targets[@]}" -eq 0 ]; then
    echo "  nothing to kill"
    return 0
  fi

  hdr "killing"
  for pid in "${targets[@]}"; do
    if kill -TERM "$pid" 2>/dev/null; then
      echo "  sent SIGTERM to $pid"
    else
      echo "  could not signal $pid (already gone, or permission denied)"
    fi
  done

  sleep 1
  hdr "still running after SIGTERM (listing, not counting)"
  local alive=0
  for pid in "${targets[@]}"; do
    if ps -o pid=,args= -p "$pid" >/dev/null 2>&1; then
      ps -o pid=,args= -p "$pid" | cut -c1-120
      alive=1
    fi
  done
  if [ "$alive" -eq 0 ]; then
    echo "  none"
  else
    echo "  Re-check these by PID; use 'kill -9 PID' yourself only if SIGTERM is ignored."
  fi
}

case "${1:-}" in
  "") report ;;
  --kill) shift; kill_pids "$@" ;;
  *) usage ;;
esac
