import aiosqlite

DB_FILE = "miner.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 0,
                power INTEGER DEFAULT 1
            )
        ''')
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT * FROM users WHERE user_id=?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"user_id": row[0], "coins": row[1], "power": row[2]}
            else:
                await db.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
                await db.commit()
                return {"user_id": user_id, "coins": 0, "power": 1}

async def update_user(user_id, coins=None, power=None):
    async with aiosqlite.connect(DB_FILE) as db:
        if coins is not None:
            await db.execute('UPDATE users SET coins=? WHERE user_id=?', (coins, user_id))
        if power is not None:
            await db.execute('UPDATE users SET power=? WHERE user_id=?', (power, user_id))
        await db.commit()


