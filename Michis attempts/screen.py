from selenium import webdriver


driver = webdriver.PhantomJS()
driver.set_window_size(533, 300) # optional
driver.get('https://github.com/d3/d3')
driver.save_screenshot('git_ex.png')
