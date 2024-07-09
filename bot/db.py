import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
                            user_id INTEGER PRIMARY KEY,
                            question_index INTEGER,
                            correct_answers INTEGER DEFAULT 0)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
                            user_id INTEGER PRIMARY KEY,
                            correct_answers INTEGER,
                            total_questions INTEGER)''')
        await db.commit()

async def update_correct_answers(user_id, increment):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR IGNORE INTO quiz_state (user_id, question_index, correct_answers) VALUES (?, 0, 0)', (user_id,))
        await db.execute('UPDATE quiz_state SET correct_answers = correct_answers + ? WHERE user_id = ?', (increment, user_id))
        await db.commit()

async def get_correct_answers(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers FROM quiz_state WHERE user_id = ?', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result and result[0] is not None:
                return result[0]
            else:
                return 0

async def reset_quiz_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answers) VALUES (?, 0, 0)', (user_id,))
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET question_index = ? WHERE user_id = ?', (index, user_id))
        await db.commit()

async def get_quiz_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers, total_questions FROM quiz_results WHERE user_id = ?', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result:
                return result
            else:
                return None

async def update_quiz_result(user_id, correct_answers, total_questions):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, correct_answers, total_questions) VALUES (?, ?, ?)',
                         (user_id, correct_answers, total_questions))
        await db.commit()
