# -*- mode: python -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='00099988878')


a = Analysis(['server.py'],
             pathex=['D:\\mdf\\OneDrive\\MDF\\python_lab\\pysocket_ssl'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='server',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
