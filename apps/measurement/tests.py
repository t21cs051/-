from django.test import TestCase
from apps.accounts.models import CustomUser
from django.urls import reverse
from django.utils import timezone
from .models import CurrentMeasurement
from .forms import MeasurementForm
from apps.master.models import Rack, Ups, PowerSystem

class CurrentMeasurementAddViewTest(TestCase):

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

        # テストユーザーを作成
        self.user = CustomUser.objects.create_user(
                employee_number='123456',
                full_name='田中太郎',
                password='password123',
            )

    """
    電流記録追加機能のテストケース
    """

    def test_measurement_add_view(self):
        """
        正しいデータで電流記録を追加した場合、データベースに正しく保存されることを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('measurement:add')

        # 電流記録のデータを作成
        measurement_data = {
            'measurement_date': timezone.now(),
            'current_value': 1.0,
            'power_system': self.power_system.id,
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(CurrentMeasurement.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, measurement_data)

        # リクエストが成功したかどうかを確認
        #self.assertEqual(response.status_code, 302)

        # データベースに作業記録が正しく追加されたかを確認
        self.assertEqual(CurrentMeasurement.objects.count(), 1)
        measurement = CurrentMeasurement.objects.first()
        self.assertEqual(measurement.current_value, measurement_data['current_value'])
        self.assertEqual(measurement.power_system.id, measurement_data['power_system'])
        self.assertEqual(measurement.employee, self.user)
        

    def test_invalid_large_current_value_measurement_add_view(self):
        """
        間違ったデータ（上限を超えた電流値）で作業記録を追加した場合、データベースに正しく保存されないことを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('measurement:add')

        # 電流記録のデータを作成
        measurement_data = {
            'measurement_date': timezone.now(),
            'current_value': 101.0,#無効な電流値
            'power_system': self.power_system.id,
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(CurrentMeasurement.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, measurement_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(CurrentMeasurement.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_invalid_small_current_value_measurement_add_view(self):
        """
        間違ったデータ（下限を超えた電流値）で作業記録を追加した場合、データベースに正しく保存されないことを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('measurement:add')

        # 電流記録のデータを作成
        measurement_data = {
            'measurement_date': timezone.now(),
            'current_value': -1.0,#無効な電流値
            'power_system': self.power_system.id,
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(CurrentMeasurement.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, measurement_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(CurrentMeasurement.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_invalid_power_system_measurement_add_view(self):
        """
        間違ったデータ（無効な電源系統）で作業記録を追加した場合、データベースに正しく保存されないことを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('measurement:add')

        # 電流記録のデータを作成
        measurement_data = {
            'measurement_date': timezone.now(),
            'current_value': 1.0,
            'power_system': self.power_system.id+1,#無効な電源系統
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(CurrentMeasurement.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, measurement_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(CurrentMeasurement.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)


