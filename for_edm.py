import os
import time
from pathlib import Path
from configparser import ConfigParser

CONFIG_PATH = 'config.ini'
OUTPUT_TITLES = ['email', 'name', 'PID', 'sex']
ALL_OUTPUT_TITLES = ['hash', 'email', 'name', 'id', 'sex', 'source']

def main():
    print('-----start-----')
    cf = read_config()
    if cf is None:
        return
    
    file_writer = txtWriter(OUTPUT_TITLES)
    all_writer = txtWriter(ALL_OUTPUT_TITLES)
    no_more_hash = False
    current_file_name = ''
    for file_name in os.listdir(cf['src_folder']):
        if no_more_hash:
            break
        file = os.path.join(cf['src_folder'], file_name)
        if file.endswith('.txt'):
            file_writer.count = 1
            current_file_name = file_name[:-4]
            file_datas = read_source(file)
            for file_data in file_datas:
                try:
                    # check pid
                    pid = file_data[2]
                    if pid in cf['out_history']['pid_set']:
                        continue
                    # check hash
                    hash_key = ''
                    while hash_key == '':
                        hash_key = next(cf['hash_gen'])
                        if hash_key in cf['out_history']['hash_set']:
                            hash_key = ''
                    if file_writer.append([file_data[0],hash_key,hash_key,file_data[3]]) >= cf['out_count']:
                        file_writer.save(current_file_name)
                    all_writer.append([hash_key] + file_data + [current_file_name])
                except StopIteration:
                    no_more_hash = True
                    break
            file_writer.save(current_file_name)
    all_writer.save()
    print('-----finish-----')
    os.system('pause')

class txtWriter():
    def __init__(self, titles = []):
        self.titles = titles
        self.rows = []
        self.count = 1

    def append(self, row = []):
        self.rows.append(row)
        return len(self.rows)
    
    def save(self, file_name = None):
        if file_name is None:
            file_path = os.path.join('output', 'all.txt')
            file_exist = os.path.exists(file_path)            
            with open(file_path, 'a' if file_exist else 'w', encoding="utf-8") as txtfile:
                if not file_exist:
                    txtfile.write('{}\n'.format(','.join(self.titles)))
                for row in self.rows:
                    line = ','.join(row).replace('\n', '').replace('\r', '')
                    txtfile.write('{}\n'.format(line))
                print('{} 新增{}筆資料'.format(file_path, len(self.rows)))          
        else:
            file_path = os.path.join('output', 'R_{}_{}.txt'.format(file_name, self.count))
            while os.path.exists(file_path):
                self.count += 1
                file_path = os.path.join('output', 'R_{}_{}.txt'.format(file_name, self.count))            
            with open(file_path, 'w', encoding="utf-8") as txtfile:
                txtfile.write('{}\n'.format(','.join(self.titles)))
                for row in self.rows:
                    line = ','.join(row).replace('\n', '').replace('\r', '')
                    txtfile.write('{}\n'.format(line))
                print('{} 新增{}筆資料'.format(file_path, len(self.rows)))
        self.rows = []

def get_history():
    history = {
        'hash_set': set(),
        'pid_set': set()
    }
    all_file = os.path.join('output', 'all.txt')
    if os.path.exists(all_file):
        history_sets = read_part(all_file, col_indexes=[0, 3])
        history['hash_set'].update(history_sets[0])
        history['pid_set'].update(history_sets[1])
    return history
            
def read_part(txtfile, col_indexes=[]):
    datas = [list() for _ in range(len(col_indexes))]
    try:
        with open(txtfile, 'r', encoding="utf-8") as f:
            for idx, line in enumerate(f):
                if idx > 0:
                    col_values = line.split(',')
                    if len(col_values) > 0:
                        for i, col_index in enumerate(col_indexes):
                            if len(col_values) > col_index:
                                datas[i].append(col_values[col_index])
    except Exception as ex:
        print('read_part error')
        print(ex)
    return datas

def read_source(txtfile):
    try:
        rows = []
        with open(txtfile, 'r', encoding="utf-8") as f:
            for idx, line in enumerate(f):
                if idx > 0:
                    rows.append(line.split(','))
        return rows
    except Exception as ex:
        print('read_source error')
        print(ex)
        return []

def read_hash(hash_file):
    try:
        hashs = []
        with open(hash_file, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                hash_key = line.replace('\n', '').replace('\r', '').strip()
                if len(hash_key) > 0:
                    hashs.append(hash_key) 
        return hashs
    except:
        print('不使用hashes.txt')
        return []

def hash_gen(hash_setting):
    def gen_specific():
        for h in hash_setting:
            yield h
    def gen_normal(num = 0):
        num = yield num
        while True:
            yield '{}{}'.format(hash_setting, str(num).zfill(7))
            num += 1
    if isinstance(hash_setting, list):
        return gen_specific()
    else:
        g = gen_normal()
        next(g)
        return g

def read_config():
    try:
        config = ConfigParser()
        config.read(CONFIG_PATH, encoding='utf-8-sig')
        src_folder = config.get('Source', 'Path')
        hash_setting = config.get('Source', 'HashPrefix')
        hash_start = int(config.get('Source', 'HashStart')) - 1
        out_count = int(config.get('Output', 'Count'))

        # check setting
        if not os.path.exists(src_folder):
            print('source path not exist {}'.format(src_folder))
            return None
        Path('output').mkdir(parents=True, exist_ok=True)

        out_history = get_history()

        hashes = read_hash('hashes.txt')
        if len(hashes) == 0:
            print('使用隨機亂數,開頭為: {}'.format(hash_setting))
            hash_generator = hash_gen(hash_setting)
            hash_generator.send(len(out_history['hash_set']) + hash_start)
        else:
            hash_generator = hash_gen(hashes)

        return {
            'src_folder': src_folder,
            'hash_gen': hash_generator,
            'out_count': out_count,
            'out_history': out_history
        }
    except Exception as ex:
        print('read_config error')
        print(ex)
        return None

if __name__ == '__main__':
    main()