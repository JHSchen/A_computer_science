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

        # --- 定时器设置 (保持不变) ---
        test_time = datetime.datetime.now() + datetime.timedelta(seconds=20)
        target_buy_time_str = test_time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"抢购时间设定为: {target_buy_time_str}")
        if not schedule_task(target_buy_time_str):
            return
        
        print("正在刷新购物车页面...")
        driver.refresh()

        # 延长等待时间，给JavaScript渲染留出足够时间
        wait = WebDriverWait(driver, 30)

        # 3. 勾选商品 (使用新的、更稳健的等待策略)
        try:
            # ** 步骤1: 等待关键UI元素（整个'全选'标签）出现，确认JS已渲染 **
            print("正在等待购物车UI渲染完成...")
            select_all_label_selector = (By.XPATH, "//label[contains(@class, 'ant-checkbox-wrapper') and .//span[normalize-space()='全选']]")
            print(f"使用选择器等待UI标志: {select_all_label_selector}")
            
            # 使用 presence_of_element_located，只检查元素是否存在于DOM中
            wait.until(EC.presence_of_element_located(select_all_label_selector))
            print("购物车UI渲染完成（已找到'全选'标签）。")

            # ** 步骤2: 现在我们知道元素已存在，再等待它变为可点击状态并操作 **
            print("正在尝试勾选“全选购物车”复选框...")
            input_selector = (By.XPATH, "//label[contains(@class, 'ant-checkbox-wrapper') and .//span[normalize-space()='全选']]//input[@class='ant-checkbox-input' and @type='checkbox']")
            checkbox_element = wait.until(EC.element_to_be_clickable(input_selector))
            
            if not checkbox_element.is_selected():
                # 使用JS点击，对于React等框架构建的复杂UI，这通常更可靠
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'}); arguments[0].click();", checkbox_element)
                print("“全选购物车”已勾选。")
            else:
                print("“全选购物车”已被勾选。")
        except Exception as e:
            print(f"错误：勾选“全选购物车”失败: {e}")
            driver.save_screenshot("error_全选失败.png")
            print("已保存截图: error_全选失败.png")
            return

        # --- 后续“结算”和“提交订单”步骤 (保持不变) ---
        try:
            print("正在尝试点击结算按钮...")
            checkout_button_selector = (By.XPATH, "//div[starts-with(@class, 'btn--') and normalize-space(text())='结算']")
            checkout_button = wait.until(EC.element_to_be_clickable(checkout_button_selector))
            driver.execute_script("arguments[0].click();", checkout_button)
            print("已点击结算按钮！")
        except Exception as e:
            print(f"错误：点击结算按钮失败: {e}")
            driver.save_screenshot("error_结算失败.png")
            return

        try:
            print("等待订单确认页面加载并尝试提交订单...")
            wait.until(EC.any_of(EC.url_contains("buy.taobao.com"), EC.url_contains("buy.tmall.com")))
            submit_order_button_selector = (By.XPATH, "//div[starts-with(@class, 'btn--') and normalize-space(text())='提交订单']")
            submit_order_button = wait.until(EC.element_to_be_clickable(submit_order_button_selector))
            driver.execute_script("arguments[0].click();", submit_order_button)
            print("已点击“提交订单”按钮！")
            time.sleep(20)
        except Exception as e:
            print(f"错误：点击“提交订单”按钮失败或页面加载超时: {e}")
            driver.save_screenshot("error_提交订单失败.png")

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