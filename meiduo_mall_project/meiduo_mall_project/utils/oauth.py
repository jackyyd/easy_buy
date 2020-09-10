# 导包
from QQLoginTool.QQtool import OAuthQQ
# QQ登录参数
# QQ互联的appid
QQ_CLIENT_ID = '101474184'
# QQ互联的appkey
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# QQ互联的回调地址
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
# 实例化OAuthQQ类的对象
oauth = OAuthQQ(
    client_id=QQ_CLIENT_ID,
    client_secret=QQ_CLIENT_SECRET,
    redirect_uri=QQ_REDIRECT_URI,
    state=next
)