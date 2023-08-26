import sqlite3

connection = sqlite3.connect('user_profiles.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id TEXT PRIMARY KEY,
        leetcode_username TEXT,
        solved_problems TEXT,
        score INTEGER
    )
''')

connection.commit()

def register_user(user_id, leetcode_username):
    cursor.execute('INSERT OR REPLACE INTO user_profiles (user_id, leetcode_username) VALUES (?, ?)', (user_id, leetcode_username))
    connection.commit()


def get_user_profile(user_id):
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    profile = cursor.fetchone()
    return profile

def update_user_profile(user_id, leetcode_username):
    cursor.execute('UPDATE user_profiles SET leetcode_username = ? WHERE user_id = ?', (leetcode_username, user_id))
    connection.commit()

def get_leetcode_id(user_id):
    cursor.execute('SELECT leetcode_username FROM user_profiles WHERE user_id = ?', (user_id,))
    leetcode_username = cursor.fetchone()
    return leetcode_username[0]