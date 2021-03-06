# -*- mode: python -*-

import guidata
import guiqwt
import pymzml
import pyopenms

import inspect
# the build folder should be the first path on the stack
dirname = os.path.dirname(os.path.abspath( inspect.stack()[0][1] ))
tapir_exe = os.path.join(os.path.join(dirname, ".."), "TAPIR.py")
tapir_icon = os.path.join(os.path.join(dirname, "icons"), "tapir.icns")

def dir_files(path, rel):
    ret = []
    for p,d,f in os.walk(path):
        relpath = p.replace(path, '')[1:]
        for fname in f:
            ret.append((os.path.join(rel, relpath, fname),
                        os.path.join(p, fname), 'DATA'))
    return ret

block_cipher = None


path = os.path.dirname(pyopenms.__file__)

def pyopenms_libs(path):
  ret = []
  for f in os.listdir(path):
      if f.endswith(".so") and not f.startswith("pyopenms"):
        # print (os.path.join("pyopenms", f), os.path.join(path, f),"BINARY")
        ret.append( (os.path.join("pyopenms", f), 
          os.path.join(path, f),"BINARY") )
  return ret

a = Analysis([tapir_exe],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             cipher=block_cipher)
a.datas.extend(dir_files(os.path.join(os.path.dirname(guidata.__file__),
    'images'), os.path.join('guidata', 'images')))
a.datas.extend(dir_files(os.path.join(os.path.dirname(guiqwt.__file__),
    'images'), os.path.join('guiqwt', 'images')))
a.datas.extend(dir_files(os.path.join(os.path.dirname(pymzml.__file__),
    'obo'), os.path.join('pymzml', 'obo')))
a.datas.extend(dir_files(os.path.join(os.path.dirname(pyopenms.__file__),
    'share'), os.path.join('pyopenms', 'share')))
# Add all the OpenMS libraries (seems necessary for Linux)
a.datas.extend(pyopenms_libs( (os.path.dirname(pyopenms.__file__) ) ) )

pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='TAPIR',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon=tapir_icon)
app = BUNDLE(exe,
             name='TAPIR.app',
             icon=tapir_icon,
             bundle_identifier='ch.ethz.imsb.tapir',
             version='1.0',)

