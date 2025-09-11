from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os

# --- 定时执行函数 (保持不变) ---
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
    print("重要提示：请确保您已在手动启动的Chrome浏览器实例中登录了淘宝账户！")
    time.sleep(3)

    # --- ChromeDriver和浏览器选项配置 (保持不变) ---
    chrome_driver_path = "/home/jesse_chen/.wdm/drivers/chromedriver/linux64/137.0.7151.41/chromedriver-linux64/chromedriver"
    if not os.path.exists(chrome_driver_path):
        print(f"错误: 指定的ChromeDriver路径不存在: {chrome_driver_path}")
        return
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = None
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("成功连接到Chrome浏览器！")
        
        cart_url = "https://cart.taobao.com/cart.htm"
        print(f"正在导航到购物车页面: {cart_url}")
        driver.get(cart_url)

        # --- 定时器设置 ---
        test_time = datetime.datetime.now() + datetime.timedelta(seconds=20) # 测试：20秒后
        target_buy_time_str = test_time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"抢购时间设定为: {target_buy_time_str}")
        if not schedule_task(target_buy_time_str):
            return
        
        print("正在刷新购物车页面...")
        driver.refresh()

        wait = WebDriverWait(driver, 30)

        # 3. 勾选商品 (使用从日志中发现的ID)
        try:
            # ** 使用从录制日志中发现的 ID 'cart-operation-fixed' 构建新选择器 **
            # 这个选择器现在非常精确和稳定
            select_all_checkbox_selector = (By.XPATH, "//div[@id='cart-operation-fixed']//input[@type='checkbox']")
            print(f"使用高可靠性选择器查找'全选'复选框: {select_all_checkbox_selector}")

            checkbox_element = wait.until(EC.element_to_be_clickable(select_all_checkbox_selector))
            
            if not checkbox_element.is_selected():
                # 使用JS点击，以防万一
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'}); arguments[0].click();", checkbox_element)
                print("“全选购物车”已勾选。")
            else:
                print("“全选购物车”已被勾选。")
        except Exception as e:
            print(f"错误：勾选“全选购物车”失败: {e}")
            driver.save_screenshot("error_全选失败.png")
            print("已保存截图: error_全选失败.png")
            return

        # 4. 点击“结算”按钮 (使用从日志中发现的ID)
        try:
            # ** 使用从录制日志中发现的 ID 'settlementContainer_1' 构建新选择器 **
            checkout_button_selector = (By.XPATH, "//div[@id='settlementContainer_1']//div[normalize-space(text())='结算']")
            print(f"使用高可靠性选择器查找'结算'按钮: {checkout_button_selector}")
            
            checkout_button = wait.until(EC.element_to_be_clickable(checkout_button_selector))
            driver.execute_script("arguments[0].click();", checkout_button)
            print("已点击结算按钮！")
        except Exception as e:
            print(f"错误：点击结算按钮失败: {e}")
            driver.save_screenshot("error_结算失败.png")
            return

        # 5. 处理提交订单页面 (使用从日志中发现的ID)
        try:
            print("等待订单确认页面加载并尝试提交订单...")
            wait.until(EC.any_of(EC.url_contains("buy.taobao.com"), EC.url_contains("buy.tmall.com")))
            print(f"已跳转到订单确认页面，当前URL: {driver.current_url}")

            # ** 使用从录制日志中发现的 ID 'submitOrder' 构建新选择器 **
            submit_order_button_selector = (By.XPATH, "//div[@id='submitOrder']//div[normalize-space(text())='提交订单']")
            print(f"使用高可靠性选择器查找'提交订单'按钮: {submit_order_button_selector}")

            submit_order_button = wait.until(EC.element_to_be_clickable(submit_order_button_selector))
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
    finally:
        if driver:
            print("脚本执行完毕。浏览器将保持打开状态，您可以继续操作。")
        else:
            print("Driver 未成功初始化。")

if __name__ == "__main__":
    main()