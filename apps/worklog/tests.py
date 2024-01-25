from django.test import TestCase
from apps.accounts.models import CustomUser
from django.urls import reverse
from django.utils import timezone
from .models import WorkLog, Employee
from .forms import WorkLogForm
from apps.master.models import Rack, Ups, PowerSystem


class WorkLogAddViewTest(TestCase):

    def setUp(self):
        # テスト用のラックを作成
        self.rack = Rack.objects.create(rack_number=100)
        # テストユーザーを作成
        self.user = CustomUser.objects.create_user(
                employee_number='123456',
                full_name='田中太郎',
                password='password123',
            )

    """
    作業記録追加機能のテストケース
    """

    def test_worklog_add_view(self):
        """
        正しいデータで作業記録を追加した場合、データベースに正しく保存されることを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('worklog:add')

        # 作業記録のデータを作成
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "installation",
            'description': 'テスト作業内容',
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 302)

        # データベースに作業記録が正しく追加されたかを確認
        
        self.assertEqual(WorkLog.objects.count(), 1)
        worklog = WorkLog.objects.first()
        self.assertEqual(worklog.rack.id, worklog_data['rack'])
        self.assertEqual(worklog.work_type, worklog_data['work_type'])
        self.assertEqual(worklog.description, worklog_data['description'])
        self.assertEqual(worklog.employee, self.user)

    def test_invalid_rack_worklog_add_view(self):
        """
        間違ったデータ（存在しないラック）で作業記録を追加した場合、データベースに正しく保存されないことを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('worklog:add')

        # 作業記録のデータを作成します
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id + 1,  # 無効なデータ
            'work_type': "installation",
            'description': 'テスト作業内容',
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(WorkLog.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_invalid_work_type_worklog_add_view(self):
        """
        間違ったデータ（無効な作業区分）で作業記録を追加した場合、データベースに正しく保存されないことを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('worklog:add')

        # 作業記録のデータを作成します
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "invalid",  # 無効なデータ
            'description': 'テスト作業内容',
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(WorkLog.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_invalid_description_worklog_add_view(self):
        """
        間違ったデータ（備考欄が無記入）で作業記録を追加した場合、データベースに正しく保存されないことを確認する。
        """
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得
        url = reverse('worklog:add')

        # 作業記録のデータを作成
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "installation",
            'description': '',  # 無効なデータ
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(WorkLog.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
       ######################################################################################################################

       
class WorkLogupdateViewTest(TestCase):

    def setUp(self):
        # テスト用のラックを作成
        self.rack = Rack.objects.create(rack_number=100)
        self.rack2 = Rack.objects.create(rack_number=101)
        # テストユーザーを作成
        self.user = CustomUser.objects.create_user(
                employee_number='123456',
                full_name='田中太郎',
                password='password123',
            )
        # テスト用作業記録を作成
        self.worklog = WorkLog.objects.create(
            date=timezone.now(),
            rack=self.rack,
            work_type="installation",
            description='テスト作業内容',
            employee=self.user,
        )
        
        

    """
    作業記録編集機能のテストケース
    """

    def test_worklog_update_view(self):
        """
        正しいデータで作業記録を編集した場合、データベースに正しく保存されることを確認する。
        """
        # テストユーザーでログイン
        self.client.login(username='123456', password='password123')
        # 作業記録編集ビューのURLを取得
        url = reverse('worklog:update', args=[self.worklog.id])

        # 作業記録のデータを作成します
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "installation",
            'description': 'テスト作業内容',
            'employee': self.user,
        }
        self.assertEqual(WorkLog.objects.count(), 1)
        
        # 作業記録を追加するリクエストを作成します
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が正しく編集されたかを確認
        
        self.assertEqual(WorkLog.objects.count(), 1)
        worklog = WorkLog.objects.first()
        self.assertEqual(self.worklog.rack.id, worklog_data['rack'])
        self.assertEqual(self.worklog.work_type, worklog_data['work_type'])
        self.assertEqual(self.worklog.description, worklog_data['description'])
        self.assertEqual(self.worklog.employee, worklog_data['employee'])

    def test_invalid_rack_worklog_update_view(self):
        """
        間違ったデータ（存在しないラック）で作業記録を編集した場合、データベースに保存されないことを確認する。
        """
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:update', args=[self.worklog.id])

        # 作業記録のデータを作成します
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id + 5,  # 無効なデータ
            'work_type': "installation",
            'description': 'テスト作業内容',
            'employee': self.user,
        }
        
        # 作業記録を追加するリクエストを作成します
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # 作業記録が編集されていないことを確認
        self.assertNotEqual(self.worklog.rack.id, worklog_data['rack'])
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_invalid_work_type_worklog_update_view(self):
        """
        間違ったデータ（無効な作業区分）で作業記録を編集した場合、データベースに保存されないことを確認する。
        """
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:update', args=[self.worklog.id])

        # 作業記録のデータを作成します
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "invalid",  # 無効なデータ
            'description': 'テスト作業内容',
        }
        
        # 作業記録を追加するリクエストを作成します
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # 作業記録が編集されていないことを確認
        self.assertNotEqual(self.worklog.work_type, worklog_data['work_type'])
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        
    def test_invalid_description_worklog_update_view(self):
        """
        間違ったデータ（備考欄が無記入）で作業記録を編集した場合、データベースに保存されないことを確認する。
        """
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:update', args=[self.worklog.id])

        # 作業記録のデータを作成します
        worklog_data = {
            'date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "installation",
            'description': '',  # 無効なデータ
        }
        
        # 作業記録を追加するリクエストを作成します
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)
        
        # 作業記録が編集されていないことを確認
        self.assertNotEqual(self.worklog.description, worklog_data['description'])
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors) 
        
        
