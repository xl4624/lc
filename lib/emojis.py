def get_lc_emoji(self):
    return self.bot.get_emoji(1290903612351844464)

def get_dc_emoji(self):
    return self.bot.get_emoji(1290903900169310248)

def get_cpp_emoji(self):
    return self.bot.get_emoji(1291107027971608740)

def get_c_emoji(self):
    return self.bot.get_emoji(1291107714679967818)

def get_java_emoji(self):
    return self.bot.get_emoji(1291107026143019028)

def get_js_emoji(self):
    return self.bot.get_emoji(1291107024016506971)

def get_rust_emoji(self):
    return self.bot.get_emoji(1291107029368438814)

def get_ts_emoji(self):
    return self.bot.get_emoji(1291107716319805463)

def get_py_emoji(self):
    return self.bot.get_emoji(1291107031322988605)

def get_go_emoji(self):
    return self.bot.get_emoji(1291112608698732594)

def get_all_emojis(self):
    emojis = {}
    emojis["lc"] = get_lc_emoji(self)
    emojis["dc"] = get_dc_emoji(self)
    emojis["cpp"] = get_cpp_emoji(self)
    emojis["c"] = get_c_emoji(self)
    emojis["java"] = get_java_emoji(self)
    emojis["js"] = get_js_emoji(self)
    emojis["rust"] = get_rust_emoji(self)
    emojis["ts"] = get_ts_emoji(self)
    emojis["py"] = get_py_emoji(self)
    emojis["go"] = get_go_emoji(self)
    return emojis
    