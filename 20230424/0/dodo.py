PICTURE = 'd1'
DOIT_CONFIG =  {'default_tasks': ['png']}

def task_png():
    return {
        'actions': [f'dia {PICTURE}.dia -s 1024 -e {PICTURE}.png'],
        'file_dep': [f'{PICTURE}.dia'],
        'targets': [f'{PICTURE}.png'],
    }


def task_mini():
    
    for size in 16, 32, 64:
        yield {
            'name': f'do{size}',
            'file_dep': [f'{PICTURE}.png'],
            'actions': [f'convert {PICTURE}.png -resize {size} {PICTURE}-{size}.png'],
            'targets': [f'{PICTURE}-{size}.png'],            
        }

def task_icon():
    return {
        'action':[f'convert {PICTURE}-64.png {PICTURE}.icon'],
        'task_dep': ['mini:do64'],
    }


def task_erase():
    return {
        'actions': [f'rm -f {PICTURE}.png'],
    }