import re, hashlib, os, tarfile, zipfile
from urllib.request import urlopen

# 處理的資料清單
black_list_source = [
    "https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt",
    "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareAdGuardHome.txt",
    "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt",
    "https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt",
    "https://raw.githubusercontent.com/AssoEchap/stalkerware-indicators/master/generated/hosts",
    "https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hosts",
    "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh.txt"
]

# 定義輸出檔案名稱
fileFolder = "domain"
fileName = "unsafelist"

try:
    # 建立目錄
    try:
        os.mkdir(fileFolder)
    except Exception:
        pass

    # 開啟檔案準備進行寫入
    with open(f'{fileFolder}/{fileName}.txt', 'w') as f:
        for url in black_list_source:
            try:
                # 從網路開啟檔案
                web_file = urlopen(url)
                lines = web_file.read().decode('utf-8').split('\n')
                for line in lines:
                    # 忽略註解
                    if line.startswith("#") or line.startswith("!"): continue

                    # 清除開頭字元
                    line = line.replace("|", "").replace("^", "").replace(
                        "0.0.0.0 ", "")

                    # 忽略僅有 IP 的資訊
                    pattern = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",
                                         re.MULTILINE | re.UNICODE)
                    if re.match(pattern, line) != None:
                        continue

                    # 忽略不符合網址規範的資訊
                    pattern = re.compile("\.?([0-9a-z-_]+\.?)",
                                         re.MULTILINE | re.UNICODE)
                    if re.match(pattern, line) == None:
                        continue

                    # 判斷清除完後的資料是否為空行
                    if len(line) < 1: continue

                    # 進行檔案寫入
                    print(line, file=f)

                # 關閉網路來源檔案
                web_file.close()
            except Exception:
                print(f"issue: {url}")

    # 產出 md5 資料檔
    m = hashlib.md5()
    with open(f'{fileFolder}/{fileName}.txt', "rb") as f:
        # 分批讀取檔案內容，計算 MD5 雜湊值
        for chunk in iter(lambda: f.read(4096), b""):
            m.update(chunk)
    with open(f'{fileFolder}/{fileName}.md5', 'w') as f:
        print(m.hexdigest(), file=f, end='')

    # 產出 zip 壓縮檔
    with zipfile.ZipFile(f'{fileFolder}/{fileName}.zip',
                         mode='w',
                         compression=zipfile.ZIP_DEFLATED) as f:
        f.write(f'{fileFolder}/{fileName}.txt', arcname=f'{fileName}.txt')

    # 產出 tar.gz 壓縮檔
    with tarfile.open(f'{fileFolder}/{fileName}.tar.gz', 'w:gz') as f:
        f.add(f'{fileFolder}/{fileName}.txt', arcname=f'{fileName}.txt')

    # # 產出 tar.xz 壓縮檔
    with tarfile.open(f'{fileFolder}/{fileName}.tar.xz', 'w:xz') as f:
        f.add(f'{fileFolder}/{fileName}.txt', arcname=f'{fileName}.txt')

    # # 產出 tar.zb2 壓縮檔
    with tarfile.open(f'{fileFolder}/{fileName}.tar.bz2', 'w:bz2') as f:
        f.add(f'{fileFolder}/{fileName}.txt', arcname=f'{fileName}.txt')
except Exception as ex:
    print(f"issue: {ex}")
