from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options # 确保使用 Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def main(): # 或者您原来的函数名
    print("脚本开始执行...")

    # --- ChromeDriver 设置 ---
    # 指定与您Windows Chrome版本匹配的ChromeDriver版本
    target_chrome_version = "137.0.7151.41" # 您Windows上Chrome的完整版本号
    # 或者只指定主版本号，让ChromeDriverManager查找最新的137.x驱动
    # target_chrome_version_major = "137"

    try:
        print(f"正在尝试为Chrome版本 {target_chrome_version} 安装/更新 ChromeDriver (for Linux in WSL2)...")
        # 使用 driver_version 参数指定版本
        chrome_driver_path = ChromeDriverManager(driver_version=target_chrome_version).install()
        # 如果上面的完整版本号找不到，可以尝试只用主版本号：
        # chrome_driver_path = ChromeDriverManager(version=target_chrome_version_major).install()
        
        service = Service(executable_path=chrome_driver_path)
        print(f"ChromeDriver (for Linux) 版本 {target_chrome_version} 已安装/找到于: {chrome_driver_path}")
    except Exception as e:
        print(f"错误: 为版本 {target_chrome_version} 下载 ChromeDriver 失败: {e}")
        print("可能的原因：")
        print(f"1. ChromeDriverManager无法找到版本为 {target_chrome_version} 的Linux ChromeDriver。")
        print("   您可以尝试只指定主版本号，例如 '137'，让其寻找最新的137.x系列驱动。")
        print("2. 网络问题或webdriver-manager的源暂时不可用。")
        print("如果自动下载持续失败，您需要手动下载：")
        print("   a. 访问 Chrome for Testing (CfT) JSON endpoints: https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
        print("   b. 在该JSON数据中找到与您Chrome版本137.0.7151.41最接近的版本条目。")
        print("   c. 在该版本条目下，找到 'chromedriver' 部分，复制 'linux64' 平台的下载URL。")
        print("   d. 在WSL2中下载并解压该zip文件，例如：")
        print("      wget <复制的URL>")
        print("      unzip chromedriver-linux64.zip")
        print("   e. 将解压后的 'chromedriver' 文件移动到您希望存放的位置，并赋予执行权限：")
        print("      mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver_v137")
        print("      chmod +x /usr/local/bin/chromedriver_v137")
        print("   f. 然后在脚本中直接指定路径：")
        print("      # chrome_driver_path = ChromeDriverManager(...).install()")
        print("      # service = Service(executable_path='/usr/local/bin/chromedriver_v137')")
        return

    # --- Chrome 浏览器选项配置 ---
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    # 强烈建议为WSL2->Windows的自动化启用无头模式
    options.add_argument('--headless')
    print("已启用 --headless 和 --disable-gpu 选项。")

    windows_chrome_path = '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'
    if not os.path.exists(windows_chrome_path):
        print(f"错误: 在WSL2中未找到指定的Windows Chrome浏览器路径: {windows_chrome_path}")
        return
    options.binary_location = windows_chrome_path
    print(f"将使用此Windows Chrome浏览器: {options.binary_location}")

    # --- 启动浏览器 ---
    driver = None
    try:
        print(f"尝试使用 ChromeDriver: {service.path}")
        print(f"尝试使用 Chrome 浏览器: {options.binary_location}")
        driver = webdriver.Chrome(service=service, options=options)
        print("Chrome浏览器启动成功！")
        
        print("正在打开淘宝首页...")
        driver.get("https://www.taobao.com")
        print(f"页面标题: {driver.title}")
        
        print("模拟操作：等待5秒...")
        time.sleep(5)
        
        print("操作完成。")

    except Exception as e:
        print(f"在浏览器操作过程中发生错误: {e}")
        # ... (保留之前的错误处理逻辑) ...
    finally:
        if driver:
            print("正在关闭Chrome浏览器...")
            driver.quit()
            print("Chrome浏览器已关闭。")
        else:
            print("Driver 未成功初始化，无需关闭。")
        print("脚本执行完毕。")

if __name__ == "__main__":
    main()