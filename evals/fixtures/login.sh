#!/usr/bin/env bash
mkdir -p src/auth
cat > src/auth/login.js <<'JS'
// POST /login
export async function login(req, res) {
  const { email, password } = req.body;
  const user = await db.users.findByEmail(email);
  if (!user || !(await verify(password, user.hash))) return res.status(401).end();
  res.json({ token: sign(user.id) });
}
JS
