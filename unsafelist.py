import re
from urllib.request import urlopen

black_list_source = [
  "https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt",
  "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareAdGuardHome.txt",
  "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt",
  "https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt",
  "https://raw.githubusercontent.com/AssoEchap/stalkerware-indicators/master/generated/hosts",
  "https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hosts",
  "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh.txt"
]

try:
  with open("unsafelist.txt", 'w') as f:
    for url in black_list_source:
      try:
        web_file = urlopen(url)
        lines = web_file.read().decode('utf-8').split('\n')
        for line in lines:
          if line.startswith("#") or line.startswith("!"): continue
          # 清除開頭字元
          line = line.replace("|", "").replace("^", "").replace("0.0.0.0 ", "")
          # 忽略僅有 IP 的資訊
          pattern = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",
                               re.MULTILINE | re.UNICODE)
          if re.match(pattern, line) != None:
            continue
          # 忽略不符合網址規範的資訊
          pattern = re.compile("\.?([0-9a-z-_]+\.?)", re.MULTILINE | re.UNICODE)
          if re.match(pattern, line) == None:
            continue
          # 判斷清除完後的資料是否為空行
          if len(line) < 1: continue
          print(line, file=f)

        web_file.close()
      except Exception as ex:
        print(f"error: {url}")
except Exception as ex:
  print(f"write file issue: {ex}")
