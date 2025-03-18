# Transcription_app

Pour la génération du ".exe", utilise le script "trans_interface.py". 
Il te faudra créer un fichier .env dans lequel tu copies "<<ASSEMBLY_AI = xxxxxxxxxxxxxxxxxxxxxxxxx>>". Il s'agit de la clé API pour le transcripteur utilisé : asembly.ai.

Vérifie que la transcription fonctionne avant de lancer le fichier ".exe"

1_ Copie un lien Youtube
2_ Lance le script trans_interface.py (python3 trans_interface.py _____ sous linux)
3_Colle le lien youtube 
4_ Tu devrais avoir un fichier txt dans ton dossier de projet (le chemin te sera affiché quand meme)

Quand le script marche, tu peux lancer la mise en place du fichie ".exe"


############# Création du fichier .exe #############

Quand tu lanceras pyinstaller, je suppose que tu auras également un fichier ".spec" créé. 


1. Générez un fichier `.spec` en utilisant PyInstaller :
   
   pyinstaller --onefile --add-data "path/to/your/.env; .env" --hidden-import "yt_dlp" --trans_interface.py
   ("pour le path/to/your/" tu peux utiliser "os.path.dirname(__file__)" ou le chemin absolu "C:\\path\\to\\your\\script']" : ce qui marche)

   Cela créera un fichier `.spec` dans le même répertoire du script.

2. Modifiez le fichier `.spec` pour inclure toutes les options nécessaires. 
Par exemple :
   
   # your_script.spec
   (contenu du fichier .scrip)
   # -*- mode: python ; coding: utf-8 -*-

   block_cipher = None

   a = Analysis(
       ['your_script.py'],
       pathex=[os.path.dirname(__file(nom du script)__)],
       binaries=[],
       datas=[('path/to/your/.env', '.env')],
       hiddenimports=['yt_dlp (important, c'est une dépendance qui permet les télkéchargements)'],
       hookspath=[],
       runtime_hooks=[],
       excludes=[],
       win_no_prefer_redirects=False,
       win_private_assemblies=False,
       cipher=block_cipher,
   )
   pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
   exe = EXE(
       pyz,
       a.scripts,
       [],
       exclude_binaries=True,
       name='your_script',
       debug=False,
       bootloader_ignore_signals=False,
       strip=False,
       upx=True,
       upx_exclude=[],
       runtime_tmpdir=None,
       console=True,
   )
   coll = COLLECT(
       exe,
       a.binaries,
       a.zipfiles,
       a.datas,
       strip=False,
       upx=True,
       upx_exclude=[],
       name='your_script',
   )
   ```

3. Exécutez PyInstaller avec le fichier `.spec` :
   
   pyinstaller your_script.spec
  

#### Bon c'est un peu mon apport et vérifie aussi que ca marche.

Veuille bien zipper pour me l'envoyer


Merci pour ton big aide
