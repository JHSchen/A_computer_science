from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os # 导入os模块用于检查路径

def main():
    # 自动管理驱动版本 (这会在WSL2中下载Linux版本的ChromeDriver)
    try:
        print("正在尝试安装/更新 ChromeDriver...")
        chrome_driver_path = ChromeDriverManager().install()
        service = Service(executable_path=chrome_driver_path)
        print(f"ChromeDriver 已安装/找到于: {chrome_driver_path}")
    except Exception as e:
        print(f"错误: ChromeDriver 安装/查找失败: {e}")
        print("请确保您有正常的网络连接和写入权限。")
        print("如果问题持续，您可能需要手动下载与您Windows Chrome版本匹配的Linux版ChromeDriver，")
        print("并将其可执行文件路径传递给 Service 对象，例如：service = Service(executable_path='/path/to/your/chromedriver')")
        return

    # 浏览器配置
# ...
options = Options() # 或者 webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# --- 启用以下两行 ---
options.add_argument('--headless')
options.add_argument('--disable-gpu') # 通常与 --headless 一起使用
# --------------------

options.add_argument("--window-size=1920,1080") # 这一行在无头模式下仍然有用，可以定义虚拟窗口大小

# 关键配置：指定Windows上Chrome浏览器的可执行文件路径
windows_chrome_path = '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'
options.binary_location = windows_chrome_path
# ...
    # 检查指定的Chrome路径是否存在
    if not os.path.exists(options.binary_location):
        print(f"错误: 在WSL2中未找到Chrome二进制文件: {options.binary_location}")
        print("请仔细检查以下几点：")
        print(f"1. 确认您的Windows Chrome是否确实安装在 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'")
        print(f"2. 确认您的WSL2中C盘是否正确挂载为 /mnt/c/")
        print(f"3. 路径中的空格和大小写是否正确。")
        return

    driver = None  # 初始化driver变量
    try:
        print(f"尝试使用 ChromeDriver: {service.path}")
        print(f"尝试使用 Chrome 浏览器: {options.binary_location}")
        driver = webdriver.Chrome(service=service, options=options)
        print("浏览器启动成功!")
        
        driver.get("https://www.taobao.com")
        print("页面标题:", driver.title)
        
        # 在这里编写您的抢购逻辑，例如登录、选择商品、点击购买等
        print("模拟操作：等待5秒...")
        time.sleep(5) # 等待5秒，仅为演示，实际抢购脚本需要更复杂逻辑
        
    except Exception as e:
        print(f"在浏览器操作过程中发生错误: {e}")
        if "DevToolsActivePort file doesn't exist" in str(e) or "was started ChromeDriver" in str(e) or "cannot connect to DevTools" in str(e):
            print("错误提示表明 ChromeDriver 可能无法成功启动或连接到 Chrome 浏览器进程。")
            print("可能的原因和解决方案：")
            print("1. 确保没有其他 Chrome 实例或 ChromeDriver 进程正在运行，它们可能占用了必要的端口。")
            print("2. 尝试启用上面注释掉的 '--headless' 和 '--disable-gpu' 选项，无头模式有时能避免此类问题。")
            print("3. 确保您的 Windows Chrome 版本与 WSL2 中 ChromeDriver 的版本大致兼容。")
            print("   `ChromeDriverManager` 通常会处理好版本问题，但极端情况下可能需要手动指定。")
            print("4. (备选方案) 考虑在Windows上手动启动Chrome并开启远程调试端口，然后在脚本中连接它：")
            print("   a. 在Windows的命令提示符或PowerShell中运行: ")
            print("      \"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --remote-debugging-port=9222 --user-data-dir=\"C:\\ChromeTemp\"")
            print("   b. 然后在Python脚本中修改options（注释掉 options.binary_location）:")
            print("      options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')")
            print("      (WSL2访问Windows主机的端口通常可以用 127.0.0.1)")
        elif "net::ERR_CONNECTION_REFUSED" in str(e):
             print("错误提示表明连接被拒绝。如果使用了 debuggerAddress，请确保Chrome在Windows上以指定的调试端口启动。")
        elif "'chrome not reachable'" in str(e) or "session not created" in str(e) :
            print("错误: Chrome无法访问或会话未创建。")
            print("这通常意味着Chrome浏览器未能成功启动或启动后立即崩溃了。")
            print("请再次核对 `options.binary_location` 的路径是否绝对正确，并且WSL2有权限执行它。")
            print("如果Chrome尝试以GUI模式启动（未设置--headless），可能需要X Server环境。对于脚本，强烈建议使用 --headless。")

    finally:
        if driver:
            print("正在关闭浏览器...")
            driver.quit()
            print("浏览器已关闭。")
        else:
            print("Driver 未成功初始化，无需关闭。")

if __name__ == "__main__":
    main()