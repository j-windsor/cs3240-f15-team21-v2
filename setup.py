from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('nicegui.py', base=base, targetName = 'secureshare')
]

setup(name='SecureShare',
      version = '1.0',
      description = 'CS3240 project',
      options = dict(build_exe = buildOptions),
      executables = executables)
