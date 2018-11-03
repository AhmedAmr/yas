
from yas.main import YasTest

def test_yas(tmp):
    with YasTest() as app:
        res = app.run()
        print(res)
        raise Exception

def test_command1(tmp):
    argv = ['command1']
    with YasTest(argv=argv) as app:
        app.run()
