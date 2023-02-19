from glob import iglob

for br in iglob('../../.git/refs/heads/*', recursive=True):
    print(br.split('/')[-1])
