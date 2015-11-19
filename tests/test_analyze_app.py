import os

# Compile and run code to test out for trivial mistakes
def test_import_app():
    app_filename = 'bin/fpa'
    with open(app_filename) as f:
        code = compile(f.read(), app_filename, 'exec')
        exec(code)
