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
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:add')

        # 作業記録のデータを作成します
        worklog_data = {
            'work_date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "installation",
            'description': 'テスト作業内容',
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成します
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
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:add')

        # 作業記録のデータを作成します
        worklog_data = {
            'work_date': timezone.now(),
            'rack': self.rack.id + 1,  # 無効なデータ
            'work_type': "installation",
            'description': 'テスト作業内容',
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成します
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
        # テストユーザーでログインします
        self.client.login(username='123456', password='password123')

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:add')

        # 作業記録のデータを作成します
        worklog_data = {
            'work_date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "invalid",  # 無効なデータ
            'description': 'テスト作業内容',
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成します
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

        # 作業記録追加ビューのURLを取得します
        url = reverse('worklog:add')

        # 作業記録のデータを作成します
        worklog_data = {
            'work_date': timezone.now(),
            'rack': self.rack.id,
            'work_type': "installation",
            'description': '',  # 無効なデータ
        }
        # 最初の時点ではデータがないことを確認
        self.assertEqual(WorkLog.objects.count(), 0)
        
        # 作業記録を追加するリクエストを作成します
        response = self.client.post(url, worklog_data)

        # リクエストが成功したかどうかを確認
        self.assertEqual(response.status_code, 200)

        # データベースに作業記録が追加されていないことを確認
        self.assertNotEqual(WorkLog.objects.count(), 1)
        
        # フォームがエラーを含んでいることを確認
        form = response.context['form']
        self.assertTrue(form.errors)
        

