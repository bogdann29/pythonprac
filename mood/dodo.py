def task_whlserver():
	return {
		'actions': ['python3 -m build -n -w moodserver'],
		'file_dep': ['moodserver/pyproject.toml'],
		'targets': ['moodserver/dist/*.whl'],
		}

def task_whlclient():
	return {
		'actions': ['python3 -m build -n -w moodclient'],
		'file_dep': ['moodclient/pyproject.toml'],
		'targets': ['moodclient/dist/*.whl'],
		}

def task_wheels():
	return {
		'actions': [],
		'task_dep': ['whlserver', 'whlclient'],
		}