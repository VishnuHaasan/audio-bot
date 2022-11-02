import os


def LoadEnv():
    f = open(os.getcwd() + "/.env")
    for i in f.readlines():
        k = i.strip().split("=")
        os.environ[k[0]] = k[1]
    