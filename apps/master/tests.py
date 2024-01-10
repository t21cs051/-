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
        url = reverse('master:rack_delete', args=[self.rack.id])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースからラックが削除されたかを確認
        self.assertFalse(Rack.objects.filter(id=self.rack.id).exists())


        #存在しないラック番号がフォームに渡されることはないのでテストケースは割愛している

class RackEditTest(TestCase):
    """
    ラック編集機能のテストケース
    """

    def setUp(self):
        # テスト用のラックを作成
        self.rack = Rack.objects.create(rack_number=42)

    def test_edit_valid_rack_number(self):
        """
        正しいラック番号を指定してラックを編集した場合、変更が正しく反映されることを確認する。
        """
        # RackEditViewに対するURLを取得
        url = reverse('master:rack_edit', args=[self.rack.id])

        # テストに使用する新しいラック番号
        new_rack_number = 456

        # POSTリクエストを送信
        response = self.client.post(url, {'rack_number': new_rack_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースのラックが正しく更新されたかを確認
        self.rack.refresh_from_db()
        self.assertEqual(self.rack.rack_number, new_rack_number)

    def test_edit_invalid_negative_rack_number(self):
        """
        負のラック番号を指定してラックを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # RackEditViewに対するURLを取得
        url = reverse('master:rack_edit', args=[self.rack.id])

        # 負のラック番号
        invalid_rack_number = -1

        # POSTリクエストを送信
        response = self.client.post(url, {'rack_number': invalid_rack_number})

        # ラックが更新されていないことを確認
        self.rack.refresh_from_db()
        self.assertNotEqual(self.rack.rack_number, invalid_rack_number)

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_edit_invalid_large_rack_number(self):
        """
        上限を超えるラック番号を指定してラックを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # RackEditViewに対するURLを取得
        url = reverse('master:rack_edit', args=[self.rack.id])

        # 上限を超えるラック番号
        invalid_rack_number = 1000

        # POSTリクエストを送信
        response = self.client.post(url, {'rack_number': invalid_rack_number})

        # ラックが更新されていないことを確認
        self.rack.refresh_from_db()
        self.assertNotEqual(self.rack.rack_number, invalid_rack_number)

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
        url = reverse('master:ups_delete', args=[self.ups.id])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースからUPSが削除されたかを確認
        self.assertFalse(Ups.objects.filter(id=self.ups.id).exists())


        #存在しないUPS番号がフォームに渡されることはないのでテストケースは割愛している

class UpsEditTest(TestCase):
    """
    UPS編集機能のテストケース
    """

    def setUp(self):
        # テスト用のUPSを作成
        self.ups = Ups.objects.create(ups_number=42)

    def test_edit_valid_ups_number(self):
        """
        正しいUPS番号を指定してUPSを編集した場合、変更が正しく反映されることを確認する。
        """
        # UpsEditViewに対するURLを取得
        url = reverse('master:ups_edit', args=[self.ups.id])

        # テストに使用する新しいUPS番号
        new_ups_number = 45

        # POSTリクエストを送信
        response = self.client.post(url, {'ups_number': new_ups_number})

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースのUPSが正しく更新されたかを確認
        self.ups.refresh_from_db()
        self.assertEqual(self.ups.ups_number, new_ups_number)

    def test_edit_invalid_negative_ups_number(self):
        """
        負のUPS番号を指定してUPSを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # UpsEditViewに対するURLを取得
        url = reverse('master:ups_edit', args=[self.ups.id])

        # 負のUPS番号
        invalid_ups_number = -1

        # POSTリクエストを送信
        response = self.client.post(url, {'ups_number': invalid_ups_number})

        # UPSが更新されていないことを確認
        self.ups.refresh_from_db()
        self.assertNotEqual(self.ups.ups_number, invalid_ups_number)

        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_edit_invalid_large_ups_number(self):
        """
        上限を超えるUPS番号を指定してUPSを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # UpsEditViewに対するURLを取得
        url = reverse('master:ups_edit', args=[self.ups.id])

        # 上限を超えるUPS番号
        invalid_ups_number = 100

        # POSTリクエストを送信
        response = self.client.post(url, {'ups_number': invalid_ups_number})

        # UPSが更新されていないことを確認
        self.ups.refresh_from_db()
        self.assertNotEqual(self.ups.ups_number, invalid_ups_number)

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
            'supply_source': self.ups.id,
            'supply_rack': self.rack.id,
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
            'supply_source': self.ups.id,
            'supply_rack': self.rack.id,
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
            'supply_source': self.ups.id,
            'supply_rack': self.rack.id,
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
        url = reverse('master:power_system_delete', args=[self.power_system.id])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # リダイレクトが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースから電源系統が正しく削除されたかを確認
        self.assertFalse(PowerSystem.objects.filter(id=self.power_system.id).exists())



    def test_delete_nonexistent_power_system(self):
        """
        存在しない電源系統を削除しようとした場合、ObjectDoesNotExist例外が発生することを確認する。
        """
        # 存在しない電源系統番号を指定して削除を試みる
        invalid_power_system_id = self.power_system.id + 1
        
        # PowerSystemDeleteViewに対するURLを取得
        url = reverse('master:power_system_delete', args=[invalid_power_system_id])

        # DELETEリクエストを送信
        response = self.client.delete(url)

        # 電源系統が削除されていないことを確認
        self.assertTrue(PowerSystem.objects.filter(id=self.power_system.id).exists())


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
            'supply_source': self.ups.id,
            'supply_rack': self.rack.id,
        }
        
        # PowerSystemEditViewに対するURLを取得
        url = reverse('master:power_system_edit', args=[self.power_system.id])

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
            'supply_source': self.ups.id,
            'supply_rack': self.rack.id,
        }

        # PowerSystemEditViewに対するURLを取得
        url = reverse('master:power_system_edit', args=[self.power_system.id])

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
            
            
