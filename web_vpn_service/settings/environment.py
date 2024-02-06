import os

import environ

current_path = environ.Path(__file__) - 1
site_root = current_path - 2

env = environ.Env()
env_file = os.path.join(site_root, '.env')
if os.path.isfile(env_file):
    environ.Env.read_env(env_file=env_file)
