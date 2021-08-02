import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    필요한 패키지는 전역에 있어야 합니다
    이 스크립트는 가상환경을 실행시킬 수 없습니다
    --OS 에러 발생--
    """

    help = "모든 데이터를 생성합니다."

    def handle(self, *args, **options):

        prefix = "python manage.py seed_"

        command_list = [
            prefix + "users --total 150",
            prefix + "constituents --total 150",
            prefix + "flavor_tags",
            prefix + "postings --total 200",
            prefix + "custom_lists --total 140",
        ]

        for command in command_list:
            # Popen쓰지 마라 여기서 멀티 프로세싱은 위험하다
            subprocess.run(command)
