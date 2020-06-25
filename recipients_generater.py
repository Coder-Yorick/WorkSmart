import os
import time
from pathlib import Path
from configparser import ConfigParser

CONFIG_PATH = 'test/config.ini'
OUTPUT_TITLES = ['email', 'name', 'id', 'gender']
ALL_OUTPUT_TITLES = ['hash', 'email', 'name', 'id', 'gender']

def main():
    cf = read_config()
    if cf is not None:
        out_name = 'output'
        file_count = 0
        count = 0
        file_writer = txtWriter(OUTPUT_TITLES)
        all_writer = txtWriter(ALL_OUTPUT_TITLES)
        for file_name in os.listdir(cf['src_folder']):
            file = os.path.join(cf['src_folder'], file_name)
            if file.endswith('.txt'):
                file_datas = read_txt(file)
                for file_data in file_datas:
                    count += 1
                    hash_key = 'hash{}'.format(count)
                    all_writer.append([hash_key] + file_data)
                    if file_writer.append([file_data[0],hash_key,hash_key,file_data[3]]) >= cf['out_count']:
                        file_count += 1
                        file_writer.save(os.path.join(cf['out_folder'], '{}{}.txt'.format(out_name, file_count)))
        if len(file_writer.rows) > 0:
            file_count += 1
            file_writer.save(os.path.join(cf['out_folder'], '{}{}.txt'.format(out_name, file_count)))  
        all_writer.save(os.path.join(cf['out_folder'], 'all.txt'))

class txtWriter():
    def __init__(self, titles = []):
        self.titles = titles
        self.rows = []

    def append(self, row = []):
        self.rows.append(row)
        return len(self.rows)
    
    def save(self, file_name):
        with open(file_name, 'w', encoding="utf-8") as txtfile:
            txtfile.write('{}\n'.format(','.join(self.titles)))
            for row in self.rows:
                line = ','.join(row).replace('\n', '').replace('\r', '')
                txtfile.write('{}\n'.format(line))
        self.rows = []

def read_txt(txtfile):
    try:
        rows = []
        with open(txtfile, 'r', encoding="utf-8") as f:
            escaped_title = False
            for line in f.readlines():
                if escaped_title:
                    rows.append(line.split(','))
                else:
                    escaped_title = True        
        return rows
    except Exception as ex:
        print(ex)
        return []

def read_config():
    try:
        config = ConfigParser()
        config.read(CONFIG_PATH)
        src_folder = config.get('Source', 'Path')
        out_folder = config.get('Output', 'Path')
        out_count = int(config.get('Output', 'Count'))

        # check setting
        if not os.path.exists(src_folder):
            print('source path not exist {}'.format(src_folder))
            return None
        Path(out_folder).mkdir(parents=True, exist_ok=True)

        return {
            'src_folder': src_folder,
            'out_folder': out_folder,
            'out_count': out_count
        }
    except Exception as ex:
        print(ex)
        return None

if __name__ == '__main__':
    main()