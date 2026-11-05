import { expect, test } from 'claude-code/testing'
import { commandOf, complete, parseHint } from './flags'

const EXPLAIN = parseHint('[-r engineer|pm|business-manager|designer|qa|executive] [-l novice|competent|proficient|expert] [-b bare|lean|normal|verbose] <topic>')
const at = (text: string) => {
  const start = text.length - (/\S+$/.exec(text)?.[0].length ?? 0)
  return complete(EXPLAIN, text, start, text.slice(start))
}

test('parses hint groups, skips free-form', async () => {
  expect(EXPLAIN.length).toBe(3)
  expect(EXPLAIN[0]).toEqual({ short: '-r', long: undefined, values: ['engineer', 'pm', 'business-manager', 'designer', 'qa', 'executive'] })
  expect(parseHint('[-r|--role a|b] [name]')).toEqual([{ short: '-r', long: '--role', values: ['a', 'b'] }])
  expect(parseHint(undefined)).toEqual([])
})

test('command detection', async () => {
  expect(commandOf('/explain -r', 9)).toBe('explain')
  expect(commandOf('/explain', 1)).toBe(undefined)
})

test('exact flag lists values', async () => {
  const rows = at('/explain -r')
  expect(rows.map(r => r.label)).toEqual(['engineer', 'pm', 'business-manager', 'designer', 'qa', 'executive'])
  expect(rows[0].text).toBe('-r engineer ')
  expect(at('/explain -R')[0].text).toBe('-r engineer ')
})

test('partial value after flag filters', async () => {
  expect(at('/explain -l pro').map(r => r.text)).toEqual(['proficient '])
  expect(at('/explain -l expert')).toEqual([])
})

test('dash lists unused flags', async () => {
  expect(at('/explain -').map(r => r.text)).toEqual(['-r', '-l', '-b'])
  expect(at('/explain -r pm -').map(r => r.text)).toEqual(['-l', '-b'])
})

test('long form with =', async () => {
  const f = parseHint('[-r|--role engineer|pm]')
  expect(complete(f, '/x --role=e', 3, '--role=e').map(r => r.text)).toEqual(['--role=engineer '])
})

test('topic words get nothing', async () => {
  expect(at('/explain how oauth')).toEqual([])
})
