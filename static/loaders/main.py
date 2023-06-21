


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import os
binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# Configure Firefox options
options = webdriver.FirefoxOptions()
options.binary_location = binary_path

# Create a new instance of the Firefox driver
driver = webdriver.Firefox(options=options)
# Open Scrapingbee's website
driver.get("https://www.cssportal.com/css-loader-generator/")
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

directory = "loaders"
# Check whether the specified path exists or not
isExist = os.path.exists(directory)
if not isExist:


   os.makedirs(directory)

   print("The new directory is created!")
array_loaders = ["spinners","dots","bars","dotsbars","infinity","continuous","progress","shapes","hypnotic","ninja","flipping","line","cut","arrow"]
array_loaders_regex = ["s","d","b","db","i","c","p","sh","h","n","f","l","cu","a"]

for index_loader,loads in enumerate(array_loaders):
    index_loader=index_loader+1
    path = directory+"/" +array_loaders[index_loader-1]
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    button = driver.find_element(By.XPATH,f"/html/body/main/div/div/div/div[1]/div[2]/div[1]/div[1]/select/option[{index_loader}]").click();
    spinner = driver.find_element(By.ID, array_loaders[index_loader-1])
    SPINNERS = spinner.find_elements(By.CLASS_NAME, 'loader')

    text_start = f'<div class="card shadow-none border border-300 my-4" data-component-card="data-component-card"><div class="card-header p-4 border-bottom border-300 bg-soft"><div class="row g-3 justify-content-between align-items-center"><div class="col-12 col-md"><h4 class="text-900 mb-0" data-anchor="data-anchor">{array_loaders[index_loader-1].upper()}</h4></div><div class="col col-md-auto"><nav class="nav nav-underline justify-content-end doc-tab-nav align-items-center" role="tablist"><button class="btn btn-link px-2 text-900 copy-code-btn" type="button"><span class="fas fa-copy me-1"></span>Copy Code</button><a class="btn btn-sm btn-cmsAti-primary code-btn ms-2" data-bs-toggle="collapse"href="#{array_loaders[index_loader-1]}-code" role="button" aria-controls="{array_loaders[index_loader-1]}-code"aria-expanded="false"><span class="me-2" data-feather="code"></span>Viewcode</a><a class="btn btn-sm btn-cmsAti-primary preview-btn ms-2"><span class="me-2"data-feather="eye"></span>Preview</a></nav></div></div></div><div class="card-body p-0"><div class="collapse code-collapse" id="growing-colors-code"><pre class="scrollbar" style="max-height: 420px"><code class="language-html"></code></pre></div><div class="p-4 code-to-copy"><div class="row">'
    with open(f'{path}/{array_loaders[index_loader - 1]}.css', 'w') as c:

        with open(f'{path}/{array_loaders[index_loader - 1]}.html', 'w') as f:
            f.write(BeautifulSoup(text_start, features="html.parser").prettify())
            for index,element in enumerate(SPINNERS):
                index = index+1
                print(index)

                time.sleep(1)
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable(element))
                element.click()
                text_div_element = f'<div class="col-6 col-md-1 mx-auto p-2"><div class="custom-loader-{array_loaders[index_loader - 1]}{index}"></div> </div>'

                f.write(BeautifulSoup(text_div_element,features="html.parser").prettify())

                loader_elements = driver.find_element(By.CLASS_NAME, 'language-css')
                text_code_element = loader_elements.get_attribute('textContent')

                text_code_element = re.sub(f'{array_loaders_regex[index_loader - 1]}(\d)+',f' {array_loaders[index_loader - 1]}{index} ',text_code_element)
                text_code_element = text_code_element.replace("custom-loader", f"custom-loader-{array_loaders[index_loader - 1]}{index}")


                c.write(BeautifulSoup(text_code_element,features="html.parser").prettify())
            text_end = f'</div></div></div></div>'
            f.write(BeautifulSoup(text_end, features="html.parser").prettify())
            text_li = f'<li class ="nav-item" ><a class ="nav-link" href="#{array_loaders[index_loader - 1]}"> {array_loaders[index_loader - 1].upper()} </a ></li>'
            f.write(BeautifulSoup(text_li, features="html.parser").prettify())

    c.close()
