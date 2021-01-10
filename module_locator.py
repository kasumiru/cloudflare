# utf-8 ? we need unicode
import sys
import os


'''for find absolute path dir. see https://coderoad.ru/2632199/Как-получить-путь-к-текущему-исполняемому-файлу-в-Python#2632297
or https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory
'''

def we_are_frozen():
    return hasattr(sys, "frozen")

def module_path():
    if we_are_frozen():
        a = os.path.dirname(sys.executable)
        return a.encode().decode()

    a = os.path.dirname(__file__)
    return a.encode().decode()

#def we_are_frozen():
#    # All of the modules are built-in to the interpreter, e.g., by py2exe
#    return hasattr(sys, "frozen")
#
#def module_path():
#    encoding = sys.getfilesystemencoding()
#    if we_are_frozen():
#        return os.path.dirname(unicode(sys.executable, encoding))
#    return os.path.dirname(unicode(__file__, encoding))
