import unittest
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from apps.accounts.models import CustomUser
from apps.master.models import Rack, Ups, PowerSystem

"""
ラックマスタのテストケース
"""
class RackModelTest(TestCase):
    """
    ラック追加機能のテストケース
    """

    def test_valid_rack_number(self):
        """
        正しいrack_numberを指定してPOSTリクエストを送信することで、ラックが追加されることを確認
        """
        # テストに使用するデータ
        rack_number = 123

        # RackAddViewに対するURLを取得
        url = reverse('master:rack_add')

        # POSTリクエストを送信
        response = self.client.post(url, {'rack_number': rack_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースにラックが正しく追加されたかを確認
        self.assertTrue(Rack.objects.filter(rack_number=rack_number).exists())

    def test_invalid_negative_rack_number(self):
        """
        負のrack_numberを指定してPOSTリクエストを送信した場合、エラーが返されることを確認
        """

        # テストに使用するデータ（無効なrack_number）
        invalid_rack_number = -1

        # RackAddViewに対するURLを取得
        url = reverse('master:rack_add') 

        # POSTリクエストを送信
        response = self.client.post(url, {'rack_number': invalid_rack_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

        # データベースにラックが追加されていないことを確認
        self.assertFalse(Rack.objects.filter(rack_number=invalid_rack_number).exists())

    def test_invalid_large_rack_number(self):
        """
        上限を超えるrack_numberを指定してPOSTリクエストを送信した場合、エラーが返されることを確認
        """
        # テストに使用するデータ（無効なrack_number）
        invalid_rack_number = 1000

        # RackAddViewに対するURLを取得
        url = reverse('master:rack_add') 

        # POSTリクエストを送信
        response = self.client.post(url, {'rack_number': invalid_rack_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

        # データベースにラックが追加されていないことを確認
        self.assertFalse(Rack.objects.filter(rack_number=invalid_rack_number).exists())
  
    
class RackDeleteTest(TestCase):
    """
    ラック削除機能のテストケース
    """

    def setUp(self):
        # テスト用のラックを作成
        self.rack = Rack.objects.create(rack_number=42)

    def test_delete_existing_rack(self):
        """
        存在するラックを削除した場合、該当のラックが削除されることを確認する。
        """
        # RackDeleteViewに対するURLを取得
        url = reverse('master:rack_delete', args=[self.rack.rack_number])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースからラックが削除されたかを確認
        self.assertFalse(Rack.objects.filter(id=self.rack.rack_number).exists())


        #存在しないラック番号がフォームに渡されることはないのでテストケースは割愛している

class RackEditTest(TestCase):
    """
    ラック編集機能のテストケース
    """

    def setUp(self):
        # テスト用のラックを作成
        self.rack = Rack.objects.create(rack_number=42, description='Old Description')

    def test_edit_valid_rack_number(self):
        """
        正しいラック番号を指定してラックを編集した場合、変更が正しく反映されることを確認する。
        """
        # RackEditViewに対するURLを取得
        url = reverse('master:rack_edit', args=[self.rack.rack_number])

        # テストに使用する新しいラック番号
        new_rack_data = {
            'rack_number': 456,
            'description': 'New Description',
        }

        # POSTリクエストを送信
        response = self.client.post(url, new_rack_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースのラックが正しく更新されたかを確認
        self.rack.refresh_from_db()
        self.assertEqual(self.rack.rack_number, new_rack_data['rack_number'])
        self.assertEqual(self.rack.description, new_rack_data['description'])

    def test_edit_invalid_negative_rack_number(self):
        """
        負のラック番号を指定してラックを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # RackEditViewに対するURLを取得
        url = reverse('master:rack_edit', args=[self.rack.rack_number])

        # 負のラック番号
        invalid_rack_data = {
            'rack_number': -1,
            'description': 'Invalid Description',
        }

        # POSTリクエストを送信
        response = self.client.post(url, invalid_rack_data)

        # ラックが更新されていないことを確認
        self.rack.refresh_from_db()
        self.assertNotEqual(self.rack.rack_number, invalid_rack_data['rack_number'])
        self.assertNotEqual(self.rack.description, invalid_rack_data['description'])

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_edit_invalid_large_rack_number(self):
        """
        上限を超えるラック番号を指定してラックを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # RackEditViewに対するURLを取得
        url = reverse('master:rack_edit', args=[self.rack.rack_number])

        # 上限を超えるラック番号
        invalid_rack_data = {
            'rack_number': 1000,
            'description': 'Invalid Description',
        }

        # POSTリクエストを送信
        response = self.client.post(url, invalid_rack_data)

        # ラックが更新されていないことを確認
        self.rack.refresh_from_db()
        self.assertNotEqual(self.rack.rack_number, invalid_rack_data['rack_number'])
        self.assertNotEqual(self.rack.description, invalid_rack_data['description'])

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

"""
UPSマスタのテストケース
"""
class UpsModelTest(TestCase):
    """
    UPS追加機能のテストケース
    """

    def test_valid_ups_number(self):
        """
        正しいups_numberを指定してPOSTリクエストを送信することで、UPSが追加されることを確認
        """
        # テストに使用するデータ
        ups_number = 12

        # UpsAddViewに対するURLを取得
        url = reverse('master:ups_add')

        # POSTリクエストを送信
        response = self.client.post(url, {'ups_number': ups_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースにUPSが正しく追加されたかを確認
        self.assertTrue(Ups.objects.filter(ups_number=ups_number).exists())

    def test_invalid_negative_ups_number(self):
        """
        負のups_numberを指定してPOSTリクエストを送信した場合、エラーが返されることを確認
        """

        # テストに使用するデータ（無効なups_number）
        invalid_ups_number = -1

        # UpsAddViewに対するURLを取得
        url = reverse('master:ups_add') 

        # POSTリクエストを送信
        response = self.client.post(url, {'ups_number': invalid_ups_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

        # データベースにUPSが追加されていないことを確認
        self.assertFalse(Ups.objects.filter(ups_number=invalid_ups_number).exists())

    def test_invalid_large_ups_number(self):
        """
        上限を超えるups_numberを指定してPOSTリクエストを送信した場合、エラーが返されることを確認
        """
        # テストに使用するデータ（無効なups_number）
        invalid_ups_number = 100

        # UpsAddViewに対するURLを取得
        url = reverse('master:ups_add') 

        # POSTリクエストを送信
        response = self.client.post(url, {'ups_number': invalid_ups_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

        # データベースにUPSが追加されていないことを確認
        self.assertFalse(Ups.objects.filter(ups_number=invalid_ups_number).exists())
  
    
class UpsDeleteTest(TestCase):
    """
    UPS削除機能のテストケース
    """

    def setUp(self):
        # テスト用のUPSを作成
        self.ups = Ups.objects.create(ups_number=42)

    def test_delete_existing_ups(self):
        """
        存在するUPSを削除した場合、該当のUPSが削除されることを確認する。
        """
        # UpsDeleteViewに対するURLを取得
        url = reverse('master:ups_delete', args=[self.ups.ups_number])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースからUPSが削除されたかを確認
        self.assertFalse(Ups.objects.filter(id=self.ups.ups_number).exists())


        #存在しないUPS番号がフォームに渡されることはないのでテストケースは割愛している

class UpsEditTest(TestCase):
    """
    UPS編集機能のテストケース
    """

    def setUp(self):
        # テスト用のUPSを作成
        self.ups = Ups.objects.create(ups_number=42, description='Old Description')

    def test_edit_valid_ups_number(self):
        """
        正しいUPS番号を指定してUPSを編集した場合、変更が正しく反映されることを確認する。
        """
        # UpsEditViewに対するURLを取得
        url = reverse('master:ups_edit', args=[self.ups.ups_number])

        # テストに使用する新しいUPS番号
        new_ups_data = {
            'ups_number': 45,
            'description': 'New Description',
        }

        # POSTリクエストを送信
        response = self.client.post(url, new_ups_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースのUPSが正しく更新されたかを確認
        self.ups.refresh_from_db()
        self.assertEqual(self.ups.ups_number, new_ups_data['ups_number'])
        self.assertEqual(self.ups.description, new_ups_data['description'])

    def test_edit_invalid_negative_ups_number(self):
        """
        負のUPS番号を指定してUPSを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # UpsEditViewに対するURLを取得
        url = reverse('master:ups_edit', args=[self.ups.ups_number])

        # 負のUPS番号
        invalid_ups_data = {
            'ups_number': -1,
            'description': 'Invalid Description',
        }

        # POSTリクエストを送信
        response = self.client.post(url, invalid_ups_data)

        # UPSが更新されていないことを確認
        self.ups.refresh_from_db()
        self.assertNotEqual(self.ups.ups_number, invalid_ups_data['ups_number'])
        self.assertNotEqual(self.ups.description, invalid_ups_data['description'])

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_edit_invalid_large_ups_number(self):
        """
        上限を超えるUPS番号を指定してUPSを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # UpsEditViewに対するURLを取得
        url = reverse('master:ups_edit', args=[self.ups.ups_number])

        # 上限を超えるUPS番号
        invalid_ups_data = {
            'ups_number': 100,
            'description': 'Invalid Description',
        }

        # POSTリクエストを送信
        response = self.client.post(url, invalid_ups_data)

        # UPSが更新されていないことを確認
        self.ups.refresh_from_db()
        self.assertNotEqual(self.ups.ups_number, invalid_ups_data['ups_number'])
        self.assertNotEqual(self.ups.description, invalid_ups_data['description'])

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
        
    
"""
電源系統マスタのテストケース
"""
class PowerSystemAddTest(TestCase):
    """
    電源系統追加機能のテストケース
    """

    def setUp(self):
        # テスト用のUPSとラックを作成
        self.ups = Ups.objects.create(ups_number=42)
        self.rack = Rack.objects.create(rack_number=100)

    def test_add_valid_power_system(self):
        """
        正しいデータで電源系統を追加した場合、データベースに正しく保存されることを確認する。
        """
        # 正しいデータで電源系統を作成
        power_system_data = {
            'power_system_number': 1,
            'max_current': 50.0,
            'supply_source': self.ups.ups_number,
            'supply_rack': self.rack.rack_number,
        }
        
        # PowerSystemAddViewに対するURLを取得
        url = reverse('master:power_system_add')
        
        # POSTリクエストを送信
        response = self.client.post(url, power_system_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースに電源系統が正しく追加されたかを確認
        self.assertTrue(PowerSystem.objects.filter(power_system_number=power_system_data['power_system_number']).exists())

        
    def test_add_invalid_ups_number_power_system(self):
        """
        不正な電源系統番号で電源系統を追加しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正な電源系統番号で電源系統を作成しようとした場合、ValidationErrorが発生することを確認
        invalid_power_system_data = {
            'power_system_number': -1, # 不正な電源系統番号
            'max_current': 2.0,  
            'supply_source': self.ups.ups_number,
            'supply_rack': self.rack.rack_number,
        }
        
        # PowerSystemAddViewに対するURLを取得
        url = reverse('master:power_system_add')

        # POSTリクエストを送信
        response = self.client.post(url, invalid_power_system_data)

        # 電源系統が追加されていないことを確認
        self.assertFalse(PowerSystem.objects.filter(power_system_number=invalid_power_system_data['power_system_number']).exists())

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)


    def test_add_invalid_max_current_power_system(self):
        """
        不正な最大電流値で電源系統を追加しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正な最大電流値で電源系統を作成しようとした場合、ValidationErrorが発生することを確認
        invalid_power_system_data = {
            'power_system_number': 2,
            'max_current': 150.0,  # 不正な最大電流値
            'supply_source': self.ups.ups_number,
            'supply_rack': self.rack.rack_number,
        }

        # PowerSystemAddViewに対するURLを取得
        url = reverse('master:power_system_add')

        # POSTリクエストを送信
        response = self.client.post(url, invalid_power_system_data)

        # 電源系統が追加されていないことを確認
        self.assertFalse(PowerSystem.objects.filter(power_system_number=invalid_power_system_data['power_system_number']).exists())

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

class PowerSystemDeleteTest(TestCase):
    """
    電源系統削除機能のテストケース
    """

    def setUp(self):
        # テスト用のUPSとラックを作成
        self.ups = Ups.objects.create(ups_number=42)
        self.rack = Rack.objects.create(rack_number=100)

        # テスト用の電源系統を作成
        self.power_system = PowerSystem.objects.create(
            power_system_number=1,
            max_current=50.0,
            supply_source=self.ups,
            supply_rack=self.rack,
        )

    def test_delete_existing_power_system(self):
        """
        存在する電源系統を削除した場合、該当の電源系統が削除されることを確認する。
        """
        # PowerSystemDeleteViewに対するURLを取得
        url = reverse('master:power_system_delete', args=[self.power_system.power_system_number])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースから電源系統が正しく削除されたかを確認
        self.assertFalse(PowerSystem.objects.filter(id=self.power_system.power_system_number).exists())



    def test_delete_nonexistent_power_system(self):
        """
        存在しない電源系統を削除しようとした場合、ObjectDoesNotExist例外が発生することを確認する。
        """
        # 存在しない電源系統番号を指定して削除を試みる
        invalid_power_system_id = self.power_system.power_system_number + 1
        
        # PowerSystemDeleteViewに対するURLを取得
        url = reverse('master:power_system_delete', args=[invalid_power_system_id])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # 電源系統が削除されていないことを確認
        self.assertTrue(PowerSystem.objects.filter(id=self.power_system.power_system_number).exists())


class PowerSystemEditTest(TestCase):
    """
    電源系統編集機能のテストケース
    """

    def setUp(self):
        # テスト用のUPSとラックを作成
        self.ups = Ups.objects.create(ups_number=42)
        self.rack = Rack.objects.create(rack_number=100)

        # テスト用の電源系統を作成
        self.power_system = PowerSystem.objects.create(
            power_system_number=1,
            max_current=50.0,
            supply_source=self.ups,
            supply_rack=self.rack,
        )

    def test_edit_valid_power_system(self):
        """
        正しいデータで電源系統を編集した場合、データベースに正しく変更が反映されることを確認する。
        """
        # 正しいデータで電源系統を編集
        edited_power_system_data = {
            'power_system_number': 1,
            'max_current': 75.0,  # 新しい最大電流値
            'supply_source': self.ups.ups_number,
            'supply_rack': self.rack.rack_number,
        }
        
        # PowerSystemEditViewに対するURLを取得
        url = reverse('master:power_system_edit', args=[self.power_system.power_system_number])

        # POSTリクエストを送信
        response = self.client.post(url, edited_power_system_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースの電源系統が正しく更新されたかを確認
        self.power_system.refresh_from_db()
        self.assertEqual(self.power_system.power_system_number, edited_power_system_data['power_system_number'])
        self.assertEqual(self.power_system.max_current, edited_power_system_data['max_current'])

    def test_edit_invalid_power_system(self):
        """
        不正なデータで電源系統を編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正なデータで電源系統を編集しようとした場合、ValidationErrorが発生することを確認
        invalid_power_system_data = {
            'power_system_number': 2,
            'max_current': 150.0,  # 許容範囲外の値
            'supply_source': self.ups.ups_number,
            'supply_rack': self.rack.rack_number,
        }

        # PowerSystemEditViewに対するURLを取得
        url = reverse('master:power_system_edit', args=[self.power_system.power_system_number])

        # POSTリクエストを送信
        response = self.client.post(url, invalid_power_system_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースの電源系統が更新されていないことを確認
        self.power_system.refresh_from_db()
        self.assertNotEqual(self.power_system.power_system_number, invalid_power_system_data['power_system_number'])
        self.assertNotEqual(self.power_system.max_current, invalid_power_system_data['max_current'])
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
            
            
    
"""
アカウント管理のテストケース
"""
class EmployeeDeleteTest(TestCase):
    """
    アカウント削除機能のテストケース
    """

    def setUp(self):

        # テスト用のアカウントを作成
        self.user = CustomUser.objects.create_user(
            employee_number='123456',
            full_name='田中太郎',
            password='password123',
        )

    def test_delete_existing_employee(self):
        """
        アカウントが正常に削除されることを確認する。
        """
        # EmployeeDeleteViewに対するURLを取得
        url = reverse('master:employee_delete', args=[self.user.employee_number])
        
        # ログイン状態にするためにログイン処理を実行
        self.client.login(username='123456', password='password123')

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースからアカウントが正しく削除されたかを確認
        self.assertFalse(CustomUser.objects.filter(employee_number='123456').exists())


class EmployeeEditViewTest(TestCase):
    def setUp(self):
        # テスト用のアカウントを作成
        self.user = CustomUser.objects.create_user(
            employee_number='123456',
            full_name='田中太郎',
            password='password123',
        )

    def test_employee_edit_view_success(self):
        # 社員名が正常に編集されることを確認するテストケース

        # EmployeeEditViewに対するURLを取得
        url = reverse('master:employee_edit', args=[self.user.employee_number])

        # テストに使用する新しい社員名
        new_employee_data = {
            'employee_number':'123456',
            'full_name':'Jane Doe',
        }
        # ログイン状態にするためにログイン処理を実行
        self.client.login(username='123456', password='password123')

        # ログインしているユーザーのデータを取得
        logged_in_user = CustomUser.objects.get(employee_number='123456')

        # POSTリクエストを送信
        response = self.client.post(url, new_employee_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースのユーザーが正しく更新されたかを確認
        logged_in_user.refresh_from_db()
        self.assertEqual(logged_in_user.full_name, new_employee_data['full_name'])

    def test_employee_edit_view_invalid_data(self):
        # 無効なデータを使用して社員名を編集した場合、データベースが更新されないことを確認するテストケース

        # EmployeeEditViewに対するURLを取得
        url = reverse('master:employee_edit', args=[self.user.employee_number])
        
        # テストに使用する無効な社員名のデータ
        invalid_employee_data = {
            'employee_number':'123456',
            'full_name':'', #無効な社員名
        }
        
        # ログイン状態にするためにログイン処理を実行
        self.client.login(username='123456', password='password123')

        # ログインしているユーザーのデータを取得
        logged_in_user = CustomUser.objects.get(employee_number='123456')

        # POSTリクエストを送信
        response = self.client.post(url, invalid_employee_data)

        # データベースが更新されていないことを確認
        logged_in_user.refresh_from_db()
        self.assertNotEqual(logged_in_user.full_name, invalid_employee_data['full_name'])
        
        
class PasswordChangeViewTest(TestCase):
    def setUp(self):
        # テスト用のアカウントを作成
        self.user = CustomUser.objects.create_user(
            employee_number='123456',
            full_name='田中太郎',
            password='password123',
        )

    def test_password_change_view_success(self):
        # パスワードが正常に変更されることを確認するテストケース

        # PasswordChangeViewに対するURLを取得
        url = reverse('master:password_change_form')

        # テストに使用する新しいパスワードのデータ
        new_password_data = {
            'old_password': 'password123',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword',
        }

        # ログイン状態でPOSTリクエストを送信
        self.client.login(username='123456', password='password123')
        response = self.client.post(url, new_password_data)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースのユーザーが正しく更新されたかを確認
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password_data['new_password1']))

    def test_password_change_view_invalid_data(self):
        # 無効なデータを使用してパスワードを変更した場合、データベースが更新されないことを確認するテストケース

        # PasswordChangeViewに対するURLを取得
        url = reverse('master:password_change_form')

        # テストに使用する無効なパスワードのデータ（新しいパスワードが異なる）
        invalid_password_data = {
            'old_password': 'password123',
            'new_password1': '1234',
            'new_password2': '1234',  # 無効な値
        }

        # ログイン状態でPOSTリクエストを送信
        self.client.login(username='123456', password='password123')
        response = self.client.post(url, invalid_password_data)

        # データベースが更新されていないことを確認
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(invalid_password_data['new_password1']))
        
        
    def test_password_change_view_same_data(self):
        # 同じパスワードを変更した場合、フォームがエラーとなることを確認するテストケース

        # PasswordChangeViewに対するURLを取得
        url = reverse('master:password_change_form')

        # テストに使用する無効なパスワードのデータ（新しいパスワードが異なる）
        invalid_password_data = {
            'old_password': 'password123',
            'new_password1': 'password123',
            'new_password2': 'password123',  # 同じパスワード
        }

        # ログイン状態でPOSTリクエストを送信
        self.client.login(username='123456', password='password123')
        response = self.client.post(url, invalid_password_data)

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_password_change_view_invalid_nowpass_data(self):
        # 現在のパスワードが間違っている場合、フォームがエラーとなることを確認するテストケース

        # PasswordChangeViewに対するURLを取得
        url = reverse('master:password_change_form')

        # テストに使用する無効なパスワードのデータ（新しいパスワードが異なる）
        invalid_password_data = {
            'old_password': 'testpass123',# 間違ったパスワード
            'new_password1': 'password123',
            'new_password2': 'password123',  
        }

        # ログイン状態でPOSTリクエストを送信
        self.client.login(username='123456', password='password123')
        response = self.client.post(url, invalid_password_data)

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        