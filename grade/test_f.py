import threading

from django.db.models import F

from grade.models import Grade


class ChangeThread(threading.Thread):
    """ 改变分数 """

    def __init__(self, max_count=1000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_count = max_count

    def run(self):
        count = 0
        grade_obj = Grade.objects.get(pk=1)
        while True:
            # 最多循环max_count次
            if count >= self.max_count:
                break

            print(self.getName(), count)
            # grade_obj.score += 1
            grade_obj.score = F('score') + 1  # F函数
            grade_obj.save()
            count += 1


def main():
    t1 = ChangeThread(max_count=800, name='T1')
    t2 = ChangeThread(max_count=500, name='T2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
