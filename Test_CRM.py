import os,datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from random import *
from faker import Faker
import unittest, sys, time, pickle, os.path
from selenium.webdriver.common.action_chains import ActionChains

fake = Faker()



class CRM(unittest.TestCase):

    # --> Setup Which Runs Before Every Testcase.

    def setUp(self):
        cd = os.environ.get("DRIVERPATH", "/Users/username/Downloads/chromedriver")
        self.driver = webdriver.Chrome(cd)
        self.base_url = "http://dev.crm.com:8001"
        self.driver.set_window_size(1440, 1024)
        self.driver.maximize_window()
        if not os.path.exists("./Cookies.pkl"):
            driver = self.driver
            driver.get(self.base_url + "/login")
            driver.find_element_by_name("username").send_keys("username")
            driver.find_element_by_name("password").send_keys("pswd")
            driver.find_element_by_class_name('loginContainerSubmit').click()
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navSideContainer"]/div[1]')))
            with open("Cookies.pkl","wb") as Cookies:
                pickle.dump(driver.get_cookies(),Cookies)


    # --> Handling Cookies.

    def handle_Cookies(self):
        driver = self.driver
        with open("Cookies.pkl","rb") as Cookies:
            cookie = pickle.load(Cookies)
            for ck in  cookie:
                driver.add_cookie(ck)


    # --> Handle Create Deal Form.

    def handle_Create_Deal_Form(self):
        driver = self.driver
        # Name
        driver.find_element_by_name("Deal_Name").clear()
        Name = fake.name()
        driver.find_element_by_name("Deal_Name").send_keys(Name)
        # Assigned_To
        driver.find_element_by_name("Assigned_To").click()
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/section/div/div/div[4]/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]').click()
        # Worth
        driver.find_element_by_name("Worth").clear()
        driver.find_element_by_name("Worth").send_keys(fake.random_number(4, 3))
        # Description
        driver.find_element_by_name('Description').clear()
        driver.find_element_by_name('Description').send_keys(fake.sentence())
        driver.find_element_by_class_name('button').click()
        time.sleep(2)
        return Name



    # --> Test Case For Creation of Deal.

    def test_Create_Deal(self):
        driver = self.driver
        driver.get(self.base_url + "/pipeline")
        self.handle_Cookies()
        driver.get(self.base_url + "/pipeline")
        # Creation
        drive = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,'pipelineNavCreateDeal')))
        drive.click()
        time.sleep(1)
        # Due_Date
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[9]/section/div/div/div[3]/div[2]/div[2]/div').click()
        time.sleep(1)
        driver.find_element_by_class_name('DayPickerNavigation__next').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{}]/td[{}]/button'.format(randint(2, 4),randint(1,7))).click()
        # Assigned_To
        driver.find_element_by_name("Assigned To").click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[3]/div/div/div[2]/div/div[{}]/div[2]/div[1]'.format(randint(1,3))).click()
        # Stages
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[7]/div').click()
        time.sleep(1.5)
        stg_Select = randint(1, 2)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[7]/div/div/div[2]/div/div[{}]'.format(
                str(stg_Select))).click()
        time.sleep(1)
        # Lead
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[8]/div').click()
        time.sleep(1.5)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[8]/div/div/div[2]/div/div/div[{}]'.format(
                str(randint(2, 4)))).click()
        # Product
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[9]/div').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[9]/div/div/div[2]/div/div[{}]/div[2]/div[1]'.format(str(randint(1, 2)))).click()
        time.sleep(0.5)
        Actions = driver.find_element_by_name("Contact")
        ActionChains(driver).move_to_element(Actions).perform()
        # Contact
        driver.find_element_by_name('Contact').click()
        time.sleep(1.5)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[10]/div/div/div[2]/div/div/div[{}]/div[2]/div'.format(str(randint(2, 4)))).click()
        Actions = driver.find_element_by_name("Deal Name")
        ActionChains(driver).move_to_element(Actions).perform()
        Dname = self.handle_Create_Deal_Form()
        try:
            driver.find_element_by_xpath('//*[@id="pipelineContainer"]/div/div[2]/div/div[1]/div/div[{}]/div/div[2]/div/div[1]/div[1]'.format(str(stg_Select))).click()
            time.sleep(1.2)
            msg = driver.find_element_by_class_name('dataNameDealIndividual').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Dname.lower(),msg.lower(), "Common Buddy Check Your Code --> Deal not created")

        ### Edit_Total Deal

        driver.find_element_by_class_name('dataIndiHeadDealEdit').click()
        time.sleep(2)
        # Contact
        driver.find_element_by_name('Contact').click()
        time.sleep(1.5)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[7]/div/div/div[2]/div/div/div[{}]/div[2]/div'.format(str(randint(2, 4)))).click()
        Dname = self.handle_Create_Deal_Form()
        #time.sleep(2)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
        time.sleep(2)
        #check Name in individual page
        try:
            msg = driver.find_element_by_class_name('dataNameDealIndividual').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Dname.lower(),msg.lower(), "Common Buddy Check Your Code --> Deal Not Updated")

        ####### Edit Deal Indivdual Page #########

        # Change_Stage
        select = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div[2]/div[2]/div/div[3]')
        select.click()
        time.sleep(1)
        name = select.text
        driver.refresh()
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,'auditLogTime')))
        time.sleep(0.5)
        try:
            Stage_name = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/span[3]/span[2]').text

        except NoSuchElementException:
            Stage_name = ""
        self.assertEqual(name.lower(), Stage_name.lower(),"Common Buddy Check Your Code --> Stage Not Changed")
        time.sleep(2)

        ### Create_todo_in_deal
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[2]').click()
        driver.find_element_by_class_name('dataIndividualPageCreateButton').find_element_by_class_name('buttonBlue').click()
        time.sleep(2)
        # To Uncheck The Default Checked Deal
        #driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[5]/div/div[4]').click()
        #time.sleep(2)
        todo_name = self.handle_Todo_Form()
        # Choosing_Options
        for i in range(1, 3):
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[5]/div/div[{}]'.format(str(i))).click()

        # Move_to_element
        Actions = driver.find_element_by_class_name('appCreateButtonLabel')
        ActionChains(driver).move_to_element(Actions).perform()
        # Contacts
        driver.find_element_by_name('people').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[7]/div/div/div[2]/div/div/div[{}]/div[2]/div'.format(str(randint(2, 4)))).click()
        # Lead
        driver.find_element_by_name('lead').click()
        time.sleep(1.5)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[8]/div/div/div[2]/div/div/div[{}]/div[2]'.format(str(randint(2, 4)))).click()
        time.sleep(2)
        try:
            data = driver.find_element_by_class_name('activityInRowDayToDoData').text
        except:
            data = ""
        self.assertEqual(todo_name.lower(),data.lower(),"Common Buddy Check Your Code --> Todo Not Created In Deals")
        time.sleep(2)
        ## Edit DueDate
        driver.find_element_by_class_name('DateInput__input').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr[4]/td[{}]/button'.format(str(randint(1,6)))).click()
        time.sleep(1.5)
        # Get Due Date
        text = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div').text
        driver.refresh()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
        #try:
         #   data = driver.find_element_by_class_name('cardActionNameData').text
        #except:
        #    data = ""
        #self.assertEqual(text,data,"Common Buddy Check Your Code --> Problem In Updating Due Date")

        # Notes
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[5]').click()
        driver.find_element_by_class_name('icon-Add').click()
        Note_title = fake.safe_color_name()
        driver.find_element_by_id('title').send_keys(Note_title)
        driver.find_element_by_id('body').send_keys(fake.address())
        driver.find_element_by_class_name('save').click()
        driver.refresh()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[5]').click()
        try:
            Notes = driver.find_element_by_class_name('data').text
        except:
            Notes = ""
        self.assertEqual(Note_title.lower(),Notes.lower(),"Common Buddy Check Your Code --> Notes Not Created In Deals")
        # Delete_Notes
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/i').click()
        driver.find_element_by_class_name('buttonDiv').find_element_by_class_name('btn').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('data').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertNotEqual(Note_title.lower(), msg, "Common Buddy Check Your Code --> Notes Not Deleted In Deals")
        driver.refresh()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
        # State
        driver.find_element_by_class_name('chooser').click()
        Won_or_loss = randint(1,2)
        if Won_or_loss == 2:
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[3]/div[{}]'.format(str(Won_or_loss))).click()
            driver.find_element_by_name('name').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/section/div/div/div[3]/div[2]/div[1]/div/div/div[2]/div/div[{}]'.format(str(randint(1,4)))).click()
            reason =  driver.find_element_by_name('name').text
            time.sleep(1)
            driver.find_element_by_class_name('widgetBoxContentMBoxButton').click()
            time.sleep(1)
            driver.refresh()
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
            time.sleep(1.5)
            try:
                data = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/span[3]/span[2]').text
            except:
                data = ""
            self.assertEqual(reason.lower(), data.lower(),"Common Buddy Check Your Code --> Loss Reason Not Updated")
        else:
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[3]/div[1]').click()
            driver.refresh()
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
            time.sleep(1.5)
            try:
                data = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/span[3]/span[2]').text
            except:
                data = ""
            self.assertEqual("Won", data, "Common Buddy Check Your Code --> Won Not Updated In Deals")
        time.sleep(1)
        # Send_Email
        driver.find_element_by_class_name('email').click()
        driver.find_element_by_name('subject').send_keys(fake.street_name())
        driver.find_element_by_name('body').send_keys(fake.address())
        driver.find_element_by_class_name('appNewMessageComposeOptionsSendmail').click()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'showToast')))
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("message sent" in msg, "Common Buddy Check Your Code --> Mail Not Sent In Deals")
        time.sleep(1)
        # Assigned_To
        driver.find_element_by_class_name('Text').click()
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[{}]'.format(
                str(randint(1, 2)))).click()
        text = driver.find_element_by_class_name('info').text
        driver.refresh()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
        time.sleep(1.5)
        try:
            data = driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/span[3]/span[2]').text
        except:
            data = ""
        self.assertEqual(text, data, "Common Buddy Check Your Code --> AssignedTo Not Updated In Deals")
        driver.back()
        time.sleep(1)
        ## Delete Deal
        Del = randint(1,3)
        driver.find_element_by_xpath('//*[@id="pipelineContainer"]/div/div[2]/div/div[1]/div/div[{}]/div/div[2]/div/div[1]/div[1]/div[2]'.format(str(Del))).click()
        time.sleep(1)
        Name = driver.find_element_by_class_name('dataNameDealIndividual').text
        driver.find_element_by_class_name('delete').click()
        driver.find_element_by_class_name('btn').click()
        try:
            data = driver.find_element_by_xpath('//*[@id="pipelineContainer"]/div/div[2]/div/div[1]/div/div[{}]/div/div[2]/div/div[1]/div[1]/div[2]'.format(str(Del))).text
        except:
            data = ""
        self.assertEqual(Name, data, "Common Buddy Check Your Code --> Deal Not Deleted")
        time.sleep(1)

        time.sleep(5)


    # --> Handles Create Form Data

    def handle_Create_Lead_Form(self):
        driver = self.driver
        driver.find_element_by_name('First Name').clear()
        Name = fake.first_name()
        driver.find_element_by_name('First Name').send_keys(Name)
        driver.find_element_by_name('Middle Name').clear()
        driver.find_element_by_name('Middle Name').send_keys(fake.last_name())
        driver.find_element_by_name('Last Name').clear()
        driver.find_element_by_name('Last Name').send_keys(fake.last_name())
        driver.find_element_by_name('Company').clear()
        driver.find_element_by_name('Company').send_keys(fake.company())
        driver.find_element_by_name('Primary Email').clear()
        driver.find_element_by_name('Primary Email').send_keys(fake.email())
        driver.find_element_by_name('Business Email').clear()
        driver.find_element_by_name('Business Email').send_keys(fake.email())
        driver.find_element_by_name('Work Phone').clear()
        driver.find_element_by_name('Work Phone').send_keys(fake.random_number(10))
        driver.find_element_by_name('Mobile').clear()
        driver.find_element_by_name('Mobile').send_keys(fake.random_number(10))
        driver.find_element_by_name('Country').clear()
        driver.find_element_by_name('Country').send_keys(fake.country())
        # Assigned_To
        driver.find_element_by_name('Assigned To').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[10]/div/div/div[2]/div/div[{}]'.format(
                str(randint(1, 3)))).click()
        # Contact
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[12]/div').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[12]/div/div/div[2]/div/div/div[{}]/div[2]/div'.format(
                str(randint(2, 4)))).click()
        driver.find_element_by_class_name('appCreateButtonLabel').click()
        time.sleep(2)
        return  Name



    # --> Test Case For Creation Of Lead.

    def test_Create_Lead(self):
        driver = self.driver
        driver.get(self.base_url + "/leads")
        self.handle_Cookies()
        driver.get(self.base_url + "/leads")
        time.sleep(3)
        # Creation
        driver.find_element_by_class_name('createNewLead').click()
        time.sleep(1)
        Name = self.handle_Create_Lead_Form()
        try:
            msg = driver.find_element_by_class_name('leadDataRowContainerItemsIn').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Name.lower(),msg, "Common Buddy Check Your Code --> Lead Not Created")

        # Edit_Lead

        driver.find_element_by_class_name('leadDataRowContainerItemsIn').click()
        time.sleep(2)
        driver.find_element_by_class_name('edit').click()
        time.sleep(1)
        Edit = self.handle_Create_Lead_Form()
        driver.back()
        try:
            msg = driver.find_element_by_xpath('//*[@id="leadContainer"]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Edit.lower(),msg, "Common Buddy Check Your Code --> Lead Not Updated")
        time.sleep(2)
        # Edit In Individual Page
        driver.find_element_by_xpath('//*[@id="leadContainer"]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]').click()
        time.sleep(2)
        # Create_Todo
        # Click_Todo_Tab
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[2]').click()
        # Create
        driver.find_element_by_class_name('btn').find_element_by_class_name('buttonBlue').click()
        # To UnCheck Default Lead Option
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[5]/div/div[3]').click()
        Edit_Todo = self.handle_Todo_Form()
        driver.refresh()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'auditLogTime')))
        # Click To_Do
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[2]').click()
        try:
            msg = driver.find_element_by_class_name('activityInRowDayToDoData').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Edit_Todo.lower(),msg, "Common Buddy Check Your Code --> Todo Not Created In Leads")
        time.sleep(2)
        #  Notes
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[5]').click()
        driver.find_element_by_class_name('options').click()
        title = fake.color_name()
        driver.find_element_by_id('title').send_keys(title)
        driver.find_element_by_id('body').send_keys(fake.address())
        driver.find_element_by_class_name('save').click()
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'auditLogTime')))
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[1]/div[5]').click()
        try:
            msg = driver.find_element_by_class_name('data').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertEqual(title.lower(), msg, "Common Buddy Check Your Code --> Notes Not Created In Leads")
        time.sleep(1)
        # Delete Notes
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/i').click()
        driver.find_element_by_class_name('buttonDiv').find_element_by_class_name('blue').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('datar').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertNotEqual(title.lower(), msg, "Common Buddy Check Your Code --> Notes Not Deleted In Leads")
        # Assigned To
        driver.find_element_by_class_name('dataIndiHeadDealInfoAssignedTo').click()
        time.sleep(2)
        check = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[1]/div[2]/div/section/div/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div[{}]/div[2]/div[1]'.format(
                str(randint(1, 2))))
        Name = check.text
        check.click()
        try:
            msg = driver.find_element_by_class_name('dataIndiHeadDealInfoAssignedTo').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Name, msg, "Common Buddy Check Your Code --> Notes Not Deleted In Leads")
        time.sleep(2)
        # Send Email
        driver.find_element_by_class_name('dataIndiHeadDealEmail').click()
        driver.find_element_by_name('subject').send_keys(fake.street_name())
        driver.find_element_by_name('body').send_keys(fake.address())
        driver.find_element_by_class_name('appNewMessageComposeOptionsSendmail').click()
        time.sleep(2)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'showToast')))
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("message sent" in msg, "Common Buddy Check Your Code --> Mail Not Sent In Leads")
        time.sleep(2)
        # Delete_Lead
        driver.find_element_by_class_name('dataIndiHeadDealDelete').click()
        driver.find_element_by_class_name('dataBlueBtn').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("lead successfully deleted" in msg, "Common Buddy Check Your Code --> Lead Not Deleted")
        time.sleep(2)


    # --> Test Case For Services.

    def test_Service_Plan(self):
        driver = self.driver
        driver.get(self.base_url + "/services")
        self.handle_Cookies()
        driver.get(self.base_url + "/services")
        # Create Service Plan
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'servicePlan')))
        time.sleep(2)
        driver.find_element_by_class_name('servicePlan').click()
        time.sleep(1)
        driver.find_element_by_class_name('dataAppServiceButtonPlan').click()
        time.sleep(1)
        Name = fake.name()
        driver.find_element_by_name('Name').send_keys(Name)
        # Product_Select
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/div/div').click()
        time.sleep(2.5)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div/div[2]/div/div[{}]'.format(
                str(randint(1, 3)))).click()
        # Slots
        slots = randint(1, 3)
        driver.find_element_by_name('Maximum Number of Slots').send_keys(str(slots))
        driver.find_element_by_class_name('servicePlanMailTemplate').send_keys(fake.sentence())
        Actions = driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name('buttonBlue')
        ActionChains(driver).move_to_element(Actions).perform()
        Yes_No = randint(1, 2)
        if Yes_No == 1:
            # Check_Yes
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[5]/div/span[{}]'.format(str(Yes_No))).click()
            # Select
            driver.find_element_by_class_name('serviceIntervalSelected').click()
            select = randint(1, 2)
            # Select Day/Month
            if select == 1 or select == 2:
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div/div[1]/span[2]/div/div/div/div[2]/div[{}]'.format((str(select)))).click()
                driver.find_element_by_name('interval').send_keys(randint(1, 12))
                driver.find_element_by_name('cost').send_keys(randint(5000, 10000))
                driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name('buttonBlue').click()
                time.sleep(1)
            # Other Than Day/Mnth
            else:
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[5]/div/span[{}]'.format(str(select))).click()
                driver.find_element_by_name('cost').send_keys(randint(5000, 10000))
                driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name('buttonBlue').click()
                time.sleep(1)
            try:
                msg = driver.find_element_by_class_name('dataServicePlanListServiceName').text
            except NoSuchElementException:
                msg = ""
            self.assertEqual(Name, msg, "Common Buddy Check Your Code --> Service Plan Not Created")
        else:
            # Check No
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[5]/div/span[{}]'.format(str(Yes_No))).click()
            for i in range(1, slots + 1):
                # Select
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div[{}]/div[1]/span[2]/div/div/div/div'.format(str(i))).click()
                time.sleep(1)
                # Year
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div[{}]/div[1]/span[2]/div/div/div/div[2]/div[5]'.format(str(i))).click()
                # Cost
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div[{}]/div[2]/span[2]/input'.format(str(i))).send_keys(randint(5000, 10000))
            driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name('buttonBlue').click()
            time.sleep(1)
            try:
                msg = driver.find_element_by_class_name('dataServicePlanListServiceName').text
            except NoSuchElementException:
                msg = ""
            self.assertEqual(Name, msg, "Common Buddy Check Your Code --> Service Plan Not created")

        # Edit Service Plan
        driver.find_element_by_class_name('servicePlaneEidtIcon').click()
        driver.find_element_by_name('Name').clear()
        Edit_Name = fake.name()
        driver.find_element_by_name('Name').send_keys(Edit_Name)
        # Slots
        slots = randint(1, 3)
        driver.find_element_by_name('Maximum Number of Slots').clear()
        driver.find_element_by_name('Maximum Number of Slots').send_keys(str(slots))
        driver.find_element_by_class_name('servicePlanMailTemplate').clear()
        driver.find_element_by_class_name('servicePlanMailTemplate').send_keys(fake.sentence())
        Actions = driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name('buttonBlue')
        ActionChains(driver).move_to_element(Actions).perform()
        Yes_No = randint(1, 2)
        if Yes_No == 1:
            # Check Yes
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[4]/div/span[{}]'.format(str(Yes_No))).click()
            driver.find_element_by_class_name('serviceIntervalSelected').click()
            select = randint(1, 2)
            # Select Day/Month
            if select == 1 or select == 2:
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[5]/div/div[1]/span[2]/div/div/div/div[2]/div[{}]'.format(str(select))).click()
                driver.find_element_by_name('interval').send_keys(randint(1, 12))
                driver.find_element_by_name('cost').send_keys(randint(5000, 10000))
                driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name(
                    'buttonBlue').click()
                time.sleep(1)
            # Other Than Day/Mnth
            else:
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[5]/div/div[1]/span[2]/div/div/div/div[2]/div[{}]'.format(str(select)))
                driver.find_element_by_name('cost').send_keys(randint(5000, 10000))
                driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name(
                    'buttonBlue').click()
                time.sleep(1)
            try:
                msg = driver.find_element_by_class_name('dataServicePlanListServiceName').text
            except NoSuchElementException:
                msg = ""
            self.assertEqual(Edit_Name, msg, "Common Buddy Check Your Code --> Service Plan Not Updated")
        else:
            # Check No
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[4]/div/span[{}]'.format(str(Yes_No))).click()
            for i in range(1, slots + 1):
                # Select
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[5]/div[{}]/div[1]/span[2]/div/div/div/div'.format(str(i))).click()
                # Year
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[5]/div[{}]/div[1]/span[2]/div/div/div/div[2]/div[5]'.format(str(i))).click()
                # Cost
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[4]/div/div/div/div[5]/div[{}]/div[2]/span[2]/input'.format(str(i))).send_keys(randint(5000, 10000))
            driver.find_element_by_class_name('createServicePlanBtn').find_element_by_class_name('buttonBlue').click()
            time.sleep(1)
            try:
                msg = driver.find_element_by_class_name('dataServicePlanListServiceName').text
            except NoSuchElementException:
                msg = ""
            self.assertEqual(Edit_Name, msg, "Common Buddy Check Your Code --> Service Plan Not Updated")
        driver.find_element_by_class_name('servicePlaneArchive').click()
        driver.find_element_by_class_name('buttonDiv').find_element_by_class_name('dataBlueBtn').click()
        # Select Archive Tab
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]').click()
        time.sleep(2)
        try:
            msg = driver.find_element_by_class_name('dataServicePlanListServiceName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Edit_Name, msg, "Common Buddy Check Your Code --> Service Plan Not Archived")
        time.sleep(2)

    # --> Test Case For Subscription

    def test_Subscription(self):
        driver = self.driver
        driver.get(self.base_url + "/services")
        self.handle_Cookies()
        driver.get(self.base_url + "/services")
        # Create Subscription
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'serviceSubscription')))
        time.sleep(2)
        driver.find_element_by_class_name('serviceSubscription').click()
        time.sleep(1)
        driver.find_element_by_class_name('dataAppServiceButtonSub').click()
        driver.find_element_by_class_name('SubScriptionCommon').click()
        Ppl_Org = randint(1,2)
        # Select Either Ppl or Org
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[1]/span[2]/select/option[{}]'.format(str(Ppl_Org))).click()
        time.sleep(1)
        if Ppl_Org == 1:
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/span/div/div').click()
            time.sleep(1.5)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/span/div/div/div/div[2]/div/div/div[{}]'.format(str(randint(2,3)))).click()
        else :
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/div/div').click()
            time.sleep(1.5)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[{}]'.format(str(randint(2,3)))).click()
        # Service Plan
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[3]/div/div').click()
        Plan = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[3]/div/div/div/div[2]/div/div[{}]'.format(str(randint(1,3))))
        Name = Plan.text
        Plan.click()
        # Assigned_To
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[4]/div/div').click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[4]/div/div/div/div[2]/div/div[1]')))
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[4]/div/div/div/div[2]/div/div[{}]'.format(randint(1,2))).click()
        # Move To Bottom
        Actions = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/span/button')
        ActionChains(driver).move_to_element(Actions).perform()
        # Pipeline
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[5]/div/div').click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[5]/div/div/div/div[2]/div/div[1]')))
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[5]/div/div/div/div[2]/div/div[{}]'.format(str(randint(1,2)))).click()
        # Deal Loss Reason
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div/div').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div/div/div/div[2]/div/div[1]')))
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[6]/div/div/div/div[2]/div/div[{}]'.format((randint(1,2)))).click()
        # Notify Before
        driver.find_element_by_name('Notify Before').send_keys(randint(1,4))
        # Create a Deal Before
        driver.find_element_by_name('Create a Deal Before').send_keys(randint(1,3))
        # Date
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[9]/div/div').click()
        driver.find_element_by_class_name('DayPickerNavigation__next').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/div[9]/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{}]/td[{}]/button'.format(str(randint(2,4)),str(randint(1,6)))).click()
        # Submit
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/span/button').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('dataScriptionPlaneInnName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Name, msg, "Common Buddy Check Your Code --> Subscription Not Created")
        # Edit Subscription
        driver.find_element_by_class_name('servicePlaneEidtIcon').click()
        # Assigned_To
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div/div').click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]')))
        Assign = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[{}]/div[2]/div[1]'.format(str(randint(1,2))))
        Edit_Name = Assign.text
        Assign.click()
        # Deal Loss Reason
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div').click()
        time.sleep(1.5)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[{}]'.format(str(randint(1,3)))).click()
        # Notify Before
        driver.find_element_by_name('Notify Before').send_keys(randint(1,4))
        # Create a Deal Before
        driver.find_element_by_name('Create a Deal Before').send_keys(randint(1,3))
        # Submit
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/span/button').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div[2]/div/span[6]').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Edit_Name, msg, "Common Buddy Check Your Code --> Subscription Not Updated")
        # Archive Subscription
        Plan_name = driver.find_element_by_class_name('dataScriptionPlaneInnName').text
        driver.find_element_by_class_name('subscribeArchive').click()
        driver.find_element_by_class_name('buttonDiv').find_element_by_class_name('dataBlueBtn').click()
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]').click()
        time.sleep(1.5)
        try:
            msg = driver.find_element_by_class_name('dataScriptionPlaneInnName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Plan_name, msg, "Common Buddy Check Your Code --> Subscription Not Archived")

        time.sleep(2)


    # --> Handle Create People Contact Data.

    def handle_CreateContact_Form(self):
        driver = self.driver
        #driver.find_element_by_name('Profile Image').send_keys(os.getcwd() + "/Cartoon.jpg")
        driver.find_element_by_name('First Name').clear()
        driver.find_element_by_name('First Name').send_keys(fake.first_name())
        driver.find_element_by_name('Middle Name').clear()
        driver.find_element_by_name('Middle Name').send_keys(fake.last_name())
        driver.find_element_by_name('Last Name').clear()
        driver.find_element_by_name('Last Name').send_keys(fake.last_name())
        driver.find_element_by_name('Primary Email').clear()
        driver.find_element_by_name('Primary Email').send_keys(fake.email())
        driver.find_element_by_name('Mobile').clear()
        Phone = fake.random_number(10)
        driver.find_element_by_name('Mobile').send_keys(Phone)
        driver.find_element_by_name('Company').clear()
        driver.find_element_by_name('Company').send_keys(fake.company())
        driver.find_element_by_name('Job Role').clear()
        driver.find_element_by_name('Job Role').send_keys(fake.job())
        driver.find_element_by_name('Business Email').clear()
        driver.find_element_by_name('Business Email').send_keys(fake.email())
        driver.find_element_by_name('Work Phone').clear()
        driver.find_element_by_name('Work Phone').send_keys(fake.random_number(10))
        driver.find_element_by_class_name('appCreateButtonLabel').click()
        time.sleep(2)
        print(Phone)
        return Phone

    # --> Test Case For Creation Of People Contact.

    def test_Create_Contact_People(self):
        driver = self.driver
        driver.get(self.base_url + "/contact")
        self.handle_Cookies()
        driver.get(self.base_url + "/contact")
        time.sleep(2)
        # Creation
        driver.find_element_by_class_name('contactNavCreateNew').click()
        time.sleep(2)
        Phone = self.handle_CreateContact_Form()
        time.sleep(2)
        driver.find_element_by_class_name('contactDataIcon').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[3]').text
            msg = int(msg)
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Phone ,msg, "Common Buddy Check Your Code --> Contact Not Created")
        time.sleep(2)
        # Edit_People_Contact
        driver.find_element_by_class_name('contactOptions').click()
        driver.find_element_by_class_name('contactOptionEditProfile').click()
        time.sleep(2)
        edit_Phone = self.handle_CreateContact_Form()
        time.sleep(1)
        try:
            msg = driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[3]').text
            msg = int(msg)
        except NoSuchElementException:
            msg = ""
        self.assertEqual(edit_Phone ,msg, "Common Buddy Check Your Code --> Contact Not Updated")
        time.sleep(2)
        # Add_Todo
        driver.find_element_by_class_name('Activities').click()
        driver.find_element_by_class_name('buttonBlue').click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[5]/div/div[2]').click()
        todo_Name = self.handle_Todo_Form()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'Activities')))

        try:
           msg = driver.find_element_by_class_name('activityInRowDayToDoData').text
           msg = msg.lower()
        except NoSuchElementException:
           msg = ""
        self.assertEqual(todo_Name, msg, "Common Buddy Check Your Code --> Todo_Not Created")

        # Create_Notes
        driver.find_element_by_class_name('Notes').click()
        driver.find_element_by_class_name('icon-Add').click()
        Note_title = fake.safe_color_name()
        driver.find_element_by_id('title').send_keys(Note_title)
        driver.find_element_by_id('body').send_keys(fake.address())
        driver.find_element_by_class_name('dataAppNotesFootSave').click()
        driver.refresh()
        click_Notes = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'Notes')))
        click_Notes.click()
        try:
            Notes = driver.find_element_by_class_name('dataAppNotesIndiData').text
        except:
            Notes = ""
        self.assertEqual(Note_title.lower(), Notes.lower(),"Common Buddy Check Your Code --> Problem In Creation Of Notes")


        # Delete Contact
        driver.find_element_by_class_name('contactOptions').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[3]/div[4]').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("contact deleted" in msg, "Common Buddy Check Your Code --> Contact Not Deleted")
        time.sleep(2)


    # -->  Handle Create Organisation Contact Data.

    def handle_Contact_Org(self):
        driver = self.driver
        driver.find_element_by_name('Profile Image').send_keys(os.getcwd() + "/Cartoon.jpg")
        driver.find_element_by_name('Name').clear()
        driver.find_element_by_name('Name').send_keys(fake.first_name())
        driver.find_element_by_name('Email').clear()
        driver.find_element_by_name('Email').send_keys(fake.email())
        driver.find_element_by_name('Primary Phone').clear()
        Phone = fake.random_number(10)
        driver.find_element_by_name('Primary Phone').send_keys(Phone)
        driver.find_element_by_name('Website').clear()
        driver.find_element_by_name('Website').send_keys(fake.url())
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[4]/div/div[1]/div').click()
        time.sleep(1)
        return Phone


    # --> Test Case For Creation Of Organization Contact.

    def test_Create_Contact_Org(self):
        driver=self.driver
        driver.get(self.base_url + "/contact")
        self.handle_Cookies()
        driver.get(self.base_url + "/contact")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[1]/div[1]/div[2]/div[2]').click()
        time.sleep(2)
        driver.find_element_by_class_name('contactNavCreateNew').click()
        time.sleep(2)
        driver.find_element_by_class_name('widgetBoxContentMBoxButtonAddMoreField').click()
        driver.find_element_by_xpath('//*[@id="dataAppAddFileSelect"]/div/div[1]/div[2]/div[3]/div').click()
        Phone = self.handle_Contact_Org()
        time.sleep(2.5)
        driver.find_element_by_class_name('contactDataIcon').click()
        time.sleep(3)
        try:
            msg = driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]').text
            msg = int(msg)
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Phone,msg, "Common Buddy Check Your Code --> Organisation Contact Not Created")
        # Edit_Org_Contact
        driver.find_element_by_class_name('contactOptions').click()
        driver.find_element_by_class_name('contactOptionEditProfile').click()
        time.sleep(2)
        edit_Phone = self.handle_Contact_Org()
        time.sleep(1)
        try:
            msg = driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[3]').text
            msg = int(msg)
        except NoSuchElementException:
            msg = ""
        self.assertEqual(edit_Phone,msg, "Common Buddy Check Your Code --> Organisation Contact Not Updated")
        time.sleep(1)
        # Delete Cotact
        driver.find_element_by_class_name('contactOptions').click()
        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="contactMainBox"]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[3]/div[4]').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("organisation deleted" in msg, "Common Buddy Check Your Code --> Organisation Not Deleted")
        time.sleep(2)


    # --> Create New Pipeline.

    def test_Create_Pipeline(self):
        driver = self.driver
        driver.get(self.base_url + "/pipeline")
        self.handle_Cookies()
        driver.get(self.base_url + "/pipeline")
        drive = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,'pipelineNavChoosePipelineName')))
        drive.click()
        driver.find_element_by_class_name('pipelineChooseCreateNew').click()
        driver.find_element_by_name('name').send_keys(fake.street_name())
        driver.find_element_by_name('description').send_keys(fake.sentence())

        # Addition of stages
        for i in range(1,4):
            driver.find_element_by_name('stage' + str(i)).send_keys(fake.city())
            if i!=3:
                driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div[3]/div[2]/div[4]').click()

        driver.find_element_by_class_name('appCreateButtonLabel').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("new pipeline has been created" in msg, "Common Buddy Check Your Code --> Pipeline Not Created")
        time.sleep(2)

        # Edit_Pipeline
        driver.find_element_by_class_name('pipelineNavTopLayerOptions').click()
        time.sleep(1.5)
        driver.find_element_by_name('name').clear()
        driver.find_element_by_name('name').send_keys(fake.street_name())
        driver.find_element_by_name('description').clear()
        driver.find_element_by_name('description').send_keys(fake.sentence())
        for i in range(1,4):
            driver.find_element_by_name('stage' + str(i)).clear()
            driver.find_element_by_name('stage' + str(i)).send_keys(fake.city())
        driver.find_element_by_class_name('appCreateButtonLabel').click()
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,"showToast")))
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("new pipeline has been created" in msg, "Common Buddy Check Your Code --> Pipeline Not Updated")
        time.sleep(2)


    # --> Handle_Todo_Form

    def handle_Todo_Form(self):
        driver = self.driver
        driver.find_element_by_class_name('activityTypeChooser').click()
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[2]/div/div[2]/div[2]/div[{}]'.format(str(randint(1, 6)))).click()
        # Todo_Name
        todo_name = fake.color_name()
        driver.find_element_by_name('name').send_keys(todo_name)
        driver.find_element_by_name('description').send_keys(fake.sentence())
        # Assigned_to
        driver.find_element_by_name('assignedto').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/section/div/div/div/div[3]/div[3]/div[3]/div/div/div[2]/div/div[{}]'.format(str(randint(1, 3)))).click()
        # Due_Date


        # YET TO DO


        # Location
        driver.find_element_by_name('location').send_keys(fake.city())
        driver.find_element_by_class_name('appCreateButtonLabel').click()
        time.sleep(2)
        return todo_name


    # --> Test Case for Creation of_Todo

    def test_Create_todo(self):
        driver = self.driver
        driver.get(self.base_url + "/dashboard")
        self.handle_Cookies()
        driver.get(self.base_url + "/dashboard")
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,'dataQuickAddButton')))
        #Quick Action
        driver.find_element_by_class_name('dataQuickAddButton').click()
        driver.find_element_by_class_name('dataAppATask').click()
        time.sleep(2)
        self.handle_Todo_Form()




    # --> Handle Goal Form Data.

    def handle_Goal_Form(self):
        driver = self.driver
        today = datetime.date.today()
        end = date(today.year, 3, today.day)
        Name = fake.company()
        driver.find_element_by_name('name').send_keys(Name)
        driver.find_element_by_name('description').send_keys(fake.sentence())
        driver.find_element_by_name('target').send_keys(randint(10,100))
        # Slection Of Different Options
        Choice = randint(1,4)
        if Choice == 1:
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[4]/div[{}]'.format(Choice)).click()
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[5]/div').click()
            time.sleep(1.5)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[5]/div/div/div[2]/div/div[{}]'.format(str(randint(1,3)))).click()
            driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(str(today))
            driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(str(end))
            driver.find_element_by_xpath( '//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[7]/div').click()
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[7]/div/div/div[2]/div/div[{}]'.format(str(randint(1,3)))).click()

        elif Choice == 3:
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[4]/div[{}]'.format(Choice)).click()
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[5]/div').click()
            time.sleep(1.5)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[5]/div/div/div[2]/div/div[{}]'.format(str(randint(1,2)))).click()
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[5]/div/div/div[3]/span').click()
            driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(str(today))
            driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(str(end))
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[7]/div').click()
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[7]/div/div/div[2]/div/div[{}]'.format(str(randint(1, 3)))).click()

        else:
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[4]/div[{}]'.format(Choice)).click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(str(today))
            driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(str(end))
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[6]/div').click()
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[6]/div/div/div[2]/div/div[{}]'.format(str(randint(1,3)))).click()

        driver.find_element_by_class_name('widgetBoxContentMBoxButton').click()
        time.sleep(2)
        return Name


    # --> Test Case For Creation Of Goal.

    def test_Create_Goal(self):
        driver = self.driver
        driver.get(self.base_url + "/goals")
        self.handle_Cookies()
        driver.get(self.base_url + "/goals")
        time.sleep(2)
        driver.find_element_by_class_name('dataGoalSystemListHeadCreate').click()
        # Selection Of Goal Type
        Choice = randint(1,4)
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[{}]'.format(Choice)).click()
        Name = str(self.handle_Goal_Form())
        try:
            msg = driver.find_element_by_class_name('goalName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Name.lower(), msg.lower(), "Common Buddy Check Your Code --> Goal Not Created")
        time.sleep(1)

        # Edit_Goal

        driver.find_element_by_class_name('goalOptionsEdit').click()
        edit_Name = fake.company()
        driver.find_element_by_name('name').clear()
        driver.find_element_by_name('name').send_keys(edit_Name)
        driver.find_element_by_name('description').clear()
        driver.find_element_by_name('description').send_keys(fake.sentence())
        driver.find_element_by_class_name('widgetBoxContentMBoxButton').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('goalName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(edit_Name.lower(), msg.lower(), "Common Buddy Check Your Code --> Problem In Updating Goal")
        # View Goal
        driver.find_element_by_class_name('goalOptionsView').click()
        time.sleep(2)
        Goal_Name = driver.find_element_by_class_name('dataGoalsIndiRowGoalIndi').text
        driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/div/h4/i').click()
        try:
            msg = driver.find_element_by_class_name('goalName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Goal_Name, msg, "Common Buddy Check Your Code --> Goal Not Viewed")
        time.sleep(2)
        # Archive Goal
        driver.find_element_by_class_name('goalOptionsArchieve').click()
        driver.find_element_by_class_name('dataBlueBtn').click()
        time.sleep(1)
        driver.find_element_by_class_name('dataGoalSystemListHeadArchieved').click()
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,'goalName')))
        try:
            msg = driver.find_element_by_class_name('goalName').text
        except NoSuchElementException:
            msg = ""
        self.assertEqual(Goal_Name, msg, "Common Buddy Check Your Code --> Goal Not Archived")
        # Move Back To Active Goals
        driver.find_element_by_class_name('dataGoalSystemListHeadActive').click()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'goalName')))
        time.sleep(1)
        # Delete Goal
        Name = driver.find_element_by_class_name('goalName').text
        driver.find_element_by_class_name('goalOptionsDelete').click()
        driver.find_element_by_class_name('dataBlueBtn').click()
        time.sleep(2)
        try:
            msg = driver.find_element_by_class_name('goalName').text
        except NoSuchElementException:
            msg = ""
        self.assertNotEqual(Name.lower(), msg.lower(), "Common Buddy Check Your Code --> Goal Not Deleted")
        time.sleep(2)



    # -->Test Case For Update_Basic_Info

    def test_Edit_Basic_Info(self):
        driver = self.driver
        driver.get(self.base_url + "/settings/basic")
        self.handle_Cookies()
        driver.get(self.base_url + "/settings/basic")
        time.sleep(2)
        driver.find_element_by_id('fileuploader').send_keys(os.getcwd() + "/Cartoon.jpg")
        driver.find_element_by_name('first_name').clear()
        driver.find_element_by_name('first_name').send_keys(fake.first_name())
        driver.find_element_by_name('last_name').clear()
        driver.find_element_by_name('last_name').send_keys(fake.last_name())
        driver.find_element_by_name('phone').clear()
        driver.find_element_by_name('phone').send_keys(fake.random_number(10))
        driver.find_element_by_class_name('appSaveButton').click()
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME,'showToast')))
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        print(msg)
        self.assertEqual("user info updated",msg, "Common Buddy Check Your Code --> User Info Not Updated")
        time.sleep(1)



    # --> Test Case For Deletion Of Deal.

    def test_Delete_Lead(self):
        driver = self.driver
        driver.get(self.base_url + "/leads")
        self.handle_Cookies()
        driver.get(self.base_url + "/leads")
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH,'//*[@id="leadContainer"]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div')))
        driver.find_element_by_xpath('//*[@id="leadContainer"]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]').click()
        time.sleep(2)
        driver.find_element_by_class_name('dataIndiHeadDealDelete').click()
        driver.find_element_by_class_name('dataBlueBtn').click()
        time.sleep(1)
        try:
            msg = driver.find_element_by_class_name('showToast').text
            msg = msg.lower()
        except NoSuchElementException:
            msg = ""
        self.assertTrue("lead successfully deleted" in msg, "Common Buddy Check Your Code --> Lead Not Deleted")
        time.sleep(2)


    # --> Test Case For Deletion Of Goal

    def test_Del_Goal(self):
        driver = self.driver
        driver.get(self.base_url + "/goals")
        self.handle_Cookies()
        driver.get(self.base_url + "/goals")
        time.sleep(2)
        Name = driver.find_element_by_class_name('goalName').text
        driver.find_element_by_class_name('goalOptionsDelete').click()
        driver.find_element_by_class_name('dataBlueBtn').click()
        time.sleep(2)
        try:
            msg = driver.find_element_by_class_name('goalName').text
        except NoSuchElementException:
            msg = ""
        self.assertNotEqual(Name.lower(), msg.lower(), "Common Buddy Check Your Code --> Goal Not Deleted")



    # --> Test Case For Deletion Of People Contact.

    def test_del_Contact(self):
        driver = self.driver
        driver.get(self.base_url + "/contact")
        self.handle_Cookies()
        driver.get(self.base_url + "/contact")
        time.sleep(2)
        for i in range(20):
            driver.find_element_by_class_name('contactOptions').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[3]/div[4]').click()
            time.sleep(1)
            try:
                msg = driver.find_element_by_class_name('showToast').text
                msg = msg.lower()
            except NoSuchElementException:
                msg = ""
            self.assertTrue("contact deleted" in msg,"Common Buddy Check Your Code --> Contact Not Deleted")
        time.sleep(2)


    # --> Test Case For Deletion Of Organisation Contact.

    def test_del_Org_Contact(self):
        driver = self.driver
        driver.get(self.base_url + "/contact")
        self.handle_Cookies()
        driver.get(self.base_url + "/contact")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[1]/div[1]/div[2]/div[2]').click()
        time.sleep(2)
        for i in range(19):
            driver.find_element_by_class_name('contactOptions').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="contactMainBox"]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[3]/div[4]').click()
            time.sleep(1)
            try:
                msg = driver.find_element_by_class_name('showToast').text
                msg = msg.lower()
            except NoSuchElementException:
                msg = ""
            self.assertTrue("organisation deleted" in msg,"Common Buddy Check Your Code --> Organisation Not Deleted")
            time.sleep(2)
        time.sleep(2)






    # --> Teardown Which Runs After Every Testcase.

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()







