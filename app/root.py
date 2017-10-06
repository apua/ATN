from hug import extend_api

@extend_api('/testcase')
def _():
    import testcase
    return [testcase]
