class UsernameConverter:
    """
    定义用户名路由转换器
    """
    # 定义用户名的正则表达式
    regex = '[a-zA-Z0-9_-]{5,20}'
    
    def to_python(self, value):
        """
        将匹配结果传递到视图内部使用
        :param value: 
        :return: 
        """
        return str(value)
     
    def to_url(self, value):
        """
        将匹配结果用于反向解析传值时使用
        :param value: 
        :return: 
        """
        return str(value)
    

class MobileConverter:
    """
    定义手机号码路由转换器
    """
    # 定义手机号的正则表达式
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        """
        将匹配结果传递给视图函数使用
        :param value: 
        :return: 
        """
        return str(value)

    def to_url(self, value):
        """
        将匹配结果用于反向解析传值时使用
        :param value: 
        :return: 
        """
        return str(value)
