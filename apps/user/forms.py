__author__ = 'LY'
__date__ = '2019/9/15 20:04'
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    """
    这里的两个字段必须跟前台input定义的name相同
    """
    username=forms.CharField(required=True)
    password=forms.CharField(required=True)


class RegisterForm(forms.Form):
    """
    这里对注册的表单进行验证和生成验证码，验证码的方法captcha已经写好了
    验证码会在前台生成一个hidden的input框，后台会生成一长串的字符串，然后联合查询验证码的正确与否
    """
    registerUsername=forms.CharField(required=True,min_length=2)
    registerPassword=forms.CharField(required=True,min_length=6)
    registeremail=forms.EmailField(required=True,min_length=6)               #使用forms.EmailField会对邮箱进行正则表达式的匹配，就不用开发者自己来写了
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
