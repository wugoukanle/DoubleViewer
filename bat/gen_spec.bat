rem ### 生成spec文件 ###

rem # 1.关闭控制台，启动debug #
rem pyi-makespec --noconsole --onedir --debug --name DCheck main.py
rem # 2.关闭控制台，关闭debug #
rem pyi-makespec --noconsole --onedir --name DCheck main.py
rem # 3.打开控制台，关闭debug #
rem pyi-makespec --onedir  --name DCheck main.py

rem # 4.添加隐含导入包 #
rem pyi-makespec --onedir --name DCheck main.py

rem # 5.添加图标，修改软件名字 #
rem pyi-makespec --noconsole --onedir --debug  --icon  "./qss/logo-C.ico" --name DCheck main.py

rem pyi-makespec --noconsole --onefile --icon "./images/logo/logo.ico" --name DoubleViewer main.py
rem pyi-makespec --noconsole --onedir --icon "./qss/logo-C.ico" --name DCheck main.py

rem ### 使用spec文件发布 ###
pyinstaller --clean --noconfirm main.spec
pyinstaller --onedir main.spec

pyinstaller --noconsole --onefile --icon "./images/logo/logo.ico" --noconfirm --uac-admin DoubleViewer.spec
pyinstaller --noconsole --onefile --icon "./images/logo/logo.ico" --noconfirm --uac-admin main.spec







