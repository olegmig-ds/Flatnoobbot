from environs import Env


env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
ADMINS = [int(i) for i in env.list('ADMINS')]