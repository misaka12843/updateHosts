# updateHosts

## 简介

`updateHosts` 是一款自动从网络下载并更新 `hosts` 文件的工具。用户可以自定义 `hosts` 源，便捷地进行管理和更新。

本项目基于 [ladder1984/updateHosts](https://github.com/ladder1984/updateHosts) 进行二次修改，已将原有的 `updateHosts.py` 脚本适配至 Python 3。

## 使用说明

1. **安装 Python 3**

   请确保你的计算机上已安装 [Python 3](https://www.python.org/)，并设置好环境变量。

2. **下载并解压项目**

   [点击这里下载项目](https://github.com/misaka12843/updateHosts/archive/refs/heads/master.zip)，将压缩包解压至本地。

3. **运行程序**

   进入解压后的目录，右键点击 `Run.bat` 文件，选择“以管理员身份运行”即可自动更新 `hosts` 文件。

4. **自定义配置**

   - `config.ini` 文件中包含了 `hosts` 文件源的地址。你可以根据需要修改其中的 URL 地址。
   - 本项目默认使用 [GitHub520](https://github.com/521xueweihan/hosts) 作为 `hosts` 源。

## 运行环境

- **操作系统**：Windows、Linux、Mac OS
- **编程语言**：Python 3.6 及以上版本

## 注意事项

- 请确保以管理员权限运行 `Run.bat`，否则无法修改 `hosts` 文件。
- 如需修改 `hosts` 文件的下载源，编辑 `config.ini` 文件中的 `source_select` 部分。

## 开源许可

本项目基于 [MIT License](https://opensource.org/licenses/MIT) 开源许可协议发布，欢迎自由使用、修改和分发。
