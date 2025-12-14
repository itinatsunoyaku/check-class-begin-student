import tkinter as tk
from tkinter import messagebox

from ccbTeacherSDK import check_in, CResult
from main import password_input, info


def get_input(text_widget: tk.Entry):
    """从文本框获取输入内容"""
    return text_widget.get().strip()


def checkin_btn_callback():
    """按钮点击回调函数"""
    sent = get_input(password_input)
    if not sent:
        messagebox.showwarning("警告", "请输入签到秘钥！")
        return 0
    send_check_in(sent)


def send_check_in(sent):
    def async_check_in():
        info["pass"] = sent
        result = check_in(info)
        checkin_feedback(result, True)


def checkin_feedback(result: CResult):
    # 处理错误和响应
    """处理签到响应"""
    if CResult:
        if result == CResult.SUCCESS:
            messagebox.showinfo("成功", f"签到成功！")
        elif result == CResult.P_WRONG:
            messagebox.showerror("失败", "签到失败：秘钥错误")
        elif result == CResult.ALREADY:
            messagebox.showwarning("提示", "已经签到过了")
        else:
            messagebox.showerror("失败", f"签到失败！")
    else:
        messagebox.showerror("系统错误！")
