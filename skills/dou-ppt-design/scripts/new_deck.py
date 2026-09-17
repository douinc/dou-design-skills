"""새 발표자료 작업 폴더 만들기: python3 new_deck.py <폴더>
<폴더>/build/ 에 엔진·테마·템플릿을 복사하고 필요한 도구를 설치한다."""
import os, shutil, subprocess, sys

if len(sys.argv) < 2:
    sys.exit("사용법: python3 new_deck.py <폴더>")
KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit")
dst = os.path.join(os.path.abspath(sys.argv[1]), "build")
if os.path.exists(os.path.join(dst, "deck.py")):
    sys.exit(f"이미 있음: {dst} — 기존 deck.py 를 고쳐서 쓴다")
shutil.copytree(KIT, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules", "preview", "__pycache__"))

missing = []
for mod in ("pptx", "lxml"):
    try:
        __import__(mod)
    except ImportError:
        missing.append("python-pptx" if mod == "pptx" else mod)
if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", "--user", *missing], check=False)
if shutil.which("npm"):
    subprocess.run(["npm", "install", "--silent"], cwd=dst, check=False)
else:
    print("[주의] node/npm 이 없어 아이콘·미리보기 이미지를 만들 수 없다 → brew install node")
print(f"준비 완료: {dst}")
