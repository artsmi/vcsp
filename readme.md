# VCS_P. Создание и управление ветками

**VCS_P** - программа Promobot (VCS Promobot) основанная на VCS. Позволяет эффективно работать с модулями (сабмодулями) объединенными в рамках одного проекта (направления):
- базируется в главном репозитории (на одном уровне с данным файлом);
- основан на [VCS](https://github.com/dirk-thomas/vcstool);
- для запуска применить команду chmod 755 ./vcs_p.py;
- для запуска необходим **python 3.x**;
- программа создает **vcs_p.json** файл:
  - *repos* - все репозитории подключенные в VCS;
  - *editor* - редактор для редактирования файла **vcs_p.json**;
  - *editor_commit* - редактор для редактирования commit (git) - по умолчанию **nano**;
  - *autor* - ваше имя или никнейм разработчика. Добавляется в конец каждого коммита;
  - *profile* - активный профиль (ветка / задача), над которыми ведется работа;
  - *profiles* - все профили в структуре <имя>:<содержание>, каждый содержит следующую информацию:
    - *branch_name* - текущее имя ветки, применимое **ко всем** командам если профиль активный;
    - *repos* - список реопзиториев (модулей) данного профиля;
- актуальные команды и описание можно посмотреть командой **--help**, далее перечислены некоторые особенности **VCS_P**:
  - **--checkoutb <branch_name>** - изменяет **branch_name** текущего профиля;
  - **--sync** - синхронизирует **branch_name** текущего профиля с реальным значением, данная команда автоматически срабатывает при любом старте **VCS_P**;
  - **--profile  <profile_name>** - создает новый профиль c именем **profile_name**, при этом список модулей задается по умолчанию. Для редактирования списка можно использовать команду **--edit**;
  - **--edit** - открывает **vcs_p.json** файл с помощью редактора, указанного в **editor** на первом уровне вложенности;
- вы можете использовать несколько команд в одной строчке:
  ```bash
  ./vcs_p.py --clear --init --docker
  ```

### Примеры workflow:
1) инициализировать репозиторий;
```bash
./vcs_p.py --clear --init
```
2) в открывшемся редакторе измените **"repos"** в **deafult** профиле на те, в которых необходимо произвести изменения (сохраните файл);
3) проверьте данной командой операции 1 и 2;
```bash
./vcs_p.py --status
```
4) создайте для всех репозиториев одну ветку;
```bash
./vcs_p.py --checkoutb my_branch_name_for_pm
```
5) создайте изменения в коде и прочих файлах;
6) добавьте изменения (**! все модули (репозитории) должны быть корректно настроены .gitignore файлом !**) - это аналог **git add .** ;
```bash
./vcs_p.py --add
```
7) для частного добавления изменений используете данные команды - открывается **gnome-terminal** c pwd на корень ФС модуля (**<repo_name>** - имя репозитория из списка модулей профиля);
```bash
./vcs_p.py --orep <repo_name>
```
или
```bash
./vcs_p.py --oallrep
```
8) команда **--oallrep** открывает **gnome-terminal** на **ВСЕ** модули (аналогия с пунктом 7);
9) используете **--commit** для написания комита. При этом поля *autor* и **<branch_name>** будут добавлены в коммит сообщение. Программа по умолчанию откроет **nano** редактор для создания коммит сообщения. **Atom** и **nano** редакторы протестированы и работают;
```bash
./vcs_p.py --commit
```
10) отправьте свои изменения в удаленные репозитории;
```bash
./vcs_p.py --push
```
