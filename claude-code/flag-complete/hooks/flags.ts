// Pure logic: parse argument-hints, answer a token. No engine calls.

export type Flag = { short?: string; long?: string; values: string[] }
export type Row = { text: string; label?: string; description?: string }

// `[-r a|b|c]`, `[-r|--role a|b]`, `[--role a|b]`. Groups without `|` in values are free-form, skipped.
const GROUP = /\[\s*(-[A-Za-z0-9])?(?:\s*\|\s*)?(--[A-Za-z0-9][\w-]*)?\s+([^\]\s]+)\s*\]/g

export function parseHint(hint: string | undefined): Flag[] {
  if (!hint) return []
  const flags: Flag[] = []
  for (const m of hint.matchAll(GROUP)) {
    const [, short, long, raw] = m
    if (!short && !long) continue
    const values = raw.split('|').filter(Boolean)
    if (values.length < 2) continue
    flags.push({ short, long, values })
  }
  return flags
}

const names = (f: Flag) => [f.short, f.long].filter((n): n is string => !!n)
const find = (flags: Flag[], tok: string) =>
  flags.find(f => names(f).includes(tok)) ??
  flags.find(f => names(f).some(n => n.toLowerCase() === tok.toLowerCase()))

const valueRows = (f: Flag, prefix: string, write: (v: string) => string): Row[] => {
  const p = prefix.toLowerCase()
  const hits = f.values.filter(v => v.toLowerCase().startsWith(p))
  if (hits.length === 1 && hits[0].toLowerCase() === p) return [] // already complete
  return hits.map(v => ({ text: write(v) + ' ', label: v, description: names(f).join(' ') }))
}

/** Command name at start of the draft, if the cursor is past it. */
export function commandOf(text: string, start: number): string | undefined {
  const m = /^\s*\/(\S+)\s/.exec(text)
  return m && start >= m[0].length ? m[1] : undefined
}

/** Rows for the token at the cursor. text/start/token as prompt.autocomplete gives them. */
export function complete(flags: Flag[], text: string, start: number, token: string): Row[] {
  if (!flags.length) return []

  // --role=val
  const eq = /^(--[\w-]+)=(.*)$/.exec(token)
  if (eq) {
    const f = find(flags, eq[1])
    return f ? valueRows(f, eq[2], v => `${f.long}=${v}`) : []
  }

  // exact flag: -r -> "-r engineer", ...
  const exact = find(flags, token)
  if (exact) return valueRows(exact, '', v => `${names(exact).find(n => n.toLowerCase() === token.toLowerCase()) ?? token} ${v}`)

  // partial flag: "-" / "--ro" -> list unused flags
  if (token.startsWith('-')) {
    const used = new Set(text.split(/\s+/))
    return flags
      .filter(f => !names(f).some(n => used.has(n) && n !== token))
      .flatMap(f => {
        const n = names(f).find(n => n.startsWith(token))
        return n ? [{ text: n, description: f.values.join('|') }] : []
      })
  }

  // value after a flag: "-r en" -> engineer
  const prev = /(\S+)\s+$/.exec(text.slice(0, start))?.[1]
  const f = prev ? find(flags, prev) : undefined
  return f ? valueRows(f, token, v => v) : []
}
