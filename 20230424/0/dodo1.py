import glob


def task_po():
    return {
        'actions': ['pybabel extract -o counter.pot counter.py',],
        'file_dep': ['counter.py',],
        'targets': ['counter.po',],
    }


def task_pot():
    return {
        'actions': ['pybabel update -D counter -d po -i counter.pot -l ru',],
        'task_dep': ['po',],
        'targets': ['counter.pot',],
    }


def task_mo():
    return {
        'actions': ['pybabel compile -D counter -d po -l ru',],
        'task_dep': ['pot',],
        'targets': ['counter.mo',],
    }


def task_test():
    return {
        'actions': ['python3 -m unittest test.py',],
        'file_dep': ['counter.py',],
    }