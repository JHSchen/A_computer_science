from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os

# --- 定时执行函数 ---
def schedule_task(target_time_str):
    try:
        target_time = datetime.datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S')
        print(f"任务已安排在: {target_time_str}")
    except ValueError:
        print("错误: 时间格式不正确，请使用 'YYYY-MM-DD HH:MM:SS'")
        return False

    while True:
        now = datetime.datetime.now()
        if now >= target_time:
            print("到达预定时间，开始执行任务！")
            break
        else:
            remaining = target_time - now
            if remaining.total_seconds() < 60 or int(remaining.total_seconds()) % 5 == 0:
                 print(f"距离任务开始还有: {remaining}", end='\r')
            time.sleep(0.1)
    print("\n")
    return True

def main():
    print("脚本开始执行...")
    print("重要提示：请确保您已按照说明，在手动启动的Chrome浏览器实例中登录了淘宝账户！")
    print("启动Chrome的Windows PowerShell命令示例 (无 --headless，用于登录):")
    print('& "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --disable-gpu --remote-debugging-port=9222 --user-data-dir="C:\\ChromeTemp"')
    print("登录完成后，保持该Chrome窗口运行，然后脚本将连接。")
    time.sleep(5)

    chrome_driver_path = "/home/jesse_chen/.wdm/drivers/chromedriver/linux64/137.0.7151.41/chromedriver-linux64/chromedriver"
    if not os.path.exists(chrome_driver_path):
        print(f"错误: 指定的ChromeDriver路径不存在: {chrome_driver_path}")
        return
    service = Service(executable_path=chrome_driver_path)
    print(f"将使用此ChromeDriver (for Linux): {chrome_driver_path}")

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    print(f"将尝试连接到在 127.0.0.1:9222 上运行的Chrome实例。")

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("成功连接到Chrome浏览器！")
        
        cart_url = "https://cart.taobao.com/cart.htm"
        print(f"正在导航到购物车页面: {cart_url}")
        driver.get(cart_url)

        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        current_day = datetime.datetime.now().day
        # !! 修改为你需要的时间 (时, 分, 秒) !!
        #test_time = datetime.datetime.now() + datetime.timedelta(seconds=30) # 测试：30秒后
        #target_buy_time_str = test_time.strftime('%Y-%m-%d %H:%M:%S')
        target_buy_time_str = f"{current_year}-{current_month:02d}-{current_day:02d} 15:05:00" # 示例：当天 15:02:00
        print(f"抢购时间设定为: {target_buy_time_str}")
        
        if not schedule_task(target_buy_time_str):
            return

        print("正在刷新购物车页面...")
        driver.refresh()

        wait = WebDriverWait(driver, 20)

        # 3. 勾选商品 (使用“全选购物车”逻辑)
        try:
            print("正在尝试勾选“全选购物车”复选框...")
            
            # ** 使用根据您提供的HTML信息制作的、高可靠性的新选择器 **
            select_all_checkbox_selector = (By.XPATH, "//label[contains(@class, 'ant-checkbox-wrapper') and .//span[normalize-space()='全选']]//input[@class='ant-checkbox-input' and @type='checkbox']")
            
            print(f"使用选择器: {select_all_checkbox_selector}")

            checkbox_element = wait.until(EC.element_to_be_clickable(select_all_checkbox_selector))
            
            if not checkbox_element.is_selected():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'}); arguments[0].click();", checkbox_element)
                print("“全选购物车”已勾选。")
            else:
                print("“全选购物车”已被勾选。")
        except Exception as e:
            print(f"错误：勾选“全选购物车”失败: {e}")
            driver.save_screenshot("error_全选失败.png")
            print("已保存截图: error_全选失败.png")
            return

        # 4. 点击“结算”按钮
        try:
            print("正在尝试点击结算按钮...")
            checkout_button_selector = (By.XPATH, "//div[starts-with(@class, 'btn--') and normalize-space(text())='结算']")
            
            checkout_button = wait.until(EC.element_to_be_clickable(checkout_button_selector))
            driver.execute_script("arguments[0].click();", checkout_button)
            print("已点击结算按钮！")
        except Exception as e:
            print(f"错误：点击结算按钮失败: {e}")
            driver.save_screenshot("error_结算失败.png")
            print("已保存截图: error_结算失败.png")
            return

        # 5. 处理提交订单页面
        try:
            print("等待订单确认页面加载并尝试提交订单...")
            wait.until(EC.any_of(
                EC.url_contains("buy.taobao.com"),
                EC.url_contains("buy.tmall.com")
            ))
            print(f"已跳转到订单确认页面，当前URL: {driver.current_url}")

            submit_order_button_selector = (By.XPATH, "//div[starts-with(@class, 'btn--') and normalize-space(text())='提交订单']")
            
            print(f"正在查找提交订单按钮，使用选择器: {submit_order_button_selector}")
            submit_order_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(submit_order_button_selector)
            )
            print("找到提交订单按钮，尝试点击...")
            driver.execute_script("arguments[0].click();", submit_order_button)
            print("已点击“提交订单”按钮！后续请在浏览器中查看订单状态或完成支付。")
            
            time.sleep(20)

        except Exception as e:
            print(f"错误：点击“提交订单”按钮失败或页面加载超时: {e}")
            driver.save_screenshot("error_提交订单失败.png")
            print("已保存截图: error_提交订单失败.png")

        print("抢购流程已执行。")

    except Exception as e:
        print(f"在浏览器操作过程中发生主要错误: {e}")
        if driver:
            driver.save_screenshot("error_main_exception.png")
            print("已保存截图: error_main_exception.png")
    finally:
        if driver:
            print("脚本执行完毕。浏览器将保持打开状态，您可以继续操作。")
        else:
            print("Driver 未成功初始化。")
        

if __name__ == "__main__":
    main()