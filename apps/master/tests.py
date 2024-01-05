from django.test import TestCase

# Create your tests here.

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
