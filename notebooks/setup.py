import os, sys
from decouple import config

PWD = config('PWD')

PROJ_MISSING_MSG = """Set an enviroment variable:\n
`DJANGO_PROJECT=your_project_name`\n
or call:\n
`init_django(your_project_name)`
"""


def init_django(project_name=None):
    os.chdir(PWD)
    project_name = project_name or config('DJANGO_PROJECT') or None
    if project_name is None:
        raise Exception(PROJ_MISSING_MSG)
    sys.path.insert(0, config('PWD'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django
    django.setup()

