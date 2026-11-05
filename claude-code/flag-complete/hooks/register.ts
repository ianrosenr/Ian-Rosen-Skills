import type { Register } from 'claude-code'
import { commandOf, complete, parseHint, type Flag } from './flags'

// command name -> flags, captured as the engine lists commands for the typeahead.
const specs = new Map<string, Flag[]>()

export const register: Register = on => {
  on('command.describe', async ($, e, next) => {
    const r = await next(e)
    const flags = parseHint(r.argumentHint)
    if (flags.length) specs.set(e.command, flags)
    else specs.delete(e.command)
    return r
  })

  // Reload wipes `specs`; force the engine to describe commands again.
  on('session.start', ($, e, next) => {
    $.ui.invalidate('command.describe')
    return next(e)
  })

  on('prompt.autocomplete', async ($, e, next) => {
    const base = await next(e)
    const cmd = commandOf(e.text, e.start)
    const flags = cmd ? specs.get(cmd) : undefined
    if (!flags) return base
    const mine = complete(flags, e.text, e.start, e.token)
    return mine.length ? { suggestions: [...base.suggestions, ...mine] } : base
  })
}
