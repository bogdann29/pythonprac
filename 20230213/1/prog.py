from glob import iglob
import zlib


def commit(commit_hash):
    commit_file = '../../.git/objects/' + commit_hash[0:2] + '/' + commit_hash[2:].replace('\n', '')

    with open(commit_file, 'rb') as f:
        commit_data = zlib.decompress(f.read())

    idx = commit_data.rindex(b'+0300\n\n')

    commit_msg = commit_data[idx + len(b'+0300\n\n'):].decode()[:-1]

    commit_data = str(commit_data[:idx + len(b'+0300\n\n') - 1])

    idx = commit_data.index('x00')
    commit_data = commit_data[idx + len('x00'):-1].split('\\n')

    tmp = commit_data[2].split()
    commit_data[2] = ' '.join(tmp[:-2])

    tmp = commit_data[3].split()
    commit_data[3] = ' '.join(tmp[:-2])

    commit_data.append(commit_msg)
    return commit_data


def tree(tree_hash):
    tree_file = '../../.git/objects/' + tree_hash[0:2] + '/' + tree_hash[2:].replace('\n', '')
    with open(tree_file, 'rb') as f:
        tree_data = zlib.decompress(f.read())

    data = tree_data.partition(b'\x00')[-1]

    while data:
        obj, _, data = data.partition(b'\x00')
        obj_mode, obj_name = obj.split()
        obj_num = data[:20].hex()
        data = data[20:]
        obj_type = 'er mode'
        if obj_mode.decode() == '40000':
            obj_type = 'tree'
        elif obj_mode.decode() == '100644':
            obj_type = 'blob'
        print(obj_type, obj_num, obj_name.decode())


branch_name = '../../.git/refs/heads/' + input()

with open(branch_name, 'r') as f:
    commit_hash = f.read()

commit_data = commit(commit_hash)

tree_hash = commit_data[0].split()[1]
tree(tree_hash)
