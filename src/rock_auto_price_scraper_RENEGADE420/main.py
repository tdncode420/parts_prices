from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException as WDE


class PartSearcher:
    def createDriver(self):
        options = Options()
        options.headless = True
        return webdriver.Firefox(options=options)
    
class RockAutoPartSearcher(PartSearcher):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.rockauto.com/'
        self.driver = None
        self.input_ele = None
        self.search_btn = None
    def _setup(self, url):
        self.driver = super().createDriver()
        self.driver.get(url)
    def _submitSearch(self, input_value):
        self.input_ele = self.driver.find_element(By.ID, 'topsearchinput[input]')
        self.search_btn = self.driver.find_element(By.ID, 'btntabsearch')
        self.input_ele.send_keys(str(input_value))
        self.search_btn.submit()
        return
    def _searchResults(self, method):
        if method == 'by_part_no':
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "listing-inner")))
                opts = self.driver.find_elements(By.CLASS_NAME, "listing-inner")
                res = []
                for opt in opts:
                    res.append(opt.text)
                return res
            except WDE:
                return False
            
        if method == 'by_vehicle':
            pass
    def _shutdown(self):
        self.driver.close()
        
    def _resultCheck(self, res):
        if not res:
            return False
        parts = []
        for r in res:
            arr = r.split('\n')
            brand = arr[0]
            category = arr[1].replace('Category: ', '')
            price = arr[2]
            parts.append({
                "brand": brand,
                "category": category,
                "price": price,
            })
            return parts
    def searchByPartNo(self, part_no):
        '''
            Search for parts by <part_no>
            
            Parameters:
                part_no (str) - the part number to search for
            
            Returns:
                
        '''
        self._setup(self.base_url)
        self._submitSearch(str(part_no))
        results = self._resultCheck(self._searchResults('by_part_no'))
        self._shutdown()
        return results
    
    def searchByVehicle(self, veh_desc, part):
        '''
            Search for parts by <vehicle>
            
            Parameters:
                veh_desc (list) - [year, make, model] of vehicle to search part compatability for
                part (str) - the name of the part to search for
            
            Returns:
        '''
        
        year = str(veh_desc[0])
        make = str(veh_desc[1]).lower()
        model = str(veh_desc[2]).lower()
        url_ext = 'en/catalog/{},{},{},'.format(make, year, model)
        url = self.base_url + url_ext
        self._setup(url)
        self.driver.execute_script('window.cataloglite.LinkIntercept_ToggleNavNode("309");')
        # make_dropdowns = self.driver.find_elements(By.CLASS_NAME, 'ranavnode')
        # for md in make_dropdowns:
        #     if str(md.text).upper() == make.upper():
        #         node_no = str(md.get_dom_attribute('id'))
        #         self.driver.execute_script('window.cataloglite.LinkIntercept_ToggleNavNode("{}")'.format(node_no))
        #         break
        # self._shutdown()
            
        
# RockAutoPartSearcher().searchByVehicle([2005, 'Acura', 'MDX'], '')
