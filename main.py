#Copyright ©github.com/imjianglee1




import cv2
import numpy as np
import pyautogui
import time
import sys
import os

def find_image_on_screen(template_path, threshold=0.8):
    """在屏幕中查找模板图像，返回中心坐标和匹配度"""
    # 截屏
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 读取模板
    template = cv2.imread(template_path, 0)
    if template is None:
        print(f"错误：无法加载模板图像 {template_path}")
        return None

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w = template.shape
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y, max_val)
    return None

def sequential_loop(red_packet_path, open_button_path, back_button_path, threshold=0.8, interval=1.0, post_click_delay=0.5, open_button_timeout=1.0):
    """
    顺序查找红包、打开按钮和返回按钮，循环执行
    :param red_packet_path: 红包图标路径
    :param open_button_path: 打开按钮图标路径
    :param back_button_path: 返回按钮图标路径
    :param threshold: 匹配阈值
    :param interval: 检测间隔（秒）
    :param post_click_delay: 点击后等待时间（秒）
    :param open_button_timeout: 等待打开按钮的超时时间（秒），超时则跳过直接返回
    """
    # 检查模板文件是否存在
    for path in [red_packet_path, open_button_path, back_button_path]:
        if not os.path.exists(path):
            print(f"错误：文件不存在 {path}")
            sys.exit(1)

    print("顺序图像识别程序已启动，按 Ctrl+C 退出")
    print(f"红包模板: {red_packet_path}")
    print(f"打开按钮模板: {open_button_path}")
    print(f"返回按钮模板: {back_button_path}")
    print(f"阈值: {threshold} | 检测间隔: {interval}秒 | 点击后延迟: {post_click_delay}秒 | 打开按钮超时: {open_button_timeout}秒")

    try:
        while True:
            # 第一阶段：查找红包并点击
            print("等待红包出现...")
            while True:
                result = find_image_on_screen(red_packet_path, threshold)
                if result:
                    x, y, confidence = result
                    print(f"找到红包！坐标: ({x}, {y}), 置信度: {confidence:.2f}")
                    pyautogui.click(x, y)
                    print("已点击红包")
                    time.sleep(post_click_delay)  # 等待打开按钮出现
                    break
                time.sleep(interval)

            # 第二阶段：查找打开按钮，设置超时
            print("等待打开按钮出现...")
            start_time = time.time()
            found_open = False
            while True:
                # 检查超时
                if time.time() - start_time > open_button_timeout:
                    print(f"等待打开按钮超时 ({open_button_timeout}秒)，跳过点击打开按钮")
                    break

                result = find_image_on_screen(open_button_path, threshold)
                if result:
                    x, y, confidence = result
                    print(f"找到打开按钮！坐标: ({x}, {y}), 置信度: {confidence:.2f}")
                    pyautogui.click(x, y)
                    print("已点击打开按钮")
                    found_open = True
                    break
                time.sleep(interval)

            # 如果找到了打开按钮，等待一下让动画完成
            if found_open:
                time.sleep(post_click_delay)

            # 第三阶段：查找返回按钮并点击（准备下一轮）
            print("等待返回按钮出现...")
            while True:
                result = find_image_on_screen(back_button_path, threshold)
                if result:
                    x, y, confidence = result
                    print(f"找到返回按钮！坐标: ({x}, {y}), 置信度: {confidence:.2f}")
                    pyautogui.click(x, y)
                    print("已点击返回按钮")
                    time.sleep(post_click_delay)  # 等待返回完成
                    break
                time.sleep(interval)

            print("一轮操作完成，准备下一轮...\n")
    except KeyboardInterrupt:
        print("\n程序已手动停止")
        sys.exit(0)

if __name__ == "__main__":
    # 配置参数
    RED_PACKET_PATH = r"D:\py-pycharm\image\red_packet_icon.png"
    OPEN_BUTTON_PATH = r"D:\py-pycharm\image\open_button.png"
    BACK_BUTTON_PATH = r"D:\py-pycharm\image\back_icon.png"
    THRESHOLD = 0.8
    INTERVAL = 0.1
    POST_CLICK_DELAY = 0.1
    OPEN_BUTTON_TIMEOUT = 1.0   # 等待打开按钮的超时时间（秒）

    sequential_loop(RED_PACKET_PATH, OPEN_BUTTON_PATH, BACK_BUTTON_PATH, THRESHOLD, INTERVAL, POST_CLICK_DELAY, OPEN_BUTTON_TIMEOUT)
