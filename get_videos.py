"""This service allows to get videos form database"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor

r = get_redis()

def get_videos(type, col=False, value=False):
    """Returns videos info from databse (table videos)"""
    cursor, _ = get_cursor()
    if not cursor:
        # log that failed getting cursor
        return False
    q = '''SELECT * FROM videos '''
    if type is not None:
        value = value.replace(";", "")
        value = value.replace("'", "''")
        if type == "WHERE" and col and value:
            q += f"""WHERE {col} = '{value}'"""
        else:
            return False
    try:
        cursor.execute(q)
    except MySQLdb.Error as error:
        return error
        # LOG
        return False
        # sys.exit("Error:Failed getting new videos from database")
    data = cursor.fetchall()
    cursor.close()
    return data


if __name__ == '__main__':
    q = Queue('get_videos', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r,  name='get_videos')
        worker.work()
