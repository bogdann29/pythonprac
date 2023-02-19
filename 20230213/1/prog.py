from glob import iglob
import zlib

branch_name = '../../.git/refs/heads/' + input()

with open(branch_name, 'r') as f:
    commit_hash = f.read()

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

print(*commit_data, commit_msg, sep='\n')