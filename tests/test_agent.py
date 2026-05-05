from app.code_agent import CodeAgent


def test_cleaners():
    a = CodeAgent()
    assert a.money('$1,234.50') == 1234.50
    assert a.rating('4.7') == 4.7
