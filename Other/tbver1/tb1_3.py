from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

def main(): # 或者您原来的函数名
    print("脚本开始执行...")

    # --- ChromeDriver 设置 ---
    # 您已经成功下载了正确的ChromeDriver，直接使用其路径
    # 这是从您之前的日志中获取的路径：
    chrome_driver_path = "/home/jesse_chen/.wdm/drivers/chromedriver/linux64/137.0.7151.41/chromedriver-linux64/chromedriver"
    
    if not os.path.exists(chrome_driver_path):
        print(f"错误: 指定的ChromeDriver路径不存在: {chrome_driver_path}")
        print("请确保此路径正确，或者重新运行之前的ChromeDriverManager逻辑来下载。")
        return
        
    service = Service(executable_path=chrome_driver_path)
    print(f"将使用此ChromeDriver (for Linux): {chrome_driver_path}")

    # --- Chrome 浏览器选项配置 ---
    options = Options()
    # 当连接到已运行的浏览器时，以下选项在Selenium端可能不是必需的，
    # 因为浏览器已在Windows端以特定参数启动。但保留它们通常无害。
    options.add_argument('--no-sandbox') # 对于Linux上的ChromeDriver本身可能仍有意义
    # options.add_argument('--headless') # 浏览器已在Windows端以headless启动
    # options.add_argument('--disable-gpu') # 浏览器已在Windows端以disable-gpu启动
    
    # **关键修改：连接到远程调试地址**
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") # WSL2访问Windows主机的端口通常用127.0.0.1
    
    # **重要：当使用 debuggerAddress 时，不要设置 binary_location**
    # options.binary_location = '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe' # 注释掉或删除此行
    
    print(f"将尝试连接到在 127.0.0.1:9222 上运行的Chrome实例。")

    # --- 启动浏览器 (实际上是连接到已运行的浏览器) ---
    driver = None
    try:
        # 注意：service参数仍然是好的，确保Selenium使用正确的ChromeDriver与远程浏览器通信
        driver = webdriver.Chrome(service=service, options=options)
        print("成功连接到Chrome浏览器！")
        
        print("正在打开淘宝首页...")
        driver.get("https://www.taobao.com")
        print(f"页面标题: {driver.title}")
        
        print("模拟操作：等待5秒...")
        time.sleep(5)
        
        print("操作完成。")

    except Exception as e:
        print(f"在浏览器操作过程中发生错误: {e}")
        if "net::ERR_CONNECTION_REFUSED" in str(e):
            print("连接被拒绝！请确保您已在Windows上使用 --remote-debugging-port=9222 启动了Chrome，")
            print("并且Windows防火墙没有阻止来自WSL2的本地连接。")
        elif "DevToolsActivePort file doesn't exist" in str(e) or "session not created" in str(e):
             print("错误仍然是DevToolsActivePort或session not created。")
             print("请确认：")
             print("1. Windows上启动Chrome的命令完全正确，并且Chrome仍在后台运行。")
             print("2. WSL2中使用的ChromeDriver版本 (`137.0.7151.41`) 与Windows上运行的Chrome版本完全兼容。")
             print("3. 尝试在Windows上启动Chrome时不加 `--headless`，看看是否有任何错误信息弹出（虽然这样就不是无头了）。")
        # ... (其他错误处理) ...
    finally:
        if driver:
            print("正在关闭与Chrome浏览器的连接 (浏览器本身在Windows上可能仍在运行)...")
            # driver.quit() 在连接到远程调试实例时，行为可能不同。
            # 它可能会尝试关闭浏览器，也可能只是断开会话。
            # 如果您希望手动启动的Chrome在脚本结束后继续运行，可以考虑不调用quit，或者只调用driver.close()关闭标签页。
            # 为了简单起见，我们先保留 driver.quit()
            driver.quit()
            print("与Chrome浏览器的会话已关闭。")
        else:
            print("Driver 未成功初始化，无需关闭。")
        print("脚本执行完毕。")

if __name__ == "__main__":
    main()