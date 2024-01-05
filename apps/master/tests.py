import unittest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
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
        正しいラック番号が与えられた場合、ValidationErrorが発生しないことを確認する。
        """
        # 正常なラック番号
        rack_number = 42

        try:
            # テスト対象のラックを作成
            rack = Rack(rack_number=rack_number)
            # 例外が発生しないことを確認
            rack.full_clean()
        except ValidationError:
            self.fail("ValidationErrorが発生しました。")

    def test_invalid_negative_rack_number(self):
        """
        ラック番号が負の値の場合、ValidationErrorが発生することを確認する。
        """
        # 負のラック番号
        rack_number = -1

        # ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            rack = Rack(rack_number=rack_number)
            rack.full_clean()

    def test_invalid_large_rack_number(self):
        """
        ラック番号が上限値を超える場合、ValidationErrorが発生することを確認する。
        """
        # 上限を超えるラック番号
        rack_number = 1000

        # ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            rack = Rack(rack_number=rack_number)
            rack.full_clean()

    def test_invalid_non_integer_rack_number(self):
        """
        ラック番号が整数でない場合、ValidationErrorが発生することを確認する。
        """
        # 不正なラック番号（文字列）
        rack_number = "invalid"

        # ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            rack = Rack(rack_number=rack_number)
            rack.full_clean()
  
    
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
        # ラックの数を記録
        initial_rack_count = Rack.objects.count()

        # ラックを削除
        self.rack.delete()

        # ラックが正常に削除されたことを確認
        self.assertEqual(Rack.objects.count(), initial_rack_count - 1)

        # ラックが存在しないことを確認
        with self.assertRaises(ObjectDoesNotExist):
            Rack.objects.get(rack_number=42)

    def test_delete_nonexistent_rack(self):
        """
        存在しないラックを削除しようとした場合、ObjectDoesNotExist例外が発生することを確認する。
        """
        # 存在しないラック番号を指定して削除を試みる
        nonexistent_rack_number = 999
        with self.assertRaises(ObjectDoesNotExist):
            Rack.objects.get(rack_number=nonexistent_rack_number).delete()


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
        # ラックの番号を変更
        new_rack_number = 100
        self.rack.rack_number = new_rack_number
        self.rack.full_clean() #バリデーションを確認
        self.rack.save()

        # データベースから再度取得して変更が反映されていることを確認
        updated_rack = Rack.objects.get(pk=self.rack.pk)
        self.assertEqual(updated_rack.rack_number, new_rack_number)

    def test_edit_invalid_rack_number(self):
        """
        不正なラック番号を指定してラックを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正なラック番号
        invalid_rack_number = -1

        # ラックの番号を不正に変更しようとした場合、ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            self.rack.rack_number = invalid_rack_number
            self.rack.full_clean()

        # データベースから再度取得して変更が反映されていないことを確認
        not_updated_rack = Rack.objects.get(pk=self.rack.pk)
        self.assertNotEqual(not_updated_rack.rack_number, invalid_rack_number)



"""
UPSマスタのテストケース
"""
class UpsAddTest(TestCase):
    """
    UPS追加機能のテストケース
    """
    def test_valid_ups_number(self):
        """
        正しいUPS番号が与えられた場合、ValidationErrorが発生しないことを確認する。
        """
        # 正常なUPS番号
        ups_number = 42

        try:
            # テスト対象のUPSを作成
            ups = Ups(ups_number=ups_number)
            # 例外が発生しないことを確認
            ups.full_clean()
        except ValidationError:
            self.fail("ValidationErrorが発生しました。")

    def test_invalid_negative_ups_number(self):
        """
        UPS番号が負の値の場合、ValidationErrorが発生することを確認する。
        """
        # 負のUPS番号
        ups_number = -1

        # ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            ups = Ups(ups_number=ups_number)
            ups.full_clean()

    def test_invalid_large_ups_number(self):
        """
        UPS番号が上限値を超える場合、ValidationErrorが発生することを確認する。
        """
        # 上限を超えるUPS番号
        ups_number = 1000

        # ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            ups = Ups(ups_number=ups_number)
            ups.full_clean()

    def test_invalid_non_integer_ups_number(self):
        """
        UPS番号が整数でない場合、ValidationErrorが発生することを確認する。
        """
        # 不正なUPS番号（文字列）
        ups_number = "invalid"

        # ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            ups = Ups(ups_number=ups_number)
            ups.full_clean()
   
         
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
        # UPSの数を記録
        initial_ups_count = Ups.objects.count()

        # UPSを削除
        self.ups.delete()

        # UPSが正常に削除されたことを確認
        self.assertEqual(Ups.objects.count(), initial_ups_count - 1)

        # UPSが存在しないことを確認
        with self.assertRaises(ObjectDoesNotExist):
            Ups.objects.get(ups_number=42)

    def test_delete_nonexistent_ups(self):
        """
        存在しないUPSを削除しようとした場合、ObjectDoesNotExist例外が発生することを確認する。
        """
        # 存在しないUPS番号を指定して削除を試みる
        nonexistent_ups_number = 999
        with self.assertRaises(ObjectDoesNotExist):
            Ups.objects.get(ups_number=nonexistent_ups_number).delete()


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
        # UPSの番号を変更
        new_ups_number = 99
        self.ups.ups_number = new_ups_number
        self.ups.full_clean() #バリデーションを確認
        self.ups.save()

        # データベースから再度取得して変更が反映されていることを確認
        updated_ups = Ups.objects.get(pk=self.ups.pk)
        self.assertEqual(updated_ups.ups_number, new_ups_number)

    def test_edit_invalid_ups_number(self):
        """
        不正なUPS番号を指定してUPSを編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正なUPS番号
        invalid_ups_number = -1

        # UPSの番号を不正に変更しようとした場合、ValidationErrorが発生することを確認
        with self.assertRaises(ValidationError):
            self.ups.ups_number = invalid_ups_number
            self.ups.full_clean()

        # データベースから再度取得して変更が反映されていないことを確認
        not_updated_ups = Ups.objects.get(pk=self.ups.pk)
        self.assertNotEqual(not_updated_ups.ups_number, invalid_ups_number)
        
        
    
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
            'supply_source': self.ups,
            'supply_rack': self.rack,
        }

        try:
            # バリデーションを実行し、データベースに保存
            power_system = PowerSystem(**power_system_data)
            power_system.full_clean()
            power_system.save()
        except ValidationError:
            self.fail("バリデーションエラーが発生しました。")

        # データベースから取得して確認
        added_power_system = PowerSystem.objects.get(power_system_number=1)
        self.assertEqual(added_power_system.max_current, 50.0)
        
    def test_add_invalid_ups_number_power_system(self):
        """
        不正な電源系統番号で電源系統を追加しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正な電源系統番号で電源系統を作成しようとした場合、ValidationErrorが発生することを確認
        invalid_power_system_data = {
            'power_system_number': -1, # 不正な電源系統番号
            'max_current': 2.0,  
            'supply_source': self.ups,
            'supply_rack': self.rack,
        }

        with self.assertRaises(ValidationError):
            power_system = PowerSystem(**invalid_power_system_data)
            power_system.full_clean()
            power_system.save()


    def test_add_invalid_max_current_power_system(self):
        """
        不正な最大電流値で電源系統を追加しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正な最大電流値で電源系統を作成しようとした場合、ValidationErrorが発生することを確認
        invalid_power_system_data = {
            'power_system_number': 2,
            'max_current': 150.0,  # 不正な最大電流値
            'supply_source': self.ups,
            'supply_rack': self.rack,
        }

        with self.assertRaises(ValidationError):
            power_system = PowerSystem(**invalid_power_system_data)
            power_system.full_clean()
            power_system.save()
            

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
        # 電源系統の数を記録
        initial_power_system_count = PowerSystem.objects.count()

        # 電源系統を削除
        self.power_system.delete()

        # 電源系統が正常に削除されたことを確認
        self.assertEqual(PowerSystem.objects.count(), initial_power_system_count - 1)

        # 電源系統が存在しないことを確認
        with self.assertRaises(ObjectDoesNotExist):
            PowerSystem.objects.get(power_system_number=1)

    def test_delete_nonexistent_power_system(self):
        """
        存在しない電源系統を削除しようとした場合、ObjectDoesNotExist例外が発生することを確認する。
        """
        # 存在しない電源系統番号を指定して削除を試みる
        nonexistent_power_system_number = 999
        with self.assertRaises(ObjectDoesNotExist):
            PowerSystem.objects.get(power_system_number=nonexistent_power_system_number).delete()


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
            'supply_source': self.ups,
            'supply_rack': self.rack,
        }

        # バリデーションを実行し、データベースに保存
        edited_power_system = PowerSystem.objects.get(power_system_number=1)
        edited_power_system.max_current = edited_power_system_data['max_current']

        try:
            edited_power_system.full_clean()
            edited_power_system.save()
        except ValidationError:
            self.fail("バリデーションエラーが発生しました。")

        # データベースから取得して変更が反映されていることを確認
        updated_power_system = PowerSystem.objects.get(power_system_number=1)
        self.assertEqual(updated_power_system.max_current, 75.0)

    def test_edit_invalid_power_system(self):
        """
        不正なデータで電源系統を編集しようとした場合、ValidationErrorが発生することを確認する。
        """
        # 不正なデータで電源系統を編集しようとした場合、ValidationErrorが発生することを確認
        invalid_power_system_data = {
            'power_system_number': 1,
            'max_current': 150.0,  # 許容範囲外の値
            'supply_source': self.ups,
            'supply_rack': self.rack,
        }

        edited_power_system = PowerSystem.objects.get(power_system_number=1)
        edited_power_system.max_current = invalid_power_system_data['max_current']

        with self.assertRaises(ValidationError):
            edited_power_system.full_clean()
            edited_power_system.save()