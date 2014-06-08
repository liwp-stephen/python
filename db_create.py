__author__ = 'Stephen'

from xml.etree.cElementTree import ElementTree
import sqlite3
import subprocess
import hashlib


def create_db(file_path):
    tree = ElementTree(file=file_path)
    root = tree.getroot()
    db_name = root.attrib['name']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for table in tree.iter(tag='table'):
        create_sql_arr = ['CREATE TABLE IF NOT EXISTS %s' % table.attrib['name'], ' (']
        index = 0
        for column in table:
            if index != 0:
                create_sql_arr.append(', ')
            index += 1
            create_sql_arr.append('%s %s' % (column.attrib['name'], column.attrib['type']))
            if 'pk' in column.attrib and column.attrib['pk'] == '1':
                create_sql_arr.append(' PRIMARY KEY')
        create_sql_arr.append(')')
        create_sql = ''.join(create_sql_arr)
        c.execute(create_sql)
        print 'Execute sql:%s' % create_sql
    conn.commit()
    conn.close()


def create_zip(file_path):
    tree = ElementTree(file=file_path)
    root = tree.getroot()
    db_name = root.attrib['name']

    if 'zip_name' in root.attrib:
        zip_name = root.attrib['zip_name']
        subprocess.call(['zip', '-q', '-r', zip_name, db_name])
        print('The MD5 checksum of %s is %s' % (zip_name, md5_checksum(zip_name)))


def md5_checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


if __name__ == "__main__":
    create_db('AB001.xml')
    create_zip('AB001.xml')
    create_db('AB002.xml')
    create_zip('AB002.xml')