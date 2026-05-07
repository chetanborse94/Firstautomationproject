"""
Driver 007 Admin Portal - Comprehensive Test Suite
Tests based on SRS requirements
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
from datetime import datetime

class TestResults:
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.bugs = []
    
    def add_test(self, test_name, status, error=None):
        self.tests.append({
            'test_name': test_name,
            'status': status,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        if status == 'PASSED':
            self.passed += 1
        else:
            self.failed += 1
    
    def add_bug(self, bug_title, description, severity, steps_to_reproduce):
        bug = {
            'id': f"BUG-{len(self.bugs) + 1}",
            'title': bug_title,
            'description': description,
            'severity': severity,  # CRITICAL, HIGH, MEDIUM, LOW
            'steps_to_reproduce': steps_to_reproduce,
            'timestamp': datetime.now().isoformat(),
            'status': 'OPEN'
        }
        self.bugs.append(bug)
    
    def generate_report(self):
        report = {
            'test_summary': {
                'total_tests': self.passed + self.failed,
                'passed': self.passed,
                'failed': self.failed,
                'pass_rate': f"{(self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0:.2f}%"
            },
            'test_results': self.tests,
            'bugs_found': len(self.bugs),
            'bugs': self.bugs
        }
        return report
    
    def save_report(self, filename='test_report.json'):
        with open(filename, 'w') as f:
            json.dump(self.generate_report(), f, indent=2)
        print(f"\n✓ Report saved to {filename}")

class DriverTestSuite:
    def __init__(self):
        self.driver = None
        self.results = TestResults()
        self.base_url = 'https://driver007.com/admin/'
        self.valid_email = 'sst.superadmin@yopmail.com'
        self.valid_password = 'admin@321'
    
    def setup(self):
        """Initialize WebDriver"""
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.results.add_test('Setup Browser', 'PASSED')
        except Exception as e:
            self.results.add_test('Setup Browser', 'FAILED', str(e))
            raise
    
    def teardown(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
    
    # ===== AUTHENTICATION TESTS =====
    def test_page_load(self):
        """TC-001: Verify login page loads successfully"""
        try:
            print("\n[TC-001] Testing page load...")
            self.driver.get(self.base_url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
            self.results.add_test('Page Load', 'PASSED')
            print("✓ Page loaded successfully")
        except Exception as e:
            self.results.add_test('Page Load', 'FAILED', str(e))
            print(f"✗ Page load failed: {e}")
    
    def test_email_field_exists(self):
        """TC-002: Verify email input field exists"""
        try:
            print("\n[TC-002] Testing email field exists...")
            email_input = self.driver.find_element(By.ID, 'validation-form-2')
            assert email_input.get_attribute('type') == 'email'
            self.results.add_test('Email Field Exists', 'PASSED')
            print("✓ Email field exists and is correct type")
        except Exception as e:
            self.results.add_test('Email Field Exists', 'FAILED', str(e))
            print(f"✗ Email field test failed: {e}")
    
    def test_password_field_exists(self):
        """TC-003: Verify password input field exists"""
        try:
            print("\n[TC-003] Testing password field exists...")
            password_input = self.driver.find_element(By.ID, 'validation-form-3')
            assert password_input.get_attribute('type') == 'password'
            self.results.add_test('Password Field Exists', 'PASSED')
            print("✓ Password field exists and is correct type")
        except Exception as e:
            self.results.add_test('Password Field Exists', 'FAILED', str(e))
            print(f"✗ Password field test failed: {e}")
    
    def test_valid_login(self):
        """TC-004: Verify valid login credentials work"""
        try:
            print("\n[TC-004] Testing valid login...")
            self.driver.get(self.base_url)
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'validation-form-2'))
            )
            password_input = self.driver.find_element(By.ID, 'validation-form-3')
            
            email_input.send_keys(self.valid_email)
            password_input.send_keys(self.valid_password)
            password_input.send_keys(Keys.RETURN)
            
            sleep(3)
            
            # Check if we're logged in
            current_url = self.driver.current_url
            if 'admin' in current_url or self.driver.title != 'Login':
                self.results.add_test('Valid Login', 'PASSED')
                print("✓ Valid login successful")
            else:
                self.results.add_test('Valid Login', 'FAILED', 'Still on login page after submission')
                print("✗ Login failed - still on login page")
        except Exception as e:
            self.results.add_test('Valid Login', 'FAILED', str(e))
            print(f"✗ Valid login test failed: {e}")
    
    def test_invalid_email_login(self):
        """TC-005: Verify invalid email is rejected"""
        try:
            print("\n[TC-005] Testing invalid email rejection...")
            self.driver.get(self.base_url)
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'validation-form-2'))
            )
            password_input = self.driver.find_element(By.ID, 'validation-form-3')
            
            email_input.send_keys('invalid@email.com')
            password_input.send_keys(self.valid_password)
            password_input.send_keys(Keys.RETURN)
            
            sleep(2)
            
            # Check if error message appears
            error_elements = self.driver.find_elements(By.CLASS_NAME, 'error')
            if error_elements or self.driver.current_url == self.base_url:
                self.results.add_test('Invalid Email Rejection', 'PASSED')
                print("✓ Invalid email properly rejected")
            else:
                self.results.add_test('Invalid Email Rejection', 'FAILED', 'No error message shown')
                self.results.add_bug(
                    'Missing Error Message for Invalid Email',
                    'System did not display error message for invalid email',
                    'MEDIUM',
                    ['1. Navigate to login page', '2. Enter invalid email', '3. Enter valid password', '4. Submit form']
                )
                print("✗ No error message for invalid email")
        except Exception as e:
            self.results.add_test('Invalid Email Rejection', 'FAILED', str(e))
            print(f"✗ Invalid email test failed: {e}")
    
    def test_invalid_password_login(self):
        """TC-006: Verify invalid password is rejected"""
        try:
            print("\n[TC-006] Testing invalid password rejection...")
            self.driver.get(self.base_url)
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'validation-form-2'))
            )
            password_input = self.driver.find_element(By.ID, 'validation-form-3')
            
            email_input.send_keys(self.valid_email)
            password_input.send_keys('wrongpassword')
            password_input.send_keys(Keys.RETURN)
            
            sleep(2)
            
            if self.driver.current_url == self.base_url:
                self.results.add_test('Invalid Password Rejection', 'PASSED')
                print("✓ Invalid password properly rejected")
            else:
                self.results.add_test('Invalid Password Rejection', 'FAILED', 'Login succeeded with wrong password')
                self.results.add_bug(
                    'Security Issue: Wrong Password Accepted',
                    'System accepted login with incorrect password',
                    'CRITICAL',
                    ['1. Navigate to login page', '2. Enter valid email', '3. Enter invalid password', '4. Submit form']
                )
                print("✗ Wrong password was accepted - SECURITY ISSUE!")
        except Exception as e:
            self.results.add_test('Invalid Password Rejection', 'FAILED', str(e))
            print(f"✗ Invalid password test failed: {e}")
    
    def test_empty_email_validation(self):
        """TC-007: Verify empty email is not accepted"""
        try:
            print("\n[TC-007] Testing empty email validation...")
            self.driver.get(self.base_url)
            
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'validation-form-3'))
            )
            
            password_input.send_keys(self.valid_password)
            password_input.send_keys(Keys.RETURN)
            
            sleep(2)
            
            if self.driver.current_url == self.base_url:
                self.results.add_test('Empty Email Validation', 'PASSED')
                print("✓ Empty email properly rejected")
            else:
                self.results.add_test('Empty Email Validation', 'FAILED', 'Login succeeded with empty email')
                self.results.add_bug(
                    'Input Validation Issue: Empty Email Accepted',
                    'System allowed login with empty email field',
                    'HIGH',
                    ['1. Navigate to login page', '2. Leave email empty', '3. Enter password', '4. Submit form']
                )
                print("✗ Empty email was accepted")
        except Exception as e:
            self.results.add_test('Empty Email Validation', 'FAILED', str(e))
            print(f"✗ Empty email test failed: {e}")
    
    def test_empty_password_validation(self):
        """TC-008: Verify empty password is not accepted"""
        try:
            print("\n[TC-008] Testing empty password validation...")
            self.driver.get(self.base_url)
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'validation-form-2'))
            )
            password_input = self.driver.find_element(By.ID, 'validation-form-3')
            
            email_input.send_keys(self.valid_email)
            password_input.send_keys(Keys.RETURN)
            
            sleep(2)
            
            if self.driver.current_url == self.base_url:
                self.results.add_test('Empty Password Validation', 'PASSED')
                print("✓ Empty password properly rejected")
            else:
                self.results.add_test('Empty Password Validation', 'FAILED', 'Login succeeded with empty password')
                self.results.add_bug(
                    'Input Validation Issue: Empty Password Accepted',
                    'System allowed login with empty password field',
                    'HIGH',
                    ['1. Navigate to login page', '2. Enter email', '3. Leave password empty', '4. Submit form']
                )
                print("✗ Empty password was accepted")
        except Exception as e:
            self.results.add_test('Empty Password Validation', 'FAILED', str(e))
            print(f"✗ Empty password test failed: {e}")
    
    def run_all_tests(self):
        """Execute all test cases"""
        print("="*60)
        print("DRIVER 007 - COMPREHENSIVE TEST SUITE")
        print("="*60)
        
        try:
            self.setup()
            
            # Authentication Tests
            print("\n--- AUTHENTICATION TESTS ---")
            self.test_page_load()
            self.test_email_field_exists()
            self.test_password_field_exists()
            self.test_valid_login()
            self.test_invalid_email_login()
            self.test_invalid_password_login()
            self.test_empty_email_validation()
            self.test_empty_password_validation()
            
        except Exception as e:
            print(f"\n✗ Test suite encountered error: {e}")
        finally:
            self.teardown()
        
        # Generate and display report
        self.display_summary()
    
    def display_summary(self):
        """Display test summary and bug report"""
        report = self.results.generate_report()
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {report['test_summary']['total_tests']}")
        print(f"Passed: {report['test_summary']['passed']} ✓")
        print(f"Failed: {report['test_summary']['failed']} ✗")
        print(f"Pass Rate: {report['test_summary']['pass_rate']}")
        
        if self.results.bugs:
            print("\n" + "="*60)
            print(f"BUGS FOUND: {len(self.results.bugs)}")
            print("="*60)
            for bug in self.results.bugs:
                print(f"\n[{bug['id']}] {bug['title']}")
                print(f"Severity: {bug['severity']}")
                print(f"Description: {bug['description']}")
                print(f"Steps to Reproduce:")
                for step in bug['steps_to_reproduce']:
                    print(f"  - {step}")
        
        # Save report
        self.results.save_report('test_report.json')


if __name__ == '__main__':
    suite = DriverTestSuite()
    suite.run_all_tests()
