from pathlib import Path
from services.db_context import db
from asyncpg.exceptions import DuplicateColumnError
import nonebot

driver = nonebot.get_driver()


@driver.on_startup
async def _init_database():
    file = Path() / 'plugins' / 'database_scripts.py'
    if file.exists():
        update_sql = [
            'ALTER TABLE russian_users ADD winning_streak Integer default 0;',
            'ALTER TABLE russian_users ADD losing_streak Integer default 0;',
            'ALTER TABLE russian_users ADD max_winning_streak Integer default 0;',
            'ALTER TABLE russian_users ADD max_losing_streak Integer default 0;',
            'ALTER TABLE group_info_users ADD uid Integer default 0;'
        ]
        for sql in update_sql:
            try:
                query = db.text(sql)
                await db.first(query)
            except DuplicateColumnError:
                pass
        file.unlink()



